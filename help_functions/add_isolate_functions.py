import numpy as np
from isolate_class import Isolate
from panel_class import Panel
from help_functions.score_calc_functions import calc_scores


def choose_isolate(
    available_isolates: list[Isolate],
    panel: Panel,
    hyperparameters: np.ndarray,
    concentration_ranges: dict,
    redundancy_threshold: int,
):
    """
    Iterates over all available isolates. For each isolate:
        1. Add it to the panel
        2. Calculate all scores
        3. Check if the score is better than current best, if yes, then replace, else, pass
    Add the best isolate to the panel
    """
    best_isolate, best_score = None, -np.inf
    best_score_vec = None

    for isolate in available_isolates:
        panel.append_isolate(isolate)
        temp_spread_score, temp_coverage_score, temp_redundancy_score = calc_scores(
            panel, concentration_ranges, redundancy_threshold
        )
        temp_scores = np.array(
            (
                temp_spread_score,
                temp_coverage_score,
                -temp_redundancy_score,
                # panel.get_number_of_isolates(),
            )
        )
        # Matrix multiplcation to get coefficients times scores
        temp_total_score = (temp_scores @ hyperparameters).sum()
        if temp_total_score > best_score:
            best_score = temp_total_score
            best_isolate = isolate
            best_score_vec = temp_scores
        panel.remove_isolate(isolate)
    panel.append_isolate(best_isolate)
    return best_isolate


def add_isolate(
    number_of_isolates: int,
    all_isolates: list[Isolate],
    panel: Panel,
    hyperparameter: np.ndarray,
    concentration_ranges: dict,
    redundancy_threshold: int = 1,
):
    """Uses choose_isolate() function to add n isolates to the panel"""
    available_isolates = [
        isolate
        for isolate in all_isolates
        if isolate.get_name() not in panel.get_all_isolate_names()
    ]

    for _ in range(number_of_isolates):
        chosen_isolate = choose_isolate(
            available_isolates,
            panel,
            hyperparameter,
            concentration_ranges,
            redundancy_threshold,
        )
        available_isolates.remove(chosen_isolate)
