import pandas as pd
import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
from IPython.display import display
import random
import json
import plotly.express as px
import plotly.graph_objects as go
import plotly.graph_objects as go 
import plotly.subplots as sp
import numpy as np

def extract_chosen_isolates(
   chosen_isolates: pd.DataFrame, matrix_EU: pd.DataFrame
) -> pd.DataFrame:
   """
   Select the chosen isolates from the script. Return a DataFrame only containing the rows of selected isolates
   """
   chosen_rows = matrix_EU["Isolate"].isin(chosen_isolates["Isolate"])
   return matrix_EU[chosen_rows]


def find_digits(SIR: str) -> int:
   """Find numbers in a string"""
   digit = ""
   for character in SIR:
       if character.isdigit() or character == ".":
           digit += character
   return float(digit)


def parse_SIR(SIR: str) -> bool:
   """
   Find the isolates with valid SIRs. Not 'Missing BP'
   and not 'nip'.
   """
   if SIR.startswith("Missing BP"):
       return False
   if SIR == "nip":
       return False
   return True


def extract_SIR(chosen_isolates: pd.DataFrame, antibiotics: list) -> dict:
   """
   Extract all SIRs for an antibiotic. Returns a dictionary
   with antibiotcs as keys and lists of the isolates and their
   SIRs in tuples as value.
   """
   chosen_isolates_SIR = {antibiotic: [] for antibiotic in antibiotics}
  
   for index, row in chosen_isolates.iterrows():
       antibiotic_SIR = list(row[3:].items())
       for antibiotic, SIR in antibiotic_SIR:
           if parse_SIR(SIR):
               mic_category = SIR[0]
               mic = find_digits(SIR)
               chosen_isolates_SIR[antibiotic].append(mic_category)
           else:
               # If SIR = "Missing BP" or "nip"
               chosen_isolates_SIR[antibiotic].append((None))
   return chosen_isolates_SIR


def extract_SIR_M(chosen_isolates: pd.DataFrame, antibiotics: list) -> dict:
   """
   Extract all SIRs for an antibiotic. Returns a dictionary
   with antibiotcs as keys and lists of the isolates and their
   SIRs in tuples as value, M if there is a missing MIC-value.
   """
   chosen_isolates_SIR = {antibiotic: [] for antibiotic in antibiotics}
  
   for index, row in chosen_isolates.iterrows():
       antibiotic_SIR = list(row[3:].items())
       for antibiotic, SIR in antibiotic_SIR:
           if parse_SIR(SIR):
               mic_category = SIR[0]
               mic = find_digits(SIR)
               chosen_isolates_SIR[antibiotic].append(mic_category)
           else:
               # If SIR = "Missing BP" or "nip"
               chosen_isolates_SIR[antibiotic].append(('M'))
   return chosen_isolates_SIR


def filter_mic_values(chosen_isolates_SIR: dict) -> None:
   """
   Remove the tuples that have None in their SIR data
   """
   for antibiotic, SIR_data in chosen_isolates_SIR.items():
       chosen_isolates_SIR[antibiotic] = list((tup for tup in SIR_data if tup is not None))
   return chosen_isolates_SIR


def collect_number_of_S_I_R(chosen_isolates_SIR: dict, antibiotics: list) -> dict:
    """
    Counts every S,I,R value for every antibiotic. Returns a dictionary with the antibiotic as the key, and a list with hte counts of the S,I,R-values 
    (in that order)
    """
    count_isolates_SIR={}
    for antibiotic, SIR_data in chosen_isolates_SIR.items():
        S_count=0
        I_count=0
        R_count=0
        
        for SIR in SIR_data:
            if SIR=='S':
                S_count+=1
            if SIR=='I':
                I_count+=1
            if SIR=='R':
                R_count+=1


        count_isolates_SIR[antibiotic]=  list((S_count, I_count, R_count))
    return count_isolates_SIR

def plot_coverage(antibiotics: list, S_I_R_per_antibiotic: dict) -> None:
    """
    Plots the panel in the form of a stack plot, with the amount of Sensitive MIC-values in green, Intermediate MIC-values in yellow, and Resistant
    MIC-values in red. 
    """
    S =[]
    I = []
    R = []
    for antibiotic, SIR in S_I_R_per_antibiotic.items():
        S.append(SIR[0])
        I.append(SIR[1])
        R.append(SIR[2])
    
    labels=[i for i in antibiotics]
    labels[20]='T.sulfamethoxazole'

    fig = go.Figure(data=[
        go.Bar(name='Känslig', x = labels, y=S, marker=dict(color='limegreen')),
        go.Bar(name='Intermediär', x = labels, y=I, marker=dict(color='gold')),
        go.Bar(name='Resistent', x = labels, y=R, marker = dict(color='tomato'), )
    ])


    fig.update_layout(
        title={
            'text': "Täckning per antibiotika", 
            'x': 0.5, 
            'xanchor': 'center', 
            'font_size': 25
            }, 
        xaxis_title="Antibiotika",
        yaxis_title="Antal stammar",
        barmode='stack', 
        template = 'plotly_dark')

    # Saves the plot
    #fig.write_image('stacked1.png')

    #Show the plot
    fig.show()


