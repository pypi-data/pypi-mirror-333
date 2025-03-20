import dash
from datetime import datetime
import dash_bio as dashbio
from dash import dash_table, dcc, html, Input, Output, State, ctx, ALL
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import io
import base64
import os
from dash.dash import no_update

import glob

from plots._get_gene_expression_tab_plots import gene_expression_violin_plot
from plots._get_tf_expression_tab_plots import tf_expression_violin_plot
import plots._get_deep_pileup_plots as deeppileup
from _helper_functions import _get_information_page, _get_reverse_complement, _get_ncbi_definition_from_database
from _config import EXAMPLE_FILES, REQUIRED_COLUMNS, DATAFRAME_SETTINGS, PATH_TO_DEEP_PILEUP_REPOSITORY, PATH_TO_GENOME_TORNADO_PLOTS_REPOSITORY
from _visualization_styles import PLOTLY_BOLDED_STYLE, SEPARATION_LINE_FOR_TABS

# Initialize the Dash app with Bootstrap
app = dash.Dash(
    __name__, 
    suppress_callback_exceptions=True, 
    external_stylesheets=[dbc.themes.BOOTSTRAP], 
    title="pSNV Hunter"
)

app._favicon = "pSNV_Hunter_logo.ico" 

# Define the column names that are within the data files.
NAME_OF_GENE_COLUMN = DATAFRAME_SETTINGS["name_of_the_gene_column"]
NAME_OF_CHROMOSOME_COLUMN = DATAFRAME_SETTINGS["name_of_the_chromosome_column"]
NAME_OF_POSITION_COLUMN = DATAFRAME_SETTINGS["name_of_position_column"]
NAME_OF_REFERENCE_NUCLEOTIDE_COLUMN = DATAFRAME_SETTINGS["name_of_reference_nucleotide_column"]
NAME_OF_ALTERNATIVE_NUCLEOTIDE_COLUMN = DATAFRAME_SETTINGS["name_of_alternative_nucleotide_column"]
NAME_OF_SEQUENCE_CONTEXT_COLUMN = DATAFRAME_SETTINGS["name_of_sequence_context_column"]

NAME_OF_COHORT_COLUMN = DATAFRAME_SETTINGS["name_of_cohort_column"]

NAME_OF_TFBS_COLUMN = DATAFRAME_SETTINGS["name_of_tfbs_column"]
TFBS_BINDING_AFFINITY_CREATION_THRESHOLD = DATAFRAME_SETTINGS["tfbs_binding_affinity_creation_threshold"]
TFBS_BINDING_AFFINITY_DESTRUCTION_THRESHOLD = DATAFRAME_SETTINGS["tfbs_binding_affinity_destruction_threshold"]
NAME_OF_COLUMN_WITH_LIST_OF_CREATED_TFS = DATAFRAME_SETTINGS["name_of_column_with_list_of_created_tfbs"]
NAME_OF_COLUMN_WITH_LIST_OF_DESTROYED_TFS = DATAFRAME_SETTINGS["name_of_column_with_list_of_destroyed_tfbs"]

NAME_OF_PATHS_WITH_RECURRENCE_COLUMN = DATAFRAME_SETTINGS["name_of_paths_with_recurrence_column"]
NAME_OF_EXPRESSION_TRACES_COLUMN = DATAFRAME_SETTINGS["name_of_expression_traces_column"]

NAME_OF_EXPRESSION_COLUMN = DATAFRAME_SETTINGS["name_of_expression_column"]
NAME_OF_NORMALIZED_EXPRESSION_COLUMN = DATAFRAME_SETTINGS["name_of_normalized_expression_column"]
NAME_OF_PID_COLUMN = DATAFRAME_SETTINGS["name_of_pid_column"]

# Global layout with dcc.Store
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='uploaded-files-store', storage_type='memory'),  # Store data in memory storage
    dcc.Store(id='notes-store', storage_type='memory', data={}),  # Store notes for each row
    dcc.Store(id='saved-mutations', storage_type='memory', data = {}),
    html.Div(id='page-content')
])

# Global storage for uploaded files.
uploaded_files = {}

# Placeholder for the selected dataframe.
chosen_filename = None

# Load in the gene/tf name and description database.
# NOTE: Taken from https://github.com/nicholas-abad/ncbi_gene_names_and_descriptions
descriptions_database = pd.read_csv("https://media.githubusercontent.com/media/nicholas-abad/ncbi_gene_names_and_descriptions/refs/heads/main/outputs/gene_names_and_descriptions_2025-Feb-04_18%3A24%3A13.csv", delimiter="\t")

