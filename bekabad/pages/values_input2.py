import dash
import dash_bootstrap_components as dbc
import json
from app import app
import pandas as pd
import numpy as np
import json
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html


def create_layout(app):

    df2  = pd.read_excel('corner.xlsx')
    return  dbc.Container ([

                              dbc.Row(dbc.Col(html.I('Целевые параметры контроля качества помола'),  style={"height": "100%", "textAlign" :"center"}), className = "mb-3"),
                              dbc.Row([dbc.Col(dbc.Card(dcc.Dropdown(id ='dropdown_cement_type', value = df2.iloc[0:, 3].unique()[0],
                                   options = [{'label': i, 'value': i} for i in list(df2.iloc[0:, 3].dropna().unique())]
                                                                     )
                                                         )
                                             )

                                      ], className ="mb-4"
                                     )  ,

                                     dbc.Col ( html.Div(id = 'page_input'))

                             ])


@app.callback (Output ('page_input', 'children'),
               Input('dropdown_cement_type', 'value')

               )

def zalupa (cement_type):

    df = pd.read_csv('jope1111.csv')


    return html.Div(children = [


                                 dbc.Row( [

                                             dbc.Col(dbc.InputGroup(
                                                 [
                                                   dbc.InputGroupText("помол. 80 мкм, верхняя граница", style ={'width': '265px'}),
                                                   dbc.Input(placeholder="Amount", id = "residue80_top", value = df.loc[(df['цемент'] == 'top') & (df['type'] == cement_type  ), ' помол. 80 мкм' ].iloc[0],  type="number"),
                                                   dbc.InputGroupText("помол. 80 мкм, нижняя граница", style ={'width': '265px'}),
                                                   dbc.Input(placeholder="Amount", id = "residue80_low", value = df.loc[(df['цемент'] == 'low') & (df['type'] == cement_type  ), ' помол. 80 мкм' ].iloc[0], type="number" ),

                                                 ],
                                                 ))

                                          ], className = "mb-3"

                                         ),

                                 dbc.Row( [

                                             dbc.Col(dbc.InputGroup(
                                                 [
                                                   dbc.InputGroupText("помол, 45 мкм, верхняя граница", style ={'width': '265px'}),
                                                   dbc.Input(placeholder="Amount", id = "residue45_top", value = df.loc[(df['цемент'] == 'top') & (df['type'] == cement_type  ), ' помол, 45 мкм' ].iloc[0], type="number" ),
                                                   dbc.InputGroupText("помол, 45 мкм, нижняя граница", style ={'width': '265px'}),
                                                   dbc.Input(placeholder="Amount", id = "residue45_low", value = df.loc[(df['цемент'] == 'low') & (df['type'] == cement_type  ), ' помол, 45 мкм' ].iloc[0], type="number"),

                                                 ],
                                                 ))

                                          ], className = "mb-3"

                                         ),


                                 dbc.Row( [

                                             dbc.Col(dbc.InputGroup(
                                                 [
                                                   dbc.InputGroupText("уд.поверхность, верхняя граница", style ={'width': '265px'}),
                                                   dbc.Input(placeholder="Amount", id = "blain_top", value = df.loc[(df['цемент'] == 'top') & (df['type'] == cement_type  ), 'уд.поверхность' ].iloc[0], type="number"),
                                                   dbc.InputGroupText("уд.поверхность, нижняя граница", style ={'width': '265px'}),
                                                   dbc.Input(placeholder="Amount", id = "blain_low", value = df.loc[(df['цемент'] == 'low') & (df['type'] == cement_type  ), 'уд.поверхность' ].iloc[0], type="number"),

                                                 ],
                                                 ))

                                          ], className = "mb-3"

                                         ),

                                 dbc.Row( [

                                             dbc.Col(dbc.InputGroup(
                                                 [
                                                   dbc.InputGroupText("SO3,%, верхняя граница", style ={'width': '265px'}),
                                                   dbc.Input(placeholder="Amount", id = "so3_top", value = df.loc[(df['цемент'] == 'top') & (df['type'] == cement_type  ), 'SO3,%' ].iloc[0], type="number"),
                                                   dbc.InputGroupText("SO3,%, нижняя граница", style ={'width': '265px'}),
                                                   dbc.Input(placeholder="Amount", id = "so3_low", value  = df.loc[(df['цемент'] == 'low') & (df['type'] == cement_type  ), 'SO3,%' ].iloc[0], type="number"),

                                                 ],
                                                 ))

                                          ]

                                         ),

                                        html.Div(id = 'limitation')




                               ]
                    )

@app.callback (Output('limits', 'data'),
               Input('residue80_top', 'value'),
               Input('residue80_low', 'value'),
               Input ('residue45_top', 'value'),
               Input('residue45_low', 'value'),
               Input('blain_top', 'value'),
               Input('blain_low','value'),
               Input("so3_top", 'value'),
               Input('so3_low', 'value'),
               Input ('dropdown_cement_type', 'value')



               )

def enter_targets(residue80_top, residue80_low, residue45_top, residue45_low,
     blain_top, blain_low, so3_top, so3_low,cement_type):

     df = pd.read_csv('jope1111.csv')

     df.loc[(df['цемент'] == 'top') & (df['type'] == cement_type), ' помол. 80 мкм' ] = residue80_top

     df.loc[(df['цемент'] == 'low') & (df['type'] == cement_type), ' помол. 80 мкм' ] = residue80_low

     df.loc[(df['цемент'] == 'top') & (df['type'] == cement_type), ' помол, 45 мкм' ] = residue45_top

     df.loc[(df['цемент'] == 'low') & (df['type'] == cement_type), ' помол, 45 мкм' ] = residue45_low

     df.loc[(df['цемент'] == 'top') & (df['type'] == cement_type), 'уд.поверхность' ] = blain_top

     df.loc[(df['цемент'] == 'low') & (df['type'] == cement_type), 'уд.поверхность' ] = blain_low

     df.loc[(df['цемент'] == 'top') & (df['type'] == cement_type), 'SO3,%' ] = so3_top

     df.loc[(df['цемент'] == 'low') & (df['type'] == cement_type), 'SO3,%' ] = so3_low


     df.to_csv('jope1111.csv', index =False)



     hui = df.to_json(orient='records')
     return hui
