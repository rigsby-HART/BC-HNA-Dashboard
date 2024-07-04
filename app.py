# Import necessary libraries
from dash import html, dcc, clientside_callback
from dash.dependencies import Input, Output
from dash_extensions import EventListener

# from dash_extensions import Download
# from dash_extensions.snippets import send_file
# Connect to main app_file.py file
from app_file import app

# Connect to app pages
# from pages import page1, page2, page3, page4, page5, page6, page7, page8
from pages import page1, page2


# Define the index page layout
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Button("Export to PDF", id="export_to_pdf_btn", n_clicks=0),
        html.Div(id="page-content", children=[]),
    ]
)

server = app.server

# @app.callback(Output("download", "data"), [Input("btn", "n_clicks")])
# def func(n_clicks):
#     return dcc.send_file("././Untitled.png")


# Create the callback to handle multipage inputs
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/page1":
        return page1.layout
    if pathname == "/page2":
        return page2.layout
    else:  # if redirected to unknown link
        return "404 Page Error! Please choose a link"


# Client-side callback for export to PDF button
app.clientside_callback(
    """
    function(n_clicks) {
        if (n_clicks > 0) {
            const { jsPDF } = window.jspdf;
            const doc = new jsPDF();
            doc.addPage(document.getElementById('page-content'));
            doc.save('sample-file.pdf');
        }
    }
    """,
    Input("export_to_pdf_btn", "n_clicks"),
)

# Run the app on localhost:8050
if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")
