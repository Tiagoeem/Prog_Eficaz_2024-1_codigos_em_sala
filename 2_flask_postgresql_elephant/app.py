# Webservice - Não REST - com Flask e PostgreSQL

# doc: https://www.tutorialspoint.com/python_data_access/python_postgresql_introduction.htm

from flask import Flask, request
import psycopg2

app = Flask(__name__)

# Configuração da conexão com o banco de dados
conn = psycopg2.connect(
    dbname="grgrqypi",
    user="grgrqypi",
    password="7fufAM2kDacm7X8YTYEbdpY71_Q_Au-h",
    host="silly.db.elephantsql.com"
)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/livro", methods=['POST'])
def cadastra_livro():
    dic_livro = request.json

    titulo = dic_livro.get('titulo', '')
    autor = dic_livro.get('autor', '')
    ano_de_publi = dic_livro.get('ano_de_publi', '')
    genero = dic_livro.get('genero', '')

    if not titulo or not genero:
        return {'erro': 'titulo e gênero são obrigatórios'}
    
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO livros (titulo, autor, ano_de_publi, genero) VALUES (%s, %s, %s, %s)", (titulo, autor, ano_de_publi, genero))
        conn.commit()
    except psycopg2 as e:
        conn.rollback()
        return {"erro": str(e)}, 500
    finally:
        cur.close()

    resp = {
        "mensagem": "Livro cadastrado com sucesso",
        "livros": dic_livro
    }
    return resp



@app.route('/livro', methods=['GET'])
def lista_livros():
    genero = request.args.get('genero')  
    cur = conn.cursor()
    try:
        if genero: 
            cur.execute("SELECT * FROM livros WHERE genero = %s", (genero,))  
        else:
            cur.execute("SELECT * FROM livros")
        livros = cur.fetchall()
    except psycopg2.Error as e:
        return {"erro": str(e)}, 500
    finally:
        cur.close()

    livros_lista = []
    for livro in livros:
        livros_lista.append({
            "id": livro[0],
            "titulo": livro[1],
        })
    return livros_lista, 200


@app.route('/livro/<int:id>', methods=['GET'])
def detalhes_livro(id):
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM livros WHERE id = %s", (id,))
        livros = cur.fetchone()
        if livros is None:
            return {"erro": "livro não encontrado"}, 404
    except psycopg2.Error as e:
        return {"erro": str(e)}, 500
    finally:
        cur.close()

    livros_lista = {
        "id": livros[0],
        "titulo": livros[1],
        "autor": livros[2],
        "ano_de_publi": livros[3],
        "genero": livros[4]
    }
    
    return livros_lista, 200

@app.route("/livro/<int:id>", methods=["DELETE"])
def deletar_livro(id):
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM livros WHERE id = %s", (id,))
        livro = cur.fetchone()
        if livro is None:
            return {"erro": "Livro não existe"}
        else:
            cur.execute("DELETE FROM livros WHERE id = %s", (id,))
            conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return {"erro": str(e)}, 500
    finally:
        cur.close()

    resp = {
        "Livro deletado": f"O livro com o id:{id} e de nome: {livro[1]} que você selecionou foi deletado com sucesso!"
    }

    return resp, 200

@app.route("/usuario", methods=["POST"])
def cadastra_usuario():
    dic_usuario = request.json

    nome = dic_usuario.get('nome', '')
    email = dic_usuario.get('email', '')
    data_cadastro = dic_usuario.get('data_cadastro', '')
    
    if not nome:
        return {'erro': 'Nome é obrigatório'}
    
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO usuarios (nome, email, data_cadastro) VALUES (%s, %s, %s)", (nome, email, data_cadastro))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return {"erro": str(e)}, 500
    finally:
        cur.close()

    resp = {
        "mensagem": "Usuario cadastrado com sucesso",
        "Usuarios": dic_usuario
    }

    return resp

@app.route("/usuario", methods=["GET"])
def lista_usuario():
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM usuarios")
        usuarios = cur.fetchall()
    except psycopg2.Error as e:
        return {"erro": str(e)}, 500
    finally:
        cur.close()

    usuarios_lista = []
    for usuario in usuarios:
        usuarios_lista.append({
            "id": usuario[0],
            "nome": usuario[1]
        })
    
    return usuarios_lista, 200

@app.route("/usuario/<int:id>", methods=["GET"])
def detalhe_usuario(id):
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
        usuario = cur.fetchone()
        if usuario is None:
            return {"erro": "usuario não encontrado"}, 404
    except psycopg2.Error as e:
        return {"erro": str(e)}, 500
    finally:
        cur.close()

    usuario_lista = {
        "id": usuario[0],
        "nome": usuario[1],
        "email": usuario[2],
        "data_cadastro": usuario[3]
    }
    
    return usuario_lista, 200

@app.route("/usuario/<int:id>", methods=["DELETE"])
def deletar_usuario(id):
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM usuarios where id = %s", (id,))
        usuario = cur.fetchone()
        if usuario is None:
            return {"erro": "usuario não existe"}
        else:
            cur.execute("DELETE FROM usuarios WHERE id = %s", (id,))
            conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return {"erro": str(e)}, 500
    finally:
        cur.close()

    resp = {
        "Usuario deletado": f"O usuario com o id:{id} e de nome: {usuario[1]} que você selecionou foi deletado com sucesso!"
    }

    return resp, 200

if __name__ == "__main__":
    app.run(debug=True)
