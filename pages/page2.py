# Importing Libraries
import pdb

import pandas as pd
# pd.set_option("styler.format.thousands", ",")
import numpy as np
import warnings
import json, os
import geopandas as gpd
# import fiona
import plotly.graph_objects as go
from dash import dcc, dash_table, html, Input, Output, ctx, callback
import dash_bootstrap_components as dbc
from sqlalchemy import create_engine

# fiona.supported_drivers
warnings.filterwarnings("ignore")
current_dir = os.path.dirname(os.path.abspath(__file__))
# db_path = os.path.join(current_dir, '..\\..\\Inputs\\new_hart.db')
# pdb.set_trace()
engine_new = create_engine('sqlite:///sources//new_hart.db')
engine_old = create_engine('sqlite:///sources//old_hart.db')



table_4a = pd.read_sql_table('table_4a_new', engine_new.connect())
table_4b = pd.read_sql_table('table_4b_new', engine_new.connect())
table_5 = pd.read_sql_table('table_5_new', engine_new.connect())
table_6 = pd.read_sql_table('table_6_new', engine_new.connect())
table_7_2006 = pd.read_sql_table('table_7_2006_new', engine_new.connect())
table_7_2021 = pd.read_sql_table('table_7_2021_new', engine_new.connect())
table_8 = pd.read_sql_table('table_8_new', engine_new.connect())
table_9 = pd.read_sql_table('table_9_new', engine_new.connect())
table_10 = pd.read_sql_table('table_10_new', engine_new.connect())
table_11 = pd.read_sql_table('table_11_new', engine_new.connect())
table_12 = pd.read_sql_table('table_12_new', engine_new.connect())
table_13 = pd.read_sql_table('table_13_new', engine_new.connect())
table_14 = pd.read_sql_table('table_14_new', engine_new.connect())
table_14 = table_14.rename(columns={'Remove this column name': ''})
table_15 = pd.read_sql_table('table_15_new', engine_new.connect())
table_16 = pd.read_sql_table('table_16_new', engine_new.connect())
# Importing Geo Code Information
# pdb.set_trace()
mapped_geo_code = pd.read_sql_table('geocodes_integrated', engine_old.connect())


# Configuration for plot icons

config = {'displayModeBar': True, 'displaylogo': False,
          'modeBarButtonsToRemove': ['zoom', 'lasso2d', 'pan', 'select', 'autoScale', 'resetScale', 'resetViewMapbox']}

# Colors for map
colors = ['#D7F3FD', '#88D9FA', '#39C0F7', '#099DD7', '#044762']
hh_colors = ['#D8EBD4', '#93CD8A', '#3DB54A', '#297A32', '#143D19']
hh_type_color = ['#002145', '#3EB549', '#39C0F7']
columns_color_fill = ['#F3F4F5', '#EBF9FE', '#F0FAF1']
modebar_color = '#099DD7'
modebar_activecolor = '#044762'

# Map color opacity

opacity_value = 0.2
def default_data(df):
    filtered_df = df.query('GEOUID_ == 5901043')
    required_df = filtered_df.iloc[:, 3:]
    required_df.columns = pd.MultiIndex.from_tuples(
        [tuple(col.split('_')) for col in required_df.columns])
    return required_df

table4a_for_dash = table_4a[table_4a['GEOUID'] == '5901043'].iloc[:, 3:]
table4b_for_dash = default_data(table_4b)
table5_for_dash = table_5[table_5['GEOUID'] == '5901043'].iloc[:, 3:]
table6_for_dash = default_data(table_6)
table7_2006_for_dash = default_data(table_7_2006)
table7_2021_for_dash = default_data(table_7_2021)
table8_for_dash = default_data(table_8)
table9_for_dash = default_data(table_9)
table10_for_dash = default_data(table_10)
table11_for_dash = default_data(table_11)
table12_for_dash = table_12[table_12['GEOUID'] == '5901043'].iloc[:, 3:]
# print(table_13.columns)
table13_for_dash = default_data(table_13)
table14_for_dash = table_14[table_14['GEOUID'] == '5901043'].iloc[:, 3:]
table15_for_dash = table_15[table_15['GEOUID'] == '5901043'].iloc[:, 3:]
table16_for_dash = table_16[table_16['GEOUID'] == '5901043'].iloc[:, 3:]

# Default location in the map

default_value = 'Vancouver CY (CSD, BC)'


# Setting orders of areas in dropdown


# Setting layout for dashboard