def homepage_layout():
    return dbc.Container([
        dcc.Store(id='previous-data', data=[]),  # Store for previous data state,
        dbc.Row([
            dbc.Col(html.H1("pSNV Hunter: Upload Your Data Files", className="text-center mt-3 mb-3"), width=12)
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Upload(
                    id='file-upload',
                    children=html.Div(['Drag and Drop or ', html.A('Select Files')], className="text-center"),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'marginBottom': '20px'
                    },
                    multiple=True
                ),
                html.Div(
                    "Or load the example files below:",
                    className="text-center mt-4 mb-2"
                ),
                dbc.Row([
                    dbc.Col(
                        dbc.Button(
                            "Load Example Files",
                            id="load-example",
                            color="secondary",
                            className="mb-2",
                            style={"width": "100%", "height": "50px", "fontSize": "16px"}
                        ),
                        width=4,
                        className="mx-auto"
                    )
                ], justify="center"),
                html.Div(id="upload-message", className="text-success text-center mt-3"),
                SEPARATION_LINE_FOR_TABS,
                html.H4("Uploaded Files", className="text-center mt-4"),
                dash_table.DataTable(
                    id='uploaded-files-table',
                    columns=[
                        {"name": "Filename", "id": "filename"},
                        {"name": "Rows", "id": "rows"},
                        {"name": "Columns", "id": "columns"},
                    ],
                    data=[],
                    editable=True,  # Allow editing of cells
                    style_table={'overflowX': 'auto'},
                    style_cell={
                        'textAlign': 'left',
                        'fontFamily': 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif',
                        'fontSize': '14px',  # Adjust font size if needed
                        'padding': '10px',   # Add padding for better readability
                    },
                    style_header={
                        'backgroundColor': '#e9ecef',
                        'fontWeight': 'bold',
                        'fontFamily': 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif',
                        'fontSize': '15px',  # Slightly larger font for headers
                        'textAlign': 'center'
                    },
                    style_data={
                        'color': 'black',
                        'backgroundColor': 'white',
                    },
                    row_deletable=True
                )
            ], width=12),
        ]),
        dbc.Row([
            dbc.Col(dbc.Button(
                "Go to File Viewer", 
                href="/viewer", 
                color="primary", 
                className="mt-3",
                style={"width": "100%", "height": "50px", "fontSize": "20px"}
            ), 
            width=4,
            className="mx-auto",
            align="center",
            style={"height": "100vh"}
            )
        ]),
        # Placeholder for data-table
        dbc.Row([
            dbc.Col([
                dash_table.DataTable(
                    id='data-table',
                    columns=[],  # Empty columns
                    data=[],  # Empty data
                    editable=True,
                    row_selectable='single',
                    dropdown={},
                    style_table={'overflowX': 'auto'},
                    style_cell={
                        'textAlign': 'left',
                        'fontFamily': 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif',
                        'fontSize': '14px',
                        'padding': '5px',
                    },
                    style_header={
                        'backgroundColor': '#e9ecef',
                        'fontWeight': 'bold',
                        'fontSize': '15px',
                    },
                    page_size=5,
                )
            ], width=12)
        ]),
    ], fluid=True)
    

def file_viewer_layout():
    return dbc.Container([
        dcc.Store(id='notes-store', storage_type='memory', data={}),
        dcc.Store(id='saved-mutations', storage_type='memory', data={}),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H1(
                        "pSNV Hunter",
                        className="text-center mt-3",
                        style={
                            "fontWeight": "bold",
                            "color": "#007bff",
                            "fontSize": "3rem"
                        }
                    ),
                    html.H5(
                        "Identifying, Prioritizing, and Visualizing Functional Promoter SNVs with the Recurrence-agnostic REMIND-Cancer Pipeline and pSNV Hunter",
                        className="text-center mt-3",
                        style={
                            "fontSize": "1.25rem",
                            "fontStyle": "italic",
                            "color": "#6c757d"
                        }
                    )
                ], style={"padding": "5px", "backgroundColor": "#f8f9fa", "borderRadius": "10px"})
            , width=12)
        ]),
        # Button to open the Offcanvas
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button(
                        "View Uploaded Files",
                        id="open-offcanvas",
                        n_clicks=0,
                        color="primary",
                        style={"marginTop": "20px", "width": "100%"}
                    ),
                    width=2
                ),
                dbc.Col(
                    [
                        dbc.Button(
                            "Download Dataset",
                            id="download-dataset-button",
                            n_clicks=0,
                            color="primary",
                            style={"marginTop": "20px", "width": "100%"}
                        ),
                        dcc.Download(
                            id="download-dataset"
                        )
                    ],
                    width=2
                ),
            ],
            justify="between"  # Push buttons to opposite ends of the row
        ),
        
        # Offcanvas definition
        dbc.Offcanvas(
            [
                html.H4("Uploaded Files", className="text-center mb-4"),
                html.Div(id="selected-file-display", className="text-center mb-3"),  # Display the chosen file
                dbc.Nav(id="file-list", vertical=True, pills=True, className="mb-3"),
                dbc.Button(
                    "OK",
                    id="close-offcanvas-button",
                    color="primary",
                    className="mb-3",
                    style={"width": "100%"}
                ),
                html.Div(
                    dbc.Button(
                        "Return to File Uploader",
                        href="/",
                        color="danger",
                        outline=True,
                        className="me-1",
                        style={"width": "100%", "fontSize": "16px"}
                    ),
                    style={
                        "position": "absolute",
                        "bottom": "20px",  # Adjust for spacing from bottom
                        "width": "90%",  # Keep button width responsive
                        "left": "5%",  # Center button horizontally
                    }
                ),
            ],
            id="offcanvas",
            title=" ",
            is_open=True,
            style={"width": "300px"}  # Adjust the width of the Offcanvas
        ),
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col(html.Div(id="error-message", className="text-danger text-center mb-3"), width=12)
                ]),
                dbc.Row([
                    dbc.Col([
                        dash_table.DataTable(
                            id='data-table',
                            columns=[],
                            data=[],
                            row_selectable='single',
                            filter_action="native",
                            sort_action="native",
                            sort_mode="multi",
                            page_action="native",
                            editable=True,
                            dropdown_conditional=[
                                {
                                    'if': {'column_id': 'interesting'},
                                    'options': [
                                        {"label": "Yes", "value": "yes"},
                                        {"label": "Maybe", "value": "maybe"},
                                        {"label": "No", "value": "no"},
                                        {"label": " ", "value": " "},
                                    ]
                                }
                            ],
                            css=[
                                {
                                    "selector": ".Select-menu-outer",
                                    "rule": "display: block !important",
                                },
                            ],
                            style_table={'overflowX': 'auto'},
                            style_cell={
                                'textAlign': 'left',
                                'fontFamily': 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif',
                                'fontSize': '14px',  # Adjust font size if needed
                                'padding': '5px',   # Add padding for better readability
                            },
                            style_header={
                                'backgroundColor': '#e9ecef',
                                'fontWeight': 'bold',
                                'fontFamily': 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif',
                                'fontSize': '15px',  # Slightly larger font for headers
                                'textAlign': 'center'
                            },
                            style_data={
                                'color': 'black',
                                'backgroundColor': 'white',
                            },
                            page_size=5
                        )
                    ], width=12, className="mb-4")
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button(
                            "Save Interesting Column",
                            id="save-interesting-button",
                            n_clicks=0,
                            color="primary",
                            style={"marginTop": "20px", "width": "100%"}
                        ),
                    ], width=2)
                ]),

                html.Div(id="save-interesting-message", className="text-success mt-2"),
                dbc.Row([
                    dbc.Col([
                        dbc.Tabs(
                        [
                            dbc.Tab(
                                label="Patient Info",
                                tab_id="tab-patient",
                                children=html.Div(id="patient-info-content", className="p-3")
                            ),
                            dbc.Tab(
                                label="Gene",
                                tab_id="tab-gene",
                                children=html.Div(id="gene-content", className="p-3")
                            ),
                            dbc.Tab(
                                label="Transcription Factors",
                                tab_id="tab-tfs",
                                children=html.Div(id="tfs-content", className="p-3")
                            ),
                            dbc.Tab(
                                label="IGV Genome Browser",
                                tab_id="tab-igv",
                                children=html.Div(id="igv-content", className="p-3")
                            ),
                            dbc.Tab(
                                label="Deep Pileup",
                                tab_id="tab-dp",
                                children=html.Div(id="dp-content", className="p-3")
                            ),
                            dbc.Tab(
                                label="Genome Tornado Plots",
                                tab_id="tab-gtp",
                                children=html.Div(id="gtp-content", className="p-3")
                            ),
                            dbc.Tab(
                                label="Notes",
                                tab_id="tab-notes",
                                children=html.Div(id="notes-content", className="p-3")
                            )
                        ],
                        id="graph-tabs",
                        active_tab="tab-patient",
                        className="mt-3"
                    ),
                        html.Div(id='row-graph')
                    ], width=12)
                ])
            ], width=12)
        ])
    ], fluid=True)

