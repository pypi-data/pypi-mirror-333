import pandas as pd
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr

# Initialize R and load the fst package
pandas2ri.activate()
fst = importr('fst')

def read_fst(path, columns=None, from_=None, to=None, as_data_table=False):
    """
    Read a fst file into a pandas DataFrame.
    
    Parameters:
    -----------
    path : str
        Path to the fst file.
    columns : list, optional
        List of column names to read. If None, all columns are read.
    from_ : int, optional
        First row to read (0-based indexing). If None, start from the first row.
    to : int, optional
        Last row to read (0-based indexing). If None, read to the end.
    as_data_table : bool, default False
        If True, return a data.table object. Otherwise, return a pandas DataFrame.
    
    Returns:
    --------
    pandas.DataFrame or data.table
        Data from the fst file.
    """
    r_path = ro.StrVector([path])
    
    kwargs = {}
    if columns is not None:
        kwargs['columns'] = ro.StrVector(columns)
    if from_ is not None:
        kwargs['from'] = from_ + 1  # R uses 1-based indexing
    if to is not None:
        kwargs['to'] = to + 1  # R uses 1-based indexing
    if as_data_table:
        kwargs['as.data.table'] = as_data_table
    
    r_df = fst.read_fst(r_path[0], **kwargs)
    
    # Convert R dataframe to pandas DataFrame
    df = pandas2ri.rpy2py(r_df)
    # Reset index to match Python's 0-based indexing
    df.reset_index(drop=True, inplace=True)
    return df

def write_fst(df, path, compress=50):
    """
    Write a pandas DataFrame to a fst file.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Data to write.
    path : str
        Path where to save the fst file.
    compress : int, default 50
        Compression level (0-100). Higher means more compression but slower.
    
    Returns:
    --------
    None
    """
    # Convert pandas DataFrame to R dataframe
    r_df = pandas2ri.py2rpy(df)
    r_path = ro.StrVector([path])
    
    # Write the dataframe to a fst file
    fst.write_fst(r_df, r_path[0], compress=compress)