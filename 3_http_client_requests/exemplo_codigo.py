import requests
import json


# Exemplo 1 - Requisição GET simples

r = requests.get('http://viacep.com.br/ws/01244001/json/')

status_code_resposta = r.status_code
print(status_code_resposta)
if status_code_resposta == 200:
    resposta_json = r.json()
    print(resposta_json)

    rua = resposta_json["logradouro"]
    print("rua: ", rua)
else:
    print("CEP invalido")


# exemplo 2 - Cadastro aluno na api do profs

url = "https://deploy-heroku-2024-1-1731d2b34d37.herokuapp.com/cadastra_aluno"
dados_entrada = {
    "nome": "via requeisição",
    "cpf": "4444444",
    "email": "tiago2@email.com",
    "idade": 21
}
payload = json.dumps(dados_entrada)
headers = {
    'Content-Type': 'application/json'
}
#response = requests.request("POST", url, headers=headers, data=payload)
response = requests.post(url, headers=headers, data=payload)
if response.status_code in [200, 201]:
    dict_resposta = response.json()
    print(dict_resposta)
else:
    print("Nao funcionou")


# exemplo 2 - Mais Facil - Cadastro aluno na api do profs

url = "https://deploy-heroku-2024-1-1731d2b34d37.herokuapp.com/cadastra_aluno"
dados_entrada = {
    "nome": "via requeisição",
    "cpf": "4444444",
    "email": "tiago2@email.com",
    "idade": 21
}
#response = requests.request("POST", url, headers=headers, data=payload)
response = requests.post(url, headers=headers, json=dados_entrada)
if response.status_code in [200, 201]:
    dict_resposta = response.json()
    print(dict_resposta)
else:
    print("Nao funcionou")


# exemplo 3 - 