layout = html.Div(children=[

    # Store Area/Comparison Area/Clicked area scale info in local storage

    dcc.Store(id='area-scale-store', storage_type='local'),
    dcc.Store(id='main-area', storage_type='local'),
    dcc.Store(id='comparison-area', storage_type='local'),

    # Add the Export to PDF button
    dbc.Button("Export to PDF", id="export-button", className="mb-3", color="primary"),

    html.Div(id='dummy-output', style={'display': 'none'}),

    html.Div(id='page-content-to-print',
            children=[

                # Table 1a
                html.Div([
                    # Title
                    html.H3(children=html.Strong('Housing units and extreme core housing need, Table 1.a'),
                            id='visualization3'),
                    # Description
                    html.Div([
                        html.H6(
                            'No text for now...')
                    ], className='muni-reg-text-lgeo'),

                    # Table

                    html.Div([
                        dash_table.DataTable(
                            id='table_4a',
                            columns=[{"name": col, "id": col, "deletable": False, "selectable": False} for col in table4a_for_dash.columns],
                            data=table4a_for_dash.to_dict('records'),
                            editable=True,
                            sort_action="native",
                            sort_mode="multi",
                            column_selectable=False,
                            row_selectable=False,
                            row_deletable=False,
                            selected_columns=[],
                            selected_rows=[],
                            page_action="native",
                            page_current=0,
                            page_size=10,
                            merge_duplicate_headers=True,
                            # render_cell=render_cell,
                            export_format="xlsx",
                            style_table={
                                          "overflowY": "auto"

                                          },
                            style_data={'whiteSpace': 'normal', 'overflow': 'hidden',
                                        'textOverflow': 'ellipsis'},
                            style_cell={'font-family': 'Bahnschrift',
                                        'height': 'auto',
                                        'whiteSpace': 'normal',
                                        'overflow': 'hidden',
                                        'textOverflow': 'ellipsis'
                                        },
                            style_header={'textAlign': 'center', 'fontWeight': 'bold',

                                          }
                        ),
                        html.Div(id='table_4a-container')
                    ], className='pg2-table-lgeo'

                    ),

                ], className='pg2-table-plot-box-lgeo'),

                # Table 1b
                html.Div([
                    # Title
                    html.H3(children=html.Strong('Housing units and extreme core housing need, Table 1.b'),
                            id='visualization3'),
                    # Description
                    html.Div([
                        html.H6(
                            'No text for now...')
                    ], className='muni-reg-text-lgeo'),

                    # Table

                    html.Div([
                        dash_table.DataTable(
                            id='table_4b',
                            columns=[{"name": [col1, col2], "id": f"{col1}_{col2}", "deletable": False, "selectable": False} for col1, col2 in table4b_for_dash.columns],
                            data=[
                                {
                                    **{f"{x1}_{x2}": y for (x1, x2), y in data},
                                }
                                for (n, data) in [
                                    *enumerate([list(x.items()) for x in table4b_for_dash.T.to_dict().values()])
                                ]
                            ],
                            editable=True,
                            sort_action="native",
                            sort_mode="multi",
                            column_selectable=False,
                            row_selectable=False,
                            row_deletable=False,
                            selected_columns=[],
                            selected_rows=[],
                            page_action="native",
                            page_current=0,
                            page_size=10,
                            merge_duplicate_headers=True,
                            # render_cell=render_cell,
                            export_format="xlsx",
                            style_table={
                                "overflowY": "auto"

                            },
                            style_data={'whiteSpace': 'normal', 'overflow': 'hidden',
                                        'textOverflow': 'ellipsis'},
                            style_cell={'font-family': 'Bahnschrift',
                                        'height': 'auto',
                                        'whiteSpace': 'normal',
                                        'overflow': 'hidden',
                                        'textOverflow': 'ellipsis'
                                        },
                            style_header={'textAlign': 'center', 'fontWeight': 'bold',

                                          }
                        ),
                        html.Div(id='table_4b-container')
                    ], className='pg2-table-lgeo'

                    ),

                ], className='pg2-table-plot-box-lgeo'),

                # Table 2
                html.Div([
                    # Title
                    html.H3(children=html.Strong('Housing units and extreme core housing need, Table 2'),
                            id='visualization3'),
                    # Description
                    html.Div([
                        html.H6(
                            'No text for now...')
                    ], className='muni-reg-text-lgeo'),


                    html.Div([
                        dash_table.DataTable(
                            id='table5',
                            columns=[{"name": col, "id": col, "deletable": False, "selectable": False}
                                     for col in table5_for_dash.columns],
                            data=table5_for_dash.to_dict('records'),
                            editable=True,
                            sort_action="native",
                            sort_mode="multi",
                            column_selectable=False,
                            row_selectable=False,
                            row_deletable=False,
                            selected_columns=[],
                            selected_rows=[],
                            page_action="native",
                            page_current=0,
                            page_size=10,
                            merge_duplicate_headers=True,
                            # render_cell=render_cell,
                            export_format="xlsx",
                            style_table={
                                "overflowY": "auto"

                            },
                            style_data={'whiteSpace': 'normal', 'overflow': 'hidden',
                                        'textOverflow': 'ellipsis'},
                            style_cell={'font-family': 'Bahnschrift',
                                        'height': 'auto',
                                        'whiteSpace': 'normal',
                                        'overflow': 'hidden',
                                        'textOverflow': 'ellipsis'
                                        },
                            style_header={'textAlign': 'center', 'fontWeight': 'bold',

                                          }
                        ),
                        html.Div(id='table8-container')
                    ], className='pg2-table-lgeo'

                    ),

                ], className='pg2-table-plot-box-lgeo'),

                # Table 3
                html.Div([
                    # Title
                    html.H3(children=html.Strong('Housing units and homelessness, Table 3'),
                            id='visualization3'),
                    # Description
                    html.Div([
                        html.H6(
                            'No text for now...')
                    ], className='muni-reg-text-lgeo'),

                    # Table

                    html.Div([
                        dash_table.DataTable(
                            id='table_6',
                            columns=[
                                {"name": [col1, col2], "id": f"{col1}_{col2}", "deletable": False, "selectable": False}
                                for col1, col2 in table6_for_dash.columns],
                            data=[
                                {
                                    **{f"{x1}_{x2}": y for (x1, x2), y in data},
                                }
                                for (n, data) in [
                                    *enumerate([list(x.items()) for x in table6_for_dash.T.to_dict().values()])
                                ]
                            ],
                            editable=True,
                            sort_action="native",
                            sort_mode="multi",
                            column_selectable=False,
                            row_selectable=False,
                            row_deletable=False,
                            selected_columns=[],
                            selected_rows=[],
                            page_action="native",
                            page_current=0,
                            page_size=10,
                            merge_duplicate_headers=True,
                            # render_cell=render_cell,
                            export_format="xlsx",
                            style_table={
                                          "overflowY": "auto"

                                          },
                            style_data={'whiteSpace': 'normal', 'overflow': 'hidden',
                                        'textOverflow': 'ellipsis'},
                            style_cell={'font-family': 'Bahnschrift',
                                        'height': 'auto',
                                        'whiteSpace': 'normal',
                                        'overflow': 'hidden',
                                        'textOverflow': 'ellipsis'
                                        },
                            style_header={'textAlign': 'center', 'fontWeight': 'bold',

                                          }
                        ),
                        html.Div(id='table_6-container')
                    ], className='pg2-table-lgeo'

                    ),

                ], className='pg2-table-plot-box-lgeo'),

                # Table 4a
                html.Div([
                    # Title
                    html.H3(children=html.Strong('Housing units and suppressed household formation, Table 4.a'),
                            id='visualization3'),
                    # Description
                    html.Div([
                        html.H6(
                            'No text for now...')
                    ], className='muni-reg-text-lgeo'),

                    # Table

                    html.Div([
                        dash_table.DataTable(
                            id='table7_2006',
                            columns=[{"name": [col1, col2], "id": f"{col1}_{col2}", "deletable": False, "selectable": False} for col1, col2 in table7_2006_for_dash.columns],
                            data=[
                                {
                                    **{f"{x1}_{x2}": y for (x1, x2), y in data},
                                }
                                for (n, data) in [
                                    *enumerate([list(x.items()) for x in table7_2006_for_dash.T.to_dict().values()])
                                ]
                            ],
                            editable=True,
                            sort_action="native",
                            sort_mode="multi",
                            column_selectable=False,
                            row_selectable=False,
                            row_deletable=False,
                            selected_columns=[],
                            selected_rows=[],
                            page_action="native",
                            page_current=0,
                            page_size=10,
                            merge_duplicate_headers=True,
                            # render_cell=render_cell,
                            export_format="xlsx",
                            style_table={
                                          "overflowY": "auto"

                                          },
                            style_data={'whiteSpace': 'normal', 'overflow': 'hidden',
                                        'textOverflow': 'ellipsis'},
                            style_cell={'font-family': 'Bahnschrift',
                                        'height': 'auto',
                                        'whiteSpace': 'normal',
                                        'overflow': 'hidden',
                                        'textOverflow': 'ellipsis'
                                        },
                            style_header={'textAlign': 'center', 'fontWeight': 'bold',

                                          }
                        ),
                        html.Div(id='table7_2006-container')
                    ], className='pg2-table-lgeo'

                    ),

                ], className='pg2-table-plot-box-lgeo'),

                # Table 4b
                html.Div([
                    # Title
                    html.H3(children=html.Strong('Housing units and suppressed household formation, Table 4.b'),
                            id='visualization3'),
                    # Description
                    html.Div([
                        html.H6(
                            'No text for now...')
                    ], className='muni-reg-text-lgeo'),

                    # Table

                    html.Div([
                        dash_table.DataTable(
                            id='table7_2021',
                            columns=[
                                {"name": [col1, col2], "id": f"{col1}_{col2}", "deletable": False, "selectable": False}
                                for col1, col2 in table7_2021_for_dash.columns],
                            data=[
                                {
                                    **{f"{x1}_{x2}": y for (x1, x2), y in data},
                                }
                                for (n, data) in [
                                    *enumerate([list(x.items()) for x in table7_2021_for_dash.T.to_dict().values()])
                                ]
                            ],
                            editable=True,
                            sort_action="native",
                            sort_mode="multi",
                            column_selectable=False,
                            row_selectable=False,
                            row_deletable=False,
                            selected_columns=[],
                            selected_rows=[],
                            page_action="native",
                            page_current=0,
                            page_size=10,
                            merge_duplicate_headers=True,
                            # render_cell=render_cell,
                            export_format="xlsx",
                            style_table={
                                "overflowY": "auto"

                            },
                            style_data={'whiteSpace': 'normal', 'overflow': 'hidden',
                                        'textOverflow': 'ellipsis'},
                            style_cell={'font-family': 'Bahnschrift',
                                        'height': 'auto',
                                        'whiteSpace': 'normal',
                                        'overflow': 'hidden',
                                        'textOverflow': 'ellipsis'
                                        },
                            style_header={'textAlign': 'center', 'fontWeight': 'bold',

                                          }
                        ),
                        html.Div(id='table7_2021-container')
                    ], className='pg2-table-lgeo'

                    ),

                ], className='pg2-table-plot-box-lgeo'),

                # Table 5
                html.Div([
                    # Title
                    html.H3(children=html.Strong('Housing units and suppressed household formation, Table 5'),
                            id='visualization3'),
                    # Description
                    html.Div([
                        html.H6(
                            'No text for now...')
                    ], className='muni-reg-text-lgeo'),


                    html.Div([
                        dash_table.DataTable(
                            id='table8',
                            columns=[{"name": [col1, col2], "id": f"{col1}_{col2}", "deletable": False, "selectable": False}
                                     for col1, col2 in table8_for_dash.columns],
                            data=[
                                {
                                    **{f"{x1}_{x2}": y for (x1, x2), y in data},
                                }
                                for (n, data) in [
                                    *enumerate([list(x.items()) for x in table8_for_dash.T.to_dict().values()])
                                ]
                            ],
                            editable=True,
                            sort_action="native",
                            sort_mode="multi",
                            column_selectable=False,
                            row_selectable=False,
                            row_deletable=False,
                            selected_columns=[],
                            selected_rows=[],
                            page_action="native",
                            page_current=0,
                            page_size=20,
                            merge_duplicate_headers=True,
                            # render_cell=render_cell,
                            export_format="xlsx",
                            style_table={
                                "overflowY": "auto"

                            },
                            style_data={'whiteSpace': 'normal', 'overflow': 'hidden',
                                        'textOverflow': 'ellipsis'},
                            style_cell={'font-family': 'Bahnschrift',
                                        'height': 'auto',
                                        'whiteSpace': 'normal',
                                        'overflow': 'hidden',
                                        'textOverflow': 'ellipsis'
                                        },
                            style_header={'textAlign': 'center', 'fontWeight': 'bold',

                                          }
                        ),
                        html.Div(id='table8-container')
                    ], className='pg2-table-lgeo'

                    ),

                ], className='pg2-table-plot-box-lgeo'),

                # Table 6
                html.Div([
                    # Title
                    html.H3(children=html.Strong('Housing units and suppressed household formation, Table 6'),
                            id='visualization3'),
                    # Description
                    html.Div([
                        html.H6(
                            'No text for now...')
                    ], className='muni-reg-text-lgeo'),


                    html.Div([
                        dash_table.DataTable(
                            id='table9',
                            columns=[{"name": [col1, col2], "id": f"{col1}_{col2}", "deletable": False, "selectable": False}
                                     for col1, col2 in table9_for_dash.columns],
                            data=[
                                {
                                    **{f"{x1}_{x2}": y for (x1, x2), y in data},
                                }
                                for (n, data) in [
                                    *enumerate([list(x.items()) for x in table9_for_dash.T.to_dict().values()])
                                ]
                            ],
                            editable=True,
                            sort_action="native",
                            sort_mode="multi",
                            column_selectable=False,
                            row_selectable=False,
                            row_deletable=False,
                            selected_columns=[],
                            selected_rows=[],
                            page_action="native",
                            page_current=0,
                            page_size=10,
                            merge_duplicate_headers=True,
                            # render_cell=render_cell,
                            export_format="xlsx",
                            style_table={
                                "overflowY": "auto"

                            },
                            style_data={'whiteSpace': 'normal', 'overflow': 'hidden',
                                        'textOverflow': 'ellipsis'},
                            style_cell={'font-family': 'Bahnschrift',
                                        'height': 'auto',
                                        'whiteSpace': 'normal',
                                        'overflow': 'hidden',
                                        'textOverflow': 'ellipsis'
                                        },
                            style_header={'textAlign': 'center', 'fontWeight': 'bold',

                                          }
                        ),
                        html.Div(id='table9-container')
                    ], className='pg2-table-lgeo'

                    ),

                ], className='pg2-table-plot-box-lgeo'),

                # Table 7
                html.Div([
                    # Title
                    html.H3(children=html.Strong('Housing units and suppressed household formation, Table 7'),
                            id='visualization3'),
                    # Description
                    html.Div([
                        html.H6(
                            'No text for now...')
                    ], className='muni-reg-text-lgeo'),


                    html.Div([
                        dash_table.DataTable(
                            id='table10',
                            columns=[{"name": [col1, col2], "id": f"{col1}_{col2}", "deletable": False, "selectable": False}
                                     for col1, col2 in table10_for_dash.columns],
                            data=[
                                {
                                    **{f"{x1}_{x2}": y for (x1, x2), y in data},
                                }
                                for (n, data) in [
                                    *enumerate([list(x.items()) for x in table10_for_dash.T.to_dict().values()])
                                ]
                            ],
                            editable=True,
                            sort_action="native",
                            sort_mode="multi",
                            column_selectable=False,
                            row_selectable=False,
                            row_deletable=False,
                            selected_columns=[],
                            selected_rows=[],
                            page_action="native",
                            page_current=0,
                            page_size=10,
                            merge_duplicate_headers=True,
                            # render_cell=render_cell,
                            export_format="xlsx",
                            style_table={
                                "overflowY": "auto"

                            },
                            style_data={'whiteSpace': 'normal', 'overflow': 'hidden',
                                        'textOverflow': 'ellipsis'},
                            style_cell={'font-family': 'Bahnschrift',
                                        'height': 'auto',
                                        'whiteSpace': 'normal',
                                        'overflow': 'hidden',
                                        'textOverflow': 'ellipsis'
                                        },
                            style_header={'textAlign': 'center', 'fontWeight': 'bold',

                                          }
                        ),
                        html.Div(id='table10-container')
                    ], className='pg2-table-lgeo'

                    ),

                ], className='pg2-table-plot-box-lgeo'),

                # Table 8
                html.Div([
                    # Title
                    html.H3(children=html.Strong('Housing units and suppressed household formation, Table 8'),
                            id='visualization3'),
                    # Description
                    html.Div([
                        html.H6(
                            'No text for now...')
                    ], className='muni-reg-text-lgeo'),


                    html.Div([
                        dash_table.DataTable(
                            id='table11',
                            columns=[{"name": [col1, col2], "id": f"{col1}_{col2}", "deletable": False, "selectable": False}
                                     for col1, col2 in table11_for_dash.columns],
                            data=[
                                {
                                    **{f"{x1}_{x2}": y for (x1, x2), y in data},
                                }
                                for (n, data) in [
                                    *enumerate([list(x.items()) for x in table11_for_dash.T.to_dict().values()])
                                ]
                            ],
                            editable=True,
                            sort_action="native",
                            sort_mode="multi",
                            column_selectable=False,
                            row_selectable=False,
                            row_deletable=False,
                            selected_columns=[],
                            selected_rows=[],
                            page_action="native",
                            page_current=0,
                            page_size=10,
                            merge_duplicate_headers=True,
                            # render_cell=render_cell,
                            export_format="xlsx",
                            style_table={
                                "overflowY": "auto"

                            },
                            style_data={'whiteSpace': 'normal', 'overflow': 'hidden',
                                        'textOverflow': 'ellipsis'},
                            style_cell={'font-family': 'Bahnschrift',
                                        'height': 'auto',
                                        'whiteSpace': 'normal',
                                        'overflow': 'hidden',
                                        'textOverflow': 'ellipsis'
                                        },
                            style_header={'textAlign': 'center', 'fontWeight': 'bold',

                                          }
                        ),
                        html.Div(id='table11-container')
                    ], className='pg2-table-lgeo'

                    ),

                ], className='pg2-table-plot-box-lgeo'),

                # Table 9
                html.Div([
                    # Title
                    html.H3(children=html.Strong('Housing units and anticipated household growth, Table 9'),
                            id='visualization3'),
                    # Description
                    html.Div([
                        html.H6(
                            'No text for now...')
                    ], className='muni-reg-text-lgeo'),

                    # Table

                    html.Div([
                        dash_table.DataTable(
                            id='table_12',
                            columns=[{"name": col, "id": col, "deletable": False, "selectable": False} for col in table12_for_dash.columns],
                            data=table12_for_dash.to_dict('records'),
                            editable=True,
                            sort_action="native",
                            sort_mode="multi",
                            column_selectable=False,
                            row_selectable=False,
                            row_deletable=False,
                            selected_columns=[],
                            selected_rows=[],
                            page_action="native",
                            page_current=0,
                            page_size=10,
                            merge_duplicate_headers=True,
                            # render_cell=render_cell,
                            export_format="xlsx",
                            style_table={
                                          "overflowY": "auto"

                                          },
                            style_data={'whiteSpace': 'normal', 'overflow': 'hidden',
                                        'textOverflow': 'ellipsis'},
                            style_cell={'font-family': 'Bahnschrift',
                                        'height': 'auto',
                                        'whiteSpace': 'normal',
                                        'overflow': 'hidden',
                                        'textOverflow': 'ellipsis'
                                        },
                            style_header={'textAlign': 'center', 'fontWeight': 'bold',

                                          }
                        ),
                        html.Div(id='table_12-container')
                    ], className='pg2-table-lgeo'

                    ),

                ], className='pg2-table-plot-box-lgeo'),

                # Table 10
                html.Div([
                    # Title
                    html.H3(children=html.Strong('Housing units and anticipated household growth, Table 10'),
                            id='visualization3'),
                    # Description
                    html.Div([
                        html.H6(
                            'No text for now...')
                    ], className='muni-reg-text-lgeo'),


                    html.Div([
                        dash_table.DataTable(
                            id='table_13',
                            columns=[
                                {"name": [col1, col2], "id": f"{col1}_{col2}", "deletable": False, "selectable": False}
                                for col1, col2 in table13_for_dash.columns],
                            data=[
                                {
                                    **{f"{x1}_{x2}": y for (x1, x2), y in data},
                                }
                                for (n, data) in [
                                    *enumerate([list(x.items()) for x in table13_for_dash.T.to_dict().values()])
                                ]
                            ],
                            editable=True,
                            sort_action="native",
                            sort_mode="multi",
                            column_selectable=False,
                            row_selectable=False,
                            row_deletable=False,
                            selected_columns=[],
                            selected_rows=[],
                            page_action="native",
                            page_current=0,
                            page_size=10,
                            merge_duplicate_headers=True,
                            # render_cell=render_cell,
                            export_format="xlsx",
                            style_table={
                                "overflowY": "auto"

                            },
                            style_data={'whiteSpace': 'normal', 'overflow': 'hidden',
                                        'textOverflow': 'ellipsis'},
                            style_cell={'font-family': 'Bahnschrift',
                                        'height': 'auto',
                                        'whiteSpace': 'normal',
                                        'overflow': 'hidden',
                                        'textOverflow': 'ellipsis'
                                        },
                            style_header={'textAlign': 'center', 'fontWeight': 'bold',

                                          }
                        ),
                        html.Div(id='table_13-container')
                    ], className='pg2-table-lgeo'

                    ),

                ], className='pg2-table-plot-box-lgeo'),

                # Table 11
                html.Div([
                    # Title
                    html.H3(children=html.Strong(' Housing units and rental vacancy rate, Table 11'),
                            id='visualization3'),
                    # Description
                    html.Div([
                        html.H6(
                            'No text for now...')
                    ], className='muni-reg-text-lgeo'),

                    # Table

                    html.Div([
                        dash_table.DataTable(
                            id='table_14',
                            columns=[{"name": col, "id": col, "deletable": False, "selectable": False} for col in table14_for_dash.columns],
                            data=table14_for_dash.to_dict('records'),
                            editable=True,
                            sort_action="native",
                            sort_mode="multi",
                            column_selectable=False,
                            row_selectable=False,
                            row_deletable=False,
                            selected_columns=[],
                            selected_rows=[],
                            page_action="native",
                            page_current=0,
                            page_size=10,
                            merge_duplicate_headers=True,
                            # render_cell=render_cell,
                            export_format="xlsx",
                            style_table={
                                          "overflowY": "auto"

                                          },
                            style_data={'whiteSpace': 'normal', 'overflow': 'hidden',
                                        'textOverflow': 'ellipsis'},
                            style_cell={'font-family': 'Bahnschrift',
                                        'height': 'auto',
                                        'whiteSpace': 'normal',
                                        'overflow': 'hidden',
                                        'textOverflow': 'ellipsis'
                                        },
                            style_header={'textAlign': 'center', 'fontWeight': 'bold',

                                          }
                        ),
                        html.Div(id='table_14-container')
                    ], className='pg2-table-lgeo'

                    ),

                ], className='pg2-table-plot-box-lgeo'),

                # Table 12
                html.Div([
                    # Title
                    html.H3(children=html.Strong(' Housing units and demand, Table 12'),
                            id='visualization3'),
                    # Description
                    html.Div([
                        html.H6(
                            'No text for now...')
                    ], className='muni-reg-text-lgeo'),

                    # Table

                    html.Div([
                        dash_table.DataTable(
                            id='table_15',
                            columns=[{"name": col, "id": col, "deletable": False, "selectable": False} for col in
                                     table15_for_dash.columns],
                            data=table15_for_dash.to_dict('records'),
                            editable=True,
                            sort_action="native",
                            sort_mode="multi",
                            column_selectable=False,
                            row_selectable=False,
                            row_deletable=False,
                            selected_columns=[],
                            selected_rows=[],
                            page_action="native",
                            page_current=0,
                            page_size=10,
                            merge_duplicate_headers=True,
                            # render_cell=render_cell,
                            export_format="xlsx",
                            style_table={
                                "overflowY": "auto"

                            },
                            style_data={'whiteSpace': 'normal', 'overflow': 'hidden',
                                        'textOverflow': 'ellipsis'},
                            style_cell={'font-family': 'Bahnschrift',
                                        'height': 'auto',
                                        'whiteSpace': 'normal',
                                        'overflow': 'hidden',
                                        'textOverflow': 'ellipsis'
                                        },
                            style_header={'textAlign': 'center', 'fontWeight': 'bold',

                                          }
                        ),
                        html.Div(id='table_15-container')
                    ], className='pg2-table-lgeo'

                    ),

                ], className='pg2-table-plot-box-lgeo'),

                # Table 13
                html.Div([
                    # Title
                    html.H3(children=html.Strong(' Twenty-year and five-year housing need, Table 13'),
                            id='visualization3'),
                    # Description
                    html.Div([
                        html.H6(
                            'No text for now...')
                    ], className='muni-reg-text-lgeo'),

                    # Table

                    html.Div([
                        dash_table.DataTable(
                            id='table_16',
                            columns=[{"name": col, "id": col, "deletable": False, "selectable": False} for col in table16_for_dash.columns],
                            data=table16_for_dash.to_dict('records'),
                            editable=True,
                            sort_action="native",
                            sort_mode="multi",
                            column_selectable=False,
                            row_selectable=False,
                            row_deletable=False,
                            selected_columns=[],
                            selected_rows=[],
                            page_action="native",
                            page_current=0,
                            page_size=10,
                            merge_duplicate_headers=True,
                            # render_cell=render_cell,
                            export_format="xlsx",
                            style_table={
                                          "overflowY": "auto"

                                          },
                            style_data={'whiteSpace': 'normal', 'overflow': 'hidden',
                                        'textOverflow': 'ellipsis'},
                            style_cell={'font-family': 'Bahnschrift',
                                        'height': 'auto',
                                        'whiteSpace': 'normal',
                                        'overflow': 'hidden',
                                        'textOverflow': 'ellipsis'
                                        },
                            style_header={'textAlign': 'center', 'fontWeight': 'bold',

                                          }
                        ),
                        html.Div(id='table_16-container')
                    ], className='pg2-table-lgeo'

                    ),

                ], className='pg2-table-plot-box-lgeo'),

                # LGEO

                html.Div([
                    'This dashboard was created in collaboration with ',
                    html.A('Licker Geospatial', href='https://www.lgeo.co/', target="_blank"), ' using Plotly.'
                ], className='lgeo-credit-text'),

            ], className='dashboard-pg2-lgeo'
        ),

], className='background-lgeo'
)

