"""
Creates a panel

Date: 24/4 
Author: Victor Wong
"""

import json
import pandas as pd
from Classes.panel_class import Panel
from help_functions.create_isolate_list import create_isolate_list
from help_functions.validate_parameters import validate_parameters
from help_functions.add_isolate_functions import add_isolate


def main():
    """Creates a panel."""
    CIB_file_path = "Q-linea_files/CIB_TF-data_AllIsolates_20230302.xlsx"
    excel_sheet_name = "matrix EU"
    antibiotic_ranges_file_path = "Parameters/antibiotic_info.json"
    parameters_file_path = "Parameters/isolate_selection_parameters.json"
    chosen_isolates_file_path = "Chosen_Isolates_folder/Chosen_isolates.csv"

    # Read in data from Excel
    CIB = pd.ExcelFile(CIB_file_path)
    matrix_EU = pd.read_excel(CIB, excel_sheet_name)
    number_of_antibiotics = len(matrix_EU.columns[3:])

    # Open json files
    antibiotic_concentration_ranges = json.load(open(antibiotic_ranges_file_path))
    (
        number_of_isolates,
        coefficients,
        coverage_demands,
        coverage_total,
        redundancy_threshold,
    ) = validate_parameters(json.load(open(parameters_file_path)))

    # Initiate variables
    panel = Panel(number_of_antibiotics)
    all_isolates = create_isolate_list(matrix_EU)

    add_isolate(
        number_of_isolates,
        all_isolates,
        panel,
        coefficients,
        antibiotic_concentration_ranges,
        redundancy_threshold,
        coverage_demands,
        coverage_total,
    )

    panel.to_csv(chosen_isolates_file_path)


if __name__ == "__main__":
    main()
