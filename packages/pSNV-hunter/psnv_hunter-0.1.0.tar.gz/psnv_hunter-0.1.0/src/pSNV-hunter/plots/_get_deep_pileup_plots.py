import plotly.graph_objects as go
import numpy as np
import pandas as pd


def af_greater_than_25_scatterplot(
    path_to_overview_file: str, 
    only_relevant: bool = True
):
    data = pd.read_csv(path_to_overview_file, delimiter="\t")

    gene_name = path_to_overview_file.split("/")[-5]
    position = path_to_overview_file.split("/")[-4]

    cohorts = {}
    for idx, row in data.iterrows():
        cohort_file = row["Cohort_File"].replace(".txt", "")
        af = float(row["SNPs_AF>25_%"])

        cohort = cohort_file.split("_")[2]
        if cohort not in cohorts:
            cohorts[cohort] = {"tumor": -1, "control": -1}
        if "control" in cohort_file:
            cohorts[cohort]["control"] = float(af)
        else:
            cohorts[cohort]["tumor"] = float(af)

    num_original_cohorts = len(cohorts.keys())

    if only_relevant:
        cohorts_to_remove = []
        for cohort in cohorts:
            control_value = cohorts[cohort]["control"]
            tumor_value = cohorts[cohort]["tumor"]
            if control_value == 0 and tumor_value == 0:
                cohorts_to_remove.append(cohort)
        for cohort in cohorts_to_remove:
            cohorts.pop(cohort, None)

    x_axis = list(cohorts.keys())

    num_current_cohorts = len(x_axis)

    if len(x_axis) == 0:
        return af_greater_than_25_scatterplot(path_to_overview_file, False)

    else:
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=x_axis,
                y=[cohorts[cohort]["tumor"] for cohort in x_axis],
                mode="markers",
                marker_color="red",
                marker={"size": 10},
                name="Tumor",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=x_axis,
                y=[cohorts[cohort]["control"] for cohort in x_axis],
                mode="markers",
                marker_color="green",
                marker={"symbol": "circle-x-open", "size": 10},
                name="Control",
            )
        )

        fig.update_layout(
            title=f"<b>Patients with a minor allele frequency > 25%</b><br><sup>Gene Name: {gene_name} / Position: {position} / Displaying {num_current_cohorts} of {num_original_cohorts} cohorts",
            xaxis_title="Cohorts",
            yaxis_title="Percent of Patients",
            # yaxis_range=[-2, 100],
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

        fig.update_xaxes(tickangle=45)

        return fig


def at_least_two_variant_alleles_scatterplot(
    path_to_overview_file: str, 
    only_relevant: bool = True,
    ref: str = None,
    alt: str = None,
):
    data = pd.read_csv(path_to_overview_file, delimiter="\t")

    gene_name = path_to_overview_file.split("/")[-5]
    position = path_to_overview_file.split("/")[-4]

    cohorts = {}

    for _, row in data.iterrows():
        # Get the maximum.
        maximum = np.max(
            [row["min_2_A"], row["min_2_C"], row["min_2_G"], row["min_2_T"]]
        )

        # Get the cohort.
        cohort = row["Cohort_File"].split("_")[2].replace(".txt", "")
        tumor_or_control = row["Cohort_File"].split("_")[1]

        # Get the counts.
        min_2_A = float(row["min_2_A"]) if float(row["min_2_A"]) != maximum else 0
        min_2_C = float(row["min_2_C"]) if float(row["min_2_C"]) != maximum else 0
        min_2_G = float(row["min_2_G"]) if float(row["min_2_G"]) != maximum else 0
        min_2_T = float(row["min_2_T"]) if float(row["min_2_T"]) != maximum else 0

        if cohort not in cohorts:
            cohorts[cohort] = {
                "tumor": {"A": -1, "C": -1, "G": -1, "T": -1},
                "control": {"A": -1, "C": -1, "G": -1, "T": -1},
            }
        cohorts[cohort][tumor_or_control]["A"] = min_2_A
        cohorts[cohort][tumor_or_control]["C"] = min_2_C
        cohorts[cohort][tumor_or_control]["G"] = min_2_G
        cohorts[cohort][tumor_or_control]["T"] = min_2_T

    num_original_cohorts = len(cohorts.keys())

    if only_relevant:
        cohorts_to_remove = []
        for cohort in cohorts:
            tumor_sum = np.sum(
                [
                    cohorts[cohort]["tumor"][nucleotide]
                    for nucleotide in ["A", "C", "G", "T"]
                ]
            )
            control_sum = np.sum(
                [
                    cohorts[cohort]["control"][nucleotide]
                    for nucleotide in ["A", "C", "G", "T"]
                ]
            )
            if (tumor_sum == 0) and (control_sum == 0):
                cohorts_to_remove.append(cohort)

        for cohort in cohorts_to_remove:
            cohorts.pop(cohort, None)

    x_axis = list(cohorts.keys())

    num_current_cohorts = len(x_axis)

    if len(x_axis) == 0:
        return at_least_two_variant_alleles_scatterplot(path_to_overview_file, False, ref, alt)
    else:
        fig = go.Figure()

        color_dict = {"A": "green", "C": "blue", "G": "orange", "T": "red"}

        for nucleotide in ["A", "C", "T", "G"]:
            if (ref and alt):
                fig.add_trace(
                    go.Scatter(
                        x=[cohort for cohort in cohorts],
                        y=[cohorts[cohort]["tumor"][nucleotide] for cohort in cohorts],
                        name=f"{nucleotide} (tumor)",
                        mode="markers",
                        marker_color=color_dict[nucleotide],
                        marker={"size": 10},
                        visible = True if (nucleotide in [ref, alt]) else "legendonly"
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=[cohort for cohort in cohorts],
                        y=[cohorts[cohort]["control"][nucleotide] for cohort in cohorts],
                        name=f"{nucleotide} (control)",
                        mode="markers",
                        marker_color=color_dict[nucleotide],
                        marker={"symbol": "circle-x-open", "size": 10},
                        visible = True if (nucleotide in [ref, alt]) else "legendonly"
                    )
                )
            else:
                fig.add_trace(
                    go.Scatter(
                        x=[cohort for cohort in cohorts],
                        y=[cohorts[cohort]["tumor"][nucleotide] for cohort in cohorts],
                        name=f"{nucleotide} (tumor)",
                        mode="markers",
                        marker_color=color_dict[nucleotide],
                        marker={"size": 10},
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=[cohort for cohort in cohorts],
                        y=[cohorts[cohort]["control"][nucleotide] for cohort in cohorts],
                        name=f"{nucleotide} (control)",
                        mode="markers",
                        marker_color=color_dict[nucleotide],
                        marker={"symbol": "circle-x-open", "size": 10},
                    )
                )

            fig.update_layout(
                title=f"<b>Patients with at least 2 Variant Alleles</b><br><sup>Gene Name: {gene_name} / Position: {position} / Displaying {num_current_cohorts} of {num_original_cohorts} cohorts",
                xaxis_title="Cohorts",
                yaxis_title="Percent of Affected Patients",
                # yaxis_range=[-2, 100],
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

            fig.update_xaxes(tickangle=45)

        return fig
