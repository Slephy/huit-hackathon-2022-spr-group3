import requests
import time
import datetime
import datetime

import requests
from bs4 import BeautifulSoup

departure_station = "札幌"
destination_station = "苗穂"
# 経路の取得先URL
urla = 'https://transit.yahoo.co.jp/search/result?from='
urlb = '&flatlon=&to='
urlc = '&fromgid=&togid=&flatlon=&tlatlon=&via=&viacode=&y=2022&m=05&d=12&hh=10&m1=3&m2=8&type=1&ticket=ic&expkind=1&userpass=1&ws=3&s=0&al=0&shin=0&ex=1&hb=0&lb=0&sr=0'
route_url = urla + departure_station + urlb + destination_station + urlc

print(route_url)
route_response = requests.get(route_url)
route_soup = BeautifulSoup(route_response.text, 'html.parser')
# 3つの候補の路線名を取得
rosens = []
a = route_soup.find_all(class_="transport")
for i in range(1, 4):
    txt = a[i].get_text()
    txt = txt.replace("[line][train]", "")
    rosens.append(txt)
print("路線名:\n", rosens)
# 3つの候補の出発時刻を取得
deptime = []
for i in range(1, 4):
    li = str(route_soup.select(
        "#route0"+str(i)+" > div > div:nth-child(1) > ul.time > li")[0])
    li = li.replace("<li>", "")
    li = li.replace("</li>", "")
    deptime.append(li)
# 3つの候補の到着時刻を取得
print("出発時刻:\n", deptime)
arrtime = []
for i in range(1, 4):
    li = str(route_soup.select(
        "#route0"+str(i)+" > div > div:nth-child(3) > ul.time > li")[0])
    li = li.replace("<li>", "")
    li = li.replace("</li>", "")
    arrtime.append(li)
print("到着時刻:\n", arrtime)
# 3つの候補の金額を取得
prices = []
for i in range(1, 4):
    li = str(route_soup.select(
        "#route0"+str(i)+" > div > div.fareSection > p > span")[0])
    li = li.replace("<span>", "")
    li = li.replace("</span>", "")
    prices.append(li)
print("金額:\n", prices)

# //*[@id="route02"]/div/div[2]/div/ul/li[1]/div/text()
