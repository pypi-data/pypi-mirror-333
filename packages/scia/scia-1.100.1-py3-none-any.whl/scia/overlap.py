import pandas as pd
import numpy as np
from scia.preprocess import prepare_scd
from scia.recombine import recombine_phases
from scia.utils import revise_names
from scia.pnd import pnd
from scia.pem import pem
from scia.pet import pet
from scia.nap import nap
from scia.pand import pand
from scia.ird import ird
from scia.tau_u import tau_u
from scia.corrected_tau import corrected_tau
import io
import sys
from contextlib import redirect_stdout

# Define a context manager to suppress stdout
class SuppressOutput:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = io.StringIO()
        return sys.stdout
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self._original_stdout

def extract_number_from_ird(result):
    """Extract numeric IRD value from the dictionary output of ird()."""
    if isinstance(result, dict) and "ird" in result:
        return float(result["ird"]) if result["ird"] is not None else np.nan
    return np.nan

def overlap(data, dvar=None, pvar=None, mvar=None, decreasing=False, phases=("A", "B")):
    # Handle missing variable names
    if dvar is None:
        dvar = 'values'
    if pvar is None:
        pvar = 'phase'
    if mvar is None:
        mvar = 'mt'

    # Prepare and recombine phases
    data = prepare_scd(data)
    data = recombine_phases(data, phases=phases)

    # Get case names
    case_names = data["case"].unique()

    # Define DataFrame columns
    vars = ["PND", "PEM", "PET", "NAP", "NAP rescaled", "PAND", 
            "IRD", "Tau_U(A)", "Tau_U(BA)", "Base_Tau", "Diff_mean", 
            "Diff_trend", "SMD", "Hedges_g"]
    
    df = pd.DataFrame(columns=vars, index=range(len(case_names)))
    df['Case'] = case_names

    for i, case in enumerate(case_names):
        case_data = data[data["case"] == case]

        # Suppress output for all function calls
        with SuppressOutput():
            # Extract values safely
            df.at[i, 'PND'] = float(pnd(case_data, decreasing=decreasing)["PND (%)"].iloc[0].replace('%', ''))
            df.at[i, 'PEM'] = float(pem(case_data, decreasing=decreasing)["PEM"].iloc[0])
            df.at[i, 'PET'] = float(pet(case_data, decreasing=decreasing)["PET"].iloc[0])
            df.at[i, 'NAP'] = float(nap(case_data, decreasing=decreasing)["NAP"].iloc[0])
            df.at[i, 'NAP rescaled'] = float(nap(case_data, decreasing=decreasing)["NAP Rescaled"].iloc[0])
            df.at[i, 'PAND'] = float(pand(case_data, decreasing=decreasing, return_values=True)["pand"])
            
            # Extract IRD correctly
            ird_result = ird(case_data, dvar=dvar, pvar=pvar, decreasing=decreasing, phases=phases)
            df.at[i, 'IRD'] = extract_number_from_ird(ird_result)

            # Extract Tau-U values
            tau_results = tau_u(case_data)
            df.at[i, 'Tau_U(A)'] = float(tau_results.loc["A vs. B - Trend A", "Tau"])
            df.at[i, 'Tau_U(BA)'] = float(tau_results.loc["A vs. B + Trend B - Trend A", "Tau"])
            
            # Extract Corrected Tau
            corrected_tau_results = corrected_tau(case_data)
            df.at[i, 'Base_Tau'] = float(corrected_tau_results[corrected_tau_results["Model"] == "Baseline corrected tau"]["tau"].iloc[0])

        # Compute mean differences, SMD, Hedges' g, trend differences
        A = case_data[case_data[pvar] == 'A'][dvar]
        B = case_data[case_data[pvar] == 'B'][dvar]
        mtA = case_data[case_data[pvar] == 'A'][mvar]
        mtB = case_data[case_data[pvar] == 'B'][mvar]

        nA = len(A.dropna())
        nB = len(B.dropna())
        n = nA + nB
        mA = A.mean()
        mB = B.mean()
        sdA = A.std()
        sdB = B.std()

        df.at[i, 'Diff_mean'] = mB - mA
        df.at[i, 'SMD'] = (mB - mA) / sdA if sdA != 0 else np.nan
        sd_hg = np.sqrt(((nA - 1) * sdA**2 + (nB - 1) * sdB**2) / (nA + nB - 2)) if nA + nB - 2 > 0 else np.nan
        df.at[i, 'Hedges_g'] = (mB - mA) / sd_hg if sd_hg is not np.nan else np.nan
        df.at[i, 'Hedges_g'] *= (1 - (3 / (4 * n - 9))) if n > 9 else np.nan

        trend_A = np.polyfit(mtA - mtA.iloc[0] + 1, A, 1)[0] if len(mtA) > 1 else np.nan
        trend_B = np.polyfit(mtB - mtB.iloc[0] + 1, B, 1)[0] if len(mtB) > 1 else np.nan
        df.at[i, 'Diff_trend'] = trend_B - trend_A if trend_A is not np.nan and trend_B is not np.nan else np.nan

    return df  # Return only the final DataFrame with no extra prints












