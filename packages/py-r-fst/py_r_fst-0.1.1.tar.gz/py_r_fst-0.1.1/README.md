# py-r-fst

Python wrapper for the R [fst](https://www.fstpackage.org/) package. The fst package provides a fast, easy and flexible way to serialize data frames.


## Installation

From PyPI:
```bash
pip install py-r-fst
```

From GitHub:
```bash
pip install git+https://github.com/msdavid/py-r-fst.git
```

From a local directory:
```bash
# Standard installation
pip install /path/to/py-r-fst

# Development mode (changes to code reflect immediately without reinstalling)
pip install -e /path/to/py-r-fst
```

### Requirements

- Python 3.6+
- R with the 'fst' package installed
- rpy2
- pandas

You need to have R installed and the fst package:

```R
install.packages("fst")
```

## Usage

```python
import pandas as pd
from pyfst import read_fst, write_fst

# Create a sample DataFrame
df = pd.DataFrame({
    'a': [1, 2, 3],
    'b': ['x', 'y', 'z']
})

# Write to fst file
write_fst(df, 'data.fst', compress=50)

# Read from fst file
df_read = read_fst('data.fst')
print(df_read)

# Read only specific columns
df_partial = read_fst('data.fst', columns=['a'])
print(df_partial)

# Read a subset of rows
df_rows = read_fst('data.fst', from_=0, to=1)
print(df_rows)
```

## API

### `read_fst(path, columns=None, from_=None, to=None, as_data_table=False)`

Read a fst file into a pandas DataFrame.

**Parameters:**
- `path`: Path to the fst file.
- `columns`: List of column names to read. If None, all columns are read.
- `from_`: First row to read (0-based indexing). If None, start from the first row.
- `to`: Last row to read (0-based indexing). If None, read to the end.
- `as_data_table`: If True, return a data.table object. Otherwise, return a pandas DataFrame.

**Returns:**
- pandas.DataFrame or data.table: Data from the fst file.

### `write_fst(df, path, compress=50)`

Write a pandas DataFrame to a fst file.

**Parameters:**
- `df`: pandas.DataFrame, data to write.
- `path`: Path where to save the fst file.
- `compress`: Compression level (0-100). Higher means more compression but slower.

**Returns:**
- None

## License

Apache 2.0