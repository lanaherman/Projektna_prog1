import re
import requests
import json

with open('kripto.html', encoding='utf-8') as f:
    vsebina = f.read()

vzorec = (
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

with open('kriptovalute.json', 'w') as f:
    json.dump(kriptovalute, f, indent=2)