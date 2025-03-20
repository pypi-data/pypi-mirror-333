import pandas as pd

def prepare_scd(data, na_rm=False):
    """
    Prepare a Single-Case DataFrame (SCD) for further analysis.

    Parameters:
    - data (pd.DataFrame): The SCD dataset.
    - na_rm (bool, default=False): If True, removes rows where the dependent variable is NaN.

    Returns:
    - pd.DataFrame: A cleaned and formatted DataFrame.
    """

    # Column names mapping
    pvar = "phase"  # Phase variable
    mvar = "mt"     # Measurement-time variable
    dvar = "values" # Dependent variable

    # Ensure column names are correctly formatted
    data.columns = [col.strip() for col in data.columns]

    # Remove rows with missing dependent variable values if na_rm=True
    if na_rm:
        data = data.dropna(subset=[dvar])

    # Ensure phase column is a categorical variable
    if not pd.api.types.is_categorical_dtype(data[pvar]):
        data[pvar] = data[pvar].astype("category")

    # Drop unused categories in phase
    data[pvar] = data[pvar].cat.remove_unused_categories()

    return data
