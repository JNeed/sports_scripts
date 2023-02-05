from bokeh.plotting import figure, show
import pandas as pd
from bokeh.models import BoxAnnotation, HoverTool, PanTool, ResetTool
from auto_completion import create_autocomplete
from bokeh.models import AutocompleteInput,CustomJS
from bokeh.layouts import column
from bokeh import events

def make_player_scatter(player,year,table,all_players):
    x = pd.to_datetime(table['Date']).dt.to_period('d')
    y = table['PTS'].astype('int32')

    played_bool = y.apply(lambda x: x != -1)
    p = figure(title=player+ " " + str(year) + " Season Points", x_axis_label="Date", y_axis_label="Points Scored", x_axis_type='datetime',tools = [HoverTool(tooltips=[('date', '@x{%F}'), ('points','@y')],formatters={'@x':'datetime','@y':'numeral'}), PanTool(), ResetTool()])

    low_box = BoxAnnotation(top=y[played_bool].quantile(.2), fill_alpha=0.2, fill_color='red')
    high_box = BoxAnnotation(bottom=y[played_bool].quantile(.8), fill_alpha=0.2, fill_color='green')

    p.add_layout(low_box)
    p.add_layout(high_box)

    p.scatter(x[played_bool], y[played_bool], legend_label="Points", color = 'blue',size=5)
    p.scatter(x[~played_bool], y[~played_bool], legend_label="Didn't Play", color = 'red',marker='x',size = 10)
    
    ac = create_autocomplete('Enter NBA Player Name Here', 'NAME', all_players)

    # ac.on_change('value',cb)
    # some_var = 'bob'
    # callback = CustomJS(args=dict(autocomp = ac,sv = some_var),code="""
    # some_var = ac.value;
    # """)
    # ac.js_on_event()
    # ac.js_on_event(events.)
    # ac.js_on_change("value",callback)

    # print(some_var)

    # def update_value(attr,old,new):
    #     print("Selected val: ",ac.value)
    # ac.on_change("value",update_value)

    show(column(ac,p))

    # cb = CustomJS(args=dict(ac=ac),code="ac.value")

    # callback = ac.js_on_change("value", "event.target.value")
    # val = ac.js_on_change('value', cb)

    # print(val)
# def cb(attr,old,new):
#     print(ac.value)

    # def some_callback(attr,old,newer):
    #     print('prev label ', old)
    #     print('new lab: ', newer)
    # stored = ac.on_change('value',some_callback)
    # print(stored)