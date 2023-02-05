from bokeh.models import AutocompleteInput
from bokeh.io import show
from sqlalchemy import create_engine, text
from db.db import get_table

big_df = get_table('player','sqlite:///db/nba.db')

print(big_df['TEAM'].unique())

# def create_autocomplete(text, col,df):
#     completion_list = df[col].tolist()
#     auto_complete_input =  AutocompleteInput(title=text, completions=completion_list, case_sensitive=False)
#     # auto_complete_input.on_event('value',cb)
#     return auto_complete_input