def generate_style_data_conditional(data):

    # data_style = [
    #
    #     {
    #         'if': {'row_index': i},
    #         # 'backgroundColor': '#b0e6fc' if (i != len(data)-1) else '#74d3f9',
    #         'backgroundColor': '#b0e6fc',
    #         'color': '#000000'
    #     }
    #     for i in range(len(data))
    # ]
    # return data_style
    data_style = [
        {
            'if': {'row_index': i},
            'backgroundColor': '#b0e6fc',
            'color': '#000000',
            'border': '1px solid #002145'
        }
        for i in range(len(data))
    ]
    # if 'Total' in data.iloc[-1, 0]:
    #     # print(data.iloc[-1,0], data)
    #     total_style = [
    #         {
    #             'if': {'row_index': i, 'column_id': 0},
    #             'backgroundColor': '#74d3f9',
    #             'color': '#000000'
    #         } for i in range(len(data))
    #     ]
    #     # print(total_style)
    #     return data_style.extend(total_style)
    # else:
    return data_style




def generate_additional_data_style(data, data_columns):
    first_and_last_columns_ids = [data_columns[0]['id'], data_columns[-1]['id']]
    new_data_style = [
        {
            'if': {'row_index': len(data) - 1, 'column_id': j['id']},
            'backgroundColor': '#74d3f9',
            'color': '#000000',
            'border-left': 'none',
            'fontWeight': 'bold'
            # 'rowSpan': 2

        } for j in data_columns[1:-1]

        ] + [
        {
            'if': {'row_index': len(data) - 1, 'column_id': col_id},
            'fontWeight': 'bold',
            'backgroundColor': '#74d3f9',
            'color': '#000000'
        } for col_id in first_and_last_columns_ids
    ]
    return new_data_style

