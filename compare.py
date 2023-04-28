import plotly.express as px
import pandas as pd
import json
from Classes.panel_class import Panel
from Classes.isolate_class import create_isolate_list
from help_functions.score_calc_functions import calc_scores
from help_functions.validate_parameters import *

# Makes the bar-chart
def compare_plot(panels):
    fig = px.bar(
        panels,
        x="Panel",
        y=["Spridning", "Täckning", "Redundans", "Totalt score"],
        color_discrete_sequence=[
            "DarkSeaGreen",
            "Teal",
            "Cornflowerblue",
            "RebeccaPurple",
        ],
        barmode="group",
    )
    fig.update_layout(
        title="Jämförelse av testpaneler",
        xaxis_tickfont_size=14,
        yaxis=dict(title="Score", titlefont_size=16, tickfont_size=14),
        template="plotly_dark",
    )
    fig.show()


# Creates a list of isolate class-objects from a list of isolate names
def create_panel(isolate_list: list):
    CIB = pd.ExcelFile("Q-linea_files/CIB_TF-data_AllIsolates_20230302.xlsx")
    matrix_EU = pd.read_excel(CIB, "matrix EU")
    number_of_antibiotics = len(matrix_EU.columns[3:])
    isolate_objects = create_isolate_list(matrix_EU)
    chosen_isolate_objects = [
        isolate for isolate in isolate_objects if isolate.get_name() in isolate_list
    ]
    panel = Panel(number_of_antibiotics, chosen_isolate_objects)
    return panel


def main():

    (_, coefficients, coverage_demands, redundancy_threshold) = validate_parameters(
        json.load(open("parameters.json"))
    )

    panel_names = json.load(open("plots_to_compare.json"))["Chosen isolates"]

    # Converts csv files to lists of chosen isolates
    isolate_lists = []
    for panel in panel_names:
        isolate_lists.append(pd.read_csv(panel)["Isolate"].tolist())

    # Calculate scores of panel with all isolates
    all_isolates = json.load(open("plots_to_compare.json"))["All isolates"]
    all_isolates_list = pd.read_csv(all_isolates)["Isolate"].tolist()
    all_isolates_panel = create_panel(all_isolates_list)
    (max_spread, max_coverage, max_redundancy) = calc_scores(
            all_isolates_panel,
            json.load(open("abx_ranges.json")),
            redundancy_threshold,
            coverage_demands
            )

    # Creates a list of all scores for the panels
    panel_scores = []
    for i in range(len(isolate_lists)):
        panel = create_panel(isolate_lists[i])
        (spread, coverage, redundancy) = calc_scores(
            panel,
            json.load(open("abx_ranges.json")),
            redundancy_threshold,
            coverage_demands
        )
        panel_dict = {
            "Panel": panel_names[i],
            "Spridning": spread/max_spread,
            "Täckning": coverage/max_coverage,
            "Redundans": redundancy/max_redundancy,
            "Totalt score": (
                coefficients[0] * spread/max_spread
                + coefficients[1] * coverage/max_coverage
                - coefficients[2] * redundancy/max_redundancy
            ),
        }
        panel_scores.append(panel_dict)

    compare_plot(pd.DataFrame(data=panel_scores))


if __name__ == "__main__":
    main()
