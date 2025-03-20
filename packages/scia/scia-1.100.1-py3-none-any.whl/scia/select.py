import pandas as pd

def select_cases(scdf, *cases):
    """
    Select specific cases from a Single-Case DataFrame (SCD).

    Parameters:
    - scdf (pd.DataFrame): The full dataset.
    - *cases: Case names or indices to select.

    Returns:
    - pd.DataFrame: A filtered DataFrame with selected cases.
    """

    if not cases:
        raise ValueError("At least one case name or index must be provided.")

    # Select cases by name or index
    if all(isinstance(case, str) for case in cases):
        selected = scdf[scdf["case"].isin(cases)]
    elif all(isinstance(case, int) for case in cases):
        selected = scdf.iloc[list(cases)]
    else:
        raise ValueError("Cases must be either all names (str) or all indices (int).")

    return selected
