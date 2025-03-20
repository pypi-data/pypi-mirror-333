import dash_bootstrap_components as dbc
from dash import html

import pandas as pd

def _get_ncbi_definition_from_database(
    name_of_gene_or_tf: str,
    descriptions_database: pd.DataFrame
):
    if name_of_gene_or_tf in list(descriptions_database["Symbol"].unique()):
        return descriptions_database[descriptions_database["Symbol"] == name_of_gene_or_tf]["Summary"].iloc[0]
    return "<unknown>"

def _get_reverse_complement(seq: str) -> str:
    """
    Get the reverse complement of a DNA sequence.

    Parameters:
    - seq (str): The input DNA sequence.

    Returns:
    - str: The reverse complement of the input DNA sequence.

    The function uses a dictionary to find the complement of each nucleotide (A, C, G, T),
    and then constructs the reverse complement by joining the complementary nucleotides in reverse order.

    Example:
    >>> _get_reverse_complement("ATCG")
    'CGAT'
    """
    complement = {"A": "T", "C": "G", "G": "C", "T": "A"}
    reverse_complement = "".join(complement.get(base, base) for base in reversed(seq))
    return reverse_complement

def _make_card(
    title: str = "",
    subtitle: str = "",
    text: str = "",
):
    """Helper function for the _get_patient_information, which is defined in this script.

    Args:
        title (str, optional): _description_. Defaults to "".
        subtitle (str, optional): _description_. Defaults to "".
        text (str, optional): _description_. Defaults to "".

    Returns:
        _type_: _description_
    """
    card = dbc.Card(
        dbc.CardBody(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H4(f"{title}", style={"color": "#3f6ffd"}),
                                html.H6(f"{subtitle}"),
                            ],
                            width=8,
                        ),
                        dbc.Col([html.H4(f"{text}")], align="center", width=4),
                    ]
                )
            ]
        ),
    )
    return card


def _get_information_page(row: pd.Series):
    """Generate an information page for a given gene mutation."""
    # Extract details for headers
    gene_name = row["GENE"]
    pos = row["POS"]
    chrom = row["#CHROM"]
    ref = row["REF"]
    alt = row["ALT"]
    strand = row["strand"]

    # Create header
    header = dbc.Row(
        dbc.Col(
            [
                html.H1(
                    f"Information on {gene_name}",
                    style={"color": "#3f6ffd", "text-align": "center"},
                ),
                html.H4(
                    f"{ref} > {alt} | chr{chrom}:{pos} | {strand} strand",
                    style={"text-align": "center", "color": "#6c757d"},
                ),
            ],
            width={"size": 6, "offset": 3},
        )
    )

    # Recurrence cards
    recurrence_cards = dbc.Row(
        [
        dbc.Col(
            _make_card(
                title="Recurrence Mutations",
                subtitle="Recurrent Mutations within the current dataset.",
                text=f"{int(row['number_of_pcawg_recurrent_mutations'])}",
            ),
            width=8,
        ),
        ],
        justify="center",
    )

    # Z-score and raw expression cards
    zscore_columns = [col for col in list(row.index) if "FPKM_Z_score" in col]
    zscore_cards = [
        dbc.Col(
            _make_card(
                title=f"{column.replace('FPKM_Z_score', '').strip()} Gene Expression",
                subtitle="FPKM Z-Score / Raw",
                text=f"{round(float(row[column]), 2)} / {round(float(row['FPKM']), 2)}",
            ),
            width=8,
        )
        for column in zscore_columns
    ]

    # CGC and ChromHMM promoter cards
    promoter_cards = [
        dbc.Col(
            _make_card(
                title="Within CGC List",
                subtitle="",
                text=f"{row['within_cgc_list']}",
            ),
            width=4,
        ),
        dbc.Col(
            _make_card(
                title="Open Chromatin",
                subtitle="",
                text=f"{row['within_chromhmm_promoter']}",
            ),
            width=4,
        ),
    ]

    # Transcription factor cards
    def generate_tf_card(title, color, num_tfs, tfs_list):
        return dbc.Card(
            dbc.CardBody(
                [
                    html.H4(title, style={"color": color}),
                    html.H6(
                        "A TF is defined as 'created' if binding affinity >= 11."
                        if "Created" in title
                        else "A TF is defined as 'destroyed' if binding affinity <= 0.09."
                    ),
                    html.Br(),
                    html.H4(f"Count: {num_tfs}", style={"color": color}),
                    html.P(
                        tfs_list,
                        style={
                            "overflowY": "auto",
                            "maxHeight": "150px",
                            "padding": "5px",
                            "backgroundColor": "#f8f9fa",
                            "borderRadius": "5px",
                            "border": "1px solid #dee2e6",
                        },
                    ),
                ]
            )
        )

    created_tfs = row["created_tfs_passing_tf_expression_threshold"]
    destroyed_tfs = row["destroyed_tfs_passing_tf_expression_threshold"]

    created_tfs_card = generate_tf_card(
        "Created Transcription Factors",
        "#28a745",  # Green
        row.get("num_created_tfs_passing_tf_expression_threshold", 0),
        created_tfs if pd.notna(created_tfs) else "No Created Transcription Factors",
    )

    destroyed_tfs_card = generate_tf_card(
        "Destroyed Transcription Factors",
        "#dc3545",  # Red
        row.get("num_destroyed_tfs_passing_tf_expression_threshold", 0),
        destroyed_tfs if pd.notna(destroyed_tfs) else "No Destroyed Transcription Factors",
    )

    # Allele frequency and CpG island cards
    allele_frequency = row["allele_frequency"]
    cpg_island = "True" if row["CpGislands"] != "." else "False"
    af_and_cpg_cards = [
        dbc.Col(
            _make_card(
                title="Allele Frequency",
                subtitle="",
                text=f"{allele_frequency}",
            ),
            width=4,
        ),
        dbc.Col(
            _make_card(
                title="CpG Island",
                subtitle="",
                text=f"{cpg_island}",
            ),
            width=4,
        ),
    ]

    # Assemble layout
    info_div = html.Div(
        [
            html.Br(),
            header,
            html.Br(),
            recurrence_cards,
            html.Br(),
            dbc.Row(zscore_cards, justify="center"),
            html.Br(),
            dbc.Row(promoter_cards, justify="center"),
            html.Br(),
            dbc.Row(af_and_cpg_cards, justify="center"),
            html.Br(),
            dbc.Row([dbc.Col(created_tfs_card, width=6), dbc.Col(destroyed_tfs_card, width=6)]),
        ]
    )
    return info_div


def _get_transcription_factor_tabs(
    row: pd.Series,
):
    # Get the name of all of transcription factors.
    tabs = []
    try:
        tfs_created = [
            tf for tf in row["created_tfs_passing_tf_expression_threshold"].split(",")
        ]
        for tf in tfs_created:
            tabs.append(
                dbc.Tab(label=f"{tf}", tab_id=f"{tf}", label_style={"color": "green"})
            )
    except:
        tfs_created = []
    try:
        tfs_destroyed = [
            tf for tf in row["destroyed_tfs_passing_tf_expression_threshold"].split(",")
        ]
        for tf in tfs_destroyed:
            tabs.append(
                dbc.Tab(label=f"{tf}", tab_id=f"{tf}", label_style={"color": "red"})
            )
    except:
        tfs_destroyed = []
    if len(tabs) == 0:
        tabs = dbc.Tabs(
            [
                dbc.Tab(
                    label="No Created or Destroyed Transcription Factors", disabled=True
                )
            ],
            id="tf-tabs",
        )
    else:
        tabs = dbc.Tabs(tabs, id="tf-tabs")
    return tabs
