import os
import numpy as np
from sklearn.model_selection import train_test_split

np.random.seed(42)

# 数据集名称与划分比例
DATASETS = ["castro", "clover", "gadget"]
SPLITS = [82, 73, 64, 55]

def main():
    for dataset in DATASETS:
        data_path = f"{dataset}.txt"
        assert os.path.exists(data_path), f"{data_path} not found"

        # 读取参数
        params = np.loadtxt(data_path, dtype=np.float32)
        n_samples = len(params)
        eids = np.arange(n_samples, dtype=int)

        # 保存 all
        np.savetxt(f"{dataset}_all_eids.txt", eids, fmt="%04d")
        np.savetxt(f"{dataset}_all_params.txt", params, fmt="%.6f")

        print(f"[{dataset}] Total {n_samples} samples")

        # 对每种比例生成划分
        for ratio in SPLITS:
            train_size = ratio / 100.0
            train_eids, infer_eids = train_test_split(
                eids, train_size=train_size, random_state=42, shuffle=True
            )

            # ✨ sort by eid
            train_eids = np.sort(train_eids)
            infer_eids = np.sort(infer_eids)

            # 保存 train
            np.savetxt(f"{dataset}_{ratio}_train_eids.txt", train_eids, fmt="%04d")
            np.savetxt(f"{dataset}_{ratio}_train_params.txt", params[train_eids], fmt="%.6f")

            # 保存 infer
            np.savetxt(f"{dataset}_{ratio}_infer_eids.txt", infer_eids, fmt="%04d")
            np.savetxt(f"{dataset}_{ratio}_infer_params.txt", params[infer_eids], fmt="%.6f")

            print(f"  Split {ratio}%: train={len(train_eids)}, infer={len(infer_eids)}")

if __name__ == "__main__":
    main()