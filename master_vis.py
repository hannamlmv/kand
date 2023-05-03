"""
Generates visualisations and print-outs for a given panel

Date: 28/4 
Author: Hanna Malmvall
"""

from Visualisation.Plots.Spread.spread_plot import main as spread_vis
from Visualisation.Plots.Spread.spread_per_antibiotic import main as spread_print
import json

panel = "Chosen_isolates_folder/Chosen_isolates.csv"
all_isolates = "Chosen_isolates_folder/all_isolates.csv"

bools = json.load(open("Parameters/visualisation_parameters.json"))

#Visualisations
if bools["Spread visualisation"]:
    spread_vis(panel)
if bools["Coverage visualisation"]:
    pass
if bools["Redundancy heatmap"]:
    pass
if bools["Redundancy tree"]:
    pass
if bools["Redundancy bars"]:
    pass

#Printouts
if bools["Spread per antibiotic print-out"]:
    spread_print(panel, all_isolates)
if bools["Uniqueness print-out"]:
    pass
