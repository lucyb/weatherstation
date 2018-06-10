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

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='The Weather Station'),

    #Auto-refresh
    dcc.Interval(
        id='interval-component',
        interval=1*20000,  # Milliseconds
        n_intervals=0),

    #Display current temperature
    html.Div(id='display-current-temp'),

    #Show timeseries of temperatures
    dcc.Graph(
        id='temperature-graph',
    ),
])

@app.callback(Output('display-current-temp', 'children'),
                   [Input('interval-component', 'n_intervals')])
def display_current_temp(n):
    df = fetch_data()
    curr_temp = df.Temp.iloc[-1]
    return u'Current Temperature {:.2f}\xb0c'.format(curr_temp)

@app.callback(Output('temperature-graph', 'figure'),
                   [Input('interval-component', 'n_intervals')])
def display_total_graph(n):
    df = fetch_data()

    timeseries = go.Scatter(
            x = df['Time'],
            y = df['Temp'],
            name = 'Temp',
            line = dict(color = '#17BECF'),
            opacity = 0.8
            )

    layout = dict(
            title='Temperature',
            height=600,
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label='1d',
                             step='day',
                             stepmode='backward'),
                        dict(count=7,
                             label='week',
                             step='day',
                             stepmode='backward'),
                        dict(step='all')
                    ])
                ),
                rangeslider=dict(),
                type='date'
            )
    )

    return go.Figure(
            data=[timeseries],
            layout=layout,
            )

def fetch_data():
    df = pd.read_csv(get_temperature_log(),
         sep='\t',
         names=["Time", "Temp", "Temp (Smooth)"],
         parse_dates=["Time"])
    return df

def get_temperature_log():
    return os.getenv('TEMP_URL',
            "http://192.168.1.204:8000/temp.log")

if __name__ == '__main__':
    app.server.run(host='0.0.0.0')
