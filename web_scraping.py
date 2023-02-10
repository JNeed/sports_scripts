from playwright.sync_api import sync_playwright
import pandas as pd
from io import StringIO

EXCEPTIONS = {
'Javonte Green':'https://www.basketball-reference.com/players/g/greenja02/gamelog/2023',
'Jalen Green':'https://www.basketball-reference.com/players/g/greenja05/gamelog/2023',
'JaMychal Green':'https://www.basketball-reference.com/players/g/greenja01/gamelog/2023',
'Bogdan Bogdanovic':'https://www.basketball-reference.com/players/b/bogdabo01/gamelog/2023',
'Bojan Bogdanovic':'https://www.basketball-reference.com/players/b/bogdabo02/gamelog/2023',
'Jalen McDaniels':'https://www.basketball-reference.com/players/m/mcdanja01/gamelog/2023',
'Jaden McDaniels':'https://www.basketball-reference.com/players/m/mcdanja02/gamelog/2023',
'Julian Champagnie':'https://www.basketball-reference.com/players/c/champju02/gamelog/2023',
'Justin Champagnie':'https://www.basketball-reference.com/players/c/champju01/gamelog/2023',
'Ziaire Williams':'https://www.basketball-reference.com/players/w/willizi02/gamelog/2023',
'Zion Williamson':'https://www.basketball-reference.com/players/w/willizi01/gamelog/2023',
'Markieff Morris':'https://www.basketball-reference.com/players/m/morrima02/gamelog/2023',
'Marcus Morris Sr.':'https://www.basketball-reference.com/players/m/morrima03/gamelog/2023',
'James Johnson':'https://www.basketball-reference.com/players/j/johnsja01/gamelog/2023',
'Jalen Johnson':'https://www.basketball-reference.com/players/j/johnsja05/gamelog/2023',
'Jalen Smith':'https://www.basketball-reference.com/players/s/smithja04/gamelog/2023',
'Jabari Smith Jr.':'https://www.basketball-reference.com/players/s/smithja05/gamelog/2023',
'Jaylin Williams':'https://www.basketball-reference.com/players/w/willija07/gamelog/2023',
'Jalen Williams':'https://www.basketball-reference.com/players/w/willija06/gamelog/2023',
'Keon Johnson':'https://www.basketball-reference.com/players/j/johnske07/gamelog/2023',
'Keldon Johnson':'https://www.basketball-reference.com/players/j/johnske04/gamelog/2023'
}


def name_handling(player_name):
    name_ls = player_name.lower().split()
    fname,lname = name_ls[0],name_ls[1]
    # fname,lname = player_name.split()
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

    # player_name_ls = player_name.split()
    # search_term = player_name_ls[0].lower() + " " + player_name_ls[1].lower()
    if player_name in EXCEPTIONS.keys():
        try:
            page.goto(EXCEPTIONS[player_name],timeout=1500)
        except:
            html_table = pd.read_html(EXCEPTIONS[player_name])[7]
            table = table_process_write(fname_short, lname_short, False, html_table)
            page.close()
            browser.close()
            return table
    try:
        page.goto(full_url,timeout=1500)
    except:
        # fails for duplicate cases like Jaylen Brown and Jabari Brown both brownja
        html_table = pd.read_html(full_url)[7]
        table = table_process_write(fname_short, lname_short, False, html_table)
        page.close()
        browser.close()
        return table

def main_web(player, year):
    table = ''
    with sync_playwright() as p:
        table = player_gamelog(player, year, p)
    return table