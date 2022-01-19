import requests

urltoken_hml = 'http://api-hml.gs1br.org/oauth/access-token'
urltoken_prd = 'http://api.gs1br.org/oauth/access-token'

# req = {
#         URL: 'https://{{HOST}}/oauth/access-token',
#         HOST: Homologação: 'api-hml.gs1br.org',
#               Produção:'api.gs1br.org',
#         Tipo de Requisição: "POST"
#         Headers: Authorization: " Basic-Auth Username: Client_ID Password: Client_Secret"
#         Content Type "application/json "
#     }

header = {
    'Authorization': 'Basic-Auth',
    'Username': 'ZGFkMjVkZmItNGQxMi0zYjEyLWJiNWYtOTc4ZGNhZGFiN2M3',
    'Password': 'Njk4ZTkxMzItZjg3OS0zMjljLWFlNjEtMzc1ODBlZTAyNzY5'
}

body = {
    "grant_type": "password",
    "username" : "heavyhide@gmail.com",
    "password" : "@Extive07@",
}

r = requests.post(urltoken_hml, data=body, headers=header)

print(r)
