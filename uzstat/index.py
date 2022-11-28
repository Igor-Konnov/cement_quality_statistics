import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from app import app
from pages import table2, analysis, values_input2, summary


#CONTENT_STYLE = {

#    "padding": "1rem ",
    #"background-color":"PaleTurquoise"

#}

content = html.Div(id="page-content")

limits = dcc.Store(id='limits', data=None, storage_type='session')


def serve_layout():

    return html.Div([dcc.Location(id="url"), content, limits],  style = {'background-image': 'url("/assets/light.jpg"'} )

app.layout=serve_layout

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/table2":
        return table2.create_layout(app)
    elif pathname == "/analysis":
        return analysis.create_layout(app)
    elif pathname == "/values_input2":
        return values_input2.create_layout(app)
    elif pathname == "/summary":
        return summary.create_layout(app)    
    else:
        return analysis.create_layout(app)




if __name__ == "__main__":
    app.run_server(port=5000,debug=True, dev_tools_ui= True,dev_tools_props_check= True )
