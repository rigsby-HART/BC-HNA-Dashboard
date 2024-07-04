
# Defining the Dash App and it's attributes

import dash
import dash_bootstrap_components as dbc

external_scripts = [
    {"src":"https://cdnjs.cloudflare.com/ajax/libs/html2canvas/0.4.1/html2canvas.min.js"},
    {"src":"https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"}
]

app = dash.Dash(__name__,
                external_scripts=external_scripts,
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{"name": "viewport", "content": "width=device-width"}],
                suppress_callback_exceptions=True)