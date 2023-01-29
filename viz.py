from bokeh.plotting import figure, show
from web_scraping import main_web
import pandas as pd

player = 'Donovan Mitchell'
year = 2023 # must be in format yyyy
table = main_web(player,year)

x = pd.to_datetime(table['Date']).dt.to_period('d')

y = table['PTS'].astype('int32')

played_bool = y.apply(lambda x: x != -1)

p = figure(title=player+ " " + str(year) + " Season Points", x_axis_label="Date", y_axis_label="Points Scored", x_axis_type='datetime')


p.scatter(x[played_bool], y[played_bool], legend_label="Points", color = 'blue',size=5)
p.scatter(x[~played_bool], y[~played_bool], legend_label="Didn't Play", color = 'red',marker='x',size = 10)

show(p)
