import numpy as np
from isolate_class import Isolate
from panel_class import Panel
from score_calc_functions import (
    calc_coverage_score,
    calc_redundancy_score,
    calc_spread_score,
)


def choose_isolate(
    available_isolates: list(Isolate), panel: Panel, hyperparameters: np.ndarray
):
    """
    Iterates over all available isolates. For each isolate:
        1. Add it to the panel
        2. Calculate all scores
        3. Check if the score is better than current best, if yes, then replace, else, pass
    Add the best isolate to the panel
    """
    best_isolate, best_score = None, 0

    for isolate in available_isolates:
        panel.append_isolate(isolate)
        temp_spread_score = calc_spread_score(panel)
        temp_coverage_score = calc_coverage_score(panel)
        temp_redundancy_score = calc_redundancy_score(panel)
        temp_scores = np.array(
            (
                temp_spread_score,
                temp_coverage_score,
                temp_redundancy_score,
                panel.get_number_of_isolates(),
            )
        )
        # Matrix multiplcation to get coefficients times scores
        temp_total_score = (temp_scores @ hyperparameters).sum()
        if temp_total_score > best_score:
            best_score = temp_total_score
            best_isolate = isolate
        panel.remove_isolate(isolate)
    panel.append_isolate(best_isolate)


def add_isolate(
    n: int, all_isolates: list(Isolate), panel: Panel, hyperparameter: np.ndarray
):
    """Uses choose_isolate() function to add n isolates to the panel"""
    available_isolates = [
        isolate
        for isolate in all_isolates
        if isolate.get_name() not in panel.get_all_isolate_names()
    ]

    for _ in range(n):
        chosen_isolate = choose_isolate(available_isolates, panel, hyperparameter)
        available_isolates.remove(chosen_isolate)
