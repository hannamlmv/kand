"""
Generates visualisations and print-outs for a given panel

Date: 28/4 
Author: Hanna Malmvall
"""

from Visualisation.Plots.Spread.spread_plot import main as spread_vis
from Visualisation.Plots.Spread.spread_per_antibiotic import main as spread_print

panel = "Chosen_isolates_folder/Chosen_isolates.csv"
all_isolates = "Chosen_isolates_folder/all_isolates.csv"

# Visualisations
spread_visualisation = True

# Print-outs
spread_printout = True



if spread_visualisation:
    spread_vis(panel)

if spread_printout:
    spread_print(panel, all_isolates)