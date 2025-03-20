import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, fisher_exact
from scia.preprocess import prepare_scd
from scia.recombine import recombine_phases
from scia.utils import revise_names

def pand(data, dvar="values", pvar="phase", decreasing=False, phases=("A", "B"), method="sort", return_values=False):
    """
    Compute the Percentage of All Non-Overlapping Data (PAND) for single-case data.

    Parameters:
    - data (pd.DataFrame): The single-case data.
    - dvar (str): Name of the dependent variable column.
    - pvar (str): Name of the phase variable column.
    - decreasing (bool, default=False): If True, expects lower values in B-phase.
    - phases (tuple or list): Two phases to compare (default: ("A", "B")).
    - method (str): "sort" (default) or "minimum" to determine calculation method.
    - return_values (bool, default=False): If True, return only numeric values (used for IRD function).

    Returns:
    - Dict: Contains `pand`, `n`, `n_a`, `n_b` if `return_values=True`.
    - Dict: Full results object with class 'sc_pand' when `return_values=False`.
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

    # Extract phase values - more accurately matching R's lapply approach
    values_a = {case: keep.loc[(keep["case"] == case) & (keep[pvar] == "A"), dvar].values for case in case_names}
    values_b = {case: keep.loc[(keep["case"] == case) & (keep[pvar] == "B"), dvar].values for case in case_names}

    n_all_a = sum(len(v) for v in values_a.values())
    n_all_b = sum(len(v) for v in values_b.values())
    total_n = n_all_a + n_all_b

    if method == "sort":
        # Match R's approach for extracting phases_data
        phases_data = []
        for case in case_names:
            case_data = keep.loc[keep["case"] == case, pvar].values
            phases_data.extend(case_data)
        
        # Match R's approach for sorting - including the random sampling before sorting
        phases_sorted = []
        for case in case_names:
            case_df = keep.loc[keep["case"] == case].copy()
            # Sample rows randomly (like R's sample function)
            case_df = case_df.sample(frac=1).reset_index(drop=True)
            # Sort by dvar and pvar
            sorted_indices = np.lexsort((case_df[pvar].values, case_df[dvar].values))
            if decreasing:
                sorted_indices = sorted_indices[::-1]
            phases_sorted.extend(case_df.iloc[sorted_indices][pvar].values)
        
        # Create contingency table
        phases_data = np.array(phases_data)
        phases_sorted = np.array(phases_sorted)
        
        # Create a proper contingency table like R's table function
        unique_phases = np.unique(phases_data)
        mat_counts = pd.DataFrame(index=unique_phases, columns=unique_phases, data=0)
        
        for i, phase1 in enumerate(unique_phases):
            for j, phase2 in enumerate(unique_phases):
                mat_counts.iloc[i, j] = np.sum((phases_data == phase1) & (phases_sorted == phase2))
        
        # Compute proportions like R's prop.table
        mat_proportions = mat_counts / mat_counts.sum().sum()
        
        # Compute PAND percentage
        pand_value = (mat_proportions.iloc[0, 0] + mat_proportions.iloc[1, 1]) * 100
        overlaps = mat_counts.iloc[0, 1] + mat_counts.iloc[1, 0]
        perc_overlap = (overlaps / total_n) * 100
        
        # Use chi2_contingency which matches R's chisq.test behavior better
        chi_result = chi2_contingency(mat_counts.values, correction=False)
        chi_stat = chi_result[0]
        chi_p = chi_result[1]
        
        # Compute Phi Effect Size
        phi = np.sqrt(chi_stat / total_n)
        
        # Compute Fisher's exact test
        fisher_result = fisher_exact(mat_counts.values)
        odds_ratio = fisher_result[0]
        fisher_p = fisher_result[1]
        
        if return_values:
            return {"pand": pand_value, "n": total_n, "n_a": n_all_a, "n_b": n_all_b}
            
        # Create output object like R's version
        out = {
            "pand": pand_value,
            "method": method,
            "phi": phi,
            "perc_overlap": perc_overlap,
            "overlaps": overlaps,
            "n": total_n,
            "N": len(case_names),
            "n_a": n_all_a,
            "n_b": n_all_b,
            "matrix": mat_proportions,
            "matrix_counts": mat_counts,
            "chi_test": {"statistic": chi_stat, "p_value": chi_p, "df": 1},
            "fisher_test": {"odds_ratio": odds_ratio, "p_value": fisher_p}
        }
        
        # Print formatted output
        if not return_values:
            print("\nPercentage of all non-overlapping data\n")
            print(f"Method: {method}\n")
            print(f"PAND = {pand_value:.2f}%")
            print(f"Φ = {phi:.3f}  ;  Φ² = {phi**2:.3f}\n")
            print(f"{total_n} measurements ({n_all_a} Phase A, {n_all_b} Phase B) in {len(case_names)} cases")
            print(f"Overlapping data: n = {overlaps} ; percentage = {perc_overlap:.2f} \n")

            print("2 x 2 Matrix of percentages")
            print(mat_proportions.to_string(index=True, header=True), "\n")

            print("2 x 2 Matrix of counts")
            print(mat_counts.to_string(index=True, header=True), "\n")

            print(f"Chi-Squared test:\nX² = {chi_stat:.3f}, df = 1, p = {chi_p:.3f} \n")

            print(f"Fisher exact test:\nOdds ratio = {odds_ratio:.3f}, p = {fisher_p:.3f} \n")

    elif method == "minimum":
        # Implement Pustejovsky's approach matching R function more precisely
        def pand_pustejovsky(values_a, values_b):
            if decreasing:
                values_a = -1 * values_a
                values_b = -1 * values_b
            
            n_a = len(values_a)
            n_b = len(values_b)
            
            # Include -Inf and Inf in the sorted arrays as R does
            x = np.concatenate([[-np.inf], np.sort(values_a)])
            y = np.concatenate([np.sort(values_b), [np.inf]])
            
            # Create grid of all possible combinations
            grid = []
            max_nonoverlaps = 0
            max_overlap = 0
            
            # This replicates R's expand.grid and the mapply logic
            for a in range(1, n_a + 2):  # Include the -Inf position
                for b in range(1, n_b + 2):  # Include the Inf position
                    no_overlap = x[a-1] < y[b-1]
                    overlap = (a-1) + n_b - (b-1)
                    if no_overlap:
                        nonoverlaps = overlap
                        if nonoverlaps > max_nonoverlaps:
                            max_nonoverlaps = nonoverlaps
                            max_overlap = overlap
            
            return {
                "pand": max_nonoverlaps / (n_a + n_b),
                "nonoverlaps": max_nonoverlaps,
                "length_a": n_a,
                "length_b": n_b
            }
        
        # Apply the function to each case
        casewise = {case: pand_pustejovsky(values_a[case], values_b[case]) for case in case_names}
        
        # Calculate total non-overlaps
        nonoverlaps = sum(case_result["nonoverlaps"] for case_result in casewise.values())
        
        pand_value = (nonoverlaps / total_n) * 100
        overlaps = total_n - nonoverlaps
        perc_overlaps = 100 - pand_value
        
        if return_values:
            return {"pand": pand_value, "n": total_n, "n_a": n_all_a, "n_b": n_all_b}
            
        # Create output object like R's version
        out = {
            "pand": pand_value,
            "overlaps": overlaps,
            "perc_overlaps": perc_overlaps,
            "n": total_n,
            "N": len(case_names),
            "n_a": n_all_a,
            "n_b": n_all_b,
            "casewise": casewise,
            "method": method
        }
        
        # Print formatted output
        if not return_values:
            print("\nPercentage of all non-overlapping data\n")
            print(f"Method: {method}\n")
            print(f"PAND = {pand_value:.2f}%")
            print(f"{total_n} measurements ({n_all_a} Phase A, {n_all_b} Phase B) in {len(case_names)} cases")
            print(f"Overlapping data: n = {overlaps} ; percentage = {perc_overlaps:.2f} \n")

            print("Casewise results:")
            for case, res in casewise.items():
                print(f"{case}: PAND = {res['pand']*100:.2f}%, Non-overlaps = {res['nonoverlaps']}, A: {res['length_a']}, B: {res['length_b']}")

    # Add class and attributes to the output object
    out["class"] = ["sc_pand"]
    out["attributes"] = {
        "phase": pvar,
        "dv": dvar
    }
    
    # return out