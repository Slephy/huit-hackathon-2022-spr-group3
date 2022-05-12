import requests
import time
import datetime
import datetime

import requests
from bs4 import BeautifulSoup

departure_station = "北18条"
destination_station = "恵庭"

# 経路の取得先URL
route_url = "https://transit.yahoo.co.jp/search/print?from=" + \
    departure_station+"&flatlon=&to=" + destination_station
print(route_url)

route_response = requests.get(route_url)


route_soup = BeautifulSoup(route_response.text, 'html.parser')


route_summary = route_soup.find("div", class_="routeSummary")

required_time = route_summary.find("li", class_="time").get_text()

transfer_count = route_summary.find("li", class_="transfer").get_text()

fare = route_summary.find("li", class_="fare").get_text()

print("======"+departure_station+"から"+destination_station+"=======")
print("所要時間："+required_time)
print(transfer_count)
print("料金："+fare)
