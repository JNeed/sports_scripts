from dash import Dash, dcc, html, Input, Output
from db.db import get_table
import pandas as pd
import numpy as np
import plotly.express as px
from web_scraping import main_web

df = get_table('player', 'sqlite:///db/nba.db')
teams = np.sort(df.TEAM.unique())
bos = df.query("TEAM == 'Bos'")

app = Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(teams, value = 'Bos', id='teams'),
    html.Div(id='dd-output-container'),
    dcc.Dropdown(options=bos.NAME, value = 'Jayson Tatum', id='players'),
    dcc.Dropdown(options=['FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'FT', 'FTA', 'FT%', 'ORB',
       'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'GmSc', '+/-'],id='stats'),
    dcc.Graph(id = 'graph')
],style = {'width':'25%'})


@app.callback(
    Output('players','options'),
    Input('teams', 'value')
)
def update_output(value):
    players = df.query('TEAM == @value').NAME
    return players

@app.callback(
    Output('graph','figure'),
    Input('players','value'),
    Input('stats','value')
)

def update_graph(p,stat):
    player = main_web(p, 2023)
    # print(player.columns)
    # player.Date = pd.to_datetime(player['Date']).dt.to_period('d')
    player.PTS = player['PTS'].astype('int32')
    player.FG = player['FG'].astype('int32')
    player.FGA = player['FGA'].astype('int32')
    player['FG%'] = player['FG%'].astype('float')
    player['3P'] = player['3P'].astype('int32')
    player['3PA'] = player['3PA'].astype('int32')
    player['3P%'] = player['3P%'].astype('float')
    player.FT = player['FT'].astype('int32')
    player.FTA = player['FTA'].astype('int32')
    player['FT%'] = player['FT%'].astype('float')
    player.ORB = player['ORB'].astype('int32')
    player.DRB = player['DRB'].astype('int32')
    player.TRB = player['TRB'].astype('int32')
    player.AST = player['AST'].astype('int32')
    player.STL = player['STL'].astype('int32')
    player.BLK = player['BLK'].astype('int32')
    player.TOV = player['TOV'].astype('int32')
    player.PF = player['PF'].astype('int32')
    player.GmSc = player['GmSc'].astype('float')
    player['+/-'] = player['+/-'].astype('int32')

    fig = px.scatter(player, 'Date',stat)
    return fig


app.run_server(debug=True)
