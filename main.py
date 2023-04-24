import pandas as pd
import numpy as np
from isolate_class import Isolate
from extract_and_parse import parse_antibiotic_data, extract_antibiotic_data


def main():
    CIB = pd.ExcelFile("Q-linea_files\CIB_TF-data_AllIsolates_20230302.xlsx")
    matrix_EU = pd.read_excel(CIB, "matrix EU")
    antibiotics = list(matrix_EU.columns[3:])

    panel = Panel()
    n = 50
    hyperparameters = np.ones((4, 1))

    all_isolates = []

    for index, row in matrix_EU.iterrows():
        isolate, antibiotic_data = row[0], list(row[3:].items())
        isolate_data = {}
        for antibiotic, data in zip(antibiotics, antibiotic_data):
            if parse_antibiotic_data(data):
                isolate_data[isolate] = extract_antibiotic_data(data)
        all_isolates.append(Isolate(isolate, isolate_data))

    n = 50
    add_isolate(n, all_isolates, panel, hyperparameters)


if __name__ == "__main__":
    main()
