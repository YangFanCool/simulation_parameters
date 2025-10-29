import os
import numpy as np
from scipy.spatial import cKDTree
from tqdm import tqdm

DATASETS = ["castro", "clover", "gadget"]
SPLITS = [55, 64, 73, 82]
EPS = 1e-8

def normalize(x, ref_min, ref_max):
    return (x - ref_min) / (ref_max - ref_min + EPS)

def suggest_k(dim):
    if dim <= 2:
        return 4
    elif dim <= 4:
        return 8
    elif dim <= 6:
        return 16
    elif dim <= 8:
        return 32
    else:
        return 64

def process_dataset(dataset):
    all_eids = np.loadtxt(f"{dataset}_all_eids.txt", dtype=int)
    all_params = np.loadtxt(f"{dataset}_all_params.txt", dtype=np.float32)

    d = all_params.shape[1]
    K = suggest_k(d)
    print(f"\n[{dataset}] param dim={d}, K={K}")

    pmin, pmax = all_params.min(axis=0), all_params.max(axis=0)
    all_params_norm = normalize(all_params, pmin, pmax)

    for split in SPLITS:
        train_eids = np.loadtxt(f"{dataset}_{split}_train_eids.txt", dtype=int)
        infer_eids = np.loadtxt(f"{dataset}_{split}_infer_eids.txt", dtype=int)

        train_params = all_params_norm[train_eids]
        infer_params = all_params_norm[infer_eids]

        tree = cKDTree(train_params)
        neighbor_path = f"{dataset}_{split}_infer_neighbors.txt"
        weight_path = f"{dataset}_{split}_infer_weights.txt"

        with open(neighbor_path, "w") as fn, open(weight_path, "w") as fw:
            for i in tqdm(range(len(infer_eids)), desc=f"{dataset}_{split}"):
                xq = infer_params[i]
                k = min(K, len(train_eids))
                dists, idxs = tree.query(xq, k=k)

                # 计算逆距离权重
                if np.any(dists == 0):
                    w = np.zeros_like(dists)
                    w[dists.argmin()] = 1.0
                else:
                    w = 1.0 / (dists + EPS)**2
                    w /= w.sum()

                fn.write(" ".join(f"{train_eids[j]:04d}" for j in idxs) + "\n")
                fw.write(" ".join(f"{w_j:.6f}" for w_j in w) + "\n")

        print(f"✅ Saved {neighbor_path}, {weight_path}")

def main():
    for dataset in DATASETS:
        if os.path.exists(f"{dataset}_all_params.txt"):
            process_dataset(dataset)
        else:
            print(f"[WARN] skip {dataset} (missing all_params)")

if __name__ == "__main__":
    main()