@app.callback(
    Output("download-dataset", "data"),
    Input("download-dataset-button", "n_clicks"),
    State("data-table", "data")
)
def download_current_dataset(n_clicks, data_table):
    ctx = dash.callback_context

    # Check if the button has been clicked
    if not n_clicks:
        return 
        
    # Get the current timestamp
    current_time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    
    name_of_file = f"{chosen_filename}_psnv_hunter_{current_time}.csv"
    
    return dcc.send_data_frame(
        uploaded_files[chosen_filename].to_csv, name_of_file
    )
    

@app.callback(
    Output("save-interesting-message", "children"),
    [
        Input("save-interesting-button", "n_clicks"),
    ],
    [
        State('data-table', 'data')
    ],
    prevent_initial_call=True
)
def display_saving_interesting_message(n_clicks, data_table):
    ctx = dash.callback_context

    # Check if the button has been clicked
    if not n_clicks:
        return "No file selected to save changes."

    uploaded_files[chosen_filename] = pd.DataFrame(data_table)
    
    
    
    # Get the current timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return f"{chosen_filename} was successfully saved at {current_time}"

@app.callback(
    [
        Output("offcanvas", "is_open"),  # Toggle off-canvas visibility
        Output("selected-file-display", "children"),  # Display the selected file
    ],
    [
        Input("open-offcanvas", "n_clicks"),  # Open off-canvas button
        Input("close-offcanvas-button", "n_clicks"),  # "OK" button to close off-canvas
        Input({'type': 'file-link', 'name': dash.ALL}, 'n_clicks'),  # File selection
    ],
    [
        State("offcanvas", "is_open"),  # Current state of the off-canvas
    ],
    prevent_initial_call=True
)
def toggle_offcanvas_and_display_file(open_click, close_click, file_clicks, is_open):
    ctx = dash.callback_context

    if not ctx.triggered:
        return is_open, dash.no_update

    triggered_id = ctx.triggered_id

    if triggered_id == "open-offcanvas":
        # Toggle off-canvas open
        return not is_open, dash.no_update

    if triggered_id == "close-offcanvas-button":
        # Close the off-canvas
        return False, dash.no_update

    if isinstance(triggered_id, dict) and triggered_id.get("type") == "file-link":
        # A file was selected
        selected_file_name = triggered_id.get("name")
        global chosen_filename
        chosen_filename = selected_file_name
        
        return is_open, f"Selected File: {selected_file_name}"

    return is_open, dash.no_update

# Update layout based on URL
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/viewer':
        return file_viewer_layout()
    return homepage_layout()

@app.callback(
    Output('upload-message', 'children'),
    [Input('file-upload', 'contents'),
     Input('load-example', 'n_clicks'),
     Input('data-table', 'data')],  # Triggered when DataTable is edited
    [State('file-upload', 'filename')],  # Capture original table data for comparison
    prevent_initial_call=True
)
def handle_file_upload_save_edits(contents, n_clicks, updated_data, filenames):
    global uploaded_files

    ctx = dash.callback_context
    if not ctx.triggered:
        return "No files uploaded yet."

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    

    # Handle example file loading
    if triggered_id == 'load-example':
        try:
            for example_file, path in EXAMPLE_FILES.items():
                df = pd.read_csv(path, delimiter="\t")

                # Validate required columns
                missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
                if missing_columns:
                    return f"Error: {example_file} is missing columns: {', '.join(missing_columns)}"

                uploaded_files[example_file] = df

            return "Successfully loaded example files: example_1.vcf and example_2.vcf."
        except Exception as e:
            return f"Error loading example files: {str(e)}"

    # Handle user-uploaded files
    if triggered_id == 'file-upload' and contents:
        if not isinstance(filenames, list):
            filenames = [filenames]
            contents = [contents]

        for content, filename in zip(contents, filenames):
            content_type, content_string = content.split(',')
            decoded = io.StringIO(io.BytesIO(base64.b64decode(content_string)).read().decode('utf-8'))
            try:
                df = pd.read_csv(decoded, delimiter="\t")

                # Validate required columns
                missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
                if missing_columns:
                    return f"Error: {filename} is missing columns: {', '.join(missing_columns)}"

                uploaded_files[filename] = df
            except Exception as e:
                return f"Error processing file {filename}: {str(e)}"

        return f"Successfully uploaded {len(filenames)} file(s)."

    return "No valid action performed."

