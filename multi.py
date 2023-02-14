from dash import Dash, dcc, html, Input, Output
from db.db import get_table
import pandas as pd
import numpy as np
import plotly.express as px
from web_scraping import main_web
import plotly.graph_objects as go
from team_scraping import get_team_per_game_stats

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
    dcc.Store(id = 'intermediate-value'),
    dcc.Store(id = 'player-names'),
    # dcc.Dropdown([i+1 for i in range(df.NAME.tolist())], id='num_to_agg')

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

@app.callback(
    Output('player-names','data'),
    Input('players','value')
)
def get_player_names(player_names):
    return player_names

@app.callback(
    Output('graph','figure'),
    Input('stats','value'),
    Input('intermediate-value','data'),
    Input('player-names','data')
)
def update_graph(stat, players_json_dfs,names):
    # TODO: add aggregation; need to handle case in which one player is injured and others aren't

    color_scales = ['Redor','Greys','BuGn','Blues',"Purples"]
    if players_json_dfs == None or stat == None:
        return go.Figure()
    injured_symbols = ['x','triangle-up','hash','asterisk','square']
    fig = go.Figure()
    
    for i,p in enumerate(players_json_dfs):
        symbols = ['circle',injured_symbols[i]]
        player = pd.read_json(p, orient='split')
        mp = player['Minutes Played']
        stat_series = player[stat]
        if i == 0:
            fig = px.scatter(player, 'Date',stat,symbol = player["Played Status"],color=player["Minutes Played"],color_continuous_scale=color_scales[i],symbol_sequence=symbols)
        else:
            a = player['Played Status']
            injured_symbol = player["Played Status"].apply(lambda x: 'circle' if x=="Played" else injured_symbols[i])
            fig.add_scatter(x = player.Date, y=player[stat],mode='markers',marker_color = player['Minutes Played'],marker=dict(size=6,colorscale = color_scales[i], symbol=injured_symbol),name=names[i],
                hovertemplate =
                    '<b>Name</b>: %{name}'+
                    "<br><b>Date</b>: %{x}<br>"+
                    "<br><b>Stat Value</b>: %{y}<br>")
            fig.update_layout(legend=dict(
                yanchor="bottom",
                xanchor="left"),legend_title_text='Played Status',plot_bgcolor='#dbdbdb')
    return fig

    # @app.callback(
    # Output('agg_reporter','value'),
    # Input('num_to_agg','value'),
    # Input('teams','value')
    # )
    # def agg_n_players(n,team_name):

    #     team_stats = get_team_per_game_stats(team_name)
    #     # don't forget to get injury report
    #     pass

app.run_server(debug=True)

# idea: go to this page (the per 36 table - will prob need an adjusted timeout + try catch again) https://www.basketball-reference.com/teams/BOS/2023.html#all_per_minute-playoffs_per_minute
# and get the table of players. sort_values('MP') and get the name field and read that into a list
# go thru each name one by one until you get 7, checking each one if their points are == -1; can concatenate these
# dataframes; no need to keep them separate because we will agg them anyway;
# idea: use team choice from above dropdown to get team; have dropdown for first n players we want to agg; agg on
# stat chosen in above dropdown