# import pandas as pd
# import numpy as np
# from scia.preprocess import prepare_scd
# from scia.recombine import recombine_phases
# from scia.utils import revise_names
# from scia.pnd import pnd
# from scia.pem import pem
# from scia.pet import pet
# from scia.nap import nap
# from scia.pand import pand
# from scia.ird import ird
# from scia.tau_u import tau_u
# from scia.corrected_tau import corrected_tau

# def extract_number_from_ird(result):
#     """Extract numeric IRD value from the dictionary output of ird()."""
#     if isinstance(result, dict) and "ird" in result:
#         return float(result["ird"]) if result["ird"] is not None else np.nan
#     return np.nan

# def overlap(data, dvar=None, pvar=None, mvar=None, decreasing=False, phases=("A", "B")):
#     # Handle missing variable names
#     if dvar is None:
#         dvar = 'values'
#     if pvar is None:
#         pvar = 'phase'
#     if mvar is None:
#         mvar = 'mt'

#     # Prepare and recombine phases
#     data = prepare_scd(data)
#     data = recombine_phases(data, phases=phases)

#     # Get case names
#     case_names = data["case"].unique()

#     # Define DataFrame columns
#     vars = ["PND", "PEM", "PET", "NAP", "NAP rescaled", "PAND", 
#             "IRD", "Tau_U(A)", "Tau_U(BA)", "Base_Tau", "Diff_mean", 
#             "Diff_trend", "SMD", "Hedges_g"]
    
#     df = pd.DataFrame(columns=vars, index=range(len(case_names)))
#     df['Case'] = case_names

#     for i, case in enumerate(case_names):
#         case_data = data[data["case"] == case]

#         # Extract values safely
#         df.at[i, 'PND'] = float(pnd(case_data, decreasing=decreasing)["PND (%)"].iloc[0].replace('%', ''))
#         df.at[i, 'PEM'] = float(pem(case_data, decreasing=decreasing)["PEM"].iloc[0])
#         df.at[i, 'PET'] = float(pet(case_data, decreasing=decreasing)["PET"].iloc[0])
#         df.at[i, 'NAP'] = float(nap(case_data, decreasing=decreasing)["NAP"].iloc[0])
#         df.at[i, 'NAP rescaled'] = float(nap(case_data, decreasing=decreasing)["NAP Rescaled"].iloc[0])

#         # **Extract PAND correctly using return_values=True**
#         df.at[i, 'PAND'] = float(pand(case_data, decreasing=decreasing, return_values=True)["pand"])

#         # Extract IRD Correctly
#         ird_result = ird(case_data, dvar=dvar, pvar=pvar, decreasing=decreasing, phases=phases)
#         df.at[i, 'IRD'] = extract_number_from_ird(ird_result)

#         # Extract Tau-U values correctly
#         tau_results = tau_u(case_data)
#         df.at[i, 'Tau_U(A)'] = float(tau_results.loc["A vs. B - Trend A", "Tau"])
#         df.at[i, 'Tau_U(BA)'] = float(tau_results.loc["A vs. B + Trend B - Trend A", "Tau"])
        
#         # Extract Corrected Tau
#         corrected_tau_results = corrected_tau(case_data)
#         df.at[i, 'Base_Tau'] = float(corrected_tau_results[corrected_tau_results["Model"] == "Baseline corrected tau"]["tau"].iloc[0])

#         # Compute mean differences, SMD, Hedges' g, trend differences
#         A = case_data[case_data[pvar] == 'A'][dvar]
#         B = case_data[case_data[pvar] == 'B'][dvar]
#         mtA = case_data[case_data[pvar] == 'A'][mvar]
#         mtB = case_data[case_data[pvar] == 'B'][mvar]

#         nA = len(A.dropna())
#         nB = len(B.dropna())
#         n = nA + nB
#         mA = A.mean()
#         mB = B.mean()
#         sdA = A.std()
#         sdB = B.std()

#         df.at[i, 'Diff_mean'] = mB - mA
#         df.at[i, 'SMD'] = (mB - mA) / sdA if sdA != 0 else np.nan
#         sd_hg = np.sqrt(((nA - 1) * sdA**2 + (nB - 1) * sdB**2) / (nA + nB - 2)) if nA + nB - 2 > 0 else np.nan
#         df.at[i, 'Hedges_g'] = (mB - mA) / sd_hg if sd_hg is not np.nan else np.nan
#         df.at[i, 'Hedges_g'] *= (1 - (3 / (4 * n - 9))) if n > 9 else np.nan

#         trend_A = np.polyfit(mtA - mtA.iloc[0] + 1, A, 1)[0] if len(mtA) > 1 else np.nan
#         trend_B = np.polyfit(mtB - mtB.iloc[0] + 1, B, 1)[0] if len(mtB) > 1 else np.nan
#         df.at[i, 'Diff_trend'] = trend_B - trend_A if trend_A is not np.nan and trend_B is not np.nan else np.nan

#     return df  # Return only the final DataFrame with no extra prints
