import pandas as pd

def recombine_phases(data, phases=(1, 2), set_phases=True, phase_names=("A", "B"), pvar="phase"):
    """
    Recombine phases in a Single-Case DataFrame (SCD).

    Parameters:
    - data (pd.DataFrame): The SCD dataset.
    - phases (tuple or list): Two phases to combine (numeric index or names).
    - set_phases (bool, default=True): Whether to rename the phases.
    - phase_names (tuple, default=("A", "B")): Names for the new phases.
    - pvar (str, default="phase"): The phase column name.

    Returns:
    - pd.DataFrame: A modified SCD dataset with recombined phases.
    """
    warning_messages = []
    dropped_cases = []
    design_list = []
    
    for case in data["case"].unique():
        case_data = data[data["case"] == case].copy()
        phase_values = case_data[pvar].astype(str).tolist()
        unique_phases = list(pd.Series(phase_values).unique())

        # Determine which phases to select
        if isinstance(phases, (tuple, list)) and len(phases) == 2:
            phases_A, phases_B = phases
        else:
            raise ValueError("Phases argument must contain exactly two elements.")

        # Validate phases
        if isinstance(phases_A, str) and isinstance(phases_B, str):
            if phases_A not in unique_phases or phases_B not in unique_phases:
                warning_messages.append(f"Phase(s) not found for case {case}. Dropping case.")
                dropped_cases.append(case)
                continue

        # Identify indices of selected phases
        A_indices = case_data.index[case_data[pvar] == phases_A]
        B_indices = case_data.index[case_data[pvar] == phases_B]

        # Rename phases if set_phases=True
        if set_phases:
            case_data.loc[A_indices, pvar] = phase_names[0]
            case_data.loc[B_indices, pvar] = phase_names[1]

        # Keep only selected phases
        case_data = case_data.loc[A_indices.union(B_indices)]
        design_list.append(unique_phases)

    # Drop cases with missing phases
    if warning_messages:
        print("\n".join(warning_messages))
    
    data = data[~data["case"].isin(dropped_cases)]
    return data
