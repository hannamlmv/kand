"""
Creates the redundancy plots and the uniqueness print-out

Date: 2/4
Author: Therese Björkman & Hanad Abdullahi
"""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import plotly.graph_objs as go
import plotly.figure_factory as ff
from prettytable import PrettyTable
from Visualisation.Redundancy.redundancy_functions import *

def heatmap_plot(isolate_data: dict, Csv_name: str, excel_name: str, sheet_name: str, plot : bool):
    """
    Takes in a dictionary containing the isolate data and uses this data to create a 
    heatmap that shows how similar each isolate is to eachother.
    """
    chosen_isolate = choose_isolates(Csv_name, excel_name, sheet_name)
    chosen_isolate_names = chosen_isolate.Isolate.values.tolist()
    first_values = {
        isolate: [float(tup[0] if tup[0] is not None else 0) for tup in isolate_data[isolate]] for isolate in chosen_isolate_names
        }

    
    similarity_matrix = np.zeros((len(chosen_isolate_names), len(chosen_isolate_names)))
    for i in range(len(chosen_isolate_names)):
        for j in range(len(chosen_isolate_names)):
            if i == j:
                similarity_matrix[i][j] = 1
            else:
                list1 = first_values[chosen_isolate_names[i]]
                list2 = first_values[chosen_isolate_names[j]]
                if all(val == 0 for val in (list1 + list2)):
                    similarity_matrix[i][j] = 1
                elif any(val is None for val in (list1 + list2)):
                    continue
                else:
                    cosine_similarity_val = cosine_similarity([list1, list2])[0][1]
                    similarity_matrix[i][j] = cosine_similarity_val

    fig = go.Figure(
        data=go.Heatmap(
        z=similarity_matrix,
        x=chosen_isolate_names,
        y=chosen_isolate_names,
        colorscale='mint',
        customdata=[(x, y) for x in chosen_isolate_names for y in chosen_isolate_names],
        hovertemplate='Isolat 1: %{x}<br>Isolat 2: %{y}<br>Likhet: %{z}<br>',
        zhoverformat='.2f'
    )
)

    fig.update_layout(
        title={
        'text': "Likhet mellan isolat",
        'x': 0.5,
        'xanchor': 'center',
        'font_size': 17
        },
    xaxis_title='Isolat',
    yaxis_title='Isolat',
    template="plotly_dark"
)
    if plot:
        fig.show()
    return similarity_matrix
   
def barplot(SIR_total_per_anti, plot:bool):
    """
    Plots the bar plot containing the amounts of MIC-values that are redundant for each antibiotic. It also
    shows the amount of redundant MIC-values from each SIR-cateegory in different colors.
    """ 
    colors = {'A': 'limegreen', 'B': 'gold', 'C': 'tomato'}
    keys = list(SIR_total_per_anti.keys())
    keys = list(map(lambda x: x.replace('Trimethoprim-sulfamethoxazole', 'T.sulfamethoxazole'), keys))
    values = list(SIR_total_per_anti.values())
    S = [dict['S'] for dict in values]
    I = [dict['I'] for dict in values]
    R = [dict['R'] for dict in values]

    fig = go.Figure(data=[
        go.Bar(name='Känslig', x = keys, y = S, marker={'color': colors['A']}),
        go.Bar(name='Intermediär', x = keys, y = I, marker={'color': colors['B']}),
        go.Bar(name='Resistent', x = keys, y = R, marker ={'color': colors['C']})
    ])

    fig.update_layout(barmode='stack', template="plotly_dark" ,title={
        'text': "Antalet redundanta isolat för varje antibiotikum",
        'x': 0.5,
        'xanchor': 'center',
        'font_size': 17
    }, xaxis_title = "Antibiotika", yaxis_title = "Antal isolat")
    if plot:
        fig.show()

def tree(similarity: np.array, Csv_name: str, excel_name: str, sheet_name: str, plot:bool):
    """
    Plots a tree plot to see how closely related the isolates are when comparing their MIC-values.
    """
    chosen_isolate = choose_isolates(Csv_name, excel_name, sheet_name)
    chosen_isolate_names = chosen_isolate.Isolate.values.tolist()
    distance_matrix = 1 - similarity

    fig = ff.create_dendrogram(distance_matrix, orientation='bottom', labels=chosen_isolate_names)

    fig.update_layout(
    autosize  = True, 
    title={
        'text': "Likhet mellan isolat",
        'x': 0.5,
        'xanchor': 'center',
        'font_size': 17},
    xaxis_title='Isolat',
    yaxis_title='Distans',
    template="plotly_dark")
    fig.update_yaxes(visible=False)

    # Customize the line thickness
    fig.update_traces(line=dict(width=6))

    if plot:
        fig.show()
     
