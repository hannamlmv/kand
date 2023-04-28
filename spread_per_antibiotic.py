"""
Generates print-out of spread for different antibiotics 
"""
import pandas as pd
from help_functions.create_panel import create_panel

def main():
    chosen_isolates_list = pd.read_csv("Chosen_isolates_folder/Chosen_isolates.csv")
    print(chosen_isolates_list)



if __name__ == "__main__":
    main()
