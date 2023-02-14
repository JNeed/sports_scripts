from playwright.sync_api import sync_playwright
import pandas as pd
from io import StringIO

def playwright_start(p):
    chromium = p.chromium
    browser = chromium.launch(headless=True)
    page = browser.new_page()
    return (page,browser)

def get_team_pergame_table(team_name, p):
    page,browser = playwright_start(p)
    full_url = "https://www.basketball-reference.com/teams/" + team_name.upper() + "/2023.html#all_per_minute-playoffs_per_minute"

    try:
        page.goto(full_url,timeout=1500)
    except:
        html_table = pd.read_html(full_url)
        table = html_table[1]
        page.close()
        browser.close()
        print(table)
        return table

def get_injury_report(p):
    page,browser = playwright_start(p)
    full_url = "https://www.basketball-reference.com/friv/injuries.fcgi"

    try:
        page.goto(full_url,timeout=1500)
    except:
        html_table = pd.read_html(full_url)
        table= html_table[0]
        print('injury tables ', table)
        print('len of injury tables ', len(table))

        page.close()
        browser.close()
        # print(table)
        return table



def get_team_per_game_stats(team_name):
    table = ''
    with sync_playwright() as p:
        table = get_team_pergame_table(team_name,p)
    return table

def inj():
    table = ''
    with sync_playwright() as p:
        table = get_injury_report(p)
    return table


inj()
# get_team_per_game_stats("BOS")

# get injury report from here https://www.basketball-reference.com/friv/injuries.fcgi
# could keep running list of injured players and list injured players on page