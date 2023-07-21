from sys import path
import time
import bs4 as bs
import csv
path.insert(0,"Engine")

from BrowserEngine import BrowserEngine
from playwright.sync_api import Page
from playwright.sync_api import Locator

engine = BrowserEngine("https://sportsbook.caesars.com/ca/on/bet/americanfootball/futures?id=007d7c61-07a7-4e18-bb40-15104b6eac92", headless=False, delay=1)
engine.doAction(Locator.click, engine.getObject(Page.get_by_text, args=["Total Regular Season Rushing Yards"]))
for i in range(80):
    engine.returnPage().mouse.wheel(0, 100)
    time.sleep(0.3)
content = engine.source()

players = []

soup = bs.BeautifulSoup(content, 'lxml')
table = soup.find_all('div', class_='groupedMarketTemplate withBorder')[2:]

for row in table:
    name = row.find('div', class_='marketTemplateTitle').text[:-23]
    date = row.find('span', class_='date underlined').text
    overNUnder = row.find_all('span', class_='cui-text-fg-default')
    over = overNUnder[0].text
    under = overNUnder[1].text
    overNUnderOdds = row.find_all('span', class_='cui-text-fg-primary cui-block heading-md cui-w-full')
    overOdd = overNUnderOdds[0].text
    underOdd = overNUnderOdds[1].text
    players.append([name, date, over, overOdd, under, underOdd])

with open('NFL/RushingOdds/Data/Caesars.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Name","Date", "Over", "Over Odds", "Under", "Under Odds"])
    for player in players:
        writer.writerow(player)