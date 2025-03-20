import plotly.graph_objects as go
import numpy as np
import ast
import pandas as pd


def gene_expression_violin_plot(
    row: pd.Series,
    name_of_gene_column: str="GENE",
    name_of_chromosome_column: str="#CHROM",
    name_of_snv_position_column: str="POS",
    name_of_reference_nucleotide_column: str="REF",
    name_of_alternative_nucleotide_column: str="ALT",
    name_of_cohort_column: str="cohort",
    name_of_paths_with_recurrence_column: str="paths_with_recurrence(format=path,pid,cohort,bp,ref,alt,gene,chr,raw_score,zscore,log_score,confidence,purity,af,(tfs_seperated_by_//))",
    name_of_tfbs_column: str="JASPAR2020_CORE_vertebrates_non_redundant(tf_name,binding_affinity,seq1,seq2,raw,zscore,log,tf_sequence_logo)",
    name_of_expression_traces_column: str="expression_traces",
    name_of_expression_column: str="FPKM",
    name_of_normalized_expression_column: str="FPKM_Z_score"
):
    gene_name = row[name_of_gene_column]
    chromosome = row[name_of_chromosome_column]
    pos = row[name_of_snv_position_column]
    ref = row[name_of_reference_nucleotide_column]
    alt = row[name_of_alternative_nucleotide_column]

    selected_patient_cohort = row[name_of_cohort_column] if name_of_cohort_column in list(row.index) else "unknown_cohort"

    recurrence = row[name_of_paths_with_recurrence_column] if name_of_paths_with_recurrence_column in list(row.index) else "."
    
    expression_trace = ast.literal_eval(row[name_of_expression_traces_column])

    relevant_cohorts = [selected_patient_cohort]

    if recurrence != ".":
        for entry in recurrence.split(";"):
            cohort = entry.split(",")[2]
            raw = entry.split(",")[8]
            if (raw != "not_available") and (cohort not in relevant_cohorts):
                relevant_cohorts.append(cohort)

    fig = go.Figure()

    for selection in ["zscore", "raw", "log"]:
        if selection == "zscore":
            legend_title = "Z-Score"
        elif selection == "raw":
            legend_title = "Raw"
        else:
            legend_title = "Log"

        # Add background traces.
        for cohort in relevant_cohorts:
            fig.add_trace(
                go.Violin(
                    y=expression_trace[row[name_of_gene_column]][cohort][selection],
                    name=f"{cohort} <br>(n={len(expression_trace[gene_name][cohort]['zscore'])})",
                    box_visible=True,
                    meanline_visible=True,
                    marker_color="lightgrey",
                    legendgroup=selection,
                    legendgrouptitle_text=legend_title,
                    visible=True if selection == "zscore" else "legendonly",
                )
            )

        # Plot the recurrence Z-scores.
        recurrence_without_ge_data_available = {}
        paths_with_recurrence = row[name_of_paths_with_recurrence_column]
        if paths_with_recurrence != ".":
            for entry in paths_with_recurrence.split(";"):
                pid, cohort = entry.split(",")[1:3]
                raw, zscore, log = entry.split(",")[8:11]

                if raw == "not_available":
                    if cohort not in recurrence_without_ge_data_available:
                        recurrence_without_ge_data_available[cohort] = 0
                    recurrence_without_ge_data_available[cohort] += 1
                    continue
                if selection == "zscore":
                    score = zscore
                elif selection == "raw":
                    score = raw
                elif selection == "log":
                    score = log
                else:
                    assert False

                fig.add_trace(
                    go.Scatter(
                        mode="markers",
                        x=[
                            [
                                f"{cohort} <br>(n={len(expression_trace[gene_name][cohort]['zscore'])})"
                            ]
                        ],
                        y=[score],
                        name=str(pid)[:8],
                        marker_size=10,
                        marker_line_width=1,
                        marker_color="black",
                        # showlegend=False,
                        legendgroup=selection,
                        visible=True if selection == "zscore" else "legendonly",
                    )
                )

        # Add scatter plot for entries.
        if row[name_of_tfbs_column] == ".":
            continue

        if selection == "zscore":
            score = float(row[name_of_normalized_expression_column])
        elif selection == "raw":
            score = float(row[name_of_expression_column])
        else:
            score = np.log(float(row[name_of_expression_column]))

        fig.add_trace(
            go.Scatter(
                mode="markers",
                x=[
                    [
                        f"{selected_patient_cohort} <br>(n={len(expression_trace[gene_name][selected_patient_cohort]['zscore'])})"
                    ]
                ],
                y=[score],
                name=f"<b>{gene_name}</b>",
                marker_size=13,
                marker_line_width=1,
                marker_color="red",
                text=["Current Gene"],
                legendgroup=selection,
                visible=True if selection == "zscore" else "legendonly",
            )
        )

    additional_text = ""
    if len(list(recurrence_without_ge_data_available.keys())) > 0:
        additional_text += (
            "<b>Additional Recurrent Mutations (No GE Data Available):</b> "
        )
        for cohort in recurrence_without_ge_data_available:
            additional_text += (
                f"{cohort} ({recurrence_without_ge_data_available[cohort]}x), "
            )
        additional_text = additional_text[:-2]

    fig.update_layout(
        title={
            "text": f"<b>Gene Expression for <i>{gene_name}</i> (chr{chromosome}:{pos} {ref}>{alt})</b><br><sup>{additional_text}",
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
