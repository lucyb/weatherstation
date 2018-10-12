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

class Sensors:

    TEMPERATURE = 'temperature'
    HUMIDITY = 'humidity'
    BATTERY = 'battery'

    def __init__(self):
        self._sensors = None

    @property
    def sensors(self):
        if not self._sensors:
            self._sensors = db.sensor_list()
        return self._sensors

class Dashboard:

    def serve_layout():
        return html.Div(children=[
            html.H2(children='The Weather Station'),

            #Auto-refresh
            dcc.Interval(
                id='interval-component',
                interval=1*20000,  # Milliseconds
                n_intervals=0),

            #Display current temperatures
            html.Div([html.Table(id='display-current-temp')]),

            #Show timeseries of temperatures
            dcc.Graph(id='temperature-graph'),

            #Show timeseries of humidity
            dcc.Graph(id='humidity-graph'),
        ])


app = dash.Dash()
#app.config.supress_callback_exceptions = True
app.layout = Dashboard.serve_layout

@app.callback(Output('display-current-temp', 'children'),
                   [Input('interval-component', 'n_intervals')])
def display_current_temp(n):
    sensors = Sensors().sensors
    readings = db.current_reading(list(sensors['id']))
    result = []
    for _, sensor in sensors.iterrows():
        result.append(html.Div(sensor['name']))
        rows = readings.loc[readings['id'] == sensor['id']]
        result.append(_display_table(rows))
    return result

@app.callback(Output('temperature-graph', 'figure'),
                   [Input('interval-component', 'n_intervals')])
def display_temperature_graph(n):
    sensors = Sensors().sensors

    timeseries = []
    for _, sensor in sensors.iterrows():
        df = db.temp_data_last_day(sensor['id'], Sensors.TEMPERATURE)
        timeseries.append(_build_timeseries(df, sensor['name']))

    return _build_graph('Today\'s Temperature', timeseries)

@app.callback(Output('humidity-graph', 'figure'),
                   [Input('interval-component', 'n_intervals')])
def display_humidity_graph(n):
    sensors = Sensors().sensors

    timeseries = []
    for _, sensor in sensors.iterrows():
        df = db.temp_data_last_day(sensor['id'], Sensors.HUMIDITY)
        timeseries.append(_build_timeseries(df, sensor['name']))

    return _build_graph('Today\'s Humidity', timeseries)

def _build_graph(title, timeseries):
    layout = dict(
            title=title,
            height=400,
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label='last hour',
                             step='hour',
                             stepmode='backward'),
                        dict(count=24,
                             label='last day',
                             step='hour',
                             stepmode='backward'),
                        dict(step='all',
                             label='last 3 days'),
                    ])
                ),
                type='date'
            )
    )

    return go.Figure(
            data=timeseries,
            layout=layout,
            )

def _build_timeseries(df, name):
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

