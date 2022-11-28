import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash
import pandas as pd
import numpy as np
import time
from datetime import datetime
from app import app
import plotly.express as px
config= {'displaylogo': False}
import plotly.graph_objects as go
from utils import smoothTriangle



def create_layout(app):
    df = pd.read_excel('corner.xlsx')
    return dbc.Container([

                         dbc.Row(dbc.Col(html.H3('Статистический анализ'), style ={'height': '100%', 'textAlign':'center'}),className = ' mb-3 mt-3' ),
                         dbc.Row([dbc.Col(dbc.Card([dbc.CardHeader(html.H3(id ='ralling_average', className="card-title")), dbc.CardBody("Kоэффициент вариации")],  body=True,color="light" ), width=2,className = 'mb-3 shadow  rounded'  ),
                                  dbc.Col(dbc.Card([dbc.CardHeader(html.H3(id = 'mean')), dbc.CardBody("Cреднее значение за период")],color="#00BFFF", inverse=True, body=True), width=2, className = 'mb-3 shadow  rounded' ),
                                  dbc.Col(dbc.Card([dbc.CardHeader(html.H3(id = 'value_compitability')),dbc.CardBody("Соответсвие системы спецификации")], color='#127aba', inverse = True,  body=True), width=2, className = 'mb-3 shadow  rounded' )], justify="around" ),
                         dbc.Row([dbc.Col([dcc.Dropdown(id ='dropdown_yaxes', value = df.columns[-1],  options = [{'label':i, 'value':i} for i in list(df.columns[4:])]),]),
                                  dbc.Col(dcc.Dropdown(id ='cement_type', options = [{'label':i, 'value':i} for i in list(df.iloc[0:, 3].dropna().unique())]+[{'label':'все типы', 'value': 'все типы'}], value ='все типы')),
                                  dbc.Col([dcc.Dropdown(id ='period', options = [{'label':  '1 неделя', 'value': 24},  {'label': 'месяц', 'value':24*30 }, {'label': '3 месяца', 'value': 24*90},
                                                                                           {'label': 'весь период', 'value': len(df)}], value = 24*30, persistence =True)



                                  ]) ]),
                         dbc.Row([
                            dbc.Col(dbc.Card(dcc.Graph(id ='rolling_average', config=config)), className = 'shadow  rounded pagination-lg ', width=6),
                            dbc.Col(dbc.Card(dcc.Graph(id = 'system_compitability', config = config)), className = 'shadow  rounded ', width =6)
                             ], justify = "around", className = "mb-3"),
                         dbc.Row([
                             dbc.Col(dbc.Card(dcc.Graph(id ='mean_time', config = config)), className = 'shadow  rounded pagination-lg ', width =6),
                             dbc.Col(dbc.Card(dcc.Graph(id ='limitation', config = config)), className = 'shadow  rounded pagination-lg ', width=6)
                             ], justify ="around")

                         ], fluid = True)

@app.callback(
            Output('rolling_average', 'figure'),
            Output('system_compitability', 'figure'),
            Output('ralling_average', 'children'),
            Output('mean', 'children'),
            Output('mean_time', 'figure' ),
            Output('value_compitability', 'children'),
            Output('limitation', 'figure'),
            Input('dropdown_yaxes', 'value'),
            Input('period', 'value'),
            Input ('cement_type', 'value')
            )
def update_graph(yaxis_column_name, period, cement_type):

    g = pd.read_excel('corner.xlsx')
    g.time = pd.to_datetime(g.time, dayfirst=True)
    if cement_type == 'все типы':
        g = g
    else:
         g = g.loc[g['цемент'] == cement_type]


    if yaxis_column_name == ' помол. 80 мкм' or yaxis_column_name == ' помол, 45 мкм':
        g[yaxis_column_name]=100-g[yaxis_column_name]
    else:
        g[yaxis_column_name] = g[yaxis_column_name]


    fig = px.scatter(g, x = 'time', y = g[yaxis_column_name].rolling(14).std()/ g[yaxis_column_name].rolling(14).mean()*100, color = g[yaxis_column_name].rolling(14).std()/ g[yaxis_column_name].rolling(14).mean()*100,
    color_continuous_scale=["white", "blue", "red"] , title = 'стабильность качества (коэффициент вариации)' )
    fig.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01        ))
    fig.add_hline(y=5, line_width=1, line_dash="dash", line_color="gray")

    fig.add_trace(go.Scatter(
    x= g.time,
    y=smoothTriangle(g[yaxis_column_name].rolling(14).std()/ g[yaxis_column_name].rolling(14).mean()*100,5),  # setting degree to 10
    mode='lines',line=dict(color='red', width=2, dash='dot'),
    marker=dict(
        size=6,
        color='#C190F0',
        symbol='141'
    ),
    name='линия тренда'
     ))
    fig2 = px.histogram(g.tail(period), x = yaxis_column_name,  template="simple_white", title = 'гистограмма распределения')
    fig2.update_yaxes( showgrid=True )

    rolling_average = round((g[yaxis_column_name].rolling(14).std()/ g[yaxis_column_name]).iloc[-1]*100,2)
    mean = round( g[yaxis_column_name].tail(period).mean(), 2)
    fig2.add_vline(x=mean, line_width=8, line_dash="dash", line_color="red")
    fig3 = px.scatter(g.tail(period), x= g.tail(period).index, y = yaxis_column_name, trendline ="lowess", title = "абсолютное значение параметра и линия тренда", color = g[yaxis_column_name].tail(period), color_continuous_scale=["red", "blue", "white"])
    fig4 = px.line(g, x= 'time', y = yaxis_column_name, template="simple_white", title ="соответствие системы заданным параметрам качества")
    fig4.update_yaxes( showgrid=True )

    limitation_capability = pd.read_csv('jope1111.csv')

    if cement_type == 'все типы':
        cement_type= limitation_capability['type'].unique()[0]
    else:
        cement_type = cement_type

    y1 =limitation_capability[yaxis_column_name].loc[(limitation_capability['цемент']== 'low') & (limitation_capability['type'] == cement_type)].values[0]
    y2= limitation_capability[yaxis_column_name].loc[(limitation_capability['цемент']== 'top') & (limitation_capability['type'] == cement_type)].values[0]

    fig4.add_hline(y=y1 , line_width=2, line_dash="dash", line_color="red")
    fig4.add_hline(y=y2 , line_width=2, line_dash="dash", line_color="red")
    comp = round ((y2-y1)/ (g[yaxis_column_name].std()*6),2)


    return fig, fig2, rolling_average, mean, fig3, comp, fig4
