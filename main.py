import json
import time
import pandas as pd
import numpy as np
from panel_class import Panel
from isolate_class import create_isolate_list
from help_functions.validate_parameters import validate_parameters
from help_functions.add_isolate_functions import add_isolate
from Visualisation.plotly_testpanel_vis import main as visualize_panel


def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Elapsed time: {end_time - start_time:.3f} seconds")
        return result

    return wrapper


@measure_time
def main():
    CIB_file_path = "Q-linea_files/CIB_TF-data_AllIsolates_20230302.xlsx"
    antibiotic_ranges_file_path = "abx_ranges.json"
    parameters_file_path = "parameters.json"
    VISUALIZE = False
    GET_CSV = True
    chosen_isolates_file_path = "Chosen_Isolates_folder/Chosen_isolates.csv"

    # Read in data from Excel
    CIB = pd.ExcelFile(CIB_file_path)
    matrix_EU = pd.read_excel(CIB, "matrix EU")
    number_of_antibiotics = len(matrix_EU.columns[3:])

    # Open json files
    antibiotic_concentration_ranges = json.load(open(antibiotic_ranges_file_path))
    (
        number_of_isolates,
        coefficients,
        coverage_penalties,
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
        coverage_penalties,
    )

    if VISUALIZE:
        visualize_panel(panel.to_DataFrame())

    if GET_CSV:
        panel.to_csv(chosen_isolates_file_path)


if __name__ == "__main__":
    main()
