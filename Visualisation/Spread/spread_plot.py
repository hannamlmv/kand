"""
Creates the spread-plot 

Date: 10/4 
Author: Victor Wong
"""

import json
import pandas as pd
from Visualisation.Spread.spread_plot_functions import (
    create_plot_df,
    plotly_dotplot,
)
from Visualisation.Spread.data_extraction_functions import (
    extract_chosen_isolates,
    extract_mic_sir_data,
    filter_mic_sir_data,
    extract_mic_values_per_antibiotic,
)


def main(chosen_isolates_list=None):
    # Load files
    if chosen_isolates_list is None:
        chosen_isolates_list = pd.read_csv("Chosen_isolates_1.csv")
    else:
        chosen_isolates_list = pd.read_csv(chosen_isolates_list)
    CIB = pd.ExcelFile("Q-linea_files/CIB_TF-data_AllIsolates_20230302.xlsx")
    matrix_EU = pd.read_excel(CIB, "matrix EU")
    antibiotic_ranges = json.load(open("Parameters/antibiotic_info.json"))
    fastidious_dict = json.load(open("Parameters/pathogen_fastidiousness.json"))

    # Rename a long name for plotting purposes
    matrix_EU.rename(
        columns={"Trimethoprim-sulfamethoxazole": "Trimeth-sulf"}, inplace=True
    )
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


if __name__ == "__main__":
    main()