# Callback to generate file list with shapes as Nav items on the file viewer page
@app.callback(
    Output('file-list', 'children'),
    Input('url', 'pathname')
)
def update_file_list(pathname):
    if pathname != '/viewer':
        return "No files uploaded yet."

    if not uploaded_files:
        return dbc.NavItem(dbc.NavLink("No files uploaded yet.", disabled=True))
    
    file_list = []
    for filename, df in uploaded_files.items():
        file_list.append(
            dbc.NavItem(
                dbc.NavLink(
                    [
                        html.Div(filename, style={"fontWeight": "bold"}),  # File name in bold
                        html.Div(f"{df.shape[0]} rows, {df.shape[1]} columns", style={"fontSize": "small", "color": "gray"})  # File shape
                    ],
                    href="#",
                    id={'type': 'file-link', 'name': filename}
                )
            )
        )
    file_list.append(
        dbc.NavItem(
            dbc.NavLink(
                [
                    html.Div("Interesting Mutations", style={"fontWeight": "bold"}),  # File name in bold
                ],
                href="#",
                id={'type': 'file-link', 'name': "interest-mutations-dataframe"}
            )
        )
    )

    return file_list


# Callback to display selected file in the DataTable and reset selected rows
@app.callback(
    [Output('data-table', 'data'),
     Output('data-table', 'columns'),
     Output('data-table', 'dropdown'),  # Add dropdown configuration
     Output('data-table', 'selected_rows'),  # Reset selected rows
     Output('error-message', 'children')],
    Input({'type': 'file-link', 'name': dash.ALL}, 'n_clicks'),
    prevent_initial_call=True
)
def display_selected_file(n_clicks):
    if not ctx.triggered:
        return [], [], [], [], ""

    triggered_id = ctx.triggered_id['name']
    if triggered_id in uploaded_files:
        df = uploaded_files[triggered_id]

        # Add the "interesting" column if it doesn't exist
        if "interesting" not in df.columns:
            df.insert(0, "interesting", " ")  # Add column at the first position

        # Prepare the DataTable columns
        columns = [
            {
                "name": col,
                "id": col,
                "presentation": "dropdown" if col == "interesting" else "input"
            }
            for col in df.columns
        ]

        # Define dropdown options for the "interesting" column
        dropdown_options = {
            "interesting": {
                "options": [
                    {"label": "Yes", "value": "yes"},
                    {"label": "Maybe", "value": "maybe"},
                    {"label": "No", "value": "no"},
                    {"label": " ", "value": " "},
                ]
            }
        }

        return (
            df.to_dict('records'),  # Data for the DataTable
            columns,  # Columns for the DataTable
            dropdown_options,  # Dropdown options
            [],  # Clear selected rows
            ""  # No error message
        )

    return [], [], {}, [], "Error: File not found."

