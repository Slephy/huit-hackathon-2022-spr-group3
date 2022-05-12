import requests
import time
import datetime
import datetime
import re
import requests
from bs4 import BeautifulSoup

departure_station = "旭川駅"
destination_station = "札幌駅"
# 経路の取得先URL
urla = 'https://transit.yahoo.co.jp/search/result?from='
urlb = '&flatlon=&to='
urlc = '&fromgid=&togid=&flatlon=&tlatlon=&via=&viacode=&y=2022&m=05&d=12&hh=10&m1=3&m2=8&type=1&ticket=ic&expkind=1&userpass=1&ws=3&s=0&al=0&shin=0&ex=1&hb=0&lb=0&sr=0'
route_url = urla + departure_station + urlb + destination_station + urlc

print(route_url)
route_response = requests.get(route_url)
route_soup = BeautifulSoup(route_response.text, 'html.parser')
# 3つの候補の路線名を取得
info_rosens = []
a = route_soup.find_all(class_="transport")
for i in range(1, 4):
    txt = a[i].get_text()
    txt = txt.replace("[line][train]", "")
    info_rosens.append(txt)
print("路線名:\n", info_rosens)
# 3つの候補の出発時刻を取得
info_deptime = []
for i in range(1, 4):
    li = str(route_soup.select(
        "#route0"+str(i)+" > div > div:nth-child(1) > ul.time > li")[0])
    li = li.replace("<li>", "")
    li = li.replace("</li>", "")
    info_deptime.append(li)
print("出発時刻:\n", info_deptime)
# 3つの候補の到着時刻を取得
info_arrtime = []
for i in range(1, 4):
    li = str(route_soup.select(
        "#route0"+str(i)+" > div > div:nth-child(3) > ul.time > li")[0])
    li = li.replace("<li>", "")
    li = li.replace("</li>", "")
    info_arrtime.append(li)
print("到着時刻:\n", info_arrtime)
# 3つの候補の金額を取得
info_prices = []
for i in range(1, 4):
    li = str(route_soup.select(
        "#route0"+str(i)+" > div > div.fareSection > p > span")[0])
    li = li.replace("<span>", "")
    li = li.replace("</span>", "")
    info_prices.append(li)
print("乗車券金額:\n", info_prices)

print("============================")
# 途中駅を追加
info_stops = []
info_times = []
for j in range(1, 4):
    i = 0
    rosen_stops = []
    rosen_times = []
    while 1:
        i += 1

        stp = route_soup.select(
            "#route0"+str(j)+" > div > div.fareSection > div > ul > li.stop > ul > li:nth-child("+str(i)+") > dl > dd")
        tim = route_soup.select(
            "#route0"+str(j)+" > div > div.fareSection > div > ul > li.stop > ul > li:nth-child("+str(i)+") > dl > dt")
        if i == 1 and not stp:  # 通過駅が一駅の場合に取得できないバグを修正
            stp = route_soup.select(
                "#route0"+str(j)+" > div > div.fareSection > div > div > ul > li.stop > ul > li > dl > dd")
            tim = route_soup.select(
                "#route0"+str(j)+" > div > div.fareSection > div > div > ul > li.stop > ul > li > dl > dt")
        if not stp:

            break
        rosen_times.append(
            re.sub("<[^<>]*>|[○\[\]]", "", str(tim)))  # タグを消去
        rosen_stops.append(
            re.sub("<[^<>]*>|[○\[\]]", "", str(stp)))  # タグを消去
    rosen_stops.append(destination_station)  # 到着駅を追加
    info_stops.append(rosen_stops)
    rosen_times.append(info_arrtime[j-1])  # 到着駅の時刻を追加
    info_times.append(rosen_times)

    print("ルート"+str(j)+"の途中駅と時刻:\n", rosen_stops)
    print(rosen_times)
