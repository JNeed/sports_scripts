from bokeh.models import AutocompleteInput
from bokeh.io import show
from sqlalchemy import create_engine, text


# def create_autocomplete(text, col,df):
#     completion_list = df[col].tolist()
#     auto_complete_input =  AutocompleteInput(title=text, completions=completion_list)
#     show(auto_complete_input)

def create_autocomplete(text, col,df):
    completion_list = df[col].tolist()
    auto_complete_input =  AutocompleteInput(title=text, completions=completion_list, case_sensitive=False)
    return auto_complete_input