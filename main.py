import pandas as pd
import numpy as np
from isolate_class import Isolate
from panel_class import Panel
from extract_and_parse import parse_antibiotic_data, extract_antibiotic_data
from add_isolate_functions import add_isolate


def main():
    # Read in data from excel
    CIB = pd.ExcelFile("Q-linea_files\CIB_TF-data_AllIsolates_20230302.xlsx")
    matrix_EU = pd.read_excel(CIB, "matrix EU")

    # Create tuple of antibiotic names
    antibiotics = tuple(matrix_EU.columns[3:])

    # Initiate variables
    panel = Panel()
    all_isolates = []
    n = 50
    spread_score_coeff = 1
    coverage_score_coeff = 1
    redundancy_score_coeff = 1
    number_of_isolates_coeff = 0.01
    hyperparameters = np.array(
        (
            spread_score_coeff,
            coverage_score_coeff,
            redundancy_score_coeff,
            number_of_isolates_coeff,
        )
    )

    for _, row in matrix_EU.iterrows():
        isolate, antibiotic_data = row[0], list(row[3:].items())
        isolate_data = {}
        # Store the MIC value and SIR data for all antibiotics that are not nip or missing bp
        for antibiotic, data in zip(antibiotics, antibiotic_data):
            if parse_antibiotic_data(data):
                isolate_data[antibiotic] = extract_antibiotic_data(data)
        # Add an isolate object to all_isolates with the current isolate name and isolate_data
        all_isolates.append(Isolate(isolate, isolate_data))

    n = 50
    add_isolate(n, all_isolates, panel, hyperparameters)


if __name__ == "__main__":
    main()
