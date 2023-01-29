from playwright.sync_api import sync_playwright
import pandas as pd
from io import StringIO

def name_handling(player_name):
    fname,lname = player_name.lower().split()
    lname_short = lname
    fletter_lname = lname[0]
    if len(lname) > 4:
        lname_short = lname_short[:5]
    fname_short = fname
    if len(fname)> 1:
        fname_short = fname_short[:2]
    return (fname_short,lname_short)

def table_process_write(fname_short,lname_short,write_excel, html_table):
    header_bool = html_table['Rk'].apply(lambda x: x!= 'Rk')
    html_table = html_table[header_bool]
    html_table = html_table.replace(['Inactive', 'Did Not Dress', 'Did Not Play'],-1)
    if write_excel:
        xl = fname_short +'_'+ lname_short + '.xlsx'
        html_table.to_excel(xl)
    return html_table

def playwright_start(p):
    chromium = p.chromium
    browser = chromium.launch(headless=True)
    page = browser.new_page()
    return (page,browser)

def player_gamelog(player_name, year, p):
    page,browser = playwright_start(p)
    fname_short,lname_short = name_handling(player_name)

    base = "https://www.basketball-reference.com/players/"
    full_url = base + lname_short[0] + '/' + lname_short + fname_short + '01/gamelog/'+ str(year)

    try:
        page.goto(full_url,timeout=1500)
    except:
        html_table = pd.read_html(full_url)[7]
        table = table_process_write(fname_short, lname_short, False, html_table)
        page.close()
        browser.close()
        return (table,page,browser)

def main_web():
    table = ''
    with sync_playwright() as p:
        player = 'Donovan Mitchell'
        y = 2023 # must be in format yyyy
        table = player_gamelog(player, y, p)
    return table