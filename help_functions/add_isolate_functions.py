"""
Adds isolates to a panel

Date: 25/4 
Author: Victor Wong and Hanna Malmvall
"""

import numpy as np
from Classes.isolate_class import Isolate
from Classes.panel_class import Panel
from help_functions.score_calc_functions import calc_scores

def choose_isolate(
    available_isolates: list[Isolate],
    panel: Panel,
    coefficients: np.ndarray,
    concentration_ranges: dict,
    redundancy_threshold: int,
    coverage_penalties: dict,
    coverage_total: int,
) -> Isolate:
    """
    Iterates over all available isolates. For each isolate:
        1. Add it to the panel
        2. Calculate all scores
        3. Check if the score is better than current best, if yes, then replace, else, pass
    Return best isolate
    """

    best_isolate, best_score = None, -np.inf
    best_score_vec = None
    for isolate in available_isolates:
        panel.append_isolate(isolate)
        temp_spread_score, temp_coverage_score, temp_redundancy_score = calc_scores(
            panel,
            concentration_ranges,
            redundancy_threshold,
            coverage_penalties,
            coverage_total,
        )
        temp_scores = np.array(
            (
                temp_spread_score,
                temp_coverage_score,
                -temp_redundancy_score,
            )
        )
        # Matrix multiplcation to get coefficients times scores
        temp_total_score = (temp_scores @ coefficients).sum()
        if temp_total_score > best_score:
            best_score = temp_total_score
            best_isolate = isolate
            best_score_vec = temp_scores
        panel.remove_isolate(isolate)
    panel.append_isolate(best_isolate)
    print(best_isolate, best_score, best_score_vec)
    return best_isolate

def add_isolate(
    number_of_isolates: int,
    all_isolates: list[Isolate],
    panel: Panel,
    coefficients: np.ndarray,
    concentration_ranges: dict,
    redundancy_threshold: int,
    coverage_penalties: dict,
    coverage_total: int,
):
    """ Use choose_isolate function to add desired number of isolates to the panel. """
    available_isolates = [
        isolate
        for isolate in all_isolates
        if isolate.get_name() not in panel.get_all_isolate_names()
    ]

    for i in range(1, number_of_isolates + 1):
        chosen_isolate = choose_isolate(
            available_isolates,
            panel,
            coefficients,
            concentration_ranges,
            redundancy_threshold,
            coverage_penalties,
            coverage_total,
        )
        available_isolates.remove(chosen_isolate)
        if i % 10 == 0:
            print(f"{i} isolates have been added")
