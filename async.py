from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright

async def player_gamelog(player_name, year, browser):
    
    # chromium = p.chromium # or "firefox" or "webkit".
    # browser = chromium.launch(headless=False)
    context = await browser.new_context()
    # context.set_default_navigation_timeout(timeout)
    page = await context.new_page()
    await context.route("**/*.{png,jpg,jpeg}", lambda route: route.abort())

    # context = await browser.new_context(block_ads=True)
    # page = await browser.new_page()

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
    
    await page.goto(full_url)
    # await page.wait_for_timeout(10000)
    # await page.wait_for_url(full_url)

    # element = await page.wait_for_selector("table_container is_setup")
    await page.evaluate("window.scrollBy(0, 350)")
    # print(page.scroll_into_view_if_needed('#pgl_basic\.940 > td:nth-child(28)'))
    await page.close()
    await browser.close()




# # with sync_playwright() as p:
# async with async_playwright() as ap:
#     player = 'Kevin Durant'
#     y = 2023 # must be in format yyyy
#     player_gamelog(player,y, ap)

import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        player = 'Kevin Durant'
        y = 2023 # must be in format yyyy
        await player_gamelog(player,y, browser)
        await browser.close()

asyncio.run(main())