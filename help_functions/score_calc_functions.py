"""
Calculates scores for a given panel

Date: 25/4 
Author: Victor Wong and Hanna Malmvall
"""

import numpy as np
from Classes.panel_class import Panel
from help_functions.spread_score_functions import score_spread_list


def concentration_to_index(concentration: float, abs_lowest_concentration: int):
    """Converts the concentration to a list index value"""
    # print(concentration)
    return int(np.log2(float(concentration)) + abs_lowest_concentration)


def extract_panel_data(panel: Panel):
    """
    Convert the data of the isolates in the panel to a dictionary
    with antibiotic names as key and the isolates MIC values and SIR
    categories as value.
    """
    panel_data = {}
    for isolate in panel.get_chosen_isolates():
        for abx, (mic, sir) in isolate.get_data().items():
            if abx not in panel_data:
                panel_data[abx] = [(mic, sir)]
            else:
                panel_data[abx].append((mic, sir))
    return panel_data


def calc_spread_score(
    panel_data: dict,
    concentration_ranges: dict,
    number_of_antibiotics: int,
    per_antibiotic: bool = False,
):
    # TODO: Clean this function up. Very messy atm. Does too many things. concentration conversion should most likely
    # be handled in own function entirely instead of partly, which it is now.
    """Calculates the spread score"""
    total_spread_list_score = 0
    abs_lowest_concentration = np.abs(
        np.log2(concentration_ranges["Lowest concentration"])
    )
    spread_per_antibiotic = {}
    for abx, mic_sir in panel_data.items():
        # Create a set of the unique mic values and remove off-scale values, denoted as None
        unique_mic_values = {mic for mic, _ in mic_sir if mic is not None}

        # Get the minimum and maximum on-scale concentration value for the antibiotic
        minimum_concentration = concentration_ranges[abx]["Lower"]
        maximum_concentration = concentration_ranges[abx]["Upper"]

        # Convert the concentration values to indices
        if minimum_concentration == "Min_C":
            minimum_concentration_index = 0
        else:
            minimum_concentration_index = concentration_to_index(
                minimum_concentration, abs_lowest_concentration
            )
        if maximum_concentration == "Max_C":
            maximum_concentration_index = concentration_ranges[
                "Concentration range length"
            ]
        else:
            maximum_concentration_index = concentration_to_index(
                maximum_concentration, abs_lowest_concentration
            )

        # Create a list for each antibiotic to display the spread of values
        spread_list = [
            0 for _ in range(concentration_ranges["Concentration range length"])
        ]

        # Set all off-scale values to None in the spread_list
        # Behöver hantera MAX_C och MIN_C
        for index in range(len(spread_list)):
            if (
                index < minimum_concentration_index
                or index > maximum_concentration_index
            ):
                spread_list[index] = None

        for mic_value in unique_mic_values:
            mic_value_index = concentration_to_index(
                mic_value, abs_lowest_concentration
            )
            spread_list[mic_value_index] = 1
        total_spread_list_score += score_spread_list(spread_list)
        if per_antibiotic:
            spread_per_antibiotic[abx] = score_spread_list(spread_list)
    if per_antibiotic:
        return spread_per_antibiotic
    return total_spread_list_score / number_of_antibiotics


def calc_coverage_score(
    panel_data: dict,
    number_of_antibiotics: int,
    coverage_demands: dict,
    coverage_total: int,
):
    """Calculates the coverage score"""
    coverage_score = 0
    for mic_sir in panel_data.values():
        coverage_counter = {key: 0 for key in coverage_demands}
        for _, sir in mic_sir:
            coverage_counter[sir] += 1
        for sir in coverage_counter:
            coverage_counter[sir] = min(coverage_counter[sir], coverage_demands[sir])
        coverage_sir_score = sum(coverage_counter.values()) / sum(
            coverage_demands.values()
        )
        total_coverage = min(1, 1 / coverage_total * len(mic_sir))
        coverage_score += coverage_sir_score * total_coverage
    return coverage_score / number_of_antibiotics


