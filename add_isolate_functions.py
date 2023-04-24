import numpy as np
from isolate_class import Isolate
from panel_class import Panel
from score_calc_functions import (
    calc_coverage_score,
    calc_redundancy_score,
    calc_spread_score,
)


def try_isolates(
    available_isolates: list(Isolate), panel: Panel, hyperparameters: np.ndarray
):
    best_isolate, best_score = None, 0

    for isolate in available_isolates:
        panel.append_isolate(isolate)
        temp_spread_score = calc_spread_score(panel)
        temp_coverage_score = calc_coverage_score(panel)
        temp_redundancy_score = calc_redundancy_score(panel)
        temp_scores = np.array(
            (temp_spread_score, temp_coverage_score, temp_redundancy_score)
        )
        temp_total_score = (temp_scores @ hyperparameters).sum()
        if temp_total_score > best_score:
            best_score = temp_total_score
            best_isolate = isolate
        panel.remove_isolate(isolate)
    panel.append_isolate(best_isolate)


def add_isolate(
    n: int, all_isolates: list(Isolate), panel: Panel, hyperparameter: np.ndarray
):
    available_isolates = [
        isolate
        for isolate in all_isolates
        if isolate.get_name() not in panel.get_all_isolate_names()
    ]

    for _ in range(n):
        chosen_isolate = try_isolates(available_isolates, panel, hyperparameter)
        available_isolates.remove(chosen_isolate)
