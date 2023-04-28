"""
Generates print-out of spread for different antibiotics 
"""

import pandas as pd
import json
from pprint import pprint
from help_functions.create_panel import create_panel
from help_functions.score_calc_functions import extract_panel_data, calc_spread_score

def main(chosen_isolates, all_isolates):

    for isolates in [chosen_isolates, all_isolates]:
        isolate_list = pd.read_csv(isolates)["Isolate"].tolist()
        isolate_panel = create_panel(isolate_list)
        spread_per_abx = calc_spread_score(
            extract_panel_data(isolate_panel),
            json.load(open("abx_ranges.json")),
            isolate_panel.get_number_antibiotics(),
            True
        )
        if isolates == chosen_isolates:
            chosen_spread_per_abx = spread_per_abx
        else:
            all_spread_per_abx = spread_per_abx
    
    for abx in chosen_spread_per_abx:
            if all_spread_per_abx[abx] == 0:
                 chosen_spread_per_abx[abx] = 1.0
            else:
                chosen_spread_per_abx[abx] = round(chosen_spread_per_abx[abx]/all_spread_per_abx[abx], 2)

    pprint(chosen_spread_per_abx)
        
if __name__ == "__main__":
    main(
        "Chosen_isolates_folder/Chosen_isolates.csv", 
        "Chosen_isolates_folder/all_isolates.csv"
        )
