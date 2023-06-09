"""
Data extraction functions

Date: 10/4 
Author: Victor Wong
"""

import pandas as pd
import numpy as np

def extract_chosen_isolates(
    chosen_isolates: pd.DataFrame, matrix_EU: pd.DataFrame
) -> pd.DataFrame:
    """
    Select the chosen isolates from the script. Return a
    DataFrame only containing the rows of selected isolates.
    """
    chosen_rows = matrix_EU["Isolate"].isin(chosen_isolates["Isolate"])
    return matrix_EU[chosen_rows]

def find_digits(mic_sir_data: str) -> int:
    """Find numbers in a string."""
    digit = ""
    for character in mic_sir_data:
        if character.isdigit() or character == ".":
            digit += character
    return float(digit)

def get_scale(mic_sir_data: str) -> bool:
    """Get on or off scale. True == on-scale."""
    if "=" in mic_sir_data:
        return True
    elif "<" in mic_sir_data or ">" in mic_sir_data:
        return False
    else:
        raise ValueError("Not a valid SIR")

def parse_on_off_scale(
    scale: bool,
    sir_category: str,
    y_values: list[float],
    mic_value_jitter: float,
    min_conc=-10,
    max_conc=11,
) -> None:
    """
    Adds the correct placement y-value placement for each data point.
    If the point is off-scale it will move it either the top or bottom of the plot
    """

    if not isinstance(scale, bool):
        raise ValueError(
            f"scale must be Boolean value, not {type(scale)}. Current value: {scale}"
        )

    if scale is True:
        y_values.append(mic_value_jitter)

    # TODO: Remove hard-coding of -10 and 11 which are the maximum and minimum values for the y_range
    # If off-scale move value to MAX_C or MIN_C
    elif scale is False:
        if sir_category == "S":
            y_values.append(min_conc)
        elif sir_category == "R":
            y_values.append(max_conc)
        else:
            raise ValueError(f"SIR Category must be either S or R, not: {sir_category}")

def parse_fastidious(
    fastidious_dict: dict[str:str], pathogen: str, fastidious_list: list[str]
) -> None:
    """Adds the fastidiousness of the isolate to the fastidious list."""
    if (
        pathogen not in fastidious_dict["Kräsen"]
        and pathogen not in fastidious_dict["Icke-kräsen"]
    ):
        raise ValueError(f"Pathogen name, {pathogen}, not found in dictionary")
    if (
        pathogen in fastidious_dict["Kräsen"]
        and pathogen in fastidious_dict["Icke-kräsen"]
    ):
        raise LookupError(
            f"Pathogen must be either fastidious or non-fastidious. Error raised by: {pathogen}"
        )
    if pathogen in fastidious_dict["Kräsen"]:
        fastidious_list.append("Kräsen")
    elif pathogen in fastidious_dict["Icke-kräsen"]:
        fastidious_list.append("Icke-kräsen")

def parse_mic_sir_data(mic_sir_data: str) -> bool:
    """
    Find the isolates with valid data. Not 'Missing BP'
    and not 'nip'.
    """
    if type(mic_sir_data) is not str:
        return False
    if mic_sir_data.startswith("Missing BP"):
        return False
    if mic_sir_data == "nip":
        return False
    return True

def extract_mic_sir_data(chosen_isolates: pd.DataFrame, antibiotics: list[str]) -> dict:
    """
    Extract all SIRs for an antibiotic. Returns a dictionary
    with antibiotcs as keys and lists of the isolates and their
    SIRs in tuples as value.
    """
    chosen_isolates_mic_sir_data = {antibiotic: [] for antibiotic in antibiotics}

    for index, row in chosen_isolates.iterrows():
        isolate, pathogen, antibiotic_mic_sir_data = (
            row[0],
            row[1],
            list(row[3:].items()),
        )
        for antibiotic, mic_sir_data in antibiotic_mic_sir_data:
            if parse_mic_sir_data(mic_sir_data):
                sir_category = mic_sir_data[0]
                mic = find_digits(mic_sir_data)
                scale = get_scale(mic_sir_data)
                chosen_isolates_mic_sir_data[antibiotic].append(
                    (isolate, mic, sir_category, scale, pathogen)
                )
            else:
                chosen_isolates_mic_sir_data[antibiotic].append(
                    (isolate, mic_sir_data, None, None, pathogen)
                )
    return chosen_isolates_mic_sir_data

def filter_mic_sir_data(chosen_isolates_mic_sir_data: dict[str:tuple]) -> None:
    """
    Remove the tuples that have None in their SIR data.
    """
    for antibiotic, mic_sir_data in chosen_isolates_mic_sir_data.items():
         chosen_isolates_mic_sir_data[antibiotic] = [
            tup for tup in mic_sir_data if tup[2] is not None
        ]

    return chosen_isolates_mic_sir_data

def extract_mic_values_per_antibiotic(
    chosen_isolates_sir: dict, antibiotics: list[str]
) -> list:
    """
    Extract the mic-values of each isolate for each antibiotic.
    Returns a nested list. Each list represents the mic-values of
    all isolates for an antibiotic.
    """
    mic_values = []
    # Iterate over all antibiotics
    for antibiotic in antibiotics:
        # Create a list to hold the mic-values of isolates for that antibiotic
        antibiotic_mic_values = []
        # Get value of current antibiotic
        sir_data = chosen_isolates_sir[antibiotic]
        for isolate, mic_value, mic_category, scale, pathogen in sir_data:
            antibiotic_mic_values.append(
                (isolate, np.log2(mic_value), mic_category, scale, pathogen)
            )
        mic_values.append(antibiotic_mic_values)
    return mic_values
