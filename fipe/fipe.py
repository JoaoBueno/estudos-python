import json
import requests

api_url_base = 'http://fipeapi.appspot.com/api/1/carros/'
headers = {'Content-Type': 'application/json'}

def get_info(url):

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

marcas = get_info(api_url_base + 'marcas.json')

# if marcas is not None:
#     print("Aqui estão suas informações: ")
#     for m in marcas:
#         print(m['name'], m['id'])
# else:
#     print('[!] Solicitação inválida')

# marca = [d['name'] for d in marcas]
marca = [m for m in marcas if m['name'] == 'VOLKSWAGEN']
m = marca[0]
mid=m['id']
print(mid)

veiculos = get_info(api_url_base + 'veiculos/' + str(mid) + '.json')
print(veiculos)