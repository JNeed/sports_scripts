from dash import Dash, dcc, html, Input, Output
from db.db import get_table
import pandas as pd
import numpy as np
import plotly.express as px
from web_scraping import main_web
import plotly.graph_objects as go

df = get_table('player', 'sqlite:///db/nba.db')
teams = np.append(np.sort(df.TEAM.unique()),"All")
bos = df.query("TEAM == 'Bos'")

app = Dash(__name__)

app.layout = html.Div([
    # TODO: Add true team names as labels to the teams dropdown e.g. Bos -> Celtics
    dcc.Dropdown(teams, value = 'All', id='teams'),
    dcc.Dropdown(options=df.NAME.tolist(), id='players'),
    dcc.Dropdown(options=['FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'FT', 'FTA', 'FT%', 'ORB',
       'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'GmSc', '+/-'],id='stats'),
    dcc.Graph(id = 'graph'),
    dcc.Store(id = 'intermediate-value')
],style = {'width':'25%'})


@app.callback(
    Output('players','options'),
    Input('teams', 'value')
)
def update_output(value):
    if value == "All":
        return df.NAME
    players = df.query('TEAM == @value').NAME
    return players

@app.callback(
    Output('intermediate-value','data'),
    Input('players','value')
)
def update_player(val):
    if val == None:
        return
    player = main_web(val, 2023)
    player["Minutes Played"] = player.MP.str.replace(":",".").astype(float)
    m = player["Minutes Played"].min()
    player["Minutes Played"] = player["Minutes Played"].fillna(m)
    for col in player.columns[10:]:
        if ('%' in col) or (col == 'GmSc'):
            player[col] = player[col].astype('float')
        elif ('%' not in col) and (col != 'GmSc') and (col != 'Minutes Played'):
            player[col] = player[col].astype('int32')
            
    injured = player.PTS.apply(lambda x: "Didn't Play" if x == -1 else "Played")
    # injured = pd.cut(player.PTS,[-1,0,1000],right=False,labels=["Didn't play", "Played"])
    player["Played Status"] = injured
    return player.to_json(date_format='iso', orient='split')

@app.callback(
    Output('graph','figure'),
    Input('stats','value'),
    Input('intermediate-value','data')
)
def update_graph(stat, p):
    if p == None or stat == None:
        return go.Figure()
    player = pd.read_json(p, orient='split')
    symbols = ['x','circle']
    fig = px.scatter(player, 'Date',stat,symbol = player["Played Status"],color=player["Minutes Played"],color_continuous_scale='blues',symbol_sequence=symbols)
    fig.update_layout(legend=dict(
        yanchor="bottom",
        xanchor="left"),legend_title_text='Played Status',plot_bgcolor='#dbdbdb')
    return fig
    
app.run_server(debug=True)
