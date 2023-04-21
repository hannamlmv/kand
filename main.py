import pandas as pd
from panel_class import Panel, Isolate


def extract_isolate_data(matrix_EU: pd.DataFrame):
    for index, row in matrix_EU.iterrows():
        if index == 1:
            print(type(row))


def main():
    chosen_isolates_list = pd.read_csv("Chosen_isolates_list.csv")
    CIB = pd.ExcelFile("Q-linea_files\CIB_TF-data_AllIsolates_20230302.xlsx")
    matrix_EU = pd.read_excel(CIB, "matrix EU")
    antibiotics = list(chosen_isolates_list.columns[3:])

    extract_isolate_data(matrix_EU)


if __name__ == "__main__":
    main()
