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

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='The Weather Station'),

    #Auto-refresh
    dcc.Interval(
        id='interval-component',
        interval=1*20000,  # Milliseconds
        n_intervals=0),

    #Display current temperatures
    html.Div([html.H4(children=u'Current temperature (\xb0c)'), html.Table(id='display-current-temp')]),

    #Show timeseries of temperatures
    dcc.Graph(
        id='temperature-graph',
    ),
])


@app.callback(Output('display-current-temp', 'children'),
                   [Input('interval-component', 'n_intervals')])
def display_current_temp(n):
    return _display_table(db.current_temp())

@app.callback(Output('temperature-graph', 'figure'),
                   [Input('interval-component', 'n_intervals')])
def display_total_graph(n):
    df = db.all_temp_data(1)

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