# Callback to update the graph based on the selected row and main tab
@app.callback(
    Output('row-graph', 'children'),
    [Input('data-table', 'selected_rows'),
     Input('graph-tabs', 'active_tab')],
    [State('data-table', 'data')]
)
def display_graph(selected_rows, active_tab, table_data):
    if not selected_rows or not table_data:
        # Display a default figure when no row is selected
        return [dcc.Graph(figure=px.scatter(title="Select a row to display a graph"))]

    # Get the selected row index
    selected_index = selected_rows[0]
    row = table_data[selected_index]
    
    row = row if type(row) == pd.Series else pd.Series(row)
    
    if active_tab == "tab-patient":
        return [_get_information_page(row)]

    elif active_tab == 'tab-gene':
        return [html.Div(
            children = [
                # 1. Plot
                dcc.Graph(
                    figure = gene_expression_violin_plot(
                        row = row,
                        name_of_gene_column = NAME_OF_GENE_COLUMN,
                        name_of_chromosome_column = NAME_OF_CHROMOSOME_COLUMN,
                        name_of_snv_position_column = NAME_OF_POSITION_COLUMN,
                        name_of_reference_nucleotide_column = NAME_OF_REFERENCE_NUCLEOTIDE_COLUMN,
                        name_of_alternative_nucleotide_column = NAME_OF_ALTERNATIVE_NUCLEOTIDE_COLUMN,
                        name_of_cohort_column = NAME_OF_COHORT_COLUMN,
                        name_of_paths_with_recurrence_column = NAME_OF_PATHS_WITH_RECURRENCE_COLUMN,
                        name_of_tfbs_column = NAME_OF_TFBS_COLUMN,
                        name_of_expression_traces_column = NAME_OF_EXPRESSION_TRACES_COLUMN,
                        name_of_expression_column = NAME_OF_EXPRESSION_COLUMN,
                        name_of_normalized_expression_column = NAME_OF_NORMALIZED_EXPRESSION_COLUMN
                    )
                ),
                SEPARATION_LINE_FOR_TABS,
                
                # 2. Gene definition
                html.H1("NCBI Gene Summary", style=PLOTLY_BOLDED_STYLE),
                html.Div(
                    f"{_get_ncbi_definition_from_database(name_of_gene_or_tf = row[NAME_OF_GENE_COLUMN], descriptions_database = descriptions_database)}"
                )
                
            ]
        )]

    elif active_tab == 'tab-tfs':
        tfs_created = []
        if NAME_OF_COLUMN_WITH_LIST_OF_CREATED_TFS in list(row.index):
            if row[NAME_OF_COLUMN_WITH_LIST_OF_CREATED_TFS]:
                for tf in row[NAME_OF_COLUMN_WITH_LIST_OF_CREATED_TFS].split(","):
                    tfs_created.append(
                        dbc.Tab(
                            label = tf,
                            tab_id = tf,
                            label_style = {"color": "green"}
                        )
                    )
                
        tfs_destroyed = []
        if NAME_OF_COLUMN_WITH_LIST_OF_DESTROYED_TFS in list(row.index):
            if row[NAME_OF_COLUMN_WITH_LIST_OF_DESTROYED_TFS]:
                for tf in row[NAME_OF_COLUMN_WITH_LIST_OF_DESTROYED_TFS].split(","):
                    tfs_destroyed.append(
                        dbc.Tab(
                            label = tf,
                            tab_id = tf,
                            label_style = {"color": "red"}
                        )
                    )
        
        created_and_destroyed_tf_tabs = dbc.Tabs(tfs_created + tfs_destroyed, id="subtab-tfs") if len(tfs_created + tfs_destroyed) > 0 \
            else dbc.Tabs(
                [
                    dbc.Tab(
                        label="No Created or Destroyed Transcription Factors", disabled=True
                    )
                ],
                id="tf-tabs",
            )
        

        return [
            dbc.Row(
                created_and_destroyed_tf_tabs
            ),
            html.Div(id="tf-plot-container")  # Placeholder for TF-specific plot
        ]
        
    elif active_tab == 'tab-igv':
        chromosome = str(row[NAME_OF_CHROMOSOME_COLUMN])
        pos = int(row[NAME_OF_POSITION_COLUMN])

        return [dashbio.Igv(
            id="default-igv",
            minimumBases=1000,
            genome="hg19",
            locus=f"chr{chromosome}:{pos-3000}-{pos+3000}",  # Focus on a 6kb region around the position
            tracks=[
                {
                    "name": "NCBI Reference",
                    "format": "refgene",
                    "url": "https://s3.amazonaws.com/igv.org.genomes/hg19/ncbiRefSeq.sorted.txt.gz",
                    "indexURL": "https://s3.amazonaws.com/igv.org.genomes/hg19/ncbiRefSeq.sorted.txt.gz.tbi",
                    "type": "annotation",
                    "color": "rgb(176,141,87)",
                    "order": 1000000,
                    "infoURL": "https://www.ncbi.nlm.nih.gov/gene/?term=$$",
                    "height": 100,
                },
                {
                    "name": 'ChromHMM',
                    "url": 'https://raw.githubusercontent.com/nicholas-abad/REMIND-Cancer/refs/heads/main/examples/data/annotations/chromhmm.bed',
                    "indexed": "false",
                    "color": "rgba(139, 0, 0, 1)"
                },
                
                
            ],
            style={"width": "100%", "height": "500px"},  # Adjust height
        )]
    
    elif active_tab == 'tab-dp':
        gene = row[NAME_OF_GENE_COLUMN]
        pos = row[NAME_OF_POSITION_COLUMN]
        ref = row[NAME_OF_REFERENCE_NUCLEOTIDE_COLUMN]
        alt = row[NAME_OF_ALTERNATIVE_NUCLEOTIDE_COLUMN]
        chromosome = str(row[NAME_OF_CHROMOSOME_COLUMN])
        if not chromosome.startswith("chr"):
            chromosome = f"chr{chromosome}"
        
        path_to_potential_deep_pileup_folder = os.path.join(
            PATH_TO_DEEP_PILEUP_REPOSITORY, str(gene), f"{chromosome}:{pos}"
        )
        if os.path.exists(path_to_potential_deep_pileup_folder):
            path_to_overview_file = glob.glob(
                os.path.join(path_to_potential_deep_pileup_folder, "Overview.tsv")
            )[0]
            plot_one = deeppileup.af_greater_than_25_scatterplot(
                path_to_overview_file, True
            )
            plot_two = (
                deeppileup.at_least_two_variant_alleles_scatterplot(
                    path_to_overview_file, True,
                    ref=ref, alt=alt
                )
            )

            plot_one_a = deeppileup.af_greater_than_25_scatterplot(
                path_to_overview_file, False
            )
            plot_two_a = (
                deeppileup.at_least_two_variant_alleles_scatterplot(
                    path_to_overview_file, False,
                    ref=ref, alt=alt
                )
            )

            return [
                dcc.Graph(figure=plot_one),
                dcc.Graph(figure=plot_two),
                dcc.Graph(figure=plot_one_a),
                dcc.Graph(figure=plot_two_a),
                html.Br(),
                html.Div(
                    children = [
                        html.Div("Original publication of Deep Pileup: "),
                        html.Div('[1] Rheinbay, Esther, et al. "Analyses of non-coding somatic drivers in 2,658 cancer whole genomes." Nature 578.7793 (2020): 102-111."'),
                        html.Br(),
                    ],
                    style={"display": "inline-block"}
                ),
            ]

        return [html.Div("No Deep Pileup Graphs found")]
        
    elif active_tab == 'tab-gtp':
        gene = row[NAME_OF_GENE_COLUMN]
        chromosome = str(row[NAME_OF_CHROMOSOME_COLUMN])
        chromosome = f"chr{chromosome}" if not chromosome.startswith("chr") else chromosome

        path_to_potential_tornado_plot_folder = os.path.join(
            PATH_TO_GENOME_TORNADO_PLOTS_REPOSITORY, chromosome
        )
        
        if os.path.exists(path_to_potential_tornado_plot_folder):
            try:
                path_to_zoomed = glob.glob(
                    os.path.join(
                        path_to_potential_tornado_plot_folder, f"{chromosome}_{gene}_zoomed.png"
                    )
                )[0]
                path_to_not_zoomed = glob.glob(
                    os.path.join(
                        path_to_potential_tornado_plot_folder,
                        f"{chromosome}_{gene}_not_zoomed.png",
                    )
                )[0]

                if os.path.exists(path_to_zoomed) and os.path.exists(
                    path_to_not_zoomed
                ):
                    zoomed_encoded = base64.b64encode(
                        open(path_to_zoomed, "rb").read()
                    )
                    not_zoomed_encoded = base64.b64encode(
                        open(path_to_not_zoomed, "rb").read()
                    )
                    return [
                        html.Img(
                            src="data:image/png;base64,{}".format(
                                zoomed_encoded.decode()
                            ),
                            style={"display": "inline-block", "width": "49%"},
                        ),
                        html.Img(
                            src="data:image/png;base64,{}".format(
                                not_zoomed_encoded.decode()
                            ),
                            style={"display": "inline-block", "width": "49%"},
                        ),
                        html.Br(),
                        html.Div(
                            children = [
                                html.Div("Original publication of Genome Tornado Plots: "),
                                dcc.Link('[2] Hong, Chen, Robin Thiele, and Lars Feuerbach. "GenomeTornadoPlot: a novel R package for CNV visualization and focality analysis." Bioinformatics 38.7 (2022): 2036-2038.', href="https://github.com/chenhong-dkfz/GenomeTornadoPlot"),
                                html.Br(),
                            ],
                            style={"display": "inline-block"}
                        ),
                    ]
            except:
                [html.Div("No Tornado Plots of this gene")]

        return [html.Div("No Tornado Plots of this gene")]
        
    elif active_tab == 'tab-notes':
        return [html.Div(
            children=[
                dbc.Textarea(
                    id="free-text", 
                    placeholder="Type your notes here...", 
                    style={"width": "100%", "height": "150px", "marginBottom": "15px"}
                ),
                dbc.Button(
                    "Save Comment",
                    id="free-text-preview-button",
                    n_clicks=0,
                    color="primary",
                ),
                html.Br(),
                SEPARATION_LINE_FOR_TABS,
                html.H1("Previously Submitted Notes", style=PLOTLY_BOLDED_STYLE),
                html.Div(id="notes-display", style={"marginTop": "20px"}),
                html.Br(),
                html.Br(),
                html.Br(),
            ]
        )]
    
    return [dcc.Graph(figure=px.scatter(title="Invalid tab selected"))]

