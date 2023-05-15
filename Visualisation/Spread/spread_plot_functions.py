"""
Functions used when creating the spread-plot 

Date: 10/4 
Author: Victor Wong
"""

import pandas as pd
import numpy as np
import plotly.express as px
from Visualisation.data_extraction_functions import (
    parse_fastidious,
    parse_on_off_scale,
)

# Set random seed
np.random.seed(1)


def create_plot_df(
    antibiotics: list,
    mic_data: list,
    fastidious_dict: dict,
    x_jitter: float = 0.15,
    y_jitter: float = 0.05,
) -> pd.DataFrame:
    """Create dataframe used for plotting."""

    mic_dict = {"S": "Känslig", "I": "Intermediär", "R": "Resistent"}

    # Set ticks of x axis
    x_axis = [i for i in range(len(antibiotics))]

    # Initialize lists to hold values used for plotting
    x_values, y_values = [], []
    SIR_category_list = []
    MIC_value_list = []
    isolate_names = []
    on_off_scale = []
    pathogen_list = []
    fastidious_list = []

    for x_value, abx_mic_data in zip(x_axis, mic_data):
        for isolate, mic_value, SIR_category, scale, pathogen in abx_mic_data:
            # Add random noise to avoid overlapping
            x_value_jitter = x_value + np.random.uniform(-x_jitter, x_jitter)
            mic_value_jitter = mic_value + np.random.uniform(-y_jitter, y_jitter)
            # Add data to the lists
            isolate_names.append(isolate)
            x_values.append(x_value_jitter)
            SIR_category_list.append(mic_dict[SIR_category])
            MIC_value_list.append(2 ** (mic_value))
            on_off_scale.append(scale)
            pathogen_list.append(pathogen)
            parse_on_off_scale(scale, SIR_category, y_values, mic_value_jitter)
            parse_fastidious(fastidious_dict, pathogen, fastidious_list)

    # Create a DF used for plotting
    plot_df = pd.DataFrame(
        {
            "Antibiotika": x_values,
            "MIC": y_values,
            "Isolatnamn": isolate_names,
            "SIR": SIR_category_list,
            "Scale": on_off_scale,
            "Patogen": pathogen_list,
            "MIC värde": MIC_value_list,
            "Kräsenhet": fastidious_list,
        },
        index=np.arange(len(x_values)),
    )

    return plot_df


def add_rectangles_to_plot(fig, antibiotics: list, antibiotic_ranges: dict) -> None:
    """Adds rectangles to represent the on-scale concentrations."""
    for i in range(len(antibiotics)):
        if antibiotics[i] in antibiotic_ranges:
            non_fastidious_minimum = antibiotic_ranges[antibiotics[i]][
                "Non-Fastidious Minimum"
            ]
            non_fastidious_maximum = antibiotic_ranges[antibiotics[i]][
                "Non-Fastidious Maximum"
            ]
            fastidious_minimum = antibiotic_ranges[antibiotics[i]]["Fastidious Minimum"]
            fastidious_maximum = antibiotic_ranges[antibiotics[i]]["Fastidious Maximum"]

            if (
                non_fastidious_maximum is not None
                and non_fastidious_minimum is not None
            ):
                box_witdh = 0.4
                fig.add_vrect(
                    x0=i - box_witdh,
                    x1=i + box_witdh,
                    y0=0.99 - (10 - np.log2(non_fastidious_minimum / 4)) / 23,
                    y1=1.01 - (10 - np.log2(non_fastidious_maximum / 4)) / 23,
                    fillcolor="skyblue",
                    layer="below",
                    line_width=0,
                    opacity=0.8,
                )

            if fastidious_minimum is not None and fastidious_maximum is not None:
                box_witdh = 0.3
                fig.add_vrect(
                    x0=i - box_witdh,
                    x1=i + box_witdh,
                    y0=0.99 - (10 - np.log2(fastidious_minimum / 4)) / 23,
                    y1=1.01 - (10 - np.log2(fastidious_maximum / 4)) / 23,
                    fillcolor="ghostwhite",
                    layer="below",
                    line_width=0,
                    opacity=0.3,
                )


def plotly_dotplot(
    plot_df: pd.DataFrame,
    antibiotics: list,
    antibiotic_ranges: dict,
) -> None:
    """Plot a scatter plot of the isolates."""

    # Set ticks of x axis
    x_axis = [i for i in range(len(antibiotics))]

    # TODO should this be outside of function scope?
    y_axis_ticktext = [
        "Off-scale Min C",
        "0.00195",
        "0.00391",
        "0.00781",
        "0.01563",
        "0.03125",
        "0.0625",
        "0.125",
        "0.25",
        "0.5",
        "1",
        "2",
        "4",
        "8",
        "16",
        "32",
        "64",
        "128",
        "256",
        "512",
        "1024",
        "Off-scale Max C",
    ]

    # plot
    fig = px.scatter(
        plot_df,
        x="Antibiotika",
        y="MIC",
        hover_name="Isolatnamn",
        color="SIR",
        opacity=0.7,
        title="Testpanel",
        range_y=[-11, 12],
        template="plotly_dark",
        hover_data={
            "Antibiotika": False,
            "MIC": False,
            "Scale": False,
            "Patogen": True,
            "MIC värde": True,
            "Kräsenhet": True,
        },
    )

    # Changes the dot color depending on SIR category
    def change_trace_color(trace):
        if trace.name == "Resistent":
            trace.update(marker_color="tomato")
        elif trace.name == "Intermediär":
            trace.update(marker_color="gold")
        elif trace.name == "Känslig":
            trace.update(marker_color="limegreen")
        else:
            raise ValueError("Not a valid trace")

    # Update dot color
    fig.for_each_trace(change_trace_color)

    add_rectangles_to_plot(fig, antibiotics, antibiotic_ranges)

    # Add border to dots
    fig.update_traces(marker=dict(line=dict(width=1, color="DarkSlateGrey")))

    # Modify x-ticks, y-ticks, legend and title
    fig.update_layout(
        xaxis=dict(tickmode="array", tickvals=x_axis, ticktext=antibiotics),
        yaxis=dict(
            tickmode="array",
            tickvals=[i for i in range(-10, 12)],
            ticktext=y_axis_ticktext,
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        title_x=0.5,
    )
    fig.show()
