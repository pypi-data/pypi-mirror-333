import pandas as pd
from itertools import groupby

def create_scd(values, B_start=None, mt=None, phase=None, phase_design=None, 
               phase_starts=None, name=None, dvar="values", pvar="phase", 
               mvar="mt", **kwargs):
    """
    Create a Single-Case DataFrame (SCD) similar to scdf in R.
    
    Parameters:
    - values (list or dict): Measurement values, optionally with phase labels.
    - B_start (int, optional): Deprecated; used only for simple AB designs.
    - mt (list, optional): Measurement time points.
    - phase (list, optional): Phase sequence.
    - phase_design (dict, optional): Named dict defining phase names and lengths.
    - phase_starts (dict, optional): Named dict defining phase start points.
    - name (str, optional): Case name.
    - dvar (str, default="values"): Name of the dependent variable.
    - pvar (str, default="phase"): Name of the phase variable.
    - mvar (str, default="mt"): Name of the measurement-time variable.
    - **kwargs: Additional variables (e.g., teacher, hour).
    
    Returns:
    - pd.DataFrame: A DataFrame representing the single-case data.
    
    Raises:
    - ValueError: If dependent variable or measurement-time is not defined correctly.
    """

    data = kwargs  # Additional variables

    # Handle values with named phases
    if isinstance(values, dict):
        flattened_values = []
        phases = []
        for phase_name, vals in values.items():
            flattened_values.extend(vals)
            phases.extend([phase_name] * len(vals))
        values = flattened_values
    else:
        phases = None  # Will be assigned later
    
    data[dvar] = values

    # Generate measurement times if missing
    if mt is None:
        mt = list(range(1, len(values) + 1))
    data[mvar] = mt

    # Handle phase assignment
    if phases is None:
        if phase is not None:
            phase_design = {k: len(list(g)) for k, g in groupby(phase)}
        elif phase_starts is not None:
            phase_design = phase_starts_to_design(phase_starts, mt)
        elif phase_design is None:
            raise ValueError("Phase design not defined correctly!")

        phases = []
        for phase_name, length in phase_design.items():
            phases.extend([phase_name] * length)
    
    data[pvar] = phases

    # Assign case name to every row
    if name:
        data["case"] = [name] * len(values)

    # Ensure all columns have the same length
    max_len = len(values)
    for key in data:
        if len(data[key]) != max_len:
            raise ValueError(f"Column '{key}' must have {max_len} elements, but got {len(data[key])}.")

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Assign metadata attributes
    df.attrs.update({"dvar": dvar, "pvar": pvar, "mvar": mvar})
    if name:
        df.attrs["name"] = name

    return df

def phase_starts_to_design(phase_starts, mt):
    """ Convert phase_starts dict to phase_design dict. """
    sorted_starts = sorted(phase_starts.items(), key=lambda x: x[1])
    phase_lengths = {sorted_starts[i][0]: mt.index(sorted_starts[i+1][1]) - mt.index(sorted_starts[i][1])
                     for i in range(len(sorted_starts) - 1)}
    last_phase = sorted_starts[-1][0]
    phase_lengths[last_phase] = len(mt) - mt.index(sorted_starts[-1][1])
    return phase_lengths