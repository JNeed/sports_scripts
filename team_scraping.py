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

def get_injury_report(p):
    page,browser = playwright_start(p)
    full_url = "https://www.basketball-reference.com/friv/injuries.fcgi"

    try:
        page.goto(full_url,timeout=1500)
    except:
        html_table = pd.read_html(full_url)
        table= html_table[0]
        page.close()
        browser.close()
        # print(table)
        return table



def get_team_per_game_stats(team_name):
    table = ''
    with sync_playwright() as p:
        table = get_team_pergame_table(team_name,p)
    return table

def get_roster(team_name,p):
    table = ''
    page,browser = playwright_start(p)
    if team_name == 'All':
        pass
    full_url = "https://www.basketball-reference.com/teams/" + team_name.upper() + "/2023.html#all_roster"

    try:
        page.goto(full_url,timeout=1500)
    except:
        html_table = pd.read_html(full_url)
        # print('len of html_table: ', len(html_table))
        # table = html_table[1]
        # for i,t in enumerate(html_table):
        #     print('table ', str(i), ': ', t)
        page.close()
        browser.close()
        return table[0]
    return table

def get_all_players_and_teams():
    with sync_playwright() as p:
        page,browser = playwright_start(p)

        full_url = 'https://www.basketball-reference.com/contracts/players.html'
        try:
            page.goto(full_url,timeout=1500)
        except:
            html_table = pd.read_html(full_url)
            # table = html_table[1]
            # print('html tab: ',html_table)
            # print('len of html_tab: ',str(len(html_table)))
            # print('type html table: ',type(html_table))
            # print('type html table[0]: ',type(html_table[0]))


            # print('html table: ',html_table)
            df = html_table[0]
            df.columns = [col[1] for col in df.columns]
            df = df[['Player','Tm']]
            # print('type df: ',type(df))

            # print('df cos: ',df.columns)
            # print('df : ',df)

            # df = html_table[['Player','Tm']]
            page.close()
            browser.close()
            # return table
            return df
        pass
    pass



def inj():
    table = ''
    with sync_playwright() as p:
        table = get_injury_report(p)
    return table


get_all_players_and_teams()
    # print(get_injury_report(p))
# with sync_playwright() as p:
#     get_roster('BOS',p)
# get_team_per_game_stats("BOS")

# get injury report from here https://www.basketball-reference.com/friv/injuries.fcgi
# could keep running list of injured players and list injured players on page