import plotly.graph_objects as go
import ast
import pandas as pd


def tf_expression_violin_plot(
    row: pd.Series,
    chosen_tf_name: str,
    name_of_expression_traces_column: str="expression_traces",
    name_of_cohort_column: str="cohort",
    name_of_tfbs_column: str="JASPAR2020_CORE_vertebrates_non_redundant(tf_name,binding_affinity,seq1,seq2,raw,zscore,log,tf_sequence_logo)",
    name_of_pid_column: str="pid",
):
    expression_trace = ast.literal_eval(row[name_of_expression_traces_column])

    fig = go.Figure()

    for selection in ["zscore", "raw", "log"]:
        if selection == "zscore":
            legend_title = "Z-Score"
        elif selection == "raw":
            legend_title = "Raw"
        else:
            legend_title = "Log"

        # Add background traces.
        cohort = row[name_of_cohort_column]
        n = len(expression_trace[chosen_tf_name][cohort][selection])

        fig.add_trace(
            go.Violin(
                y=expression_trace[chosen_tf_name][cohort][selection],
                name=f"<b>{cohort}</b><br>(n={n})",
                box_visible=True,
                meanline_visible=True,
                marker_color="lightgrey",
                legendgroup=selection,
                legendgrouptitle_text=legend_title,
                visible=True if selection == "raw" else "legendonly",
                opacity=0.6,
                line_color="black",
                points="all"
            )
        )
        # Add scatter plot.
        if row[name_of_tfbs_column] == ".":
            continue

        for entry in row[name_of_tfbs_column].split(";"):
            tf_name = entry.split(",")[0]
            if tf_name == chosen_tf_name:
                binding_affinity = entry.split(",")[1]
                raw, zscore, log = entry.split(",")[4:7]
        if selection == "zscore":
            score = zscore
        elif selection == "raw":
            score = raw
        else:
            score = log

        fig.add_trace(
            go.Scatter(
                mode="markers",
                x=[f"<b>{cohort}</b><br>(n={n})"],
                y=[score],
                marker_size=13,
                marker_line_width=1,
                marker_color="red",
                text=["Current Gene"],
                legendgroup=selection,
                visible=True if selection == "raw" else "legendonly",
                name=f'{row[name_of_pid_column][:8]}'
            )
        )

    fig.update_layout(
        title={
            "text": f"<b>Gene Expression for {chosen_tf_name}</b> <br>(Binding Affinity {binding_affinity})",
            "y": 0.9,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        },
        yaxis_title = "Expression"
    )
    
    fig.update_layout(
        plot_bgcolor='white',  # Set plotting area background to white
        paper_bgcolor='white',  # Set overall figure background to white
        xaxis=dict(
            showline=True,  # Show axis lines
            linecolor='black',  # Color of axis lines
            linewidth=1  # Width of axis lines
        ),
        yaxis=dict(
            showline=True,  # Show axis lines
            linecolor='black',  # Color of axis lines
            linewidth=1,  # Width of axis lines
            ticks='outside',  # Display ticks outside the axis
            tickcolor='black',  # Color of ticks
            tickwidth=2  # Width of ticks
        )
    )
    
    return fig
