# -*- coding: utf-8 -*-

import urllib.request
import urllib.error
import json

headers = {
    'X-Cosmos-Token': 'MxLbve3fi-0SyS53f5UzAQ',
    'Content-Type': 'application/json'
}

# req      = urllib.request.Request('https://api.cosmos.bluesoft.com.br/gtins/7891000053508.json', None, headers)
# req      = urllib.request.Request('https://api.cosmos.bluesoft.com.br/gtins/7898994063889.json', None, headers)
# response = urllib.request.urlopen(req)
# data     = json.loads(response.read())

while True:
    try:
        req = urllib.request.Request('https://api.cosmos.bluesoft.com.br/gtins/7898994063889.json', None, headers)
    except urllib.error.HTTPError as e:
        print('1 ' + e.reason)
        break
    except urllib.error.URLError as e:
        print('2 ' + e.reason)
        break
    else:
        while True:
            try:
                response = urllib.request.urlopen(req)
            except urllib.error.HTTPError as e:
                print('3 ' + e.reason)
                break
            except urllib.error.URLError as e:
                print('4 ' + e.reason)
                break
            else:
                data = json.loads(response.read())
            break
        break

print(json.dumps(data, indent=4, ensure_ascii=False))
