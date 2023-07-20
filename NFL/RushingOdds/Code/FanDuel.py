from sys import path
import time
import bs4 as bs
import csv
path.insert(0,"Engine")

from BrowserEngine import BrowserEngine
from playwright.sync_api import Page
from playwright.sync_api import Locator

engine = BrowserEngine("https://sportsbook.fanduel.com/navigation/nfl?tab=rushing-props", headless=False, delay=1)
players = []

while "Please verify you are a human" in engine.source():
    engine.close()
    time.sleep(60)
    engine.start()

clickables = engine.getObject(Page.get_by_role, args=["button"]).filter(has_text='Regular Season Total Rushing Yards')
for click in clickables.all():
    click.click()

content = engine.source()
soup = bs.BeautifulSoup(content, 'lxml')
names = soup.find_all('h3', class_="s t hc hd he hi hj h fe eb ex")
newNames = []

for name in names:
    if "2023-24 Regular Season Total Rushing Yards" in name.text:
        newNames.append(name)

dates = soup.find_all('time')

overNUnder = soup.find_all('span', class_="hq hr fe hz eb ex")
overNUnderOdds = soup.find_all('span', class_="hq hr ei eb hz ic ex")
over = []
under = []
overOdds = []
underOdds = []

for i in range(len(overNUnder)):
    if i % 2:
        over.append(overNUnder[i].text)
        overOdds.append(overNUnderOdds[i].text)
    else:
        under.append(overNUnder[i].text)
        underOdds.append(overNUnderOdds[i].text)

for i in range(len(newNames)):
    players.append([newNames[i].text[:-43], dates[i].text, over[i][2:], overOdds[i], under[i][2:], underOdds[i]])

with open('NFL/RushingOdds/Data/FanDuel.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Name","Date", "Over", "Over Odds", "Under", "Under Odds"])
    for player in players:
        writer.writerow(player)