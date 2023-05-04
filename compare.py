"""
Generates a bar-chart showing scores for different panels

Date: 27/4 
Author: Hanna Malmvall
"""

import plotly.express as px
import pandas as pd
import json
from help_functions.score_calc_functions import calc_scores
from help_functions.validate_parameters import *
from help_functions.create_panel import create_panel

# Makes the bar-chart
def compare_plot(panels):
    fig = px.bar(
        panels,
        x="Panel",
        y=["Spridningsvärde", "Täckningsvärde", "Redundansvärde", "Totalt värde"],
        labels={"variable": "Indikator"},
        color_discrete_sequence=[
            "DarkSeaGreen",
            "Teal",
            "Cornflowerblue",
            "RebeccaPurple",
        ],
        barmode="group",
    )
    fig.update_layout(
        title={'text': "Jämförelse av testpaneler", 'x': 0.5, 'xanchor': 'center', 'font_size': 25},
        xaxis_tickfont_size=14,
        yaxis=dict(title="Värde", titlefont_size=16, tickfont_size=14),
        template="plotly_dark",
    )
    fig.show()

def main():

    (_, coefficients, coverage_demands, coverage_total, redundancy_threshold) = validate_parameters(
        json.load(open("Parameters/isolate_selection_parameters.json"))
    )

    panel_names = json.load(open("Parameters/plots_to_compare.json"))["Chosen isolates"]

    # Converts csv files to lists of chosen isolates
    isolate_lists = []
    for panel in panel_names:
        isolate_lists.append(pd.read_csv(panel)["Isolate"].tolist())

    # Calculate scores of panel with all isolates
    all_isolates = json.load(open("Parameters/plots_to_compare.json"))["All isolates"]
    all_isolates_list = pd.read_csv(all_isolates)["Isolate"].tolist()
    all_isolates_panel = create_panel(all_isolates_list)
    (max_spread, max_coverage, max_redundancy) = calc_scores(
            all_isolates_panel,
            json.load(open("Parameters/antibiotic_info.json")),
            redundancy_threshold,
            coverage_demands,
            coverage_total
            )

    # Creates a list of all scores for the panels
    panel_scores = []
    for i in range(len(isolate_lists)):
        panel = create_panel(isolate_lists[i])
        (spread, coverage, redundancy) = calc_scores(
            panel,
            json.load(open("Parameters/antibiotic_info.json")),
            redundancy_threshold,
            coverage_demands,
            coverage_total
        )
        panel_dict = {
            "Panel": panel_names[i],
            "Spridningsvärde": spread/max_spread,
            "Täckningsvärde": coverage/max_coverage,
            "Redundansvärde": redundancy/max_redundancy,
            "Totalt värde": (
                coefficients[0] * spread/max_spread
                + coefficients[1] * coverage/max_coverage
                - coefficients[2] * redundancy/max_redundancy
            ),
        }
        panel_scores.append(panel_dict)

    compare_plot(pd.DataFrame(data=panel_scores))


if __name__ == "__main__":
    main()