def unique_score(isolate_selection: dict,  antibiotic_names : list, perform:bool):
    """
    This function produces a dictionary that displays how many unique mic-values each isolate has.
    This by comparing each isolates MIC-value with every other isolates MIC-value with the same index. 
    If an isolate has a value at a specific index, that no other isolate has at the same index. 
    Then the mic-value, the region(SIR) and the name of the antibiotic is saved.
    """
    result = {}
    for key, value in isolate_selection.items():
        other_values = [l for key2, l in isolate_selection.items() if key2 != key]
        unique_tuples = [(value[i][0], value[i][1], i) for i in range(len(value)) 
                        if not any(value[i] == l[i] for l in other_values)]
        result[key] = (len(unique_tuples), unique_tuples)

    for key, value in result.items():
        new_tuple_list = []
        removed_tuple_list = []
        for tuple_item in value[1]:
            if (
                tuple_item[1] == 'Missing bp' or 
                tuple_item[1] == 'Off-scale' or 
                tuple_item[1] == 'Not in panel'
                ):
                removed_tuple_list.append(
                    (int(tuple_item[0])-1, 
                     tuple_item[1], 
                     antibiotic_names[tuple_item[2]]))
            else:
                new_tuple_item = (tuple_item[0], tuple_item[1], antibiotic_names[tuple_item[2]])
                new_tuple_list.append(new_tuple_item)
        result[key] = (value[0], new_tuple_list + removed_tuple_list)

    sorted_dict = dict(sorted(result.items(), key=lambda item: item[1][0]))
    table = PrettyTable()
    table.field_names = ["Isolat", "Antal unika MIC-värden", "Antibiotika (MIC-värde, SIR-kategori))"]
    table.hrules = True
    for key, value in sorted_dict.items():
        table.add_row([key, value[0], "\n".join([f"{x[2]} ({x[0]}, {x[1]})" for x in value[1]])])
    if perform:
        print()
        print("-------------------------------")
        print("Unika MIC-värden för varje stam")
        print("-------------------------------")
        print(table)
        print()

def main(
        csv,
        threshold_redundancy, 
        display_barplot: bool, 
        display_heatmap: bool, 
        display_tree:bool, 
        print_unique_scores: bool
        ):
    """The main function calls upon all the other functions and takes boolean inputs that the 
    user chooses themselves. A true means that the visualisation or print out will be performed, 
    and a false would mean that it would not be performed.
    """
    # The specified threshold for how many values that are allowed to have the same MIC-value until it is considered redundant

    # The names of the excel file and the specific excel sheet as well as the name of the CSV-file containing the panel
    excel = "Q-linea_files/CIB_TF-data_AllIsolates_20230302.xlsx"
    excel_sheet = 'refMIC-matrix_US'

    # Here we get all the names of the isolates in the panel, this will later be used as a key
    isolate_data = create_isolate_data(csv, excel, excel_sheet,)

    # Get the MIC values for each isolate
    anti_mic_values = antibiotic_names_gets_values(csv, excel, excel_sheet)

    # Get the r-score for each antibiotic and their SIR_category
    SIR_total_per_anti = r_score(anti_mic_values, excel, excel_sheet, threshold_redundancy)

    # Plot the barplot
    barplot(SIR_total_per_anti, display_barplot)

    # Plot the heatmap and get the worst isolate score???
    similarity = heatmap_plot(isolate_data, csv, excel, excel_sheet, display_heatmap)

    # Plot the treegram
    tree(similarity, csv, excel, excel_sheet, display_tree)
    
    #Will calculate the list of antibiotic names
    names = get_antibiotic_names(excel,excel_sheet)
    #print out the unique score, depending on the boolean input of print_unique_scores:
    unique_score(isolate_data, names, print_unique_scores)

if __name__ == "__main__":
   main("Chosen_isolates_folder/Chosen_isolates.csv", 1, True, True, True, True)


