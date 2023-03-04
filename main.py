from dash import Dash, dcc, html, Input, Output
from db.db import get_table
import pandas as pd
import numpy as np
import plotly.express as px
from web_scraping import main_web
import plotly.graph_objects as go
from team_scraping import get_team_per_game_stats,inj,get_all_players_and_teams


teams_ls_dict = [{'label':'Atlanta Hawks','value':'ATL'},{'label':'Boston Celtics','value':'BOS'},{'label':'Philadelphia 76ers','value':'PHI'},{'label':'New York Knicks','value':'NYK'},{'label':'Brooklyn Nets','value':'BRK'},{'label':'Toronto Raptors','value':'TOR'},{'label':'Miluakee Bucks','value':'MIL'},{'label':'Cleveland Cavaliers','value':'CLE'},{'label':'Chicago Bulls','value':'CHI'},{'label':'Indiana Pacers','value':'IND'},{'label':'Detroit Pistons','value':'DET'},{'label':'Miami Heat','value':'MIA'},{'label':'Washing Wizards','value':'WAS'},{'label':'Orlando Magic','value':'ORL'},{'label':'Charlotte Hornets','value':'CHO'},{'label':'Denver Nuggets','value':'DEN'},{'label':'Minnesota Timberwolves','value':'MIN'},{'label':'Utah Jazz','value':'UTA'},{'label':'Oklahoma City Thunder','value':'OKC'},{'label':'Portland Trail Blazers','value':'POR'},{'label':'Sacramento Kings','value':'SAC'},{'label':'Phoenix Suns','value':'PHO'},{'label':'Golden State Warriors','value':'GSW'},{'label':'Los Angeles Clippers','value':'LAC'},{'label':'Los Angeles Lakers','value':'LAL'},{'label':'Memphis Grizzlies','value':'MEM'},{'label':'Dallas Mavericks','value':'DAL'},{'label':'New Orleans Pelicans','value':'NOP'},{'label':'San Antonio Spurs','value':'SAS'},{'label':'Houston Rockets','value':'HOU'},{'label':'All','value':'All'}]
# df = get_table('player', 'sqlite:///db/nba.db')
df = get_all_players_and_teams()


app = Dash(__name__)

app.layout = html.Div([
    # TODO: Add true team names as labels to the teams dropdown e.g. Bos -> Celtics
    dcc.Dropdown(options = teams_ls_dict, value = 'All', id='teams'),
    dcc.Dropdown(options=df.Player.tolist(), id='players',multi=True),
    dcc.Dropdown(options=['FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'FT', 'FTA', 'FT%', 'ORB',
       'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'GmSc', '+/-'],id='stats'),
    dcc.Graph(id = 'graph'),
    dcc.Store(id = 'intermediate-value'),
    dcc.Store(id = 'player-names'),
    dcc.Dropdown(options = [i+1 for i in range(len(df.Player.tolist())+1)], id='num_to_agg'),
    html.P(id="agg_reporter"),
    html.P(id="injured_players")
    # ,html.P(id="injury_report")

],style = {'width':'25%'})


@app.callback(
    Output('injured_players','children'),
    Input('teams', 'value')
)
def update_output(value):
    # TODO Figure out why I'm not getting injured players from the team I want
    if value == "All":
        return
    players = df.query('Tm == @value').Player
    injured = inj().Player
    # print(injured)

    # injured = inj().Player.str.split().str[1:].str.join(sep=' ')
    result = []
    # print('injured: ', injured)
    for a in injured:
        if a.lower() in players.str.lower():
            result.append(a)
    s = ', '.join(result)
    # if not result:
    #     return f"No {value} players are injured"
    return f"The following {value} players are injured: {s}"


@app.callback(
    Output('players','options'),
    Input('teams', 'value')
)
def update_output(value):
    if value == "All":
        return df.Player
    players = df.query('Tm == @value').Player
    return players

@app.callback(
    Output('num_to_agg','options'),
    Input('teams', 'value')
)
def agg_n_players(team_name):
    num_players_on_team = len(df.query('Tm == @team_name').Tm)
    return [i+1 for i in range(num_players_on_team+1)]

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
            fig = px.scatter(player, 'Date',stat,symbol = player["Played Status"],color=player["Minutes Played"],color_continuous_scale=color_scales[i],symbol_sequence=symbols,labels=names[i])
        else:
            a = player['Played Status']
            injured_symbol = player["Played Status"].apply(lambda x: 'circle' if x=="Played" else injured_symbols[i])
            fig.add_scatter(x = player.Date, y=player[stat],mode='markers',marker_color = player['Minutes Played'],marker=dict(size=6,colorscale = color_scales[i], symbol=injured_symbol),name=names[i],
                hovertemplate =
                    '<b>Name</b>: %{name}'+
                    "<br><b>Date</b>: %{x}<br>"+
                    "<br><b>Stat Value</b>: %{y}<br>")
            # fig.update_layout(legend=dict(
            #     yanchor="bottom",
            #     xanchor="left"), plot_bgcolor='#dbdbdb')
    return fig

@app.callback(
Output('agg_reporter','children'),
Input('num_to_agg','value'),
Input('teams','value')
)
def agg_n_players(n,team_name):
    if team_name == 'All':
        return
    team_stats = get_team_per_game_stats(team_name)
    # don't forget to get injury report
    mp = round(team_stats['MP'].sum(),2)
    return f'The total number of minutes played per player per game on this team is: {mp}'

# TODO fix team names in url creation e.g. Brooklyn should be BRK, not BRO


app.run_server(debug=True)


# idea: go to this page (the per 36 table - will prob need an adjusted timeout + try catch again) https://www.basketball-reference.com/teams/BOS/2023.html#all_per_minute-playoffs_per_minute
# and get the table of players. sort_values('MP') and get the name field and read that into a list
# go thru each name one by one until you get 7, checking each one if their points are == -1; can concatenate these
# dataframes; no need to keep them separate because we will agg them anyway;
# idea: use team choice from above dropdown to get team; have dropdown for first n players we want to agg; agg on
# stat chosen in above dropdown