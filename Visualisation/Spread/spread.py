"""
Creates the spread-plot and generates print-out of spread for different antibiotics 

Date: 28/4 
Author: Victor Wong & Hanna Malmvall
"""

import pandas as pd
from prettytable import PrettyTable
import json
import pandas as pd
from help_functions.create_panel import create_panel
from help_functions.score_calc_functions import extract_panel_data, calc_spread_score
from Visualisation.Spread.spread_functions import (
    create_plot_df,
    plotly_dotplot,
)
from Visualisation.data_extraction_functions import (
    extract_chosen_isolates,
    extract_mic_sir_data,
    filter_mic_sir_data,
    extract_mic_values_per_antibiotic,
)


def plot(chosen_isolates_list):
    """Creates a plot which visualises the spread of a panel."""
    # Load files
    chosen_isolates_list = pd.read_csv(chosen_isolates_list)
    CIB = pd.ExcelFile("Q-linea_files/CIB_TF-data_AllIsolates_20230302.xlsx")
    matrix_EU = pd.read_excel(CIB, "matrix EU").drop("D-test", axis=1)
    antibiotic_ranges = json.load(open("Parameters/antibiotic_info.json"))
    fastidious_dict = json.load(
        open("Parameters/pathogen_fastidiousness.json", encoding="UTF-8")
    )

    # Rename a long name for plotting purposes
    #matrix_EU.rename(
    #    columns={"Trimethoprim-sulfamethoxazole": "T.sulfamethoxazole"}, inplace=True
    #)
    # Select isolates
    chosen_isolates = extract_chosen_isolates(chosen_isolates_list, matrix_EU)

    # List of antiiotic names
    antibiotics = list(chosen_isolates.columns[3:])

    # Extract all data for an antibiotic.
    chosen_isolates_data = extract_mic_sir_data(chosen_isolates, antibiotics)

    # Remove the tuples that have None in their SIR data
    filtered_chosen_isolates_data = filter_mic_sir_data(chosen_isolates_data)

    # Extract the mic-values of each isolate for each antibiotic.
    mic_data = extract_mic_values_per_antibiotic(
        filtered_chosen_isolates_data, antibiotics
    )

    # Create dataframe used for plotting
    plot_df = create_plot_df(antibiotics, mic_data, fastidious_dict)

    plotly_dotplot(plot_df, antibiotics, antibiotic_ranges)


def spread_per_antibiotic(chosen_isolates: str, all_isolates: str) -> None:
    """Calculates and prints the relative spread per antibiotic."""
    for isolates in [chosen_isolates, all_isolates]:
        isolate_list = pd.read_csv(isolates)["Isolate"].tolist()
        isolate_panel = create_panel(isolate_list)
        spread_per_antibiotic = calc_spread_score(
            extract_panel_data(isolate_panel),
            json.load(open("Parameters/antibiotic_info.json")),
            isolate_panel.get_number_antibiotics(),
            True,
        )
        if isolates == chosen_isolates:
            chosen_spread_per_antibiotic = spread_per_antibiotic
        else:
            all_spread_per_antibiotic = spread_per_antibiotic

    for antibiotic in chosen_spread_per_antibiotic:
        if all_spread_per_antibiotic[antibiotic] == 0:
            chosen_spread_per_antibiotic[antibiotic] = 1.0
        else:
            chosen_spread_per_antibiotic[antibiotic] = round(
                chosen_spread_per_antibiotic[antibiotic]
                / all_spread_per_antibiotic[antibiotic],
                2,
            )

    table = PrettyTable()
    table.field_names = ["Antibiotika", "Relativ spridning"]
    for antibiotic, mic in chosen_spread_per_antibiotic.items():
        table.add_row([antibiotic, mic])
    print()
    print("---------------------------------------------")
    print("Spridning i förhållande till möjlig spridning")
    print("---------------------------------------------")
    print(table)
    print()


def main(chosen_isolates: str, all_isolates: str, do_plot: bool, do_print: bool):
    if do_plot:
        plot(chosen_isolates)
    if do_print:
        spread_per_antibiotic(chosen_isolates, all_isolates)


if __name__ == "__main__":
    main(
        "Chosen_isolates_folder/Chosen_isolates.csv",
        "Chosen_isolates_folder/all_isolates.csv",
        True,
        True,
    )
