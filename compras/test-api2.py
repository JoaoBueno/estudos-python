# -*- coding: utf-8 -*-

import requests
import json

headers = {
    'X-Cosmos-Token': 'MxLbve3fi-0SyS53f5UzAQ',
    'Content-Type': 'application/json'
}

req      = requests.get('https://api.cosmos.bluesoft.com.br/gtins/7891000053508.json', headers)
req.encoding = 'UTF-8'

print(req)
