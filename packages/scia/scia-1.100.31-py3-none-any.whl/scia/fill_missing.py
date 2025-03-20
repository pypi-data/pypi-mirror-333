import pandas as pd
import numpy as np

def fill_missing(data, dvar="values", mvar="mt", na_rm=True):
    """
    Fill in missing values (NaN) in a single-case dataset without adding extra time points.

    Parameters:
    - data (pd.DataFrame): The single-case dataset.
    - dvar (str): Name of the dependent variable column.
    - mvar (str): Name of the measurement-time column.
    - na_rm (bool, default=True): If True, removes explicit NA values before interpolation.

    Returns:
    - pd.DataFrame: The dataset with only missing values filled (no extra rows).
    """
    
    # Ensure "case" column exists
    if "case" not in data.columns:
        data["case"] = "Default_Case"

    # Create a list to store the processed cases
    filled_cases = []

    for case_name, case_data in data.groupby("case"):
        case_data = case_data.sort_values(by=mvar).reset_index(drop=True)

        # Fill missing values using linear interpolation
        case_data[dvar] = case_data[dvar].interpolate(method="linear", limit_direction="both")

        filled_cases.append(case_data)

    # Combine all cases into a single DataFrame
    filled_data = pd.concat(filled_cases, ignore_index=True)

    return filled_data
