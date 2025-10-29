import os
import numpy as np
from itertools import product

np.random.seed(42)

# === Datasets and their known grid shapes ===
# Adjust these to match your actual parameter grid resolutions
GRID_SHAPES = {
    "gadget": [10, 10, 10],
}

# Sub-grid split configurations: evenly spaced train grids
# e.g., 5×5 → 125 samples from 20×20 grid, remainder → infer
REGULAR_SPLITS = {
    "gadget": [[5, 5, 5]],
}

def make_regular_split(dataset, full_shape, sub_shape_list):
    data_path = f"{dataset}.txt"
    assert os.path.exists(data_path), f"{data_path} not found"

    params = np.loadtxt(data_path, dtype=np.float32)
    n_total = len(params)
    assert np.prod(full_shape) == n_total, f"{dataset}: {full_shape} inconsistent with {n_total} samples"

    print(f"[{dataset}] Total {n_total} samples, grid {full_shape}")

    # all EIDs
    all_eids = np.arange(n_total, dtype=int)

    # for each regular sub-grid
    for sub_shape in sub_shape_list:
        steps = [max(1, f // s) for f, s in zip(full_shape, sub_shape)]
        sub_coords = np.stack(np.meshgrid(
            *[np.arange(0, f, step, dtype=int) for f, step in zip(full_shape, steps)],
            indexing="ij"
        ), axis=-1).reshape(-1, len(full_shape))

        train_eids = np.array([
            np.ravel_multi_index(tuple(c), full_shape)
            for c in sub_coords
        ])
        train_eids = np.unique(train_eids)
        infer_eids = np.setdiff1d(all_eids, train_eids)

        np.savetxt(f"{dataset}_{'x'.join(map(str, sub_shape))}_train_eids.txt", train_eids, fmt="%04d")
        np.savetxt(f"{dataset}_{'x'.join(map(str, sub_shape))}_train_params.txt", params[train_eids], fmt="%.6f")
        np.savetxt(f"{dataset}_{'x'.join(map(str, sub_shape))}_infer_eids.txt", infer_eids, fmt="%04d")
        np.savetxt(f"{dataset}_{'x'.join(map(str, sub_shape))}_infer_params.txt", params[infer_eids], fmt="%.6f")

        print(f"  Regular split {sub_shape}: train={len(train_eids)}, infer={len(infer_eids)}")

def main():
    for dataset, shape in GRID_SHAPES.items():
        sub_shapes = REGULAR_SPLITS.get(dataset, [])
        make_regular_split(dataset, shape, sub_shapes)

if __name__ == "__main__":
    main()