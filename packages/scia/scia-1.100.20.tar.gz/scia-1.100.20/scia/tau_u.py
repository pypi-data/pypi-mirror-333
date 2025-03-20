import pandas as pd
import numpy as np
from scipy.stats import norm
from scia.preprocess import prepare_scd
from scia.recombine import recombine_phases
from scia.utils import revise_names

def kendall_tau(x, y, tau_method="b", continuity_correction=False):
    """
    Calculate Kendall's Tau correlation between two variables.

    Parameters:
    - x: First variable
    - y: Second variable
    - tau_method: 'a' or 'b' (tau-a or tau-b)
    - continuity_correction: Whether to apply continuity correction

    Returns:
    - Dictionary with Kendall's Tau statistics
    """
    n = len(x)
    if n != len(y):
        raise ValueError("x and y must have the same length")

    # Calculate S (sum of concordant minus discordant pairs)
    S = 0
    for i in range(n-1):
        for j in range(i+1, n):
            S += np.sign((x[j] - x[i]) * (y[j] - y[i]))

    # Calculate ties
    x_ties = {}
    y_ties = {}
    for i in range(n):
        x_val = x[i]
        y_val = y[i]
        x_ties[x_val] = x_ties.get(x_val, 0) + 1
        y_ties[y_val] = y_ties.get(y_val, 0) + 1

    # Sum of t(t-1)/2 for each tie
    T_x = sum(t * (t - 1) // 2 for t in x_ties.values() if t > 1)
    T_y = sum(t * (t - 1) // 2 for t in y_ties.values() if t > 1)

    # Number of pairs
    n_pairs = n * (n - 1) // 2

    # Calculate tau based on method
    if tau_method == "b":
        D = np.sqrt((n_pairs - T_x) * (n_pairs - T_y))
    else:  # tau_method == "a"
        D = n_pairs

    # Apply continuity correction if requested
    if continuity_correction and S != 0:
        S = S - np.sign(S)

    # Calculate tau
    tau = S / D if D > 0 else 0

    # Calculate standard deviation of S
    if tau_method == "b":
        # Formula for Tau-b
        v0 = n * (n - 1) * (2 * n + 5)
        vt = sum(t * (t - 1) * (2 * t + 5) for t in x_ties.values())
        vu = sum(t * (t - 1) * (2 * t + 5) for t in y_ties.values())
        v1 = sum(t * (t - 1) for t in x_ties.values()) * sum(u * (u - 1) for u in y_ties.values()) / 2
        v2 = sum(t * (t - 1) * (t - 2) for t in x_ties.values()) * sum(u * (u - 1) * (u - 2) for u in y_ties.values()) / 9
        sdS = np.sqrt((v0 - vt - vu) / 18 + v1 + v2)
    else:
        # Formula for Tau-a
        sdS = np.sqrt(n * (n - 1) * (2 * n + 5) / 18)

    # Calculate z-score and p-value
    z = S / sdS if sdS > 0 else 0
    p = 2 * (1 - norm.cdf(abs(z)))  # Two-tailed p-value

    return {
        "S": S,
        "D": D,
        "tau": tau,
        "sdS": sdS,
        "z": z,
        "p": p,
        "N": n
    }

def tau_ci(tau, n, ci=0.95, se_method="z"):
    """
    Calculate confidence interval for Kendall's tau.

    Parameters:
    - tau: Calculated tau value
    - n: Number of observations
    - ci: Confidence interval level (default: 0.95)
    - se_method: Method to calculate standard error ("z" or "tau")

    Returns:
    - Dictionary with lower and upper CI bounds
    """
    z = norm.ppf(1 - (1 - ci) / 2)

    if se_method == "z":
        # Use z-transformation method
        f_tau = 0.5 * np.log((1 + tau) / (1 - tau))
        se_f_tau = np.sqrt(1.0 / (n - 3))
        lower = np.tanh(f_tau - z * se_f_tau)
        upper = np.tanh(f_tau + z * se_f_tau)
    else:  # se_method == "tau"
        # Direct method based on tau's standard error
        se_tau = np.sqrt((4 * n + 10) / (9 * n * (n - 1)))
        lower = tau - z * se_tau
        upper = tau + z * se_tau

    return {"tau_ci_lower": lower, "tau_ci_upper": upper}

def meta_tau_u(tables, ci=0.95, se_method="z"):
    """
    Perform meta-analysis of Tau-U values.

    Parameters:
    - tables: List of Tau-U tables from individual cases
    - ci: Confidence interval level
    - se_method: Method to calculate standard error

    Returns:
    - Dictionary with meta-analysis results
    """
    row_index = "A vs. B - Trend A"

    # Extract weights and values
    weights = []
    values = []

    for table in tables:
        tau = table.loc[row_index, "Tau"]
        if not np.isnan(tau):
            if se_method == "z":
                se = table.loc[row_index, "SE_Tau"]
                weight = 1 / (se ** 2) if se > 0 else 0
            else:  # se_method == "tau"
                weight = table.loc[row_index, "n"]

            weights.append(weight)
            values.append(tau)

    if not weights:
        return {"tau": np.nan, "ci_lower": np.nan, "ci_upper": np.nan, "z": np.nan, "p": np.nan}

    # Calculate weighted average
    weighted_sum = sum(w * v for w, v in zip(weights, values))
    sum_weights = sum(weights)

    if sum_weights == 0:
        return {"tau": np.nan, "ci_lower": np.nan, "ci_upper": np.nan, "z": np.nan, "p": np.nan}

    weighted_tau = weighted_sum / sum_weights

    # Calculate standard error for the weighted average
    se_weighted = np.sqrt(1 / sum_weights)

    # Calculate z-score and p-value
    z = weighted_tau / se_weighted
    p = 2 * (1 - norm.cdf(abs(z)))

    # Calculate confidence interval
    z_ci = norm.ppf(1 - (1 - ci) / 2)
    ci_lower = weighted_tau - z_ci * se_weighted
    ci_upper = weighted_tau + z_ci * se_weighted

    return {
        "tau": weighted_tau,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "z": z,
        "p": p
    }

def tau_u(data, dvar="values", pvar="phase", method="complete", phases=("A", "B"),
          meta_analyses=True, ci=0.95, ci_method="z", meta_weight_method="z",
          tau_method="b", continuity_correction=False):
    """
    Compute Tau-U for single-case data.

    Parameters:
    - data (pd.DataFrame): The single-case dataset
    - dvar (str): Name of the dependent variable column
    - pvar (str): Name of the phase variable column
    - method (str): One of "complete", "parker", or "tarlow"
    - phases (tuple): Phases to compare (default: ("A", "B"))
    - meta_analyses (bool): Whether to perform meta-analysis across cases
    - ci (float): Confidence interval level (default: 0.95)
    - ci_method (str): Method for CI calculation ("z", "tau", or "s")
    - meta_weight_method (str): Weighting method for meta-analysis ("z" or "tau")
    - tau_method (str): Kendall's tau method ("a" or "b")
    - continuity_correction (bool): Whether to apply continuity correction

    Returns:
    - DataFrame with Tau-U results
    """
    # Method-specific settings
    if method == "parker":
        tau_method = "a"
        continuity_correction = False
    elif method == "tarlow":
        tau_method = "a"
        continuity_correction = True

    # Prepare data
    data = prepare_scd(data)
    keep = recombine_phases(data, phases=phases)
    case_names = revise_names(keep["case"].unique(), len(keep["case"].unique()))

    # Initialize output
    row_names = ["A vs. B", "Trend A", "Trend B", "A vs. B - Trend A",
                "A vs. B + Trend B", "A vs. B + Trend B - Trend A"]
    col_names = ["pairs", "pos", "neg", "ties", "S", "D", "Tau",
                "CI lower", "CI upper", "SD_S", "VAR_S", "SE_Tau", "Z", "p"]

    tables = []
    tau_u_values = []

    # Process each case
    for case in case_names:
        case_data = keep.loc[keep["case"] == case]

        # Split data by phase
        A_data = case_data.loc[case_data[pvar] == "A", dvar].dropna().values
        B_data = case_data.loc[case_data[pvar] == "B", dvar].dropna().values

        # Check if we have enough data
        if len(A_data) < 2 or len(B_data) < 1:
            continue

        # Combined data
        AB_data = np.concatenate([A_data, B_data])

        # Get dimensions
        nA = len(A_data)
        nB = len(B_data)
        nAB = nA + nB

        # Count comparisons
        AvApos, AvAneg, AvAtie = 0, 0, 0
        BvBpos, BvBneg, BvBtie = 0, 0, 0
        AvBpos, AvBneg, AvBtie = 0, 0, 0

        # A vs A comparisons
        for i in range(nA - 1):
            for j in range(i + 1, nA):
                if A_data[i] < A_data[j]:
                    AvApos += 1
                elif A_data[i] > A_data[j]:
                    AvAneg += 1
                else:
                    AvAtie += 1

        # B vs B comparisons
        for i in range(nB - 1):
            for j in range(i + 1, nB):
                if B_data[i] < B_data[j]:
                    BvBpos += 1
                elif B_data[i] > B_data[j]:
                    BvBneg += 1
                else:
                    BvBtie += 1

        # A vs B comparisons
        for a in A_data:
            for b in B_data:
                if a < b:
                    AvBpos += 1
                elif a > b:
                    AvBneg += 1
                else:
                    AvBtie += 1

        # Create phase indicators for Kendall calculations
        phase_indicator = np.concatenate([np.zeros(nA), np.ones(nB)])
        time_A = np.arange(1, nA + 1)
        time_B = np.arange(1, nB + 1)
        time_AB_A = np.concatenate([np.arange(nA, 0, -1), np.full(nB, nA + 1)])
        time_AB_B = np.concatenate([np.zeros(nA), np.arange(nA + 1, nAB + 1)])
        time_AB_B_A = np.concatenate([np.arange(nA, 0, -1), np.arange(nA + 1, nAB + 1)])

        # Calculate Kendall's tau values
        if method == "complete" and tau_method == "a":
            tau_s = {
                "AvB": kendall_tau(AB_data, phase_indicator, tau_method="a", continuity_correction=continuity_correction),
                "AvA": kendall_tau(A_data, time_A, tau_method="a", continuity_correction=continuity_correction),
                "BvB": kendall_tau(B_data, time_B, tau_method="a", continuity_correction=continuity_correction),
                "AvB_A": kendall_tau(AB_data, time_AB_A, tau_method="a", continuity_correction=continuity_correction),
                "AvB_B": kendall_tau(AB_data, time_AB_B, tau_method="a", continuity_correction=continuity_correction),
                "AvB_B_A": kendall_tau(AB_data, time_AB_B_A, tau_method="a", continuity_correction=continuity_correction)
            }
        else:
            tau_s = {
                "AvB": kendall_tau(AB_data, phase_indicator, tau_method="b", continuity_correction=continuity_correction),
                "AvA": kendall_tau(A_data, time_A, tau_method="b", continuity_correction=continuity_correction),
                "BvB": kendall_tau(B_data, time_B, tau_method="b", continuity_correction=continuity_correction),
                "AvB_A": kendall_tau(AB_data, time_AB_A, tau_method="b", continuity_correction=continuity_correction),
                "AvB_B": kendall_tau(AB_data, time_AB_B, tau_method="b", continuity_correction=continuity_correction),
                "AvB_B_A": kendall_tau(AB_data, time_AB_B_A, tau_method="b", continuity_correction=continuity_correction)
            }

        # Initialize table for this case
        table_tau = pd.DataFrame(index=row_names, columns=col_names)

        # Calculate number of pairs
        AvB_pair = nA * nB
        AvA_pair = nA * (nA - 1) // 2
        BvB_pair = nB * (nB - 1) // 2
        ABvAB_pair = nAB * (nAB - 1) // 2

        # Fill in pairs
        table_tau["pairs"] = [
            AvB_pair,
            AvA_pair,
            BvB_pair,
            AvB_pair + AvA_pair,
            AvB_pair + BvB_pair,
            AvB_pair + AvA_pair + BvB_pair
        ]

        if method == "parker":
            table_tau.loc["A vs. B - Trend A", "pairs"] = AvB_pair
            table_tau.loc["A vs. B + Trend B - Trend A", "pairs"] = ABvAB_pair

        # Fill in pos/neg/ties counts
        table_tau["pos"] = [
            AvBpos,
            AvApos,
            BvBpos,
            AvBpos + AvAneg,
            AvBpos + BvBpos,
            AvBpos + BvBpos + AvAneg
        ]

        table_tau["neg"] = [
            AvBneg,
            AvAneg,
            BvBneg,
            AvBneg + AvApos,
            AvBneg + BvBneg,
            AvBneg + BvBneg + AvApos
        ]

        table_tau["ties"] = [
            AvBtie,
            AvAtie,
            BvBtie,
            AvBtie + AvAtie,
            AvBtie + BvBtie,
            AvBtie + BvBtie + AvAtie
        ]

        # Fill in S values
        table_tau["S"] = [
            tau_s["AvB"]["S"],
            tau_s["AvA"]["S"],
            tau_s["BvB"]["S"],
            tau_s["AvB_A"]["S"],
            tau_s["AvB_B"]["S"],
            tau_s["AvB_B_A"]["S"]
        ]

        # Fill in D values
        if method == "complete" and tau_method == "b":
            table_tau["D"] = [
                tau_s["AvB"]["D"],
                tau_s["AvA"]["D"],
                tau_s["BvB"]["D"],
                tau_s["AvB_A"]["D"],
                tau_s["AvB_B"]["D"],
                tau_s["AvB_B_A"]["D"]
            ]
            table_tau.loc["A vs. B", "D"] = table_tau.loc["A vs. B", "pairs"] - table_tau.loc["A vs. B", "ties"] / 2
        else:
            table_tau["D"] = table_tau["pairs"]

        # Calculate Tau values
        table_tau["Tau"] = table_tau["S"] / table_tau["D"]

        # Calculate standard deviations
        if method == "tarlow":
            table_tau["SD_S"] = [
                tau_s["AvB"]["sdS"],
                tau_s["AvA"]["sdS"],
                tau_s["BvB"]["sdS"],
                tau_s["AvB_A"]["sdS"],
                tau_s["AvB_B"]["sdS"],
                tau_s["AvB_B_A"]["sdS"]
            ]
        else:
            # Use theoretical SD calculation
            table_tau.loc["A vs. B", "SD_S"] = np.sqrt((nA * nB) * (nA + nB + 1) / 12) * 2
            table_tau.loc["Trend A", "SD_S"] = kendall_tau(time_A, time_A, tau_method=tau_method)["sdS"]
            table_tau.loc["Trend B", "SD_S"] = kendall_tau(time_B, time_B, tau_method=tau_method)["sdS"]
            table_tau.loc["A vs. B - Trend A", "SD_S"] = tau_s["AvB_A"]["sdS"]
            table_tau.loc["A vs. B + Trend B", "SD_S"] = tau_s["AvB_B"]["sdS"]
            table_tau.loc["A vs. B + Trend B - Trend A", "SD_S"] = tau_s["AvB_B_A"]["sdS"]

        # Calculate variance
        table_tau["VAR_S"] = table_tau["SD_S"] ** 2

        # Fill in Z values
        table_tau["Z"] = [
            tau_s["AvB"]["z"],
            tau_s["AvA"]["z"],
            tau_s["BvB"]["z"],
            tau_s["AvB_A"]["z"],
            tau_s["AvB_B"]["z"],
            tau_s["AvB_B_A"]["z"]
        ]

        # Fill in p-values
        table_tau["p"] = [
            tau_s["AvB"]["p"],
            tau_s["AvA"]["p"],
            tau_s["BvB"]["p"],
            tau_s["AvB_A"]["p"],
            tau_s["AvB_B"]["p"],
            tau_s["AvB_B_A"]["p"]
        ]

        # Calculate standard errors
        table_tau["SE_Tau"] = table_tau["Tau"] / table_tau["Z"]

        # Calculate confidence intervals
        if ci is not None:
            if ci_method == "s":
                see = norm.ppf(1 - (1 - ci) / 2)
                S = table_tau["S"].copy()
                if continuity_correction:
                    S = S - 1
                table_tau["CI lower"] = (S - table_tau["SD_S"] * see) / table_tau["D"]
                table_tau["CI upper"] = (S + table_tau["SD_S"] * see) / table_tau["D"]
            else:
                for idx in table_tau.index:
                    n = nAB  # Use total sample size
                    cis = tau_ci(table_tau.loc[idx, "Tau"], n, ci=ci, se_method=ci_method)
                    table_tau.loc[idx, "CI lower"] = cis["tau_ci_lower"]
                    table_tau.loc[idx, "CI upper"] = cis["tau_ci_upper"]
        else:
            table_tau["CI lower"] = np.nan
            table_tau["CI upper"] = np.nan

        # Store results
        tables.append(table_tau)
        tau_u_values.append(table_tau.loc["A vs. B - Trend A", "Tau"])

    # Perform meta-analysis if requested
    if meta_analyses and tables:
        meta_result = meta_tau_u(tables, ci=ci, se_method=meta_weight_method)
    else:
        meta_result = None

    # Create a formatted output for display
    # Create header information
    header = f"Tau-U\n"
    header += f"Method: {method}\n"
    header += f"Applied Kendall's Tau-{tau_method}\n"

    if ci is not None:
        header += f"{int(ci*100)}% CIs for tau are reported.\n"
        header += f"CI method: {ci_method}\n"

    # Combine all parts
    output = header + "\n\n" + "\n\n".join([table.to_string() for table in tables])

    # Add overall results if meta-analysis was performed
    if meta_analyses and meta_result is not None:
        meta_table = pd.DataFrame({
            "Tau": [meta_result["tau"]],
            "CI lower": [meta_result["ci_lower"]],
            "CI upper": [meta_result["ci_upper"]],
            "Z": [meta_result["z"]],
            "p": [meta_result["p"]]
        }, index=["Combined Effect"])

        # Format meta-analysis table
        meta_table["Tau"] = meta_table["Tau"].map(lambda x: f"{x:.3f}")
        meta_table["CI lower"] = meta_table["CI lower"].map(lambda x: f"{x:.3f}")
        meta_table["CI upper"] = meta_table["CI upper"].map(lambda x: f"{x:.3f}")
        meta_table["Z"] = meta_table["Z"].map(lambda x: f"{x:.3f}")
        meta_table["p"] = meta_table["p"].map(lambda x: f"{x:.4f}")

        meta_title = "\nOverall Effect:\n"
        output += "\n\n" + meta_title + meta_table.to_string()

    # Return the DataFrame directly
    return tables[0] if tables else pd.DataFrame()
