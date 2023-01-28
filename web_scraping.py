from playwright.sync_api import sync_playwright
import pandas as pd

def player_lookup(player_name, p):
    chromium = p.chromium # or "firefox" or "webkit".
    browser = chromium.launch(headless=False)
    page = browser.new_page()

    fname,lname = player_name.lower().split()
    lname_short = lname
    fletter_lname = lname[0]

    if len(lname) > 4:
        lname_short = lname_short[:5]
        print('lname_short ', lname_short)
    fname_short = fname
    if len(fname)> 1:
        fname_short = fname_short[:2]

    base = "https://www.basketball-reference.com/players/"
    full_url = base + fletter_lname + '/' + lname_short + fname_short + '01.html'
    print(full_url)
    page.goto(full_url)
    page.close()
    browser.close()


def player_gamelog(player_name, year, p):
    chromium = p.chromium # or "firefox" or "webkit".
    browser = chromium.launch(headless=False)
    page = browser.new_page()

    fname,lname = player_name.lower().split()
    lname_short = lname
    fletter_lname = lname[0]

    if len(lname) > 4:
        lname_short = lname_short[:5]
    fname_short = fname
    if len(fname)> 1:
        fname_short = fname_short[:2]

    base = "https://www.basketball-reference.com/players/"

    full_url = base + fletter_lname + '/' + lname_short + fname_short + '01/gamelog/'+ str(year)
    try:
        page.goto(full_url,timeout=1000)
    except:
        # pts = page.query_selector("#pgl_basic\\.949 > td:nth-child(28)")
        # print('points: ', pts.inner_text())
        table = page.query_selector("#pgl_basic")
        table_str = table.inner_text().split()
        columns = table_str[:28]
        start_idx = 28
        end_idx = 58
        # print(columns)
        print(table_str[start_idx:end_idx])
        # print(table.inner_text().split())
        # print(table.inner_text().split())

        # print(type(table.inner_text()))

        # print(pd.DataFrame(table.inner_text()))
        # print(table.inner_text())


        
    page.close()
    browser.close()


## trying to find url pattern for players
# donovan mitchell: https://www.basketball-reference.com/players/m/mitchdo01.html
# kevin durant: https://www.basketball-reference.com/players/d/duranke01.html
# james harden: https://www.basketball-reference.com/players/h/hardeja01.html

# seems like the pattern is /players/first char of last name/first 5 chars of last name, first 2 chars of first name, 01.html
# what if their last name has less than 5 letters though?
# if their last name has less than 5 letters, just use all of the letters in the last name, still stick to 2 in first name
# ben uzoh: https://www.basketball-reference.com/players/u/uzohbe01.html


## Codegen
# def run(player, playwright: Playwright) -> None:
# ...
#     page.goto("https://www.basketball-reference.com/players/m/mitchdo01/gamelog/2023")
#     page.get_by_role("row", name="5 5 2022-10-28 26-051 CLE @ BOS W (+9) 1 45:42 15 25 .600 5 9 .556 6 6 1.000 0 4 4 3 1 0 7 4 41 25.2 +18").get_by_role("cell", name="41").click()
#     page.get_by_role("row", name="29 25 2022-12-14 26-098 CLE @ DAL W (+15) 1 37:38 13 20 .650 6 9 .667 2 2 1.000 1 2 3 4 1 0 3 5 34 25.3 +20").get_by_role("cell", name="1.000").click()
#     page.get_by_role("row", name="46 2023-01-18 26-133 CLE @ MEM L (-1) Inactive").get_by_role("cell", name="Inactive").click()

#     # ---------------------
#     context.close()
#     browser.close()


with sync_playwright() as p:
    player = 'Kevin Durant'
    y = 2023 # must be in format yyyy
    player_gamelog(player,y, p)