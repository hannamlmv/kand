import plotly.express as px
import pandas as pd
import json
from panel_class import Panel
from isolate_class import Isolate, create_isolate_list
from help_functions.score_calc_functions import calc_scores
from help_functions.validate_parameters import *

# Makes the bar-chart
def compare_plot(panels):
    fig = px.bar(panels, x="Panel", y=["Spridning", "Täckning", "Redundans", "Totalt score"], 
                color_discrete_sequence = ['DarkSeaGreen', 'Teal', 'Cornflowerblue', 'RebeccaPurple'],
                barmode='group')
    fig.update_layout(
    title='Jämförelse av testpaneler',
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='Score',
        titlefont_size=16,
        tickfont_size=14),
        template = 'plotly_dark')
    fig.show()

# Creates a list of isolate class-objects from a list of isolate names
def create_panel(isolate_list: list):
    CIB = pd.ExcelFile("Q-linea_files/CIB_TF-data_AllIsolates_20230302.xlsx")
    matrix_EU = pd.read_excel(CIB, "matrix EU")
    number_of_antibiotics = len(matrix_EU.columns[3:])
    isolate_objects = create_isolate_list(matrix_EU)
    chosen_isolate_objects = [isolate for isolate in isolate_objects if isolate.get_name() in isolate_list]
    panel = Panel(number_of_antibiotics, chosen_isolate_objects)
    return panel

def main():

    (number_of_isolates, 
     coefficients, 
     coverage_penalties, 
     redundancy_threshold
     ) = validate_parameters(json.load(open("parameters.json")))
    isolate_lists = []
    panel_names = json.load(open("plots_to_compare.json"))

    # Converts csv files to lists of chosen isolates
    for panel in panel_names:
        isolate_lists.append(pd.read_csv(panel)['Isolate'].tolist())

    # Creates a list of all scores for the panels
    panel_scores = []
    for i in range(len(isolate_lists)):
        panel = create_panel(isolate_lists[i])
        (spread, coverage, redundancy) = calc_scores(
            panel, 
            json.load(open("abx_ranges.json")),
            redundancy_threshold,
            coverage_penalties
            )
        panel_dict = {
            'Panel': panel_names[i], 
            'Spridning': spread, 
            'Täckning':coverage, 
            'Redundans': redundancy,
            'Totalt score': (
            coefficients[0] * spread + 
            coefficients[1] * coverage - 
            coefficients[2] * redundancy
            )
            }
        panel_scores.append(panel_dict)

    compare_plot(pd.DataFrame(data = panel_scores))

if __name__ == '__main__':
    main()



