import pandas as pd
import numpy as np


def extract_chosen_isolates(
    chosen_isolates: pd.DataFrame, matrix_EU: pd.DataFrame
) -> pd.DataFrame:
    """
    Select the chosen isolates from the script. Return a DataFrame only containing the rows of selected isolates
    """
    chosen_rows = matrix_EU["Isolate"].isin(chosen_isolates["Isolate"])
    return matrix_EU[chosen_rows]


def find_digits(SIR: str) -> int:
    """Find numbers in a string"""
    digit = ""
    for character in SIR:
        if character.isdigit() or character == ".":
            digit += character
    return float(digit)


def get_scale(SIR: str) -> bool:
    """Get on or off scale. True == on-scale"""
    if "=" in SIR:
        return True
    elif "<" in SIR or ">" in SIR:
        return False
    else:
        raise ValueError("Not a valid SIR")


def parse_on_off_scale(
    scale: bool, SIR_category: str, y_values: list, mic_value_jitter: float
) -> None:
    if scale is True:
        y_values.append(mic_value_jitter)

    # If off-scale move value to MAX_C or MIN_C
    elif scale is False:
        if SIR_category == "S":
            y_values.append(-10)
        elif SIR_category == "R":
            y_values.append(11)
        else:
            raise ValueError(f"SIR Category must be either S or R, not: {SIR_category}")
    else:
        raise ValueError(
            f"scale must be Boolean value, not {type(scale)}. Current value: {scale}"
        )


def parse_fastidious(
    fastidious_dict: dict, pathogen: str, fastidious_list: list
) -> None:
    if pathogen in fastidious_dict["Fastidious"]:
        fastidious_list.append("Fastidious")
    elif pathogen in fastidious_dict["Non-fastidious"]:
        fastidious_list.append("Non-fastidious")
    else:
        raise ValueError(f"Pathogen must be Fastidious or Non-fastidious")


def parse_SIR(SIR: str) -> bool:
    """
    Find the isolates with valid SIRs. Not 'Missing BP'
    and not 'nip'.
    """
    if SIR.startswith("Missing BP"):
        return False
    if SIR == "nip":
        return False
    return True


def extract_SIR(chosen_isolates: pd.DataFrame, antibiotics: list) -> dict:
    """
    Extract all SIRs for an antibiotic. Returns a dictionary
    with antibiotcs as keys and lists of the isolates and their
    SIRs in tuples as value.
    """
    chosen_isolates_SIR = {antibiotic: [] for antibiotic in antibiotics}

    for index, row in chosen_isolates.iterrows():
        isolate, pathogen, antibiotic_SIR = row[0], row[1], list(row[3:].items())
        for antibiotic, SIR in antibiotic_SIR:
            if parse_SIR(SIR):
                mic_category = SIR[0]
                mic = find_digits(SIR)
                scale = get_scale(SIR)
                chosen_isolates_SIR[antibiotic].append(
                    (isolate, mic, mic_category, scale, pathogen)
                )
            else:
                # If SIR = "Missing BP" or "nip"
                chosen_isolates_SIR[antibiotic].append(
                    (isolate, SIR, None, None, pathogen)
                )
    return chosen_isolates_SIR


def filter_mic_values(chosen_isolates_SIR: dict) -> None:
    """
    Remove the tuples that have None in their SIR data
    """
    for antibiotic, SIR_data in chosen_isolates_SIR.items():
        # tup = (isolate, mic_value, mic_category, scale, pathogen)

        chosen_isolates_SIR[antibiotic] = [
            tup for tup in SIR_data if tup[2] is not None
        ]

    return chosen_isolates_SIR


def extract_mic_data(chosen_isolates_SIR: dict, antibiotics: list) -> list:
    """
    Extract the mic-values of each isolate for each antibiotic.
    Returns a nested list. Each list represents the mic-values of
    all isolates for an antibiotic.
    """
    mic_values = []
    # Iterate over all antibiotics
    for antibiotic in antibiotics:
        # Create a list to hold the mic-values of isolates for that abx
        antibiotic_mic_values = []
        # Get value of current abx.
        SIR_data = chosen_isolates_SIR[antibiotic]
        for isolate, mic_value, mic_category, scale, pathogen in SIR_data:
            antibiotic_mic_values.append(
                (isolate, np.log2(mic_value), mic_category, scale, pathogen)
            )
        mic_values.append(antibiotic_mic_values)
    return mic_values
