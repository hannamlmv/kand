from Visualisation.plotly_testpanel_vis import main as spread_vis
from spread_per_antibiotic import main as spread_print

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