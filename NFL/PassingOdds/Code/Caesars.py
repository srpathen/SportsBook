from sys import path
import time
import bs4 as bs
import csv
path.insert(0,"Engine")

from BrowserEngine import BrowserEngine
from playwright.sync_api import Page
from playwright.sync_api import Locator

engine = BrowserEngine("https://sportsbook.caesars.com/ca/on/bet/americanfootball/futures?id=007d7c61-07a7-4e18-bb40-15104b6eac92", headless=False, delay=1)
engine.doAction(Locator.click, engine.getObject(Page.get_by_text, args=["Most Regular Season Passing Yards"], delay=1))
engine.doAction(Locator.click, engine.getObject(Page.get_by_text, args=["Show all"], delay=1).last)
content = engine.source()

players = []

soup = bs.BeautifulSoup(content, 'lxml')
table = soup.find_all('div', class_='groupedMarketTemplateGrid groupedMarketTemplateGrid_1Col')[-1]
names = table.find_all('a', class_='competitor')
odds = table.find_all('div', class_='selectionContainer')

for num in range(0, len(names)):
    players.append([names[num].text, odds[num].text])

with open('NFL/PassingOdds/Data/Caesars.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Name","Odds"])
    for player in players:
        writer.writerow(player)