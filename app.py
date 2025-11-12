import numpy as np
from itertools import product

def generate_params(param_specs, prefix="dataset"):
    """
    通用参数空间生成器
    param_specs: list of [min, max, num_divisions]
        例如 [[0.8, 0.95, 20], [0.8, 0.95, 20], [0.6, 1.0, 10]]
    prefix: 输出文件名前缀
    """

    def toF(x): return [f"{f:.6f}" for f in x]
    def normalize_to_pm1(arr): return 2 * (arr - arr.min()) / (arr.max() - arr.min()) - 1

    # === 生成每个维度的原始 & 归一化值 ===
    raw_axes  = [np.linspace(lo, hi, n) for lo, hi, n in param_specs]
    norm_axes = [normalize_to_pm1(axis) for axis in raw_axes]

    # === 生成笛卡尔积 ===
    combos_raw  = list(product(*raw_axes))
    combos_norm = list(product(*norm_axes))

    # === 写出原始文件 ===
    with open(f"{prefix}.txt", "w") as f_raw:
        for combo in combos_raw:
            f_raw.write(" ".join(toF(combo)) + "\n")

    # === 写出归一化文件 ===
    with open(f"{prefix}_norm.txt", "w") as f_norm:
        for combo in combos_norm:
            f_norm.write(" ".join(toF(combo)) + "\n")

    print(f"✅ Generated: {prefix}.txt  and  {prefix}_norm.txt")
    print(f"   Total combinations: {len(combos_raw)}")


# ===== Example Usage =====
if __name__ == "__main__":
    # 例如：
    # castro 模拟参数定义
    param_specs = [
        [0.0215, 0.0235, 10],
        [0.1200, 0.1550, 10],
        [0.5500, 0.8500, 10],
    ]
    generate_params(param_specs, prefix="nyx")