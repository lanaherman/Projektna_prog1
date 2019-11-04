import csv
import json
import os
import requests
import sys
import re

with open('kripto.html', encoding='utf-8') as f:
    vsebina = f.read()

vzorec = (
    r'<a.*class=".*name.*".*>(?P<name>.*)</a>\s*'
    r'</td>\s*'
    r'<td class=".*col-symbol">(?P<simbol>[A-Z]{0,})</td>\s*'
    r'<td class="no-wrap market-cap.*>\s*\$*(?P<market_cap>.*)\s*</td>\s*'
    r'<td.*>\s*'
    r'<a.*class="price".*>\s*\$*(?P<price>.*)</a>\s*'
    r'</td>\s*<td.*>\s*'
    r'<span.*data-supply="(?P<circulating_supply>.*)".*>\s*'
    r'[*|.*|\s*]\s*</td>\s*<.*>\s*'
    r'<a.*class="volume".*>\$*(?P<volume>.*)</a>\s*'
    r'</td>\s*'
    r'<td.*data-timespan="1h".*data-sort="(?P<one_hour>.*)">.*</td>\s*'
    r'<td.*data-timespan="24h".*data-sort="(?P<one_day>.*)">.*</td>\s*'
    r'<td.*data-timespan="7d".*data-sort="(?P<one_week>.*)"'
    )

count = 0
kriptovalute = []
for zadetek in re.finditer(vzorec, vsebina):
    kriptovalute.append(zadetek.groupdict())
    count += 1
print(count)

for slovar in kriptovalute:
    if slovar['market_cap'] == '?':
        slovar['market_cap'] = None
    else:
        slovar['market_cap'] = int(slovar['market_cap'].replace(',', ''))

for slovar in kriptovalute:
    if slovar['volume'] == '?' or slovar['volume'] == 'Low Vol':
        slovar['volume'] = None
    else:
        slovar['volume'] = int(slovar['volume'].replace(',', ''))

for slovar in kriptovalute:
    if slovar['circulating_supply'] == 'None':
        slovar['circulating_supply'] = None
    else:
        slovar['circulating_supply'] = float(slovar['circulating_supply'])

for slovar in kriptovalute:
    slovar['price'] = float(slovar['price'])
    slovar['one_hour'] = float(slovar['one_hour'])
    slovar['one_day'] = float(slovar['one_day'])
    slovar['one_week'] = float(slovar['one_week'])

with open('kriptovalute.json', 'w') as f:
    json.dump(kriptovalute, f, indent=2)

with open('kriptovalute.csv', 'w', encoding='utf-8') as csv_datoteka:
    writer = csv.DictWriter(csv_datoteka, fieldnames=['name', 'simbol', 'market_cap', 'price', 'circulating_supply', 'volume', 'one_hour', 'one_day', 'one_week'])
    writer.writeheader()
    for slovar in kriptovalute:
        writer.writerow(slovar)