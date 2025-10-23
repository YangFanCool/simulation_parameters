# simulation_parameters

scientific ensemble simulation parameter space exploration

This small utility generates parameter-space files for ensemble simulations. It writes two files for each parameter specification:

- <prefix>.txt — the raw parameter combinations (space-separated floats, one combination per line)
- <prefix>\_norm.txt — the same combinations but each parameter axis normalized to [-1, 1]

The generator performs a Cartesian product across parameter axes defined as [min, max, count]. Values along each axis are evenly spaced using numpy.linspace.

## Files in this repository

- `app.py` — main generator. Call `generate_params(param_specs, prefix)` or run the script directly to generate `castro.txt` and `castro_norm.txt` (example included in the script).
- `castro.txt`, `castro_norm.txt`, `clover.txt`, `clover_norm.txt`, `gadget.txt`, `gadget_norm.txt` — example outputs (committed here for reference).

## Usage

Requirements:

- Python 3.7+ (tested with 3.8+)
- numpy

Install dependencies (recommended in a virtualenv):

```bash
python3 -m pip install --user numpy
```

Run the script directly to generate the included example:

```bash
python3 app.py
```

Or import and call from Python:

```python
from app import generate_params

param_specs = [
	[0.80, 0.95, 20],  # e.g. MP
	[0.80, 0.95, 20],  # e.g. MS
]
generate_params(param_specs, prefix="castro")
```

## File format

Each output file is plain text. Each line is a single parameter combination with values separated by spaces. Numeric values are formatted to 6 decimal places.

Example line from `castro.txt`:

```
0.800000 0.800000
```

Example corresponding normalized line from `castro_norm.txt`:

```
-1.000000 -1.000000
```

## Notes and edge cases

- The normalisation maps each axis independently to [-1, 1]. If any axis has identical min and max (zero range), normalization will produce a division-by-zero — avoid degenerate axis ranges.
- The number of combinations equals the product of the `count` values. Be careful with large counts which can create very large files and high memory usage during Cartesian product construction.

## Suggested improvements

- Stream the Cartesian product to file instead of building full lists to reduce memory usage for large grids.
- Add CLI argument parsing (argparse) to accept parameter specifications from command line or configuration files.
- Support other normalization schemes (z-score, min-max without [-1,1], log-scales).

## License

MIT
