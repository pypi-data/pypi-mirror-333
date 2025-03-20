import pandas as pd
from scia.preprocess import prepare_scd
from scia.recombine import recombine_phases
from scia.utils import revise_names

def pnd(data, dvar="values", pvar="phase", decreasing=False, phases=("A", "B")):
    """
    Compute the Percentage of Non-Overlapping Data (PND) for single-case data.

    Parameters:
    - data (pd.DataFrame): The single-case data.
    - dvar (str): Name of the dependent variable column.
    - pvar (str): Name of the phase variable column.
    - decreasing (bool, default=False): If True, expects lower values in B-phase.
    - phases (tuple or list): Two phases to compare (default: ("A", "B")).

    Returns:
    - pd.DataFrame: A DataFrame containing PND results for each case.
    """

    # Ensure "case" column exists
    if "case" not in data.columns:
        data["case"] = "Default_Case"

    # Prepare data
    data = prepare_scd(data)

    # Recombine phases
    keep = recombine_phases(data, phases=phases)

    # Extract cases
    case_names = revise_names(keep["case"].unique(), len(keep["case"].unique()))

    # Define result DataFrame
    df = pd.DataFrame(columns=["Case", "PND (%)", "Total B", "Exceeds"])
    df["Case"] = case_names

    # Compute PND for each case
    for i, case in enumerate(case_names):
        case_data = keep.loc[keep["case"] == case].copy()

        A = case_data.loc[case_data[pvar] == "A", dvar].dropna()
        B = case_data.loc[case_data[pvar] == "B", dvar].dropna()

        if A.empty or B.empty:
            df.loc[i, "PND (%)"] = None
            df.loc[i, "Total B"] = len(B)
            df.loc[i, "Exceeds"] = 0
            continue

        # Compute PND
        max_A = max(A)
        min_A = min(A)

        if decreasing:
            exceeds = sum(B < min_A)
        else:
            exceeds = sum(B > max_A)

        total_B = len(B)
        pnd_value = (exceeds / total_B) * 100 if total_B > 0 else 0

        # Store results
        df.loc[i, "PND (%)"] = f"{round(pnd_value, 2)}%"
        df.loc[i, "Total B"] = total_B
        df.loc[i, "Exceeds"] = exceeds

    return df
