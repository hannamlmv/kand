import pandas as pd
from panel_class import Panel, Isolate


def main():
    chosen_isolates_list = pd.read_csv("Chosen_isolates_list.csv")
    CIB = pd.ExcelFile("Q-linea_files\CIB_TF-data_AllIsolates_20230302.xlsx")
    matrix_EU = pd.read_excel(CIB, "matrix EU")
    antibiotics = list(chosen_isolates_list.columns[3:])


if __name__ == "__main__":
    main()
