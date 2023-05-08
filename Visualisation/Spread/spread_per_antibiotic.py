"""
Generates print-out of spread for different antibiotics 

Date: 28/4 
Author: Hanna Malmvall
"""

import pandas as pd
import json
from prettytable import PrettyTable
from help_functions.create_panel import create_panel
from help_functions.score_calc_functions import extract_panel_data, calc_spread_score

def main(chosen_isolates: str, all_isolates: str) -> None:
    """Calculates and prints the relative spread per antibiotic."""
    for isolates in [chosen_isolates, all_isolates]:
        isolate_list = pd.read_csv(isolates)["Isolate"].tolist()
        isolate_panel = create_panel(isolate_list)
        spread_per_antibiotic = calc_spread_score(
            extract_panel_data(isolate_panel),
            json.load(open("Parameters/antibiotic_info.json")),
            isolate_panel.get_number_antibiotics(),
            True,
        )
        if isolates == chosen_isolates:
            chosen_spread_per_antibiotic = spread_per_antibiotic
        else:
            all_spread_per_antibiotic = spread_per_antibiotic

    for antibiotic in chosen_spread_per_antibiotic:
        if all_spread_per_antibiotic[antibiotic] == 0:
            chosen_spread_per_antibiotic[antibiotic] = 1.0
        else:
            chosen_spread_per_antibiotic[antibiotic] = round(
                chosen_spread_per_antibiotic[antibiotic] / all_spread_per_antibiotic[antibiotic], 2
            )

    table = PrettyTable()
    table.field_names = ["Antibiotika", "Relativ spridning"]
    for antibiotic, mic in chosen_spread_per_antibiotic.items():
        table.add_row([antibiotic, mic])

    print(table)

if __name__ == "__main__":
    main(
        "Chosen_isolates_folder/Chosen_isolates.csv",
        "Chosen_isolates_folder/all_isolates.csv",
    )
