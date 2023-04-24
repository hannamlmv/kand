import pandas as pd
import numpy as np
from isolate_class import create_isolate_list
from panel_class import Panel
from add_isolate_functions import add_isolate


def main():
    # Read in data from excel
    CIB = pd.ExcelFile("Q-linea_files\CIB_TF-data_AllIsolates_20230302.xlsx")
    matrix_EU = pd.read_excel(CIB, "matrix EU")

    # Create tuple of antibiotic names
    antibiotics = tuple(matrix_EU.columns[3:])

    # Initiate variables
    panel = Panel()
    all_isolates = create_isolate_list(matrix_EU, antibiotics)
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

    n = 50
    add_isolate(n, all_isolates, panel, hyperparameters)


if __name__ == "__main__":
    main()
