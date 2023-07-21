from sys import path
import time
import bs4 as bs
import csv
path.insert(0,"Engine")

from BrowserEngine import BrowserEngine
from playwright.sync_api import Page
from playwright.sync_api import Locator

engine = BrowserEngine("https://sportsbook.draftkings.com/leagues/football/nfl?category=player-stats&subcategory=rush-yards", headless=False, delay=1)
content = engine.source()

soup = bs.BeautifulSoup(content, 'lxml')
table = soup.find_all('div', class_='sportsbook-event-accordion__wrapper expanded')

players = []

for row in table:
    name = row.find('a', class_='sportsbook-event-accordion__title').text
    date = row.find('span', class_='sportsbook-event-accordion__date').text
    overAndUnder = row.find_all('span', class_='sportsbook-outcome-cell__label')
    over = overAndUnder[0].text[5:]
    under = overAndUnder[1].text[6:]
    odds = row.find_all('span', class_='sportsbook-odds american default-color')
    overOdds = odds[0].text
    underOdds = odds[1].text
    players.append([name, date, over, overOdds, under, underOdds])


with open('NFL/RushingOdds/Data/DraftKings.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Name","Date", "Over", "Over Odds", "Under", "Under Odds"])
    for player in players:
        writer.writerow(player)