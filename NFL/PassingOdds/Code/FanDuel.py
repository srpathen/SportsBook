from sys import path
import time
import bs4 as bs
import csv
path.insert(0,"Engine")

from BrowserEngine import BrowserEngine
from playwright.sync_api import Page
from playwright.sync_api import Locator

engine = BrowserEngine("https://sportsbook.fanduel.com/navigation/nfl?tab=passing-props", headless=False, delay=1)

while "Please verify you are a human" in engine.source():
    engine.close()
    time.sleep(60)
    engine.start()

engine.doAction(Locator.click, engine.getObject(Page.get_by_role, args=["button"], kwargs={"name":"Show more"}).first, delay=1)
content = engine.source()

soup = bs.BeautifulSoup(content, 'lxml')
columns = soup.find_all('div', class_="hb t h")
specificColumns = []

for column in columns:
    if column.text == "Show less":
        break
    col = column.find('div', class_="v w x y bu cd t eq h")
    if col:
        specificColumns.append(col)

players = []

players.append(specificColumns[0].find('div', class_="v z x y bu cd t hk hl h bp hm hn au"))
players.append(specificColumns[0].find('div', class_="v z x y bu cd t hk hl h bp br hm hn au"))
players.append(specificColumns[0].find('div', class_="v z x y bu cd t hk hl h br hm il au"))

for column in specificColumns:
    player1 = column.find('div', class_="v z x y bu cd t hk hl h bo bp hm hn au")
    player2 = column.find('div', class_="v z x y bu cd t hk hl h bo bp br hm hn au")
    player3 = column.find('div', class_="v z x y bu cd t hk hl h bo br hm il au")
    if player1:
        players.append(player1)
    if player2:
        players.append(player2)
    if player3:
        players.append(player3)

playerPoints = []
for player in players:
    name = player.find('div', class_="v w al y bu cd t gs h gt").text
    odds = player.find('div', class_="v w x y t ht gs h").text
    playerPoints.append([name, odds])

with open('NFL/PassingOdds/Data/FanDuel.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Name","Odds"])
    for player in playerPoints:
        writer.writerow(player)


