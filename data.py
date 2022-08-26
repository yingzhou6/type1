import pandas as pd
import numpy as np
from datetime import datetime,timedelta
import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px

sdg = pd.read_csv('https://www.dropbox.com/s/fsxgf885s1f5bro/sdg_12_tickers.csv?dl=1',on_bad_lines='skip')
esg = pd.read_csv('https://www.dropbox.com/s/7h3k7v6z67q80df/esg_12_tickers.csv?dl=1',on_bad_lines='skip')
sent = pd.read_csv('https://www.dropbox.com/s/hv3p1d3xt4l9yvc/sentiment_12_tickers.csv?dl=1',on_bad_lines='skip')

ticker = sdg['Ticker'].unique()
ticker1 = esg['Ticker'].unique()
ticker2 = sent['Ticker'].unique()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])

server = app.server

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("ESG,SDG & Sentiment",
                        className='text-center text-primary, mb-3'),
                width=16)
    ]),
    dbc.Row([
    dbc.Col(html.H1("SDG",
                        className='text-center text-primary, mb-3'),
                width=16)
    ]),
    dbc.Row([
        dbc.Col([
            html.P('Select Stock:', style={'textDecoration': 'underline'}),
            dcc.Dropdown(id='my-company', multi=True, value=ticker,
                         options=[{'label': x, 'value': x}
                                  for x in ticker]),
            dcc.Graph(id='fig1', figure={})
        ], width={'size': 20}),
    ]),
    dbc.Row([
        dbc.Col(html.H1("ESG",
                        className='text-center text-primary, mb-3'),
                width=16)
    ]),
    dbc.Row([
        dbc.Col([
            html.P('Select Date:', style={'textDecoration': 'underline'}),
            dcc.Dropdown(id='my-date', multi=True, value=ticker1,
                            options=[{'label': x, 'value': x}
                                    for x in ticker1]),
            dcc.Graph(id='fig2', figure={})
        ], width={'size': 20}),
    ]),
    dbc.Row([
        dbc.Col(html.H1("Sentiment",
                        className='text-center text-primary, mb-3'),
                width=16)
    ]),
    dbc.Row([
        dbc.Col([
            html.P('Select Date:', style={'textDecoration': 'underline'}),
            dcc.Dropdown(id='my-sent', multi=True, value=ticker2,
                            options=[{'label': x, 'value': x}
                                    for x in ticker2]),
            dcc.Graph(id='fig3', figure={})
        ], width={'size': 20}),

        ])
    ])


@app.callback(
    Output('fig1', 'figure'),
    Input('my-company', 'value')
)
def update_graph(com):
    dff = sdg[sdg['Ticker'].isin(com)]
    fighist = px.line(dff, x = 'Timestamp',y = 'SDG_Mean',color = 'Ticker')
    return fighist


@app.callback(
    Output('fig2', 'figure'),
    Input('my-date', 'value')
)
def update_graph(com):
    dff = esg[esg['Ticker'].isin(com)]
    fighist = px.line(dff, x = 'Timestamp',y = 'ESG_Mean',color = 'Ticker')
    return fighist


@app.callback(
    Output('fig3', 'figure'),
    Input('my-sent', 'value')
)
def update_graph(com):
    dff = sent[sent['Ticker'].isin(com)]
    fighist = px.line(dff, x = 'Timestamp',y = 'Sentiment',color = 'Ticker')
    return fighist



if __name__ == '__main__':
    app.run_server(debug=True, port=8000)
