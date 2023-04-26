import json
import time
import pandas as pd
import numpy as np
from panel_class import Panel
from isolate_class import create_isolate_list
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
    file_path = "Chosen_isolates.csv"
    VISUALIZE = True
    GET_CSV = False

    # Read in data from excel
    CIB = pd.ExcelFile("Q-linea_files/CIB_TF-data_AllIsolates_20230302.xlsx")
    matrix_EU = pd.read_excel(CIB, "matrix EU")
    antibiotic_concentration_ranges = json.load(open("abx_ranges.json"))
    number_of_antibiotics = len(matrix_EU.columns[3:])

    # Initiate variables
    panel = Panel(number_of_antibiotics)
    all_isolates = create_isolate_list(matrix_EU)
    redundancy_threshold = 1
    number_of_isolates = 400
    spread_score_coeff = 1
    coverage_score_coeff = 1
    redundancy_score_coeff = 1
    # number_of_isolates_coeff = 0.01
    hyperparameters = np.array(
        (
            spread_score_coeff,
            coverage_score_coeff,
            redundancy_score_coeff,
        )
    )
    add_isolate(
        number_of_isolates,
        all_isolates,
        panel,
        hyperparameters,
        antibiotic_concentration_ranges,
        redundancy_threshold,
    )

    if VISUALIZE:
        visualize_panel(panel.to_DataFrame())

    if GET_CSV:
        panel.to_csv(file_path)


if __name__ == "__main__":
    main()