def plot_grid(antibiotics:list, chosen_isolates_list:list, chosen_isolates_SIR_M: dict):
    """
    Creates heatmap over every single isolate and the coverage amount for every antibiotic. Green for sensitive, yellow for intermediate and
    red for resistant.
    """
    y_list = []
    x = chosen_isolates_list
    for i in range(len(x)):
        y = []
        for antibiotic, SIR in chosen_isolates_SIR_M.items():
            if SIR[i] == 'S':
                y.append(0)
            elif SIR[i] == 'I':
                y.append(0.2)
            elif SIR[i] == 'R':
                y.append(0.5)
            else:
                y.append(1)
        y_list.append(y)
    
    data = np.matrix(y_list)

    # Create heatmap trace
    colorscale = [[0, 'green'], [0.2, 'yellow'], [0.5, 'Red'], [1, '#111111']]

    # Create heatmap trace with categorical color scale
    heatmap = go.Heatmap(z=data, colorscale=colorscale)

    # Create subplot grid
    fig = sp.make_subplots(rows=1, cols=1)

    # Add heatmap trace to subplot
    fig.add_trace(heatmap)

    # Change the largest name to smaller
    antibiotics_edited=[i for i in antibiotics]
    antibiotics_edited[20]='T.sulfamethoxazole'

    # Set layout properties
    fig.update_layout(
        title={
            'text': "Täckning för varje antbiotika och stam", 
            'x': 0.5, 
            'xanchor': 'center', 
            'font_size': 25
            }, 
        xaxis_title="Antibiotika",
        yaxis_title="Stam",
        height=1400,
        width=550,
        margin=dict(l=50, r=50, b=50, t=50),
        showlegend=False,
        xaxis=dict(
            tickvals=[i for i in range(len(antibiotics_edited))],
            ticktext= list(antibiotics_edited)
        ),
        yaxis=dict(
            tickvals=[i for i in range(len(x))],
            ticktext=list(x)
        ),
    template = 'plotly_dark')

    fig.update_traces(showscale = False)
    
    # Saves the plot
    #fig.write_image('stacked2.png')

    #Show the plot
    fig.show()
  
 


def main(panel, sir_stackplot, coverage_per_isolates):
   # Load files
   chosen_isolates_list = pd.read_csv(panel)
   CIB = pd.ExcelFile("Q-linea_files/CIB_TF-data_AllIsolates_20230302.xlsx")
   matrix_EU = pd.read_excel(CIB, "matrix EU")
  
   # Extract isolates
   chosen_isolates = extract_chosen_isolates(chosen_isolates_list, matrix_EU)
  
   # Create array of isolate names and antibiotic names
   antibiotics = list(chosen_isolates.columns[3:])
  
   # Extract all SIRs for an antibiotic.
   chosen_isolates_SIR = extract_SIR(chosen_isolates, antibiotics)
  
   # Remove the tuples that have None in their SIR data
   filtered_chosen_isolates_SIR = filter_mic_values(chosen_isolates_SIR)

   # Count number of S,I,R per antibiotic:
   S_I_R_per_antibiotic = collect_number_of_S_I_R(filtered_chosen_isolates_SIR, antibiotics)

   # Plots a stackplot over the panel, with S,I,R-values in different colors.

   """sir_stackplot och coverage_per_isolates kan tas bort helt och läggastill i parameterlistan"""

   if sir_stackplot:
        plot_coverage(antibiotics, S_I_R_per_antibiotic)

   # Plots a heatmap over every isolate and where it has a MIC-value.
   if coverage_per_isolates:
        # Turn the isolates into a list for the plot_grid_function
        chosen_isolates_list=chosen_isolates_list['Isolate'].tolist()
        chosen_isolates_SIR_M = extract_SIR_M(chosen_isolates, antibiotics)

        # plots the heatmap
        plot_grid(antibiotics, chosen_isolates_list, chosen_isolates_SIR_M)
        

  
if __name__ == "__main__":
   main("Chosen_isolates_folder/Chosen_isolates.csv", True, True)