@app.callback(
    Output("tf-plot-container", "children"),
    [Input("subtab-tfs", "active_tab")],
    [State("data-table", "selected_rows"),
     State("data-table", "data")]
)
def update_tf_plot(active_tf, selected_rows, table_data):
    selected_index = selected_rows[0]
    row = table_data[selected_index]
    row = row if type(row) == pd.Series else pd.Series(row)

    # Get the binding affinity / created or destroyed TFBS.
    for transcription_factor_entry in row[NAME_OF_TFBS_COLUMN].split(";"):
        tf_name, binding_affinity = transcription_factor_entry.split(",")[:2]
        if tf_name == active_tf:
            break
    if float(binding_affinity) >= TFBS_BINDING_AFFINITY_CREATION_THRESHOLD:
        created_or_destroyed = "created"
    elif float(binding_affinity) <= TFBS_BINDING_AFFINITY_DESTRUCTION_THRESHOLD:
        created_or_destroyed = "destroyed"
    else:
        created_or_destroyed = "<unknown>"
    
    # Graphs.
    if not active_tf or not selected_rows or not table_data:
        return dcc.Graph(figure=px.scatter(title="Select a transcription factor to display its graph"))

    fig = tf_expression_violin_plot(
        row = row,
        chosen_tf_name = active_tf,
        name_of_expression_traces_column = NAME_OF_EXPRESSION_TRACES_COLUMN,
        name_of_cohort_column = NAME_OF_COHORT_COLUMN,
        name_of_tfbs_column = NAME_OF_TFBS_COLUMN,
        name_of_pid_column = NAME_OF_PID_COLUMN,
    )
    
    # Logo plots.
    logo_plots = dbc.Row(
        [
            html.Br(),
            html.Br(),
            dbc.Col(
                html.H3("Transcription Factor Logo Plot Alignment"),
                width={"size": 6, "offset": 3},
            ),
            dbc.Col(
                [
                    dbc.Carousel(
                        controls=True,
                        variant="dark",
                        id="chosen-tf-carousel",
                        items=[],
                    ),
                ],
                width=6,
            ),
            dbc.Col(
                [
                    html.Br(),
                    html.Div(id="display-mutation"),
                    dcc.RangeSlider(
                        0,
                        20,
                        5,
                        value=[10],
                        id="display-original-sequence-slider",
                    ),
                    html.Br(),
                    html.Div(id="display-original-sequence", style={"text-align": "center"}),
                ],
                style={"text-align": "center"},
            ),
        ],
    )
    
    return [
        dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Br(),
                            html.H4(
                                f"The {active_tf} TFBS is predicted to be {created_or_destroyed}.",
                                style = {
                                    "color": "black",
                                    "fontWeight": "bold",
                                    "textAlign": "center"
                                }
                            ),
                            html.Div(f"{_get_ncbi_definition_from_database(name_of_gene_or_tf=active_tf, descriptions_database=descriptions_database)}"),
                        ],
                        width=4,
                    ),
                    dbc.Col(
                        [
                            dcc.Graph(figure=fig),
                        ],
                        width=8,
                    ),
                ]
        ),
        SEPARATION_LINE_FOR_TABS,
        logo_plots        
    ]
    
