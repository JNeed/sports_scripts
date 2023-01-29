from bokeh.plotting import figure, show
from web_scraping import main_web
import pandas as pd
from bokeh.models import BoxAnnotation,DatetimeTickFormatter

player = 'Donovan Mitchell'
year = 2023 # must be in format yyyy
table = main_web(player,year)

x = pd.to_datetime(table['Date']).dt.to_period('d')

y = table['PTS'].astype('int32')

played_bool = y.apply(lambda x: x != -1)

p = figure(title=player+ " " + str(year) + " Season Points", x_axis_label="Date", y_axis_label="Points Scored", x_axis_type='datetime')


low_box = BoxAnnotation(top=y[played_bool].quantile(.2), fill_alpha=0.2, fill_color='red')
high_box = BoxAnnotation(bottom=y[played_bool].quantile(.8), fill_alpha=0.2, fill_color='green')

p.add_layout(low_box)
p.add_layout(high_box)

p.scatter(x[played_bool], y[played_bool], legend_label="Points", color = 'blue',size=5)
p.scatter(x[~played_bool], y[~played_bool], legend_label="Didn't Play", color = 'red',marker='x',size = 10)
p.xaxis[0].formatter = DatetimeTickFormatter(months="%B-%y")

show(p)