def calc_redundancy_score(panel_data: dict, redundancy_threshold: int):
    """Calculates the redundancy score"""
    number_of_micS = 0
    number_of_redundant_micS = 0
    for mic_sir in panel_data.values():
        mic_counter = {}
        for mic, _ in mic_sir:
            number_of_micS += 1
            if mic not in mic_counter:
                mic_counter[mic] = 1
            else:
                mic_counter[mic] += 1
                if mic_counter[mic] > redundancy_threshold:
                    number_of_redundant_micS += 1
    if number_of_micS == 0:
        return 0
    return number_of_redundant_micS / number_of_micS


def calc_scores(
    panel: Panel,
    concentration_ranges: dict,
    redundancy_threshold: int,
    coverage_penalties: dict,
    coverage_total: int,
):
    """Calculates spread, coverage and redundancy score for entire panel"""
    antibiotic_mic = extract_panel_data(panel)
    scores = (
        calc_spread_score(
            antibiotic_mic, concentration_ranges, panel.get_number_antibiotics()
        ),
        calc_coverage_score(
            antibiotic_mic,
            panel.get_number_antibiotics(),
            coverage_penalties,
            coverage_total,
        ),
        calc_redundancy_score(antibiotic_mic, redundancy_threshold),
    )

    return scores


# Possible sub-division of calc_spread_score function:


# def calc_spread_score(panel_data: dict, concentration_ranges: dict, number_of_antibiotics: int, per_antibiotic: bool = False):
#     """Calculates the spread score"""
#     total_spread_list_score = 0
#     spread_per_antibiotic = {}

#     for abx, mic_sir in panel_data.items():
#         unique_mic_values = {mic for mic, _ in mic_sir if mic is not None}
#         abs_lowest_concentration = np.abs(np.log2(concentration_ranges["Lowest concentration"]))

#         spread_list = create_spread_list(unique_mic_values, abx, concentration_ranges, abs_lowest_concentration)
#         total_spread_list_score += score_spread_list(spread_list)

#         if per_antibiotic:
#             spread_per_antibiotic[abx] = score_spread_list(spread_list)

#     if per_antibiotic:
#         return spread_per_antibiotic
#     return total_spread_list_score / number_of_antibiotics


# def create_spread_list(unique_mic_values, abx, concentration_ranges, abs_lowest_concentration):
#     """Create a list for each antibiotic to display the spread of values"""
#     minimum_concentration_index, maximum_concentration_index = convert_concentrations_to_indices(
#         abx, concentration_ranges, abs_lowest_concentration
#     )
#     spread_list = set_off_scale_values_to_none(
#         minimum_concentration_index, maximum_concentration_index, concentration_ranges
#     )
#     spread_list = mark_mic_values(unique_mic_values, abs_lowest_concentration, spread_list)
#     return spread_list


# def convert_concentrations_to_indices(abx, concentration_ranges, abs_lowest_concentration):
#     """Convert the concentration values to indices"""
#     minimum_concentration = concentration_ranges[abx]["Lower"]
#     maximum_concentration = concentration_ranges[abx]["Upper"]

#     if minimum_concentration == "Min_C":
#         minimum_concentration_index = 0
#     else:
#         minimum_concentration_index = concentration_to_index(
#             minimum_concentration, abs_lowest_concentration
#         )

#     if maximum_concentration == "Max_C":
#         maximum_concentration_index = concentration_ranges["Concentration range length"]
#     else:
#         maximum_concentration_index = concentration_to_index(
#             maximum_concentration, abs_lowest_concentration
#         )

#     return minimum_concentration_index, maximum_concentration_index


# def set_off_scale_values_to_none(minimum_concentration_index, maximum_concentration_index, concentration_ranges):
#     """Set all off-scale values to None in the spread_list"""
#     spread_list = [None] * concentration_ranges["Concentration range length"]

#     for index in range(len(spread_list)):
#         if index < minimum_concentration_index or index > maximum_concentration_index:
#             spread_list[index] = None

#     return spread_list


# def mark_mic_values(unique_mic_values, abs_lowest_concentration, spread_list):
#     """Mark the MIC values in the spread_list"""
#     for mic_value in unique_mic_values:
#         mic_value_index = concentration_to_index(mic_value, abs_lowest_concentration)
#         spread_list[mic_value_index] = 1

#     return spread_list


# def concentration_to_index(concentration, abs_lowest_concentration):
#     """Convert the concentration to an index"""
#     return int(np.round(np.abs(np.log2(concentration)) - abs_lowest_concentration))
