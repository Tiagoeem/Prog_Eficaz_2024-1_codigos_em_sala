from flask import Flask, request
from flask_pymongo import PyMongo
import web_pdb
import os

# Criando variaveis de ambiente no seu SO: https://www.alura.com.br/artigos/configurar-variaveis-ambiente-windows-linux-macos


app = Flask(__name__)

str_de_conexao_mongo = os.getenv("exemplo_prog_eficaz")
app.config["MONGO_URI"] = str_de_conexao_mongo

mongo = PyMongo(app)



@app.route('/usuarios', methods=['GET'])
def get_all_users():

    filtro = {}
    projecao = {"_id" : 0}
    dados_usuarios = mongo.db.usuarios_col.find(filtro, projecao)

    resp = {
        "usuarios": list( dados_usuarios )
    }

    return resp, 200

@app.route('/usuarios', methods=['POST'])
def post_user():
    
    data = request.json

    breakpoint()
    if "cpf" not in data:
        return {"erro": "cpf é obrigatório"}, 400
    
    result = mongo.db.usuarios_col.insert_one(data)

    return {"id": str(result.inserted_id)}, 201

    

# Desafios feitos em sala, espero que você tenha feito :)



if __name__ == '__main__':
    app.run(debug=True)