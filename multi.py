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
    dcc.Dropdown(options=df.NAME.tolist(), id='players',multi=True),
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
def update_player(player_names):
    if player_names == None:
        return
    player_df_json_ls = []
    for name in player_names:
        player = main_web(name, 2023)
        player["Minutes Played"] = player.MP.str.replace(":",".").astype(float)
        m = player["Minutes Played"].min()
        player["Minutes Played"] = player["Minutes Played"].fillna(m)
        for col in player.columns[10:]:
            if ('%' in col) or (col == 'GmSc'):
                player[col] = player[col].astype('float')
            elif ('%' not in col) and (col != 'GmSc') and (col != 'Minutes Played'):
                player[col] = player[col].astype('int32')
            
        injured = player.PTS.apply(lambda x: "Didn't Play" if x == -1 else "Played")
        player["Played Status"] = injured
        player_df_json_ls.append(player.to_json(date_format='iso', orient='split'))
    return player_df_json_ls
    


    # player = main_web(val, 2023)
    # player["Minutes Played"] = player.MP.str.replace(":",".").astype(float)
    # m = player["Minutes Played"].min()
    # player["Minutes Played"] = player["Minutes Played"].fillna(m)
    # for col in player.columns[10:]:
    #     if ('%' in col) or (col == 'GmSc'):
    #         player[col] = player[col].astype('float')
    #     elif ('%' not in col) and (col != 'GmSc') and (col != 'Minutes Played'):
    #         player[col] = player[col].astype('int32')
            
    # injured = player.PTS.apply(lambda x: "Didn't Play" if x == -1 else "Played")
    # player["Played Status"] = injured
    # return player.to_json(date_format='iso', orient='split')

@app.callback(
    Output('graph','figure'),
    Input('stats','value'),
    Input('intermediate-value','data')
)
def update_graph(stat, players_json_dfs):
    # return go.Figure()
    if players_json_dfs == None or stat == None:
        return go.Figure()
    symbols = ['circle','x']
    fig = go.Figure()
    for i,p in enumerate(players_json_dfs):
        player = pd.read_json(p, orient='split')
        if i == 0:
            fig = px.scatter(player, 'Date',stat,symbol = player["Played Status"],color=player["Minutes Played"],color_continuous_scale='blues',symbol_sequence=symbols)
        else:
            # fig.add_trace(px.scatter(player, 'Date',stat,color = player['Minutes Played'],color_continuous_scale='redor',symbol_sequence=symbols))

            fig.add_trace(go.Scatter(x=player.Date,y=player[stat],mode='markers',marker_color = player['Minutes Played'],marker=dict(size=8,colorscale = 'redor')))

            # fig.add_trace(go.Scatter(x=player.Date,y=player[stat],mode='markers'),marker_color = player['Minutes Played'],colorscale='redor')
    fig.update_layout(legend=dict(
            yanchor="bottom",
            xanchor="left"),legend_title_text='Played Status',plot_bgcolor='#dbdbdb')
    return fig
    # fig = px.scatter(player, 'Date',stat,symbol = player["Played Status"],color=player["Minutes Played"],color_continuous_scale='blues',symbol_sequence=symbols)
    # fig.update_layout(legend=dict(
    #     yanchor="bottom",
    #     xanchor="left"),legend_title_text='Played Status',plot_bgcolor='#dbdbdb')
    # return fig
    
app.run_server(debug=True)
