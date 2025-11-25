import numpy as np
from itertools import product

def generate_small(prefix="nyx", small_prefix="nyx_small", limit=200):
    """
    从 prefix.txt 和 prefix_norm.txt 截取前 limit 行
    写出 small_prefix.txt 和 small_prefix_norm.txt
    """
    # 原始
    raw_lines = open(f"{prefix}.txt").read().splitlines()
    norm_lines = open(f"{prefix}_norm.txt").read().splitlines()

    raw_small = raw_lines[:limit]
    norm_small = norm_lines[:limit]

    # 写出
    with open(f"{small_prefix}.txt", "w") as f:
        f.write("\n".join(raw_small))

    with open(f"{small_prefix}_norm.txt", "w") as f:
        f.write("\n".join(norm_small))

    print(f"✅ Generated {small_prefix}.txt and {small_prefix}_norm.txt")
    print(f"   Total lines: {limit}")

generate_small(prefix="nyx", small_prefix="nyx_small", limit=200)