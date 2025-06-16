from flask import Blueprint, request, jsonify, send_file, send_from_directory
from .database import get_db_connection
import os

api = Blueprint('api', __name__)

# Definir o caminho base do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, '..', 'frontend')  # Subir um nível adicional

# Rotas de arquivos estáticos
@api.route("/")
def home():
    try:
        template_path = os.path.join(FRONTEND_DIR, "templates", "index.html")
        if not os.path.exists(template_path):
            return jsonify({
                "error": f"Template não encontrado em: {template_path}"
            }), 404
        return send_file(template_path)
    except Exception as e:
        return jsonify({
            "error": f"Erro ao carregar template: {str(e)}",
            "path": template_path
        }), 500

# Rota para servir arquivos estáticos
@api.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join(FRONTEND_DIR, 'static'), filename)

@api.route("/auth/login", methods=["POST"])  # Novo endpoint
def login():
    data = request.get_json()  # Mudando para pegar do body
    cpf = data.get("cpf")
    senha = data.get("password")  # Mudando para corresponder ao frontend
    
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
            
        return jsonify({
            "message": "Login realizado com sucesso",
            "usuario": user
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route("/users", methods=["POST"])  # Novo endpoint para cadastro
def cadastro():
    # ...resto do código permanece igual...
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