import pandas as pd

def subset_scd(scdf, condition):
    """
    Filter a Single-Case DataFrame (SCD) based on a logical condition.

    Parameters:
    - scdf (pd.DataFrame): The dataset to filter.
    - condition (str): A string-based condition to filter rows (e.g., 'teacher == 1').

    Returns:
    - pd.DataFrame: A filtered DataFrame with selected rows.
    """
    try:
        filtered_df = scdf.query(condition)
        return filtered_df
    except Exception as e:
        raise ValueError(f"Invalid condition: {e}")
