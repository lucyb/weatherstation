# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from plotly.graph_objs import *
import pandas as pd
import datetime
import os

import database as db

class Dashboard:

    def serve_layout():
        return html.Div(children=[
            html.H1(children='The Weather Station'),

            #Auto-refresh
            dcc.Interval(
                id='interval-component',
                interval=1*20000,  # Milliseconds
                n_intervals=0),

            #Display current temperatures
            html.Div([html.H4(children=u'Current temperature (\xb0c)'), html.Table(id='display-current-temp')]),

            #Show timeseries of temperatures
            dcc.Graph(id='temperature-graph'),

        ])

app = dash.Dash()
#app.config.supress_callback_exceptions = True
app.layout = Dashboard.serve_layout


@app.callback(Output('display-current-temp', 'children'),
                   [Input('interval-component', 'n_intervals')])
def display_current_temp(n):
    return _display_table(db.current_temp())

@app.callback(Output('temperature-graph', 'figure'),
                   [Input('interval-component', 'n_intervals')])
def display_total_graph(n):
    return _build_graph()

def _build_graph():
    sensors = db.sensor_list()
    
    timeseries = []
    for index, sensor in sensors.iterrows():
        timeseries.append(_build_timeseries(sensor['id'], sensor['name']))

    layout = dict(
            title='Temperature',
            height=600,
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label='last hour',
                             step='hour',
                             stepmode='backward'),
                        dict(step='all'),
                    ])
                ),
                rangeslider=dict(),
                type='date'
            )
    )

    return go.Figure(
            data=timeseries,
            layout=layout,
            )

def _build_timeseries(id, name):    
    df = db.temp_data_last_day(id)

    timeseries = go.Scatter(
            x = df['Time'],
            y = df['Temp'],
            name = name,
            opacity = 0.8
            )

    return timeseries

def _display_table(dataframe, max_rows=1000):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

if __name__ == '__main__':
    app.server.run(host='0.0.0.0')

