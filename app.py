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
])

server = app.server

# Create the callback to handle multipage inputs
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/page1':
        return page1.layout
    elif pathname == '/page2':
        return page2.layout
    else:
        return "404 Page Error! Please choose a link"

app.clientside_callback(
      """
    function(n_clicks, geo){
        if (n_clicks > 0 && geo){
            var opt = {
                margin: 1,
                filename: geo + '.pdf',
                image: { type: 'jpeg', quality: 0.98 },
                html2canvas: { scale: 3},
                jsPDF: { unit: 'cm', format: 'a2', orientation: 'p' },
                pagebreak: { mode: ['avoid-all', 'css', 'legacy'] }
            };
            html2pdf().from(document.getElementById("page-content-to-print")).set(opt).save();
        }
    }
    """,
    Output('dummy-output', 'children'),
    Input('export-button', 'n_clicks'),
    State('main-area', 'data')
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
    [State('main-area', 'data'), State('comparison-area', 'data'), State('area-scale-store', 'data')],
    prevent_initial_call=True,
)
def download_xlsx(*args):
    ctx = callback_context
    if not ctx.triggered:
        return no_update

    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if not triggered_id.startswith("export-table"):
        return no_update

    triggered_index = int(triggered_id.split("-")[-1])
    n_clicks = args[triggered_index - 1]  # -1 because args is zero-indexed

    # Check if the button was actually clicked
    if n_clicks is None:
        return no_update

    geo = args[-3]
    geo_c = args[-2]
    scale = args[-1]

    func, filename_template = table_functions.get(triggered_id, (None, None))
    if func is None:
        return no_update

    # Update the table based on the geo parameter
    column_names, data_table, _, _, _ = func(geo, geo_c, scale, None)
    filename = f"{geo}_{filename_template}.xlsx"

    # Function to handle the conversion
    def convert_value(val):
        try:
            if val == 'n/a':
                return val
            elif '%' in val:
                return float(val.replace('%', '')) / 100
            elif ',' in val and '.' in val:
                return float(val.replace(',', ''))
            elif ',' in val:
                return int(val.replace(',', ''))
            elif '.' in val:
                return float(val)
            else:
                return val
        except ValueError:
            return val

    table = pd.DataFrame(data_table)
    for col in table.columns:
        table[col] = table[col].apply(lambda x: convert_value(str(x)))

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        table.to_excel(writer, index=False)
    output.seek(0)
    return dcc.send_bytes(output.read(), filename=filename)


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
