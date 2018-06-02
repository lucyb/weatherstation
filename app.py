# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from plotly.graph_objs import *
import pandas as pd
import datetime

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='The Weather Station'),

    #Auto-refresh
    dcc.Interval(
        id='interval-component',
        interval=1*20000,  # Milliseconds
        n_intervals=0),

    #Show timeseries of temperatures
    dcc.Graph(
        id='temperature-graph',
    ),
])

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
            title='Dining Room Temperature',
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
    df = pd.read_csv("http://192.168.1.204:8000/temp.log",
         sep='\t',
         names=["Time", "Temp", "Temp (Smooth)"],
         parse_dates=["Time"])
    return df

def get_todays_data(df):
    today     = datetime.datetime.now()
    yesterday = pd.to_timedelta("1day")
    df.today  = df[df.Time > (today - yesterday)]
    return df.today

if __name__ == '__main__':
    app.run_server(debug=True)
