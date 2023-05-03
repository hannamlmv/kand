"""
Generates visualisations and print-outs for a given panel

Date: 28/4 
Author: Hanna Malmvall
"""

import json
from help_functions.validate_parameters import validate_visualisation_parameters
from Visualisation.Plots.Spread.spread_plot import main as spread_vis
from Visualisation.Plots.Spread.spread_per_antibiotic import main as spread_print
#from Visualisation.Plots.coverage_plot import main as coverage_vis
#from Visualisation.Plots.Redundancy.redundancy_plot import main as redundancy

panel = "Chosen_isolates_folder/Chosen_isolates.csv"
all_isolates = "Chosen_isolates_folder/all_isolates.csv"
bools = validate_visualisation_parameters(
    json.load(open("Parameters/visualisation_parameters.json"))
    )

#Visualisations
if bools["Spread visualisation"]:
    #spread_vis(panel)
    pass
if bools["Coverage visualisation"]:
    #coverage_vis(panel)
    pass
if bools["Redundancy heatmap"]:
    #redundancy(panel)
    pass
if bools["Redundancy tree"]:
    #redundancy(panel)
    pass
if bools["Redundancy bars"]:
    #redundancy(panel)
    pass

#Printouts
if bools["Spread per antibiotic print-out"]:
    #spread_print(panel, all_isolates)
    pass
if bools["Uniqueness print-out"]:
    #redundancy(panel)
    pass
