import dash
import dash_bootstrap_components as dbc
import json
import pandas as pd
import numpy as np
import json
from dash.dependencies import Input, Output, State
from utils import typek
import dash_core_components as dcc
import dash_html_components as html
from app import app

def create_layout(app):

    df = pd.read_excel('corner.xlsx')
    cem_type1 = df['цемент'].unique()[0]
    cem_type2 = df['цемент'].unique()[1]

    for i in df.columns[4:]:
        var_so3_1 = round ( (df.loc[df['цемент'] == cem_type1][i].tail(14).std())/(df.loc[df['цемент'] == cem_type1][i].tail(14).mean())*100,1)
        var_so3_2 = round( (df.loc[df['цемент'] == cem_type2][i].tail(14).std())/(df.loc[df['цемент'] == cem_type2][i].tail(14).mean())*100,1)
        if  var_so3_1 > 6 :
            comments1 = 'коэффициент вариации оценка - плохо'
        elif var_so3_2 >6 :
            comments2 = 'коэффициент вариации оценка - плохо'

        else :
            comments1 = 'коэффициент вариации оценка - хорошо'
            comments2 = 'коэффициент вариации оценка - хорошо'



    def cardik(name, parameter, values, comments, colum):

        return     [
        dbc.CardHeader(name),
        dbc.CardBody(
        [
            html.H5(parameter, className="card-title"),
            html.P(colum, className ="card-text"),
            html.P( values,
                className="card-text",
            ),
            html.P(comments, className="card-text")
        ]
               ),
        ]

    return dbc.Container(
                            [dbc.Row(
                                       dbc.Col(html.H3('Выводы'),  style ={'height': '100%', 'textAlign':'center'}),className = ' mb-3 mt-3'
                                    ),
                             dbc.Row ([
                                       dbc.Col([dbc.Card(cardik(cem_type1, 'коэффициент вариации', var_so3_1, comments1, i))], width=6,className = 'mb-3 shadow  rounded'),
                                       dbc.Col([dbc.Card(cardik(cem_type2, 'коэффициент вариации', var_so3_2, comments2,i))], width=6,className = 'mb-3 shadow  rounded')

                                       ])
                            ]
                         )
