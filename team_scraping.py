from playwright.sync_api import sync_playwright
import pandas as pd
from io import StringIO

def playwright_start(p):
    chromium = p.chromium
    browser = chromium.launch(headless=True)
    page = browser.new_page()
    return (page,browser)

def get_team_per_game_stats(team_name):
    table = ''
    with sync_playwright() as p:
        page,browser = playwright_start(p)
        if team_name == 'All':
            pass
        full_url = "https://www.basketball-reference.com/teams/" + team_name.upper() + "/2023.html#all_per_minute-playoffs_per_minute"

        try:
            page.goto(full_url,timeout=1500)
        except:
            html_table = pd.read_html(full_url)
            table = html_table[1]
            page.close()
            browser.close()
            return table
        pass

def get_injury_report():
    table = ''
    with sync_playwright() as p:
        page,browser = playwright_start(p)
        full_url = "https://www.basketball-reference.com/friv/injuries.fcgi"

        try:
            page.goto(full_url,timeout=1500)
        except:
            html_table = pd.read_html(full_url)
            table= html_table[0]
            page.close()
            browser.close()
            return table
        pass

def get_all_players_and_teams():
    with sync_playwright() as p:
        page,browser = playwright_start(p)

        full_url = 'https://www.basketball-reference.com/contracts/players.html'
        try:
            page.goto(full_url,timeout=1500)
        except:
            html_table = pd.read_html(full_url)

            df = html_table[0]
            df.columns = [col[1] for col in df.columns]
            df = df[['Player','Tm']]

            page.close()
            browser.close()

            return df
        pass
    pass

get_all_players_and_teams()