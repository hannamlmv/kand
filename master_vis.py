"""
Generates visualisations and print-outs for a given panel

Date: 28/4 
Author: Hanna Malmvall
"""

import json
from help_functions.validate_parameters import validate_visualisation_parameters
from Visualisation.Spread.spread_plot import main as spread_vis
from Visualisation.Coverage.coverage_plots import main as coverage_vis
from Visualisation.Redundancy.redundancy_plots import main as redundancy
from help_functions.validate_parameters import validate_parameters

def main():
    """
    Generates all graphs and print-outs for a panel.Which ones are to
    be generated is specialised in visualisation_parameters.json.
    """
    panel = "Chosen_isolates_folder/Chosen_isolates.csv"
    all_isolates = "Chosen_isolates_folder/all_isolates.csv"
    bools = validate_visualisation_parameters(
        json.load(open("Parameters/visualisation_parameters.json"))
        )
    _, _, _, _, redundancy_threshold = validate_parameters(
        json.load(open("Parameters/isolate_selection_parameters.json"))
        )

    # Spread
    if bools["Spread visualisation"] or bools["Spread per antibiotic print-out"]:
        spread_vis(
            panel, 
            all_isolates, 
            bools["Spread visualisation"], 
            bools["Spread per antibiotic print-out"]
            )

    # Coverage
    if bools["Coverage bars"] or bools["Coverage heatmap"]:
        coverage_vis(panel, bools["Coverage bars"], bools["Coverage heatmap"])

    # Redundancy
    if (
        bools["Redundancy heatmap"]
        or bools["Redundancy tree"]
        or bools["Redundancy bars"]
        or bools["Uniqueness print-out"]
    ):
        redundancy(
            panel,
            redundancy_threshold,
            bools["Redundancy bars"],
            bools["Redundancy heatmap"],
            bools["Redundancy tree"],
            bools["Uniqueness print-out"],
        )

if __name__ == "__main__":
    main()
