import numpy as np

def transform_columns(df, columns, func, substitute=False, prefix='_'):
    """
    Transform specified columns in a dataset according to the
    passed function.

    Args:
        df: Pandas DataFrame
        columns: list of valid names of columns
        func: function that can be applied to a DataFrame 
        column
        substitute: True if columns have to be substituted
        with their mappings, False otherwise (default
        False)
        prefix: new columns names will have the prefix
        (default '_')

    Returns:
        x_tr: numpy array containing the train data.
        x_te: numpy array containing the test data.
        y_tr: numpy array containing the train labels.
        y_te: numpy array containing the test labels.

    """
    
    if not substitute:
        for col in columns:
            new_col_name = prefix + '_' + col
            if col in df.columns and new_col_name not in df.columns:
                df[new_col_name] = func(df[col])
    else:
        for col in columns:
            new_col_name = prefix + '_' + col
            if col in df.columns and new_col_name not in df.columns:
                df[new_col_name] = func(df[col])
                df.drop(columns=col, inplace=True)