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



# exceptions list
# 'Javonte Green':'https://www.basketball-reference.com/players/g/greenja02.html'
# 'Jalen Green':'https://www.basketball-reference.com/players/g/greenja05.html'
# 'JaMychal Green':'https://www.basketball-reference.com/players/g/greenja01.html'
# 'Bogdan Bogdanovic':'https://www.basketball-reference.com/players/b/bogdabo01.html'
# 'Bojan Bogdanovic':'https://www.basketball-reference.com/players/b/bogdabo02.html'
# 'Jalen McDaniels':'https://www.basketball-reference.com/players/m/mcdanja01.html'
# 'Jaden McDaniels':'https://www.basketball-reference.com/players/m/mcdanja02.html'
# 'Julian Champagnie':'https://www.basketball-reference.com/players/c/champju02.html'
# 'Justin Champagnie':'https://www.basketball-reference.com/players/c/champju01.html'
# 'Ziaire Williams':'https://www.basketball-reference.com/players/w/willizi02.html'
# 'Zion Williamson':'https://www.basketball-reference.com/players/w/willizi01.html'
# 'Markieff Morris':'https://www.basketball-reference.com/players/m/morrima02.html'
# 'Marcus Morris Sr'.:'https://www.basketball-reference.com/players/m/morrima03.html'
# 'James Johnson':'https://www.basketball-reference.com/players/j/johnsja01.html'
# 'Jalen Johnson':'https://www.basketball-reference.com/players/j/johnsja05.html'
# 'Jalen Smith':'https://www.basketball-reference.com/players/s/smithja04.html'
# 'Jabari Smith Jr.':'https://www.basketball-reference.com/players/s/smithja05.html'
# 'Jaylin Williams':'https://www.basketball-reference.com/players/w/willija07.html'
# 'Jalen Williams':'https://www.basketball-reference.com/players/w/willija06.html'
# 'Keon Johnson':'https://www.basketball-reference.com/players/j/johnske07.html'
# 'Keldon Johnson':'https://www.basketball-reference.com/players/j/johnske04.html'