def generate_style_header_conditional(columns):
    # has_blank_header = any(header == '' for col in columns for header in col)
    # print([header for header in columns])
    style_conditional = []

    for index, col in enumerate(columns):
        # print(index, col, col[1])
        # print('#######')
        if col[1] == '':
            style_conditional.append({
                'if': {'header_index': index},
                'backgroundColor': '#002145' if index == 0 else '#39C0F7',
                'color': '#FFFFFF' if index == 0 else '#000000',
                'border-bottom': 'none' if index == 0 else '', # No bottom border for blank sub-header
                'border': '1px solid #002145'
            })
        else:
            style_conditional.append({
                'if': {'header_index': index},
                'backgroundColor': '#002145' if index == 0 else '#39C0F7',
                'color': '#FFFFFF' if index == 0 else '#000000',
                'border': '1px solid #002145'
            })

    return style_conditional

def table_generator(geo, df, table_id):
    # joined_df_filtered = joined_df.query('Geography == ' + f'"{geo}"')
    geoid = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Geo_Code'].tolist()[0]

    if ((table_id == 'table_4b') or (table_id == 'table_6') or (table_id == 'table7_2006') or (table_id == 'table7_2021') or \
            (table_id == 'table_8') or (table_id == 'table_9') or (table_id == 'table_10') or (table_id == 'table_11')
            or (table_id == 'table_13')):
        filtered_df = df.query('GEOUID_ == ' + f'{geoid}')
        filtered_df.columns = pd.MultiIndex.from_tuples([tuple(col.split('_')) for col in filtered_df.columns])
    else:
        filtered_df = df.query('GEOUID == ' + f'{geoid}')

    table = filtered_df.iloc[:, 3:]
    # table = table.fillna('n/a')
    for index, row in table.iterrows():
        if any('Total' in str(cell) or 'Average' in str(cell) for cell in row.values):
            continue
        else:
            table.loc[index] = row.fillna('n/a')

    return table

def number_formatting(df, col_list, precision):
    if precision == 0:
        for cols in col_list:
            df[cols] = df[cols].apply(lambda x: '{0:,.0f}'.format(x) if pd.notnull(x) and x != 'n/a' else x)
    else:
        for cols in col_list:
            df[cols] = df[cols].apply(lambda x: '{0:,.3f}'.format(x) if pd.notnull(x) and x != 'n/a' else x)
    return df

def percent_formatting(df, col_list, mult_flag):
    if mult_flag == 0:
        for cols in col_list:
            df[cols] = df[cols].apply(lambda x: f"{x:.3%}" if pd.notnull(x) and x != 'n/a' else x)
    else:
        for cols in col_list:
            df[cols] = df[cols].apply(lambda x: f"{x*100:.3%}" if pd.notnull(x) and x != 'n/a' else x)
    return df

# Callback for storing selected areas and area scale level