@app.callback(
    Output("display-original-sequence", "children"),
    [
        Input("display-original-sequence-slider", "value"),
        Input("display-original-sequence-slider", "marks"),
        Input("subtab-tfs", "active_tab"),
    ],
    [
        State("data-table", "selected_rows"),
        State("data-table", "data")
    ]
)
def display_original_sequence(values, marks, active_tab, selected_rows, table_data):
    if not selected_rows or not table_data:
        return no_update, no_update, no_update, no_update
    
    row = table_data[selected_rows[0]]
    if type(row) != pd.Series:
        row = pd.Series(row)
        
    sequence_context = row[NAME_OF_SEQUENCE_CONTEXT_COLUMN]
    
    index_of_mutation = sequence_context.index(",")

    starting_value = values[0] - 1
    ending_value = values[-1]

    color_scheme = {
        "C": "#255c99",
        "T": "#d62839",
        "G": "#f7b32b",
        "A": "#58b67f",
        ",": "#000000",
    }

    sequence = "".join([marks[letter]["label"] for letter in marks])
    output = []
    for idx, letter in enumerate(sequence[starting_value:ending_value]):
        if idx != index_of_mutation - starting_value:
            output.append(
                html.H1(
                    f"{letter}",
                    style={
                        "display": "inline-block",
                        "color": f"{color_scheme[letter]}",
                        "width": "30px",
                        "text-align": "center",
                    },
                )
            )
        else:
            output.append(
                html.Div(
                    [
                        html.H1(
                            f"{letter}",
                            style={
                                "display": "inline-block",
                                "color": f"{color_scheme[letter]}",
                                "border-width": "3px",
                                "border-style": "solid",
                                "border-color": "black",
                            },
                        )
                    ],
                    style={
                        "text-align": "center",
                        "display": "inline-block",
                        "width": "30px",
                    },
                )
            )

    return output
    
@app.callback(
    [
        Output("display-original-sequence-slider", "min"),
        Output("display-original-sequence-slider", "max"),
        Output("display-original-sequence-slider", "value"),
        Output("display-original-sequence-slider", "marks"),
    ],
    [
        Input("subtab-tfs", "active_tab")
    ],
    [
        State("data-table", "selected_rows"),
        State("data-table", "data")
    ]
)
def display_original_sequence_slider(active_tab, selected_rows, table_data):
    if not selected_rows or not table_data:
        return no_update, no_update, no_update, no_update
    
    row = table_data[selected_rows[0]]
    if type(row) != pd.Series:
        row = pd.Series(row)
        
    sequence_context = row[NAME_OF_SEQUENCE_CONTEXT_COLUMN]
    ref = row[NAME_OF_REFERENCE_NUCLEOTIDE_COLUMN]
    
    index_of_mutation = sequence_context.index(",")
    sequence_context = sequence_context.replace(",", ref)

    # Get the range slider.
    color_scheme = {
        "C": "#255c99",
        "T": "#d62839",
        "G": "#f7b32b",
        "A": "#58b67f",
        ",": "#000000",
    }

    marks_dictionary = {}

    for value in range(1, len(sequence_context) + 1):
        marks_dictionary[value] = {
            "label": str(sequence_context[value - 1]),
            "style": {
                "color": f"{color_scheme[str(sequence_context[value - 1])]}",
                "font-size": "100%",
            },
        }
        if value == index_of_mutation + 1:
            marks_dictionary[value]["style"]["border-width"] = "3px"
            marks_dictionary[value]["style"]["border-style"] = "solid"
            marks_dictionary[value]["style"]["border-color"] = "black"

    minimum = 1
    maximum = len(sequence_context)

    value = [1, int(maximum) + 1]
    
    return minimum, maximum, value, marks_dictionary
    
@app.callback(
    Output("display-actual-tf-sequence", "children"),
    [
        Input("display-actual-tf-sequence-slider", "value"),
        Input("display-actual-tf-sequence-slider", "marks"),
    ],
)
def display_original_sequence(values, marks):
    if marks and values:
        starting_value = values[0] - 1
        ending_value = values[-1]

        color_scheme = {
            "C": "#255c99",
            "T": "#d62839",
            "G": "#f7b32b",
            "A": "#58b67f",
            ",": "#000000",
        }

        sequence = "".join([marks[letter]["label"] for letter in marks])

        return [
            html.H1(
                f"{letter}",
                style={
                    "display": "inline-block",
                    "color": f"{color_scheme[letter]}",
                    "text-align": "center",
                    "width": "30px",
                },
            )
            for letter in sequence[starting_value:ending_value]
        ]
    else:
        return []


@app.callback(
    [Output('notes-store', 'data'),
     Output('notes-display', 'children')],
    [Input('free-text-preview-button', 'n_clicks'),
     Input({'type': 'delete-note', 'row_id': ALL, 'index': ALL}, 'n_clicks')],
    [State('free-text', 'value'),
     State('data-table', 'selected_rows'),
     State('data-table', 'data'),
     State('notes-store', 'data')],
    prevent_initial_call=True
)
def manage_notes(submit_click, delete_clicks, new_note, selected_rows, table_data, notes_store):
    ctx = dash.callback_context

    # Ensure the notes store exists
    if notes_store is None:
        notes_store = {}

    if not selected_rows or not table_data:
        return notes_store, html.Div("No row selected.", style={"color": "gray"})

    # Get the selected row identifier
    selected_row = table_data[selected_rows[0]]
    row_id = f"chr{selected_row[NAME_OF_CHROMOSOME_COLUMN]}_{selected_row[NAME_OF_POSITION_COLUMN]}_{selected_row['pid']}_{selected_rows}"

    # Handle note submission
    if ctx.triggered_id == 'free-text-preview-button' and new_note:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        note_entry = {"note": new_note, "timestamp": timestamp}

        if row_id in notes_store:
            notes_store[row_id].append(note_entry)
        else:
            notes_store[row_id] = [note_entry]
            
        updated_table_data = pd.DataFrame(table_data)
        updated_table_data.at[selected_rows[0], "notes"] = notes_store[row_id]
        
        uploaded_files[chosen_filename] = updated_table_data

    # Handle note deletion
    elif isinstance(ctx.triggered_id, dict) and ctx.triggered_id['type'] == 'delete-note':
        row_id = ctx.triggered_id['row_id']
        index_to_delete = ctx.triggered_id['index']

        if row_id in notes_store and index_to_delete < len(notes_store[row_id]):
            del notes_store[row_id][index_to_delete]
            
        updated_table_data = pd.DataFrame(table_data)
        updated_table_data.at[selected_rows[0], "notes"] = notes_store[row_id]
        
        uploaded_files[chosen_filename] = updated_table_data

    # Prepare notes display for the selected row
    row_notes = notes_store.get(row_id, [])
    notes_display = html.Div(
        [
            html.Div(
                [
                    dbc.Button(
                        "x",
                        id={'type': 'delete-note', 'row_id': row_id, 'index': i},
                        color="danger",
                        size="sm",
                        style={"marginRight": "10px", "float": "left"}  # Float left
                    ),
                    html.Span(
                        f"[{note['timestamp']}] {note['note']}",
                        style={"borderBottom": "1px solid #e9ecef", "padding": "5px", "display": "inline-block", "width": "85%"}
                    ),
                ],
                style={"marginBottom": "10px", "display": "flex", "alignItems": "center"}  # Align items horizontally
            )
            for i, note in enumerate(row_notes)
        ]
    )
    
    # Save the notes to the dataframe.
    # uploaded_files[filename]
    

    return notes_store, notes_display

