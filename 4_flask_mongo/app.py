from flask import Flask, request
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config["MONGO_URI"] = "sua string de conexao com o / nome do db no final"
mongo = PyMongo(app)



@app.route('/usuarios', methods=['GET'])
def get_all_users():

    filtro = {}
    projecao = {"_id" : 0}
    dados_usuarios = mongo.db.usuarios.find(filtro, projecao)

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

# Desafios feitos em sala, espewro que vocÊ tenha feito :)



if __name__ == '__main__':
    app.run(debug=True)