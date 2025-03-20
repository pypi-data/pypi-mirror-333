import pandas as pd
import numpy as np
from scipy.stats import binomtest
from scia.preprocess import prepare_scd
from scia.recombine import recombine_phases
from scia.utils import revise_names

def pem(data, dvar="values", pvar="phase", decreasing=False, binom_test_flag=True, chi_test=False, fun=np.median, phases=("A", "B"), **kwargs):
    """
    Compute the Percentage Exceeding the Median (PEM) for single-case data.

    Parameters:
    - data (pd.DataFrame): The single-case dataset.
    - dvar (str): Name of the dependent variable column.
    - pvar (str): Name of the phase variable column.
    - decreasing (bool, default=False): If True, checks for lower values in Phase B.
    - binom_test_flag (bool, default=True): Computes a binomial test for a 50/50 distribution.
    - chi_test (bool, default=False): Computes a Chi-square test.
    - fun (function, default=np.median): Function to determine the comparison value (default is median).
    - phases (tuple, default=("A", "B")): Phases to compare.

    Returns:
    - pd.DataFrame: A summary of PEM calculations.
    """

    # Ensure "case" column exists
    if "case" not in data.columns:
        data["case"] = "NAs"  # Default to NAs if missing

    # Prepare the data
    data = prepare_scd(data)
    keep = recombine_phases(data, phases=phases)
    case_names = revise_names(keep["case"].unique(), len(keep["case"].unique()))

    # Create a dataframe for storing results
    results = pd.DataFrame(columns=["Case", "PEM", "Positives", "Total", "Binom.p"])
    results["Case"] = case_names

    # Iterate through each case
    for i, case in enumerate(case_names):
        case_data = keep.loc[keep["case"] == case]

        A = case_data.loc[case_data[pvar] == "A", dvar].dropna()
        B = case_data.loc[case_data[pvar] == "B", dvar].dropna()

        if len(A) == 0 or len(B) == 0:
            results.loc[i, ["PEM", "Positives", "Total", "Binom.p"]] = [np.nan, np.nan, np.nan, np.nan]
            continue

        # Compute the reference value from Phase A (default: median)
        threshold = fun(A, **kwargs)

        # Compute PEM (count B values exceeding the threshold)
        if decreasing:
            positives = sum(B < threshold)
        else:
            positives = sum(B > threshold)

        # Compute PEM percentage
        total_B = len(B)
        pem_value = (positives / total_B) * 100 if total_B > 0 else np.nan

        # Binomial test
        if binom_test_flag:
            binom_result = binomtest(positives, total_B, 0.5, alternative="greater")
            p_value = binom_result.pvalue  # Extract just the p-value
        else:
            p_value = np.nan

        # Store results
        results.loc[i, "PEM"] = round(pem_value, 1)  # Ensure one decimal place
        results.loc[i, "Positives"] = positives
        results.loc[i, "Total"] = total_B
        results.loc[i, "Binom.p"] = f"{p_value:.6f}"  # Ensure six decimal places

    # Print formatted output
    print("\nPercent Exceeding the Median\n")
    print(results.to_string(index=False, justify="left"))
    print("\nAlternative hypothesis: true probability > 50%")
    
    return results
