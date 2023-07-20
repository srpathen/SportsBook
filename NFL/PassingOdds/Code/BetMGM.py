from sys import path
import time
import bs4 as bs
import csv
path.insert(0,"Engine")

from BrowserEngine import BrowserEngine
from playwright.sync_api import Page
from playwright.sync_api import Locator

engine = BrowserEngine("https://sports.ny.betmgm.com/en/sports/events/2023-24-nfl-regular-season-stat-leaders-14274402", headless=False, delay=1)
engine.doAction(Locator.click, engine.getObject(Page.get_by_text, args=["Show more"], delay=1))
content = engine.source()

players = []

soup = bs.BeautifulSoup(content, 'lxml')
table = soup.find_all('ms-option', class_="option ng-star-inserted")

for row in table:
    name = row.find('div', class_="name ng-star-inserted").text
    odds = row.find('div', class_="value option-value ng-star-inserted").text[1:]
    players.append([name, odds])

with open('NFL/PassingOdds/Data/BetMGM.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Name","Odds"])
    for player in players:
        writer.writerow(player)