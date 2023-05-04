"""
Generates visualisations and print-outs for a given panel

Date: 28/4 
Author: Hanna Malmvall
"""

import json
from help_functions.validate_parameters import validate_visualisation_parameters
from Visualisation.Plots.Spread.spread_plot import main as spread_vis
from Visualisation.Plots.Spread.spread_per_antibiotic import main as spread_print
from Visualisation.Plots.Coverage.coverage_vis import main as coverage_vis
from Visualisation.Plots.Redundancy.redundancy_plots import main as redundancy

panel = "Chosen_isolates_folder/Chosen_isolates.csv"
all_isolates = "Chosen_isolates_folder/all_isolates.csv"
bools = validate_visualisation_parameters(
    json.load(open("Parameters/visualisation_parameters.json"))
    )



#Spread
if bools["Spread visualisation"]:
    spread_vis(panel)
if bools["Spread per antibiotic print-out"]:
    spread_print(panel, all_isolates)

#Coverage
if (
    bools["Coverage bars"] or 
    bools["Coverage heatmap"]
    ):
    coverage_vis(
        panel, 
        bools["Coverage bars"], 
        bools["Coverage heatmap"]
        )
    
#Redundancy
if (
    bools["Redundancy heatmap"] or 
    bools["Redundancy tree"] or 
    bools["Redundancy bars"] or 
    bools["Uniqueness print-out"]):
    redundancy(
        panel, 
        bools["Redundancy bars"], 
        bools["Redundancy heatmap"], 
        bools["Redundancy tree"], 
        bools["Uniqueness print-out"]
        )

