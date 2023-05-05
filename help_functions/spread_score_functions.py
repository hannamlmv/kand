"""
Functions used to calculate the spread in a list. 
Used in score_calc_functions

Date: 24/4 
Author: Victor Wong
"""


def count_gap_length(valid_list: list) -> float:
    """Calculates the gap length for a spread list and penalizes."""
    total_gap_length = 0
    gap_length = 0

    for value in valid_list:
        if value == 0:
            gap_length += 1
        else:  # if current value == 1
            if gap_length >= 2:
                total_gap_length += gap_length - 1
            gap_length = 0
    # If the last values were also 0s and the gap length is at least 2.
    # Add the length of the gap to the total gap length
    if gap_length >= 2:
        total_gap_length += gap_length - 1
    return total_gap_length

def check_edges(valid_list: list) -> float:
    """Checks if the edges are empty or not and penalizes accordingly."""
    edge_penalty = 0

    # Add 0.5 penalty if the edge values are empty.
    if valid_list[0] == 0:  # Check first value
        edge_penalty += 0.5
    if valid_list[-1] == 0:  # Check last value
        edge_penalty += 0.5

    return edge_penalty

def score_spread_list(spread_list: list) -> float:
    """Calculates the score"""
    valid_list = [i for i in spread_list if i == 0 or i == 1]

    if len(valid_list) <= 1:
        raise ValueError("Length of valid list must be greater than 1")

    penalty = 0
    penalty += count_gap_length(valid_list)
    penalty += check_edges(valid_list)

    score = 1 - penalty / len(valid_list)

    return score