@app.callback(
    Output("chosen-tf-carousel", "items"),
    [
        Input("subtab-tfs", "active_tab"),
    ],
    [
        State('data-table', 'selected_rows'),
        State('data-table', 'data'),
    ]
)
def display_carousel_for_chosen_tf(active_tf, selected_rows, table_data):
    if not selected_rows or not table_data:
        return []
    row = table_data[selected_rows[0]]
    if type(row) != pd.Series:
        row = pd.Series(row)
    
    transcription_factor_colname = [
        colname
        for colname in list(row.index)
        if NAME_OF_TFBS_COLUMN
        in colname
    ][0]
    transcription_factors = row[transcription_factor_colname]
    for transcription_factor in transcription_factors.split(";"):
        tf_name = transcription_factor.split(",")[0]
        tf_sequence_logo = transcription_factor.split(",")[-1]
        if tf_name == active_tf:
            reverse_complement_logo_seq = tf_sequence_logo.replace(
                ".png", ".rc.png"
            )
            carousel = [
                {
                    "key": "1",
                    "src": tf_sequence_logo,
                    "caption": "Original Logo Sequence",
                },
                {
                    "key": "2",
                    "src": reverse_complement_logo_seq,
                    "caption": "Reverse Complement",
                },
            ]
            return carousel
    return []

@app.callback(
    Output('uploaded-files-table', 'data'),
    [Input('file-upload', 'contents'),
     Input('load-example', 'n_clicks'),
     Input('uploaded-files-table', 'data')],
    [State('file-upload', 'filename')],
    prevent_initial_call=True
)
def update_uploaded_files(contents, n_clicks, current_data, filenames):
    global uploaded_files

    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Handle new file uploads
    if triggered_id == 'file-upload' and contents:
        if not isinstance(filenames, list):
            filenames = [filenames]
            contents = [contents]

        for content, filename in zip(contents, filenames):
            _, content_string = content.split(',')
            decoded = io.StringIO(io.BytesIO(base64.b64decode(content_string)).read().decode('utf-8'))
            try:
                df = pd.read_csv(decoded, delimiter="\t")
                if "notes" not in list(df.columns):
                    df["notes"] = ""
                    df["notes"] = df["notes"].astype("object")
                uploaded_files[filename] = df
            except Exception as e:
                return dash.no_update

    # Handle loading example files
    if triggered_id == 'load-example':
        for example_file, path in EXAMPLE_FILES.items():
            df = pd.read_csv(path, delimiter="\t")
            if "notes" not in list(df.columns):
                df["notes"] = ""
                df["notes"] = df["notes"].astype("object")
            uploaded_files[example_file] = df

    # Handle file deletion
    if triggered_id == 'uploaded-files-table':
        # Get the set of filenames currently displayed in the table
        displayed_filenames = {row['filename'] for row in current_data}
        # Remove any files not in the displayed filenames from uploaded_files
        uploaded_files = {k: v for k, v in uploaded_files.items() if k in displayed_filenames}

    # Generate updated table data
    table_data = [
        {
            "filename": filename,
            "rows": df.shape[0],
            "columns": df.shape[1],
        }
        for filename, df in uploaded_files.items()
    ]

    return table_data

@app.callback(
    Output("display-mutation", "children"),    
    [
        Input("subtab-tfs", "active_tab"),
    ],
    [
        State('data-table', 'selected_rows'),
        State('data-table', 'data'),
    ]
)
def display_mutation(active_tf, selected_rows, table_data):
    if not selected_rows or not table_data:
        return []
    
    row = table_data[selected_rows[0]]
    
    if type(row) != pd.Series:
        row = pd.Series(row)
    
    ref = row[NAME_OF_REFERENCE_NUCLEOTIDE_COLUMN]
    alt = row[NAME_OF_ALTERNATIVE_NUCLEOTIDE_COLUMN]

    revcomp_ref = _get_reverse_complement(ref)
    revcomp_alt = _get_reverse_complement(alt)

    created_or_destroyed = "<unknown>"

    if row[NAME_OF_TFBS_COLUMN] != ".":
        for entry in row[NAME_OF_TFBS_COLUMN].split(";"):
            tf_name = entry.split(",")[0]
            binding_affinity = float(entry.split(",")[1])
            if tf_name == active_tf:
                created_or_destroyed = (
                    "created" if binding_affinity >= TFBS_BINDING_AFFINITY_CREATION_THRESHOLD else "destroyed"
                )
                break

    return [
        html.H3(f"{tf_name} was predicted to be {created_or_destroyed}."),
        html.H1(
            f"Mutation: {ref} > {alt} / Rev Comp: {revcomp_ref} > {revcomp_alt}"
        ),
        html.Br(),
    ]

# Run the app
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8050, debug=True, dev_tools_ui=False)