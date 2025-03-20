import pandas as pd
import numpy as np
from scipy.stats import mannwhitneyu
from scia.preprocess import prepare_scd
from scia.recombine import recombine_phases
from scia.utils import revise_names

def nap(data, dvar="values", pvar="phase", decreasing=False, phases=("A", "B")):
    """
    Compute the Nonoverlap of All Pairs (NAP) for single-case data.

    Parameters:
    - data (pd.DataFrame): The single-case dataset.
    - dvar (str): Name of the dependent variable column.
    - pvar (str): Name of the phase variable column.
    - decreasing (bool, default=False): If True, considers lower values in Phase B as improvement.
    - phases (tuple, default=("A", "B")): Phases to compare.

    Returns:
    - pd.DataFrame: A summary of NAP calculations.
    """
    
    # Ensure "case" column exists
    if "case" not in data.columns:
        data["case"] = "NAs"  # Default case if missing
    
    # Prepare the data
    data = prepare_scd(data)
    keep = recombine_phases(data, phases=phases)
    case_names = revise_names(keep["case"].unique(), len(keep["case"].unique()))
    
    # Create a dataframe for storing results
    columns = ["Case", "NAP", "NAP Rescaled", "Pairs", "Non-overlaps", 
               "Positives", "Ties", "W", "p", "d", "R²"]
    results = pd.DataFrame(columns=columns)
    results["Case"] = case_names
    
    # Helper function to calculate NAP for each case
    def calculate_nap(case_data):
        A_values = case_data.loc[case_data[pvar] == "A", dvar].dropna().tolist()
        B_values = case_data.loc[case_data[pvar] == "B", dvar].dropna().tolist()
        
        if not A_values or not B_values:
            return pd.Series([np.nan] * (len(columns) - 1), index=columns[1:])
        
        pairs = len(A_values) * len(B_values)
        
        # Count positives (improvements based on decreasing flag)
        positives = 0
        for a_val in A_values:
            for b_val in B_values:
                if (decreasing and b_val < a_val) or (not decreasing and b_val > a_val):
                    positives += 1
        
        # Count ties
        ties = 0
        for a_val in A_values:
            for b_val in B_values:
                if a_val == b_val:
                    ties += 1
        
        # Calculate non-overlaps
        non_overlaps = positives + (0.5 * ties)
        
        # Calculate NAP
        nap_value = non_overlaps / pairs
        
        # Perform Mann-Whitney U test (equivalent to Wilcoxon in R for unpaired data)
        alternative = "greater" if decreasing else "less"
        test = mannwhitneyu(A_values, B_values, alternative=alternative)
        
        # Calculate effect sizes
        d = 3.464 * (1 - np.sqrt((1 - nap_value) / 0.5))
        r = d / np.sqrt(d**2 + 4)
        
        return pd.Series([
            nap_value * 100,                 # NAP
            2 * (nap_value * 100) - 100,     # NAP Rescaled
            pairs,                           # Pairs
            non_overlaps,                    # Non-overlaps
            positives,                       # Positives
            ties,                            # Ties
            test.statistic,                  # W
            test.pvalue,                     # p
            d,                               # d
            r**2                             # R²
        ], index=columns[1:])
    
    # Iterate through each case
    for i, case in enumerate(case_names):
        case_data = keep.loc[keep["case"] == case]
        results.loc[i, columns[1:]] = calculate_nap(case_data)
    
    # Round numeric columns appropriately
    results["NAP"] = results["NAP"].round(1)
    results["NAP Rescaled"] = results["NAP Rescaled"].round(1)
    results["Non-overlaps"] = results["Non-overlaps"].round(1)
    results["d"] = results["d"].round(3)
    results["R²"] = results["R²"].round(3)
    results["p"] = results["p"].map(lambda x: f"{x:.6f}" if not pd.isna(x) else x)
    
    return results