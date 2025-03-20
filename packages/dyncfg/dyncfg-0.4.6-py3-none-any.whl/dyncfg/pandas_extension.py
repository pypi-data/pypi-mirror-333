import os

import pandas as pd


def read_table_auto(filepath, **kwargs):
    """
    Reads a table from a file, automatically detecting the file type.

    Args:
        filepath (str): The path to the file.
        **kwargs: Additional keyword arguments to pass to the pandas read function.

    Returns:
        pandas.DataFrame: The DataFrame read from the file, or None if an error occurs.
    """
    try:
        _, file_extension = os.path.splitext(filepath)
        file_extension = file_extension.lower()

        if file_extension == '.csv':
            return pd.read_csv(filepath, **kwargs)
        elif file_extension == '.xlsx' or file_extension == '.xls':
            return pd.read_excel(filepath, **kwargs)
        elif file_extension == '.tsv' or file_extension == '.txt':
            kwargs.setdefault('sep', '\t')  # Default to tab-separated for .tsv and .txt
            return pd.read_csv(filepath, **kwargs)
        elif file_extension == '.json':
            return pd.read_json(filepath, **kwargs)
        elif file_extension == '.parquet':
            return pd.read_parquet(filepath, **kwargs)
        elif file_extension == '.feather':
            return pd.read_feather(filepath, **kwargs)
        elif file_extension == '.hdf' or file_extension == '.h5':
            return pd.read_hdf(filepath, **kwargs)
        elif file_extension == '.pkl' or file_extension == '.pickle':
            return pd.read_pickle(filepath, **kwargs)
        else:
            print(f"Unsupported file type: {file_extension}")
            return None

    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None