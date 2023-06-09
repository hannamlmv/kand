"""
Creates the coverage plots

Date: 2/4
Author: Elin Berg & Julia Ancker
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.graph_objects as go 
import plotly.subplots as sp
import numpy as np
from Visualisation.data_extraction_functions import extract_chosen_isolates
from Visualisation.Coverage.coverage_functions import *

def plot_coverage(antibiotics: list, S_I_R_per_antibiotic: dict) -> None:
    """
    Plots the panel in the form of a stack plot, with the amount of Sensitive 
    MIC-values in green, Intermediate MIC-values in yellow, and Resistant
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
            'text': "Täckning per antibiotikum", 
            'x': 0.5, 
            'xanchor': 'center', 
            'font_size': 17
            }, 
        xaxis_title="Antibiotika",
        yaxis_title="Antal stammar",
        barmode='stack', 
        template = 'plotly_dark',
        showlegend=True,
        legend=dict(
            bgcolor='rgba(0, 0, 0, 0)',
            font=dict(size=12, color='white')
            )
        )
    fig.show()

def plot_grid(antibiotics:list, chosen_isolates_list:list, chosen_isolates_SIR_M: dict):
    """
    Creates heatmap over every single isolate and the coverage amount for every 
    antibiotic. Green for sensitive, yellow for intermediate and red for resistant.
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

    # Change the largest name to smaller
    antibiotics_edited=[i for i in antibiotics]
    antibiotics_edited[20]='T.sulfamethoxazole'

    # Create heatmap trace with categorical color scale
    heatmap = go.Heatmap(z=data, 
                        colorscale=colorscale,
                        hovertemplate='Antibiotika: %{x}<br>Isolat: %{y}',
                        zhoverformat='.2f'
                        )

    # Create subplot grid
    fig = sp.make_subplots(rows=1, cols=1)

    # Add heatmap trace to subplot
    fig.add_trace(heatmap)

    # Set layout properties
    fig.update_layout(
        title={
            'text': "Täckning för varje antbiotikum och stam", 
            'x': 0.5, 
            'xanchor': 'center', 
            'font_size': 17
            }, 
        xaxis_title="Antibiotika",
        yaxis_title="Stam",
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
    fig.show()

def main(panel, sir_stackplot, coverage_per_isolates):
   """ Creates the coverage plots. """
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
   S_I_R_per_antibiotic = collect_number_of_S_I_R(filtered_chosen_isolates_SIR)

   # Plots a stackplot over the panel, with S,I,R-values in different colors.
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