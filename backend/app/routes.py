from flask import Blueprint, request, jsonify
from .database import get_db_connection

api = Blueprint('api', __name__)

# Rota de login
@api.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Dados JSON não enviados"}), 400

    cpf = data.get("cpf")
    senha = data.get("password")
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
            return jsonify({"error": "CPF ou senha inválidos"}), 401
        return jsonify({"message": "Login realizado com sucesso", "usuario": user}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota de cadastro de usuário
@api.route("/users", methods=["POST"])
def cadastro():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Dados JSON não enviados"}), 400

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