from sys import path
import time
import bs4 as bs
import csv
path.insert(0,"Engine")

from BrowserEngine import BrowserEngine
from playwright.sync_api import Page
from playwright.sync_api import Locator

engine = BrowserEngine("https://sports.ny.betmgm.com/en/sports/football-11/betting/usa-9/nfl-35", headless=False, delay=1)
engine.doAction(Locator.click, engine.getObject(Page.get_by_text, args=["Specials"], delay=5))

engine.doAction(Locator.click, engine.getObject(Page.get_by_text, args=["Show More"], delay=1).nth(2))
engine.doAction(Locator.click, engine.getObject(Page.get_by_text, args=["Show More"], delay=1).nth(2))
content = engine.source()

players = []

soup = bs.BeautifulSoup(content, 'lxml')
table = soup.find_all('ms-compact-event', class_='grid-compact-event ng-star-inserted')[1]
date = table.find('ms-prematch-timer', class_='starting-time timer-badge ng-star-inserted')
table = table.find_all('ms-period-option-group', class_='ng-star-inserted')[1]
names = table.find_all('div', class_='player-props-player-name')
overNUnder = table.find_all('div', class_='name ng-star-inserted')
overNUnderOdds = table.find_all('div', class_='value option-value ng-star-inserted')
over = []
under = []
overOdds = []
underOdds = []

for i in range(len(overNUnder)):
    if i % 2:
        under.append(overNUnder[i].text)
        underOdds.append(overNUnderOdds[i].text)
    else:
        over.append(overNUnder[i].text)
        overOdds.append(overNUnderOdds[i].text)

for i in range(len(names)):
    players.append([names[i].text, date.text, over[i][5:], overOdds[i][1:-1], under[i][6:], underOdds[i][1:-1]])

with open('NFL/RushingOdds/Data/BetMGM.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Name","Date", "Over", "Over Odds", "Under", "Under Odds"])
    for player in players:
        writer.writerow(player)