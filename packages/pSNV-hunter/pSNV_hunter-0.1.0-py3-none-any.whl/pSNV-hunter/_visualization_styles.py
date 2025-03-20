from dash import html

PLOTLY_BOLDED_STYLE = {
    "fontSize": "18px",     # Match Plotly's default title size
    "color": "##2b3f5e",        # Match Plotly's default title color
    "fontWeight": "bold",   # Ensure bold styling
    "textAlign": "center"   # Center the title horizontally
}

SEPARATION_LINE_FOR_TABS = html.Hr(
    style={
        "borderTop": "2px solid #bbb",  # Subtle gray line
        "width": "80%",                 # Make the line shorter than full width
        "margin": "20px auto"           # Add spacing and center the line
    }
)



# Define the displayed names of the data table.
DATA_TABLE_COLUMN_CONVERSION = {
    "within_chromhmm_promoter": {
        "table_name": "ChromHMM",
        "tooltip": "Boolean for ChromHMM Promoter. If 'True', this position is annoyed to have open chromatin.",
    },
    "within_cgc_list": {
        "table_name": "CGC List",
        "tooltip": "Boolean for CGC (Cancer Gene Census) list. If 'True', this gene is within the 2022 CGC list.",
    },
    "GENE": {"table_name": "Gene Name"},
    "num_recurrent_mutations": {"table_name": "Recurrence"},
    "#CHROM": {"table_name": "Chromosome"},
    "POS": {"table_name": "Position"},
    "REF": {"table_name": "Reference"},
    "ALT": {"table_name": "Alternative"},
    "num_created_tfs_passing_tf_expression_threshold": {"table_name": "Created TFs"},
    "num_destroyed_tfs_passing_tf_expression_threshold": {
        "table_name": "Destroyed TFs"
    },
    "SEQUENCE_CONTEXT": {
        "table_name": "Sequence Context",
        "tooltip": "Sequence around the mutation. Here, the ',' represents where the mutation takes place.",
    },
    "CpGislands": {"table_name": "CpG Island"},
    "cohort": {
        "table_name": "Cohort",
    },
}

SIDEBAR_STYLE = {
    "position": "fixed",
    "overflow-y": "scroll",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "12rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "text-align": "center",
}

CONTENT_STYLE = {
    "margin-left": f"{int(SIDEBAR_STYLE['width'].replace('rem','')) + 1}rem",
    "margin-right": "2rem",
    "padding": "1rem 1rem",
}

TABLE_HEADER_STYLE = {
    "backgroundColor": "#3f6ffd",
    "color": "white",
    "textAlign": "center",
    "font-family": "Arial, sans-serif",
    "font-size": "100%",
    "height": "200%",
}
