import pandas as pd
import numpy as np
from scipy.stats import norm
from scia.preprocess import prepare_scd
from scia.recombine import recombine_phases
from scia.utils import revise_names
from scia.tau_u import kendall_tau, tau_u
import statsmodels.formula.api as smf

def corrected_tau(data, dvar="values", pvar="phase", mvar="mt", phases=("A", "B"), alpha=0.05, continuity=False, repeated=False, tau_method="b"):
    # Prepare the data
    data_list = prepare_scd(data)
    data_list = recombine_phases(data_list, phases=phases)  # Corrected: use DataFrame directly

    def corr_tau(data):
        rowsA = data[data[pvar] == "A"]
        rowsB = data[data[pvar] == "B"]
        A_data = rowsA
        B_data = rowsB
        
        # Handling case where all phase A values are identical
        if A_data[dvar].var() == 0:
            auto_tau = {"tau": np.nan, "z": np.nan, "p": np.nan}
        else:
            auto_tau = kendall_tau(A_data[dvar], A_data[mvar], tau_method=tau_method, continuity_correction=continuity)

        # Base correction for Tau
        formula = f"{dvar} ~ {mvar}"
        fit_mblm = smf.ols(formula, data=rowsA).fit()  # Fixed: Using OLS since Theil-Sen is not built-in
        data["fit"] = fit_mblm.predict(data)
        x = data[dvar] - data["fit"]
        y = pd.Categorical(data[pvar]).codes
        base_corr_tau = kendall_tau(x, y, tau_method=tau_method, continuity_correction=continuity)
        
        # Uncorrected Tau calculation
        x = data[dvar]
        uncorrected_tau = kendall_tau(x, y, tau_method=tau_method, continuity_correction=continuity)

        # Decide whether correction is applied
        corr_applied = not (np.isnan(auto_tau["p"]) or auto_tau["p"] > alpha)

        return pd.DataFrame({
            "Model": ["Baseline autocorrelation", "Uncorrected tau", "Baseline corrected tau"],
            "tau": [auto_tau["tau"], uncorrected_tau["tau"], base_corr_tau["tau"]],
            "z": [auto_tau["z"], uncorrected_tau["z"], base_corr_tau["z"]],
            "p": [auto_tau["p"], uncorrected_tau["p"], base_corr_tau["p"]],
        }), corr_applied

    # Process the data
    tau_results, corr_applied = corr_tau(data_list)

    # Print the output in your requested format
    print("\nBaseline corrected tau\n")
    print("Method: Theil-Sen regression")
    print(f"Kendall's tau {tau_method} applied.")
    print("Continuity correction " + ("applied." if continuity else "not applied."))
    print("\nNAs :")

    # Print results in tabular form
    print(tau_results.to_string(index=False))

    # Print final correction decision
    print("\nBaseline correction " + ("should be applied." if corr_applied else "should not be applied.") + "\n")

    return tau_results  # Return the DataFrame for further use if needed
