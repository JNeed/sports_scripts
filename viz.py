from bokeh.plotting import figure, show
from web_scraping import main_web
import pandas as pd


table = main_web()

# print(table)
# # # prepare some data
x = table['Date']
# x = pd.to_datetime(table['Date'], unit='d')

y = table['PTS']
# # # create a new plot with a title and axis labels
p = figure(title="Donovan Mitchell Points", x_axis_label="Date", y_axis_label="Points Scored")

# # # add a line renderer with legend and line thickness
p.line(x, y, legend_label="Points", line_width=2)

# # # show the results
show(p)