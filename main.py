from web_scraping import main_web
from test2 import make_player_scatter
# from scatter import make_player_scatter
from db.db import get_table
from auto_completion import create_autocomplete
player = 'Donovan Mitchell'
year = 2023 # must be in format yyyy
table = main_web(player,year)
all_players = get_table('player','sqlite:///db/nba.db')
# create_autocomplete('Type the name of an NBA Player', 'NAME', all_players)

make_player_scatter(player, year, table,all_players)