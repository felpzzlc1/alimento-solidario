from flask import Flask, request, jsonify, send_file
from dotenv import load_dotenv
import mysql.connector
import os

load_dotenv()

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", 3306))
    )

app = Flask(__name__)

@app.route("/")
def home():
    return send_file("site/index.html")  # Serve o arquivo index.html

@app.route("/usuarios", methods=["GET"])
def login():
    cpf = request.args.get("cpf")
    senha = request.args.get("senha")
    if not cpf or not senha:
        return jsonify({"error": "CPF e senha são obrigatórios"}), 400
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE cpf=%s AND senha=%s", (cpf, senha))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if not user:
            return jsonify({"message": "CPF ou senha inválidos"}), 401
        return jsonify({"message": "Login realizado com sucesso", "usuario": user}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/usuarios", methods=["POST"])
def cadastro():
    data = request.get_json()
    campos = ["nome", "cpf", "data_nascimento", "telefone", "senha"]
    if not all(data.get(c) for c in campos):
        return jsonify({"error": "Todos os campos são obrigatórios"}), 400
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nome, cpf, data_nascimento, telefone, senha) VALUES (%s, %s, %s, %s, %s)",
            (data["nome"], data["cpf"], data["data_nascimento"], data["telefone"], data["senha"])
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Usuário cadastrado com sucesso"}), 201
    except Exception as e:
        return jsonify({"error": "Erro ao cadastrar usuário: " + str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)