# Import necessary libraries
from dash import html, dcc, callback_context, no_update, Input, Output, State
import dash
import pandas as pd
from io import BytesIO

from app_file import app

# Connect to app pages
from pages import page1, page2
# Dynamically import the tables
from pages.page2 import *

# Define the index page layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', children=[]),
    # Add external scripts for jsPDF and html2canvas
    html.Script(src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.4.0/jspdf.umd.min.js"),
    html.Script(src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"),
    html.Script(src="https://raw.githack.com/eKoopmans/html2pdf/master/dist/html2pdf.bundle.js"),
    dcc.Download(id="download-dataframe-xlsx"),
    dcc.Store(id='current-page', data='', storage_type='memory'),
])

server = app.server

# Create the callback to handle multipage inputs
@app.callback(
    Output('page-content', 'children'),
    Output('current-page', 'data'),
    [Input('url', 'pathname')],
)
def display_page(pathname):
    if pathname == '/page1':
        return page1.layout, 'page1'
    elif pathname == '/page2':
        return html.Div([
            page2.layout,
            # Add the export table buttons here
            html.Div(id='export-buttons', children=[
                html.Button(id=f"export-table-{i}", n_clicks=0, style={'display': 'none'}) for i in range(1, 16)
            ], style={'display': 'none'})
        ]), 'page2'
    else:
        return "404 Page Error! Please choose a link"

app.clientside_callback(
     """
    function(n_clicks){
        if(n_clicks > 0){
            var opt = {
                margin: 1,
                filename: 'myfile.pdf',
                image: { type: 'jpeg', quality: 0.98 },
                html2canvas: { scale: 3},
                jsPDF: { unit: 'cm', format: 'a2', orientation: 'p' },
                pagebreak: { mode: ['avoid-all'] }
            };
            html2pdf().from(document.getElementById("page-content-to-print")).set(opt).save();
        }
    }
    """,
    Output('dummy-output', 'children'),
    Input('export-button', 'n_clicks')
)

table_functions = {
    'export-table-1': (update_table_4a, "Table1a"),
    'export-table-2': (update_table_4b, "Table1b"),
    'export-table-3': (update_table_5, "Table2"),
    'export-table-4': (update_table_6, "Table3"),
    'export-table-5': (update_table_7a, "Table4a"),
    'export-table-6': (update_table_7b, "Table4b"),
    'export-table-7': (update_table_8, "Table5"),
    'export-table-8': (update_table_9, "Table6"),
    'export-table-9': (update_table_10, "Table7"),
    'export-table-10': (update_table_11, "Table8"),
    'export-table-11': (update_table_12, "Table9"),
    'export-table-12': (update_table_13, "Table10"),
    'export-table-13': (update_table_14, "Table11"),
    'export-table-14': (update_table_15, "Table12"),
    'export-table-15': (update_table_16, "Table13"),
}

@app.callback(
    Output("download-dataframe-xlsx", "data"),
    [Input(f"export-table-{i}", "n_clicks") for i in range(1, 16)] +
    [Input('current-page', 'data'), Input('main-area', 'data'), Input('comparison-area', 'data'), Input('area-scale-store', 'data')],
    prevent_initial_call=True,
)
def download_xlsx(*args):
    current_page = args[-4]
    if current_page != 'page2':
        return no_update

    ctx = callback_context
    if not ctx.triggered:
        return no_update

    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if not triggered_id.startswith("export-table"):
        return no_update

    print(ctx.triggered)

    # if ctx.triggered[0]["value"] == 0:
    #     return no_update

    geo = args[-3]
    geo_c = args[-2]
    scale = args[-1]

    func, filename_template = table_functions.get(triggered_id, (None, None))
    if func is None:
        return no_update

    # Update the table based on the geo parameter
    column_names, data_table, _, _, _ = func(geo, geo_c, scale, None)
    filename = f"{geo}_{filename_template}.xlsx"

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        pd.DataFrame(data_table).to_excel(writer, index=False)
    output.seek(0)
    return dcc.send_bytes(output.read(), filename=filename)


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
