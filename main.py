from web_scraping import main_web
from scatter import make_scatter
player = 'Donovan Mitchell'
year = 2023 # must be in format yyyy
table = main_web(player,year)
make_scatter(player, year, table)