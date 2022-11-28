import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import callback_context
import dash
import os
import importlib
import dash_table
from dash.exceptions import PreventUpdate
import pandas as pd
import time
from datetime import datetime
from app import app





def create_layout(app):
    df = pd.read_excel('corner.xlsx')
    return   dbc.Container( dbc.Card([

                             dbc.Row(
                                dbc.Col(html.H3('Парметры помола цемента '),
                                style={"height": "100%", "textAlign" :"center"})),


                       dbc.Row(
                           dbc.Col(
                              dash_table.DataTable(id = 'table_mill', data = df.to_dict("records"), export_format='xlsx',
                                 export_headers='display',
                                 columns = [{'id': df.columns[0], 'name': df.columns[0]},
                                 {'id': df.columns[1], 'name': df.columns[1], 'presentation': 'dropdown'},
                                 {'id': df.columns[2], 'name': df.columns[2], 'presentation': 'dropdown'},
                                 {'id': df.columns[3], 'name': df.columns[3], 'presentation': 'dropdown'},
                                 {'id': df.columns[4], 'name': df.columns[4]},
                                 {'id': df.columns[5], 'name': df.columns[5]},
                                 {'id': df.columns[6], 'name': df.columns[6]},
                                 {'id': df.columns[7], 'name': df.columns[7]},

                                 ],



                                 editable=True,
                                 style_header={ "backgroundColor": "#1E90FF", "fontSize": "18px","color": "white", 'textAlign': 'center', 'height': 'auto', 'width':'auto'},
                                 style_data={'whiteSpace': 'normal', 'height': 'auto' },
                                 fixed_rows={"headers": False},style_cell={"width": "auto", "fontSize": "auto",'textAlign': 'center'},
                                style_data_conditional=[
                                  {
                                   'if': {'row_index': 'odd'},'backgroundColor': 'lightsteelblue'},

                                   {'if': {'column_id': 'время'},
                                      'whiteSpace': 'normal','height': 'auto', 'lineHeight': '15px' }
                                                        ],


                                 # page_count=100,
                                 # style_table={'height': '3000px', 'overflowY': 'auto'},
                                  filter_action="native",
                                  sort_action="native",
                                  sort_mode="multi",
                                  page_action="native",
                                  page_current= round( len(df)/14),
                                  page_size= 14,
                                  row_deletable=True,
                                  dropdown={
            df.columns[2]: {
                'options': [
                    {'label': i, 'value': i} for i in ['1','2']

                ], 'clearable':True,
            },

            df.columns[1]: {
                    'options': [
                        {'label': i, 'value': i} for i in [str(x) for x  in list((i)  for i in range(1, 25))]

                    ], 'clearable':True,
                },
            df.columns[3]: {
                 'options': [
                    {'label': i, 'value': i} for i in ['ПЦ-500 Д20','ПЦ-500 Д0', 'ПЦ-400 Д0', 'ПЦ-400 Д20']

                ]
            }
        }
                                                ), className = 'block'
                                      )
                             ),



                          dbc.Row(
                             dbc.Col([
                                 dbc.Button('добавить строку', id='row_button',
                              n_clicks=0, outline=True, size ='lg', color = 'primary'),
                                 dbc.Button('сохранить', id='save_button',
                                 n_clicks=0, outline=True,  size ='lg', color ="primary")], #style={"height": "100%"}

                              )

                             ),

     ],style = { "padding": "1rem "}),  className = 'shadow-lg  rounded ')



@app.callback(
    Output('table_mill', 'data'),
    Input('row_button', 'n_clicks'),
    Input('save_button', 'n_clicks'),
    State('table_mill', 'data'),
    State('table_mill', 'columns'))
def add_row(row_clicks,save_click, rows, columns):
    ctx = dash.callback_context
    ctrl_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if  ctrl_id == 'row_button':
        #rows.append({columns[1]: time.ctime()})
        rows.append({c['id']: datetime.fromtimestamp(time.time()).strftime("%d %m %Y, %H:%M") for c in columns[:1]})

        df1 = pd.DataFrame(rows, columns=[c['name'] for c in columns])


        df1.to_excel('corner.xlsx', index=False)

    elif ctrl_id == 'save_button':
        df2 = pd.DataFrame(rows, columns=[c['name'] for c in columns])

        df2.to_excel('corner.xlsx',index=False)

    return rows
