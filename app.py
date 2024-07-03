# Import necessary libraries
from dash import html, dcc
from dash.dependencies import Input, Output
# from dash_extensions import Download
# from dash_extensions.snippets import send_file
# Connect to main app_file.py file
from app_file import app

# Connect to app pages
# from pages import page1, page2, page3, page4, page5, page6, page7, page8
from pages import page1, page2

# Define the index page layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', children=[]),
    # html.Button("Download", id="btn"), dcc.Download(id="download"),
    # # Add external scripts for jsPDF and html2canvas
    # html.Script(src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.4.0/jspdf.umd.min.js"),
    # html.Script(src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/0.4.1/html2canvas.min.js"),
])

server = app.server

# @app.callback(Output("download", "data"), [Input("btn", "n_clicks")])
# def func(n_clicks):
#     return dcc.send_file("././Untitled.png")

# Create the callback to handle multipage inputs
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page1':
        return page1.layout
    if pathname == '/page2':
        return page2.layout
    else: # if redirected to unknown link
        return "404 Page Error! Please choose a link"

# Client-side callback for export to PDF button
# app.clientside_callback(
#     """
#     function(n_clicks) {
#         if (n_clicks > 0) {
#             const { jsPDF } = window.jspdf;
#             const content = document.getElementById('page-content-to-print');
#             html2canvas(content, {
#                 scale: 2,
#                 useCORS: true
#             }).then(canvas => {
#                 const pdf = new jsPDF('p', 'pt', 'a4');
#                 const imgData = canvas.toDataURL('image/png');
#                 const imgWidth = 595.28;
#                 const pageHeight = 841.89;
#                 const imgHeight = canvas.height * imgWidth / canvas.width;
#                 let heightLeft = imgHeight;
#                 let position = 0;
#
#                 pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
#                 heightLeft -= pageHeight;
#
#                 while (heightLeft >= 0) {
#                     position = heightLeft - imgHeight;
#                     pdf.addPage();
#                     pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
#                     heightLeft -= pageHeight;
#                 }
#                 pdf.save('dashboard.pdf');
#             });
#         }
#         return "";
#     }
#     """,
#     Output('dummy-output', 'children'),
#     Input('export-button', 'n_clicks')
# )
# Run the app on localhost:8050
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