@callback(
    Output('table_4a', 'columns'),
    Output('table_4a', 'data'),
    Output('table_4a', 'style_data_conditional'),
    Output('table_4a', 'style_cell_conditional'),
    Output('table_4a', 'style_header_conditional'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('area-scale-store', 'data'),
    Input('table_4a', 'selected_columns'),
)
def update_table_4a(geo, geo_c, scale, selected_columns):
    # Single area mode
    # print(geo)
    if geo == geo_c or geo_c == None or (geo == None and geo_c != None):

        # When no area is selected
        if geo == None and geo_c != None:
            geo = geo_c
        elif geo == None and geo_c == None:
            geo = default_value

        # Area Scaling up/down when user clicks area scale button on page 1
        if "to-geography-1" == scale:
            geo = geo
        elif "to-region-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Region'].tolist()[0]
        elif "to-province-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Province'].tolist()[0]
        else:
            geo = geo

        # Generating table
        table = table_generator(geo, table_4a, 'table_4a')
        table = table.replace('Owner', 'Owners').replace('Renter', 'Renters')
        table.drop_duplicates(inplace=True)
        table = number_formatting(table, ['2006', '2011', '2016', '2021'], 0)
        style_data_conditional = generate_style_data_conditional(table)
        style_header_conditional = generate_style_header_conditional(table)

        # Generating callback output to update table
        # col_list = []
        # pdb.set_trace()
        table_columns = [{"name": [geo, col], "id": col} for col in table.columns]
        # additional_header = [
        #     {
        #         'if': {'header_index': 1},
        #         'textAlign': 'left'
        #     }
        # ]
        # style_header_conditional.extend(additional_header)

        style_cell_conditional = [
            {
                'if': {'column_id': table_columns[0]['id']},
                'backgroundColor': columns_color_fill[1],
                'textAlign': 'left',
                "maxWidth": "50px"
            }
            ] + [
            {
                'if': {'column_id': c['id']},
                'backgroundColor': columns_color_fill[1],
                'textAlign': 'center'
            } for c in table_columns[1:]
        ]
        # print(style_cell_conditional)
        return table_columns, table.to_dict('records'), style_data_conditional, style_cell_conditional, style_header_conditional


@callback(
    Output('table_4b', 'columns'),
    Output('table_4b', 'data'),
    Output('table_4b', 'style_data_conditional'),
    Output('table_4b', 'style_cell_conditional'),
    Output('table_4b', 'style_header_conditional'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('area-scale-store', 'data'),
    Input('table_4b', 'selected_columns'),
)
def update_table_4b(geo, geo_c, scale, selected_columns):
    # Single area mode
    # print(geo)
    if geo == geo_c or geo_c == None or (geo == None and geo_c != None):

        # When no area is selected
        if geo == None and geo_c != None:
            geo = geo_c
        elif geo == None and geo_c == None:
            geo = default_value

        # Area Scaling up/down when user clicks area scale button on page 1
        if "to-geography-1" == scale:
            geo = geo
        elif "to-region-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Region'].tolist()[0]
        elif "to-province-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Province'].tolist()[0]
        else:
            geo = geo

        # geo_id = mapped_geo_code.loc[mapped_geo_code['Geo_Code'] == geo, :]['Geo_Code'].tolist()[0]

        # pdb.set_trace()


        # Generating table
        table = table_generator(geo, table_4b, 'table_4b')
        table.drop_duplicates(inplace=True)
        # table[('2006', '% of total')] = table[('2006', '% of total')].apply(lambda x: f"{x}%" if pd.notna(x) else x)
        # table[('2011', '% of total')] = table[('2011', '% of total')].apply(lambda x: f"{x}%" if pd.notna(x) else x)
        # table[('2016', '% of total')] = table[('2016', '% of total')].apply(lambda x: f"{x}%" if pd.notna(x) else x)
        # table[('2021', '% of total')] = table[('2021', '% of total')].apply(lambda x: f"{x}%" if pd.notna(x) else x)
        # table[('', 'Average ECHN Rate')] = table[('', 'Average ECHN Rate')].apply(lambda x: f"{x}%" if pd.notna(x) else x)
        table = percent_formatting(table, [('2006', '% of total'), ('2011', '% of total'), ('2016', '% of total'),
                                           ('2021', '% of total'), ('', 'Average ECHN Rate')], 0)
        table = number_formatting(table, [('2006', '#'), ('2011', '#'),
                                          ('2016', '#'), ('2021', '#')], 0)

        style_data_conditional = generate_style_data_conditional(table)
        style_header_conditional = generate_style_header_conditional(table)

        # Generating callback output to update table
        # col_list = []
        # pdb.set_trace()
        table_columns = [{"name": [geo, col1, col2], "id": f"{col1}_{col2}"} for col1, col2 in table.columns]
        # table_columns.append({'name': [geo]})

        table_data = [
            {
                **{f"{x1}_{x2}": y for (x1, x2), y in data},
            }
            for (n, data) in [
                *enumerate([list(x.items()) for x in table.T.to_dict().values()])
            ]
        ]

        style_cell_conditional = [
                                     {
                                         'if': {'column_id': table_columns[0]['id']},
                                         'backgroundColor': columns_color_fill[1],
                                         'textAlign': 'left',
                                         "width": "18%"
                                     }
                                 ] + [
                                     {
                                         'if': {'column_id': c['id']},
                                         'backgroundColor': columns_color_fill[1],
                                         'textAlign': 'center'
                                     } for c in table_columns[1:]
                                 ] + [
                                    {
                                        'if': {'column_id': '_Average ECHN Rate'},
                                        'fontWeight': 'bold',
                                        "width": "14%"
                                    }
                                ] + [
                                    {
                                        'if': {'column_id': col_id},
                                        'width': '8%'
                                    } for col_id in ['2006_#', '2011_#', '2016_#', '2021_#']
                                ] + [
                                    {
                                        'if': {'column_id': col_id},
                                        'width': '8%'
                                    } for col_id in ['2006_% of total', '2011_% of total', '2016_% of total', '2021_% of total']
                                ]

        merge_style = [
                                    {
                                        'if': {'row_index': 0, 'column_id': j},
                                        'backgroundColor': '#b0e6fc',
                                        'color': '#b0e6fc',
                                        'border-right': 'none',
                                        'colSpan': 2

                                    }
                                    for j in ['2006_#', '2011_#', '2016_#']
                                ]
        style_data_conditional.extend(merge_style)
        return table_columns, table_data, style_data_conditional, style_cell_conditional, style_header_conditional


@callback(
    Output('table5', 'columns'),
    Output('table5', 'data'),
    Output('table5', 'style_data_conditional'),
    Output('table5', 'style_cell_conditional'),
    Output('table5', 'style_header_conditional'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('area-scale-store', 'data'),
    Input('table5', 'selected_columns'),
)
def update_table5(geo, geo_c, scale, selected_columns):
    # Single area mode
    # print(geo)
    if geo == geo_c or geo_c == None or (geo == None and geo_c != None):

        # When no area is selected
        if geo == None and geo_c != None:
            geo = geo_c
        elif geo == None and geo_c == None:
            geo = default_value

        # Area Scaling up/down when user clicks area scale button on page 1
        if "to-geography-1" == scale:
            geo = geo
        elif "to-region-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Region'].tolist()[0]
        elif "to-province-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Province'].tolist()[0]
        else:
            geo = geo

        # geo_id = mapped_geo_code.loc[mapped_geo_code['Geo_Code'] == geo, :]['Geo_Code'].tolist()[0]

        # pdb.set_trace()


        # Generating table
        table = table_generator(geo, table_5, 'table_5')
        table = number_formatting(table, ['2021 Households'], 0)
        table = number_formatting(table, ['Households in ECHN'], 3)
        # table['Households in ECHN'] = table['Households in ECHN'].apply(lambda x: '{0:,.3f}'.format(x) if pd.notnull(x) else x)
        table = percent_formatting(table, ['Average ECHN Rate'], 0)

        if not table.empty:
            index_number = table['2021 Households'].index[0]
            # print(index_number)
            table.at[index_number + 1, '2021 Households'] = table.at[index_number, '2021 Households']

        # print(table)
        # table['Average ECHN Rate'] = table['Average ECHN Rate'].apply(lambda x: f"{x}%" if pd.notna(x) else x)
        # Generating callback output to update table
        # col_list = []
        # pdb.set_trace()
        table_columns = [{"name": [geo, col], "id": col} for col in table.columns]
        style_data_conditional = generate_style_data_conditional(table)
        style_header_conditional = generate_style_header_conditional(table)

        style_cell_conditional = [
                {
                    'if': {'column_id': table_columns[0]['id']},
                    'backgroundColor': columns_color_fill[1],
                    'textAlign': 'left',
                    # "width": "18%"
                }
            ] + [
                {
                    'if': {'column_id': c['id']},
                    'backgroundColor': columns_color_fill[1],
                    'textAlign': 'center'
                } for c in table_columns[1:]
            ]
        merge_data_style = [
            {
                'if': {'row_index': 0, 'column_id': j},
                'backgroundColor': '#b0e6fc',
                'color': '#b0e6fc',
                'border-bottom': 'none',
                'rowSpan': 2

            }
            for j in ['2021 Households']

        ]
        style_data_conditional.extend(merge_data_style)

        new_data_style = generate_additional_data_style(table, table_columns)
        style_data_conditional.extend(new_data_style)
        return table_columns, table.to_dict('records'), style_data_conditional, style_cell_conditional, style_header_conditional

@callback(
    Output('table_6', 'columns'),
    Output('table_6', 'data'),
    Output('table_6', 'style_data_conditional'),
    Output('table_6', 'style_cell_conditional'),
    Output('table_6', 'style_header_conditional'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('area-scale-store', 'data'),
    Input('table_6', 'selected_columns'),
)
def update_table_6(geo, geo_c, scale, selected_columns):
    # Single area mode
    # print(geo)
    if geo == geo_c or geo_c == None or (geo == None and geo_c != None):

        # When no area is selected
        if geo == None and geo_c != None:
            geo = geo_c
        elif geo == None and geo_c == None:
            geo = default_value

        # Area Scaling up/down when user clicks area scale button on page 1
        if "to-geography-1" == scale:
            geo = geo
        elif "to-region-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Region'].tolist()[0]
        elif "to-province-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Province'].tolist()[0]
        else:
            geo = geo

        # Generating table
        table = table_generator(geo, table_6, "table_6")
        # table[('Local Population', '% of region')] = table[('Local Population', '% of region')].apply(lambda x: f"{x*100:.3%}" if pd.notna(x) else x)
        table = percent_formatting(table, [('Local Population', '% of region')], 1)
        table = number_formatting(table, [('Local Population', '#'), ('', 'Regional PEH')], 0)
        table = number_formatting(table, [('', 'Proportional Local PEH')], 3)
        # pdb.set_trace()
        if not table.empty:
            index_number = table[('', 'Regional Population')].index[0]
            table[('', 'Regional Population')][index_number] = '{:,.0f}'.format(float(table[('', 'Regional Population')][index_number]))

        blank_row = pd.DataFrame([[None] * len(table.columns)], columns=table.columns)

        # Split the DataFrame into two parts
        df_top = table.iloc[:1]
        df_bottom = table.iloc[1:]

        # Concatenate the parts together with the blank row in between
        # pdb.set_trace()
        new_table = pd.concat([df_top, blank_row, df_bottom]).reset_index(drop=True)

        table_columns = [{"name": [geo, col1, col2], "id": f"{col1}_{col2}"} for col1, col2 in new_table.columns]
        table_data = [
            {
                **{f"{x1}_{x2}": y for (x1, x2), y in data},
            }
            for (n, data) in [
                *enumerate([list(x.items()) for x in new_table.T.to_dict().values()])
            ]
        ]

        style_data_conditional = generate_style_data_conditional(new_table)
        style_header_conditional = generate_style_header_conditional(new_table)

        style_cell_conditional = [
                                     {
                                         'if': {'column_id': c['id']},
                                         'backgroundColor': columns_color_fill[1],
                                         'textAlign': 'center'

                                         # "maxWidth" : "100px"
                                     } for c in table_columns
                                 ]
        new_data_style = generate_additional_data_style(new_table, table_columns)
        style_data_conditional.extend(new_data_style)
        blank_row_style = [
                            {
                                'if': {'row_index': len(new_table) - 2, 'column_id': j['id']},
                                'color': 'transparent',
                                'backgroundColor': 'transparent',
                                'border-left': 'none',
                                'border-right': 'none'

                                # 'rowSpan': 2

                            } for j in table_columns
                        ]
        style_data_conditional.extend(blank_row_style)
        return table_columns, table_data, style_data_conditional, style_cell_conditional, style_header_conditional


@callback(
    Output('table7_2006', 'columns'),
    Output('table7_2006', 'data'),
    Output('table7_2006', 'style_data_conditional'),
    Output('table7_2006', 'style_cell_conditional'),
    Output('table7_2006', 'style_header_conditional'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('area-scale-store', 'data'),
    Input('table7_2006', 'selected_columns'),
)
def update_table7_2006(geo, geo_c, scale, selected_columns):
    # Single area mode
    # print(geo)
    if geo == geo_c or geo_c == None or (geo == None and geo_c != None):

        # When no area is selected
        if geo == None and geo_c != None:
            geo = geo_c
        elif geo == None and geo_c == None:
            geo = default_value

        # Area Scaling up/down when user clicks area scale button on page 1
        if "to-geography-1" == scale:
            geo = geo
        elif "to-region-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Region'].tolist()[0]
        elif "to-province-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Province'].tolist()[0]
        else:
            geo = geo

        # geo_id = mapped_geo_code.loc[mapped_geo_code['Geo_Code'] == geo, :]['Geo_Code'].tolist()[0]

        # pdb.set_trace()


        # Generating table
        table = table_generator(geo, table_7_2006, "table7_2006")
        table = number_formatting(table, [('2006 Households', 'Owner'), ('2006 Households', 'Renter')], 0)

        style_data_conditional = generate_style_data_conditional(table)
        style_header_conditional = generate_style_header_conditional(table)
        # print(style_header_conditional)
        # Generating callback output to update table
        # col_list = []
        # pdb.set_trace()
        table_columns = [{"name": [geo, col1, col2], "id": f"{col1}_{col2}"} for col1, col2 in table.columns]
        # table_columns.append({'name': [geo]})

        table_data = [
            {
                **{f"{x1}_{x2}": y for (x1, x2), y in data},
            }
            for (n, data) in [
                *enumerate([list(x.items()) for x in table.T.to_dict().values()])
            ]
        ]
        # print(table_data)
        # print(table_columns)
        #
        # median_row = ['Area Median Household Income', "", median_income, median_rent]
        # for i, j in zip(list(table.columns), median_row):
        #     col_list.append({"name": [geo_id, i, j], "id": i})
        # Setting geography as index to fetch median rent and income data

        # table_columns = list(table.columns)
        # geo_row = [geo] * 4
        # mapped_list = [item for pair in zip(geo_row, table_columns, median_row + [0])
        #                          for item in pair]
        # col_list = {"name": mapped_list, "id": mapped_list[i] for i in ran}
        # print(table.to_dict('record'), col_list)

        style_cell_conditional = [
                                    {
                                        'if': {'column_id': table_columns[0]['id']},
                                        'backgroundColor': columns_color_fill[1],
                                        'textAlign': 'left',
                                        # "width": "18%"
                                    }
                                ] + [
                                    {
                                        'if': {'column_id': c['id']},
                                        'backgroundColor': columns_color_fill[1],
                                        'textAlign': 'center'
                                    } for c in table_columns[1:]
                                ] + [
                                    {
                                        'if': {'column_id': '_Age - Primary Household Maintainer 2006 Categories'},
                                        # 'fontWeight': 'bold',
                                        "width": "40%"
                                    }
                                ] + [
                                    {
                                        'if': {'column_id': i},
                                        # 'fontWeight': 'bold',
                                        "width": "30%"
                                    } for i in ['2006 Households_Owner', '2006 Households_Renter']
                                ]
        # print(style_cell_conditional)
        return table_columns, table_data, style_data_conditional, style_cell_conditional, style_header_conditional


@callback(
    Output('table7_2021', 'columns'),
    Output('table7_2021', 'data'),
    Output('table7_2021', 'style_data_conditional'),
    Output('table7_2021', 'style_cell_conditional'),
    Output('table7_2021', 'style_header_conditional'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('area-scale-store', 'data'),
    Input('table7_2021', 'selected_columns'),
)
def update_table7_2021(geo, geo_c, scale, selected_columns):
    # Single area mode
    # print(geo)
    if geo == geo_c or geo_c == None or (geo == None and geo_c != None):

        # When no area is selected
        if geo == None and geo_c != None:
            geo = geo_c
        elif geo == None and geo_c == None:
            geo = default_value

        # Area Scaling up/down when user clicks area scale button on page 1
        if "to-geography-1" == scale:
            geo = geo
        elif "to-region-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Region'].tolist()[0]
        elif "to-province-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Province'].tolist()[0]
        else:
            geo = geo

        # geo_id = mapped_geo_code.loc[mapped_geo_code['Geo_Code'] == geo, :]['Geo_Code'].tolist()[0]

        # pdb.set_trace()


        # Generating table
        table = table_generator(geo, table_7_2021, "table7_2021")
        table = number_formatting(table, [('2021 Households', 'Owner'), ('2021 Households', 'Renter')], 0)
        style_data_conditional = generate_style_data_conditional(table)
        style_header_conditional = generate_style_header_conditional(table)
        # Generating callback output to update table
        # col_list = []
        # pdb.set_trace()
        table_columns = [{"name": [geo, col1, col2], "id": f"{col1}_{col2}"} for col1, col2 in table.columns]
        # table_columns.append({'name': [geo]})

        table_data = [
            {
                **{f"{x1}_{x2}": y for (x1, x2), y in data},
            }
            for (n, data) in [
                *enumerate([list(x.items()) for x in table.T.to_dict().values()])
            ]
        ]
        # print(table_data)
        # print(table_columns)
        #
        # median_row = ['Area Median Household Income', "", median_income, median_rent]
        # for i, j in zip(list(table.columns), median_row):
        #     col_list.append({"name": [geo_id, i, j], "id": i})
        # Setting geography as index to fetch median rent and income data

        # table_columns = list(table.columns)
        # geo_row = [geo] * 4
        # mapped_list = [item for pair in zip(geo_row, table_columns, median_row + [0])
        #                          for item in pair]
        # col_list = {"name": mapped_list, "id": mapped_list[i] for i in ran}
        # print(table.to_dict('record'), col_list)

        style_cell_conditional = [
                                    {
                                        'if': {'column_id': table_columns[0]['id']},
                                        'backgroundColor': columns_color_fill[1],
                                        'textAlign': 'left',
                                        # "width": "18%"
                                    }
                                ] + [
                                    {
                                        'if': {'column_id': c['id']},
                                        'backgroundColor': columns_color_fill[1],
                                        'textAlign': 'center'
                                    } for c in table_columns[1:]
                                ]  + [
                                    {
                                        'if': {'column_id': '_Age - Primary Household Maintainer 2021 Categories'},
                                        # 'fontWeight': 'bold',
                                        "width": "40%"
                                    }
                                ] + [
                                    {
                                        'if': {'column_id': i},
                                        # 'fontWeight': 'bold',
                                        "width": "30%"
                                    } for i in ['2021 Households_Owner', '2021 Households_Renter']
                                ]
        # print(style_cell_conditional)
        return table_columns, table_data, style_data_conditional, style_cell_conditional, style_header_conditional


@callback(
    Output('table8', 'columns'),
    Output('table8', 'data'),
    Output('table8', 'style_data_conditional'),
    Output('table8', 'style_cell_conditional'),
    Output('table8', 'style_header_conditional'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('area-scale-store', 'data'),
    Input('table8', 'selected_columns'),
)
def update_table8(geo, geo_c, scale, selected_columns):
    # Single area mode
    # print(geo)
    if geo == geo_c or geo_c == None or (geo == None and geo_c != None):

        # When no area is selected
        if geo == None and geo_c != None:
            geo = geo_c
        elif geo == None and geo_c == None:
            geo = default_value

        # Area Scaling up/down when user clicks area scale button on page 1
        if "to-geography-1" == scale:
            geo = geo
        elif "to-region-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Region'].tolist()[0]
        elif "to-province-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Province'].tolist()[0]
        else:
            geo = geo

        # geo_id = mapped_geo_code.loc[mapped_geo_code['Geo_Code'] == geo, :]['Geo_Code'].tolist()[0]

        # pdb.set_trace()


        # Generating table
        table = table_generator(geo, table_8, "table_8")

        # print(table.columns)
        table = number_formatting(table, [('2021', 'All Categories'), ('2021', 'Summed Categories'),
                                          ('2006', 'All Categories'), ('2006', 'Summed Categories')], 0)

        style_data_conditional = generate_style_data_conditional(table)
        style_header_conditional = generate_style_header_conditional(table)
        # print(style_header_conditional)
        # duplicated_mask = table[('2006', 'Summed Categories')].duplicated()
        # # Update the duplicated values to be blank
        # table.loc[duplicated_mask, ('2006', 'Summed Categories')] = None

        # Generating callback output to update table
        # col_list = []
        # pdb.set_trace()
        table_columns = [{"name": [geo, col1, col2], "id": f"{col1}_{col2}"} for col1, col2 in table.columns[1:]]
        # table_columns.append({'name': [geo]})

        table_data = [
            {
                **{f"{x1}_{x2}": y for (x1, x2), y in data},
            }
            for (n, data) in [
                *enumerate([list(x.items()) for x in table.T.to_dict().values()])
            ]
        ]
        first_and_last_columns_ids = [table_columns[0]['id'], table_columns[1]['id']]
        style_cell_conditional = [
                                    {
                                        'if': {'column_id': col_id},
                                        'backgroundColor': columns_color_fill[1],
                                        'textAlign': 'left',
                                        # "width": "18%"
                                    } for col_id in first_and_last_columns_ids
                                ] + [
                                    {
                                        'if': {'column_id': c['id']},
                                        'backgroundColor': columns_color_fill[1],
                                        'textAlign': 'center'
                                    } for c in table_columns[2:]
                                ] + [
                                    {
                                        'if': {'column_id': i},
                                        # 'fontWeight': 'bold',
                                        "width": "20%"
                                    } for i in ['_Age Categories - Household Maintainers', 'Age Categories -  Population']
                                ] + [
                                    {
                                        'if': {'column_id': i['id']},
                                        # 'fontWeight': 'bold',
                                        "width": "15%"
                                    } for i in table_columns[2:]
                                ]

        new_data_style = [
            {
                'if': {'row_index': i, 'column_id': j},
                'backgroundColor': '#b0e6fc',
                'color': '#b0e6fc',
                'border-top': 'none',
                'rowSpan': 2

            } for i in [1, 3, 5, 7, 9, 11, 13, 14]
            for j in ['_Age Categories – Household Maintainers']
        ] + [
            {
                'if': {'row_index': i, 'column_id': j},
                'backgroundColor': '#b0e6fc',
                'color': '#b0e6fc',
                'border-bottom': 'none',
                'rowSpan': 2

            } for i in [0, 2, 4, 6, 8, 10, 12, 13]
            for j in ['2006_Summed Categories', '2021_Summed Categories']
        ]
        style_data_conditional.extend(new_data_style)

        # print(style_data_conditional)
        return table_columns, table_data, style_data_conditional, style_cell_conditional, style_header_conditional


@callback(
    Output('table9', 'columns'),
    Output('table9', 'data'),
    Output('table9', 'style_data_conditional'),
    Output('table9', 'style_cell_conditional'),
    Output('table9', 'style_header_conditional'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('area-scale-store', 'data'),
    Input('table9', 'selected_columns'),
)
def update_table9(geo, geo_c, scale, selected_columns):
    # Single area mode
    # print(geo)
    if geo == geo_c or geo_c == None or (geo == None and geo_c != None):

        # When no area is selected
        if geo == None and geo_c != None:
            geo = geo_c
        elif geo == None and geo_c == None:
            geo = default_value

        # Area Scaling up/down when user clicks area scale button on page 1
        if "to-geography-1" == scale:
            geo = geo
        elif "to-region-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Region'].tolist()[0]
        elif "to-province-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Province'].tolist()[0]
        else:
            geo = geo

        # geo_id = mapped_geo_code.loc[mapped_geo_code['Geo_Code'] == geo, :]['Geo_Code'].tolist()[0]

        # pdb.set_trace()


        # Generating table
        table = table_generator(geo, table_9, "table_9")
        table = number_formatting(table, [('2006 Population', 'Total'),
                                          ('2006 Households', 'Owner'), ('2006 Households', 'Renter')], 0)

        table = percent_formatting(table, [('2006 Headship Rate', 'Owner'), ('2006 Headship Rate', 'Renter')], 1)
        # table[('2006 Headship Rate', 'Owner')] = (table[('2006 Headship Rate', 'Owner')] * 100).astype(str) + '%'
        # table[('2006 Headship Rate', 'Renter')] = (table[('2006 Headship Rate', 'Renter')] * 100).astype(str) + '%'
        style_data_conditional = generate_style_data_conditional(table)
        style_header_conditional = generate_style_header_conditional(table)
        # Generating callback output to update table
        # col_list = []
        # pdb.set_trace()
        table_columns = [{"name": [geo, col1, col2], "id": f"{col1}_{col2}"} for col1, col2 in table.columns]
        # table_columns.append({'name': [geo]})

        table_data = [
            {
                **{f"{x1}_{x2}": y for (x1, x2), y in data},
            }
            for (n, data) in [
                *enumerate([list(x.items()) for x in table.T.to_dict().values()])
            ]
        ]
        # print(table_data)
        # print(table_columns)
        #
        style_cell_conditional = [
                                    {
                                        'if': {'column_id': table_columns[0]['id']},
                                        'backgroundColor': columns_color_fill[1],
                                        'textAlign': 'left',
                                        # "width": "18%"
                                    }
                                ] + [
                                    {
                                        'if': {'column_id': c['id']},
                                        'backgroundColor': columns_color_fill[1],
                                        'textAlign': 'center'
                                    } for c in table_columns[1:]
                                ] + [
                                    {
                                        'if': {'column_id': i},
                                        # 'fontWeight': 'bold',
                                        "width": "20%"
                                    } for i in ['Age Categories – Household Maintainers_']
                                ] + [
                                    {
                                        'if': {'column_id': i['id']},
                                        # 'fontWeight': 'bold',
                                        "width": "16%"
                                    } for i in table_columns[1:]
                                ]
        # print(style_cell_conditional)
        return table_columns, table_data, style_data_conditional, style_cell_conditional, style_header_conditional


@callback(
    Output('table10', 'columns'),
    Output('table10', 'data'),
    Output('table10', 'style_data_conditional'),
    Output('table10', 'style_cell_conditional'),
    Output('table10', 'style_header_conditional'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('area-scale-store', 'data'),
    Input('table10', 'selected_columns'),
)
def update_table10(geo, geo_c, scale, selected_columns):
    # Single area mode
    # print(geo)
    if geo == geo_c or geo_c == None or (geo == None and geo_c != None):

        # When no area is selected
        if geo == None and geo_c != None:
            geo = geo_c
        elif geo == None and geo_c == None:
            geo = default_value

        # Area Scaling up/down when user clicks area scale button on page 1
        if "to-geography-1" == scale:
            geo = geo
        elif "to-region-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Region'].tolist()[0]
        elif "to-province-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Province'].tolist()[0]
        else:
            geo = geo

        # geo_id = mapped_geo_code.loc[mapped_geo_code['Geo_Code'] == geo, :]['Geo_Code'].tolist()[0]

        # pdb.set_trace()


        # Generating table
        table = table_generator(geo, table_10, "table_10")
        table = number_formatting(table, [('2021 Population', 'Total')], 0)
        table = number_formatting(table, [('2021 Potential Households', 'Owner'), ('2021 Potential Households', 'Renter')], 3)

        table = percent_formatting(table, [('2006 Headship Rate', 'Owner'), ('2006 Headship Rate', 'Renter')], 1)

        # table[('2006 Headship Rate', 'Owner')] = (table[('2006 Headship Rate', 'Owner')] * 100).astype(str) + '%'
        # table[('2006 Headship Rate', 'Renter')] = (table[('2006 Headship Rate', 'Renter')] * 100).astype(str) + '%'
        style_data_conditional = generate_style_data_conditional(table)
        style_header_conditional = generate_style_header_conditional(table)
        # Generating callback output to update table
        # col_list = []
        # pdb.set_trace()
        table_columns = [{"name": [geo, col1, col2], "id": f"{col1}_{col2}"} for col1, col2 in table.columns]
        # table_columns.append({'name': [geo]})

        table_data = [
            {
                **{f"{x1}_{x2}": y for (x1, x2), y in data},
            }
            for (n, data) in [
                *enumerate([list(x.items()) for x in table.T.to_dict().values()])
            ]
        ]
        # print(table_data)
        # print(table_columns)
        #
        style_cell_conditional = [
                                    {
                                        'if': {'column_id': table_columns[0]['id']},
                                        'backgroundColor': columns_color_fill[1],
                                        'textAlign': 'left',
                                        # "width": "18%"
                                    }
                                ] + [
                                    {
                                        'if': {'column_id': c['id']},
                                        'backgroundColor': columns_color_fill[1],
                                        'textAlign': 'center'
                                    } for c in table_columns[1:]
                                ] + [
                                    {
                                        'if': {'column_id': i},
                                        # 'fontWeight': 'bold',
                                        "width": "20%"
                                    } for i in ['Age Categories – Household Maintainers_']
                                ] + [
                                    {
                                        'if': {'column_id': i['id']},
                                        # 'fontWeight': 'bold',
                                        "width": "16%"
                                    } for i in table_columns[1:]
                                ]
        # print(style_cell_conditional)
        return table_columns, table_data, style_data_conditional, style_cell_conditional, style_header_conditional


@callback(
    Output('table11', 'columns'),
    Output('table11', 'data'),
    Output('table11', 'style_data_conditional'),
    Output('table11', 'style_cell_conditional'),
    Output('table11', 'style_header_conditional'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('area-scale-store', 'data'),
    Input('table11', 'selected_columns'),
)
def update_table11(geo, geo_c, scale, selected_columns):
    # Single area mode
    # print(geo)
    if geo == geo_c or geo_c == None or (geo == None and geo_c != None):

        # When no area is selected
        if geo == None and geo_c != None:
            geo = geo_c
        elif geo == None and geo_c == None:
            geo = default_value

        # Area Scaling up/down when user clicks area scale button on page 1
        if "to-geography-1" == scale:
            geo = geo
        elif "to-region-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Region'].tolist()[0]
        elif "to-province-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Province'].tolist()[0]
        else:
            geo = geo

        # geo_id = mapped_geo_code.loc[mapped_geo_code['Geo_Code'] == geo, :]['Geo_Code'].tolist()[0]

        # pdb.set_trace()


        # Generating table
        table = table_generator(geo, table_11, "table_11")
        table = number_formatting(table, [('2021 Households', 'Owner'), ('2021 Households', 'Renter')], 0)
        table = number_formatting(table, [('2021 Potential Households', 'Owner'),
                                          ('2021 Potential Households', 'Renter'), ('2021 Suppressed Households', 'Owner'),
                                          ('2021 Suppressed Households', 'Renter'), ('2021 Suppressed Households', 'Total')], 3)

        # table = percent_formatting(table, [('2006 Headship Rate', 'Owner'), ('2006 Headship Rate', 'Renter')], 1)
        # table[('2006 Headship Rate', 'Owner')] = (table[('2006 Headship Rate', 'Owner')] * 100).astype(str) + '%'
        # table[('2006 Headship Rate', 'Renter')] = (table[('2006 Headship Rate', 'Renter')] * 100).astype(str) + '%'
        style_data_conditional = generate_style_data_conditional(table)
        style_header_conditional = generate_style_header_conditional(table)
        # Generating callback output to update table
        # col_list = []
        # pdb.set_trace()
        table_columns = [{"name": [geo, col1, col2], "id": f"{col1}_{col2}"} for col1, col2 in table.columns]
        # table_columns.append({'name': [geo]})

        table_data = [
            {
                **{f"{x1}_{x2}": y for (x1, x2), y in data},
            }
            for (n, data) in [
                *enumerate([list(x.items()) for x in table.T.to_dict().values()])
            ]
        ]
        # print(table_data)
        # print(table_columns)
        #
        style_cell_conditional = [
                                    {
                                        'if': {'column_id': table_columns[0]['id']},
                                        'backgroundColor': columns_color_fill[1],
                                        'textAlign': 'left',
                                        # "width": "18%"
                                    }
                                ] + [
                                    {
                                        'if': {'column_id': c['id']},
                                        'backgroundColor': columns_color_fill[1],
                                        'textAlign': 'center'
                                    } for c in table_columns[1:]
                                ]  + [
                                    {
                                        'if': {'column_id': i},
                                        # 'fontWeight': 'bold',
                                        "width": "23%"
                                    } for i in ['Age Categories – Household Maintainers_']
                                ] + [
                                    {
                                        'if': {'column_id': i['id']},
                                        # 'fontWeight': 'bold',
                                        "width": "11%"
                                    } for i in table_columns[1:]
                                ]
        new_data_style = generate_additional_data_style(table, table_columns)
        style_data_conditional.extend(new_data_style)
        add_total_data_style = [
            {
                'if': {'row_index': len(table) - 1, 'column_id': j},
                'border-left': 'none',
                # 'rowSpan': 2

            } for j in ['2021 Potential Households_Renter', '2021 Suppressed Households_Renter']

        ]
        style_data_conditional.extend(add_total_data_style)
        return table_columns, table_data, style_data_conditional, style_cell_conditional, style_header_conditional

@callback(
    Output('table_12', 'columns'),
    Output('table_12', 'data'),
    Output('table_12', 'style_data_conditional'),
    Output('table_12', 'style_cell_conditional'),
    Output('table_12', 'style_header_conditional'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('area-scale-store', 'data'),
    Input('table_12', 'selected_columns'),
)
def update_table_12(geo, geo_c, scale, selected_columns):
    # Single area mode
    # print(geo)
    if geo == geo_c or geo_c == None or (geo == None and geo_c != None):

        # When no area is selected
        if geo == None and geo_c != None:
            geo = geo_c
        elif geo == None and geo_c == None:
            geo = default_value

        # Area Scaling up/down when user clicks area scale button on page 1
        if "to-geography-1" == scale:
            geo = geo
        elif "to-region-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Region'].tolist()[0]
        elif "to-province-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Province'].tolist()[0]
        else:
            geo = geo

        # Generating table
        table = table_generator(geo, table_12, "table_12")
        table = number_formatting(table, ['2021', '2041'], 0)

        # table = percent_formatting(table, ['Regional Growth Rate'], 0)
        # df[cols] = df[cols].apply(lambda x: f"{x:.3%}" if pd.notnull(x) else x)
        # print(table.dtypes)
        table['Regional Growth Rate'] = table['Regional Growth Rate'].map('{:,.3f}%'.format)
        style_data_conditional = generate_style_data_conditional(table)
        style_header_conditional = generate_style_header_conditional(table)
        # Generating callback output to update table
        # col_list = []
        # pdb.set_trace()
        table_columns = [{"name": [geo, col], "id": col} for col in table.columns]

        style_cell_conditional = [
                                    {
                                        'if': {'column_id': table_columns[0]['id']},
                                        'backgroundColor': columns_color_fill[1],
                                        'textAlign': 'left',
                                        # "width": "18%"
                                    }
                                ] + [
                                    {
                                        'if': {'column_id': c['id']},
                                        'backgroundColor': columns_color_fill[1],
                                        'textAlign': 'center'
                                    } for c in table_columns[1:]
                                ] + [
                                    {
                                        'if': {'column_id': i},
                                        # 'fontWeight': 'bold',
                                        "width": "28%"
                                    } for i in ['Regional District Projections']
                                ] + [
                                    {
                                        'if': {'column_id': i['id']},
                                        # 'fontWeight': 'bold',
                                        "width": "24%"
                                    } for i in table_columns[1:]
                                ]
        # print(style_cell_conditional)
        return table_columns, table.to_dict('records'), style_data_conditional, style_cell_conditional, style_header_conditional


@callback(
    Output('table_13', 'columns'),
    Output('table_13', 'data'),
    Output('table_13', 'style_data_conditional'),
    Output('table_13', 'style_cell_conditional'),
    Output('table_13', 'style_header_conditional'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('area-scale-store', 'data'),
    Input('table_13', 'selected_columns'),
)
def update_table_13(geo, geo_c, scale, selected_columns):
    # Single area mode
    # print(geo)
    if geo == geo_c or geo_c == None or (geo == None and geo_c != None):

        # When no area is selected
        if geo == None and geo_c != None:
            geo = geo_c
        elif geo == None and geo_c == None:
            geo = default_value

        # Area Scaling up/down when user clicks area scale button on page 1
        if "to-geography-1" == scale:
            geo = geo
        elif "to-region-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Region'].tolist()[0]
        elif "to-province-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Province'].tolist()[0]
        else:
            geo = geo

        # geo_id = mapped_geo_code.loc[mapped_geo_code['Geo_Code'] == geo, :]['Geo_Code'].tolist()[0]

        # pdb.set_trace()


        # Generating table
        table = table_generator(geo, table_13, "table_13")
        table = number_formatting(table, [('Households', '2021')], 0)
        table = number_formatting(table, [('Households', '2041'), ('New Units', '')], 3)
        # table['Regional Growth Rate'] = table['Regional Growth Rate'].map(lambda x: '{:,.3f}%'.format if pd.notna(x) else x)
        table[('Regional Growth Rate', '')] = table[('Regional Growth Rate', '')].apply(lambda x: f"{x:.3f}%" if pd.notna(x) and x != 'n/a' else x)
        style_data_conditional = generate_style_data_conditional(table)
        style_header_conditional = generate_style_header_conditional(table)

        blank_row = pd.DataFrame([[None] * len(table.columns)], columns=table.columns)

        # Split the DataFrame into two parts
        df_top = table.iloc[:3]
        df_bottom = table.iloc[3:]

        # Concatenate the parts together with the blank row in between
        # pdb.set_trace()
        new_table = pd.concat([df_top, blank_row, df_bottom]).reset_index(drop=True)
        # print(new_table)

        table_columns = [{"name": [geo, col1, col2], "id": f"{col1}_{col2}"} for col1, col2 in new_table.columns]
        # table_columns.append({'name': [geo]})

        table_data = [
            {
                **{f"{x1}_{x2}": y for (x1, x2), y in data},
            }
            for (n, data) in [
                *enumerate([list(x.items()) for x in new_table.T.to_dict().values()])
            ]
        ]

        style_cell_conditional = [
                                    {
                                        'if': {'column_id': table_columns[0]['id']},
                                        'backgroundColor': columns_color_fill[1],
                                        'textAlign': 'left',
                                        # "width": "18%"
                                    }
                                ] + [
                                    {
                                        'if': {'column_id': c['id']},
                                        'backgroundColor': columns_color_fill[1],
                                        'textAlign': 'center'
                                    } for c in table_columns[1:]
                                ]+ [
                                    {
                                        'if': {'column_id': i},
                                        # 'fontWeight': 'bold',
                                        "width": "30%"
                                    } for i in ['Growth Scenarios']
                                ] + [
                                    {
                                        'if': {'column_id': i['id']},
                                        # 'fontWeight': 'bold',
                                        "width": "17.5%"
                                    } for i in table_columns[1:]
                                ]
        new_data_style = generate_additional_data_style(new_table, table_columns)
        style_data_conditional.extend(new_data_style)

        first_and_last_columns_ids = [table_columns[0]['id'], table_columns[-1]['id']]
        add_total_data_style = [
            {
                'if': {'row_index': len(new_table) - 3, 'column_id': j},
                'border-right': 'none',
                # 'rowSpan': 2

            } for j in ['Regional Growth Rate_', 'Households_2021']

        ] + [
            {
                'if': {'row_index': len(new_table) - 2, 'column_id': j['id']},
                'color': 'transparent',
                'backgroundColor': 'transparent',
                'border-left': 'none',
                'border-right': 'none'

                # 'rowSpan': 2

            } for j in table_columns
        ] + [
            {
                'if': {'row_index': len(new_table)-1, 'column_id': j},
                'border-bottom': '1px solid #002145',
                'border-left': '1px solid #002145',
                'border-right': '1px solid #002145',

                # 'rowSpan': 2

            } for j in first_and_last_columns_ids
        ]+ [
            {
                'if': {'row_index': len(new_table)-1, 'column_id': j['id']},
                'border-bottom': '1px solid #002145',

                # 'rowSpan': 2

            } for j in table_columns[1:-1]
        ]
        style_data_conditional.extend(add_total_data_style)
        return table_columns, table_data, style_data_conditional, style_cell_conditional, style_header_conditional


@callback(
    Output('table_14', 'columns'),
    Output('table_14', 'data'),
    Output('table_14', 'style_data_conditional'),
    Output('table_14', 'style_cell_conditional'),
    Output('table_14', 'style_header_conditional'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('area-scale-store', 'data'),
    Input('table_14', 'selected_columns'),
)
def update_table_14(geo, geo_c, scale, selected_columns):
    # Single area mode
    # print(geo)
    if geo == geo_c or geo_c == None or (geo == None and geo_c != None):

        # When no area is selected
        if geo == None and geo_c != None:
            geo = geo_c
        elif geo == None and geo_c == None:
            geo = default_value

        # Area Scaling up/down when user clicks area scale button on page 1
        if "to-geography-1" == scale:
            geo = geo
        elif "to-region-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Region'].tolist()[0]
        elif "to-province-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Province'].tolist()[0]
        else:
            geo = geo

        # Generating table
        table = table_generator(geo, table_14, "table_14")
        table = number_formatting(table, ['Renter Households'], 0)
        table = number_formatting(table, ['Estimated Number of Units'], 3)
        # table = percent_formatting(table, ['Vacancy Rate', 'Occupied Rate'], 0)
        # table['Regional Growth Rate'] = table['Regional Growth Rate'].map(lambda x: '{:,.3f}%'.format if pd.notna(x) else x)
        # table['Regional Growth Rate'] = table['Regional Growth Rate'].apply(lambda x: f"{x:.3f}%" if pd.notna(x) else x)
        table['Vacancy Rate'] = table['Vacancy Rate'].apply(lambda x: f"{x:.3f}%" if pd.notna(x) and x != 'n/a' else x)
        table['Occupied Rate'] = table['Occupied Rate'].apply(lambda x: f"{x:.3f}%" if pd.notna(x) and x != 'n/a' else x)
        # table['Renter Households'] = table['Renter Households'].shift()

        # print(table)
        if not table.empty:
            # table.loc[table[''].index[-1]] = table.loc[table[''].index[-1]].str.replace("n/a", '')

            index_number = table['Renter Households'].index[0]
            table.at[index_number + 1, 'Renter Households'] = table.at[index_number, 'Renter Households']

        style_data_conditional = generate_style_data_conditional(table)

        style_header_conditional = [
            {
                'if': {'header_index': 0},
                'backgroundColor': '#002145',
                'color': '#FFFFFF',
                'border': '1px solid #002145'
            },
            {
                'if': {'header_index': 1},
                'backgroundColor': '#39C0F7',
                'color': '#000000',
                'border': '1px solid #002145'
                # 'width': '60px',
                # 'minWidth': '60%',
            },
            {
                'if': {'header_index': 2},
                'backgroundColor': '#39C0F7',
                'color': '#000000',
                'border': '1px solid #002145'

            }
        ]
        # Generating callback output to update table
        # col_list = []
        # pdb.set_trace()
        table_columns = [{"name": [geo, col], "id": col} for col in table.columns]

        style_cell_conditional = [
                                    {
                                        'if': {'column_id': table_columns[0]['id']},
                                        'backgroundColor': columns_color_fill[1],
                                        'textAlign': 'left',
                                        # "width": "18%"
                                    }
                                ] + [
                                    {
                                        'if': {'column_id': c['id']},
                                        'backgroundColor': columns_color_fill[1],
                                        'textAlign': 'center'
                                    } for c in table_columns[1:]
                                ]

        merge_data_style = [
            {
                'if': {'row_index': 0, 'column_id': j},
                'backgroundColor': '#b0e6fc',
                'color': '#b0e6fc',
                'border-bottom': 'none',
                'rowSpan': 2

            }
            for j in ['Renter Households']

        ]
        style_data_conditional.extend(merge_data_style)

        new_data_style = generate_additional_data_style(table, table_columns)
        style_data_conditional.extend(new_data_style)
        return table_columns, table.to_dict('records'), style_data_conditional, style_cell_conditional, style_header_conditional


@callback(
    Output('table_15', 'columns'),
    Output('table_15', 'data'),
    Output('table_15', 'style_data_conditional'),
    Output('table_15', 'style_cell_conditional'),
    Output('table_15', 'style_header_conditional'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('area-scale-store', 'data'),
    Input('table_15', 'selected_columns'),
)
def update_table_15(geo, geo_c, scale, selected_columns):
    # Single area mode
    # print(geo)
    if geo == geo_c or geo_c == None or (geo == None and geo_c != None):

        # When no area is selected
        if geo == None and geo_c != None:
            geo = geo_c
        elif geo == None and geo_c == None:
            geo = default_value

        # Area Scaling up/down when user clicks area scale button on page 1
        if "to-geography-1" == scale:
            geo = geo
        elif "to-region-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Region'].tolist()[0]
        elif "to-province-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Province'].tolist()[0]
        else:
            geo = geo

        # Generating table
        table = table_generator(geo, table_15, "table_15")
        table = number_formatting(table, ['Result'], 3)
        style_data_conditional = generate_style_data_conditional(table)
        style_header_conditional = generate_style_header_conditional(table)

        blank_row = pd.DataFrame([[None] * len(table.columns)], columns=table.columns)

        # Split the DataFrame into two parts
        df_top = table.iloc[:5]
        df_bottom = table.iloc[5:]

        # Concatenate the parts together with the blank row in between
        # pdb.set_trace()
        new_table = pd.concat([df_top, blank_row, df_bottom]).reset_index(drop=True)

        # print(new_table)
        # Generating callback output to update table
        # col_list = []
        # pdb.set_trace()
        table_columns = [{"name": [geo, col], "id": col} for col in new_table.columns]

        style_cell_conditional = [
                                    {
                                        'if': {'column_id': table_columns[0]['id']},
                                        'backgroundColor': columns_color_fill[1],
                                        'textAlign': 'left',
                                        # "width": "18%"
                                    }
                                ] + [
                                    {
                                        'if': {'column_id': c['id']},
                                        'backgroundColor': columns_color_fill[1],
                                        'textAlign': 'right'
                                    } for c in table_columns[1:]
                                ] + [
                                    {
                                        'if': {'column_id': i},
                                        # 'fontWeight': 'bold',
                                        "width": "40%"
                                    } for i in ['Component']
                                ] + [
                                    {
                                        'if': {'column_id': i['id']},
                                        # 'fontWeight': 'bold',
                                        "width": "60%"
                                    } for i in table_columns[1:]
                                ]
        new_data_style = generate_additional_data_style(new_table, table_columns)
        style_data_conditional.extend(new_data_style)
        add_total_style = [
            {
                'if': {'row_index': len(new_table) - 4, 'column_id': j['id']},
                'fontWeight': 'bold'
                # 'rowSpan': 2

            } for j in table_columns
        ] + [
            {
                'if': {'row_index': len(new_table) - 3, 'column_id': j['id']},
                'color': 'transparent',
                'backgroundColor': 'transparent',
                'border-left': 'none',
                'border-right': 'none'

                # 'rowSpan': 2

            } for j in table_columns
        ] + [
            {
                'if': {'row_index': len(new_table)-1, 'column_id': j['id']},
                'border-bottom': '1px solid #002145',
                'border-left': '1px solid #002145',
                'border-right': '1px solid #002145',

                # 'rowSpan': 2

            } for j in table_columns
        ]
        style_data_conditional.extend(add_total_style)
        return table_columns, new_table.to_dict('records'), style_data_conditional, style_cell_conditional, style_header_conditional


@callback(
    Output('table_16', 'columns'),
    Output('table_16', 'data'),
    Output('table_16', 'style_data_conditional'),
    Output('table_16', 'style_cell_conditional'),
    Output('table_16', 'style_header_conditional'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('area-scale-store', 'data'),
    Input('table_16', 'selected_columns'),
)
def update_table_16(geo, geo_c, scale, selected_columns):
    # Single area mode
    # print(geo)
    if geo == geo_c or geo_c == None or (geo == None and geo_c != None):

        # When no area is selected
        if geo == None and geo_c != None:
            geo = geo_c
        elif geo == None and geo_c == None:
            geo = default_value

        # Area Scaling up/down when user clicks area scale button on page 1
        if "to-geography-1" == scale:
            geo = geo
        elif "to-region-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Region'].tolist()[0]
        elif "to-province-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Province'].tolist()[0]
        else:
            geo = geo

        # Generating table
        table = table_generator(geo, table_16, "table_16")
        # print(table.dtypes)
        table['5 Year Need'] = table['5 Year Need'].round(3)
        table['20 Year Need'] = table['20 Year Need'].round(3)
        # table = number_formatting(table, ['5 Year Need', '20 Year Need'], 3)
        # print(table.dtypes)

        if not table.empty:
            index_5yr, index_20yr = table['5 Year Need'].index[-2], table['20 Year Need'].index[-1]
            table['5 Year Need'][index_5yr] = '{:,.0f}'.format(float(table['5 Year Need'][index_5yr]))
            table['20 Year Need'][index_20yr] = '{:,.0f}'.format(float(table['20 Year Need'][index_20yr]))

            for idx in table.index:
                if idx != index_5yr:
                    table.at[idx, '5 Year Need'] = '{:,.3f}'.format(float(table.at[idx, '5 Year Need']))
                if idx != index_20yr:
                    table.at[idx, '20 Year Need'] = '{:,.3f}'.format(float(table.at[idx, '20 Year Need']))

        # min_index = table['Component'].index[0]
        # print(min_index)
        # Create a blank row

        style_data_conditional = generate_style_data_conditional(table)
        style_header_conditional = generate_style_header_conditional(table)
        # Generating callback output to update table
        # col_list = []
        # pdb.set_trace()
        table_columns = [{"name": [geo, col], "id": col} for col in table.columns]

        style_cell_conditional = [
                                    {
                                        'if': {'column_id': table_columns[0]['id']},
                                        'backgroundColor': columns_color_fill[1],
                                        'textAlign': 'left',
                                        # "width": "18%"
                                    }
                                ] + [
                                    {
                                        'if': {'column_id': c['id']},
                                        'backgroundColor': columns_color_fill[1],
                                        'textAlign': 'right'
                                    } for c in table_columns[1:]
                                ] + [
                                    {
                                        'if': {'column_id': i},
                                        # 'fontWeight': 'bold',
                                        "width": "40%"
                                    } for i in ['Component']
                                ] + [
                                    {
                                        'if': {'column_id': i['id']},
                                        # 'fontWeight': 'bold',
                                        "width": "30%"
                                    } for i in table_columns[1:]
                                ]
        add_style_5_year = [
            {
                'if': {'row_index': len(table) - 2, 'column_id': j['id']},
                'fontWeight': 'bold'
                # 'rowSpan': 2

            } for j in table_columns
        ] + [
        {
            'if': {'row_index': len(table) - 2, 'column_id': j['id']},
            'fontWeight': 'bold',
             'backgroundColor': '#74d3f9',
            'color': '#000000'

        } for j in table_columns
    ] + [
            {
                'if': {'row_index': len(table) - 1 , 'column_id': j},
                'backgroundColor': '#74d3f9',
                'color': '#74d3f9',
            }
            for j in ['5 Year Need']

        ] + [
            {
                'if': {'row_index': len(table) - 2 , 'column_id': j},
                'backgroundColor': '#74d3f9',
                'color': '#74d3f9',
            }
            for j in ['20 Year Need']

        ]
        # style_data_conditional.extend(merge_data_style)
        new_data_style = generate_additional_data_style(table, table_columns)
        style_data_conditional.extend(new_data_style)
        style_data_conditional.extend(add_style_5_year)
        return table_columns, table.to_dict('records'), style_data_conditional, style_cell_conditional, style_header_conditional