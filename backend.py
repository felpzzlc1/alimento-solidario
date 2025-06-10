import flet as ft
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=os.getenv("DB_PORT", 3306)
    )

def main(page: ft.Page):
    page.title = "Alimento Solidário API"
    page.add(ft.Text("API rodando!"))

    @page.route("/usuarios", methods=["GET"])
    def login(req):
        cpf = req.query.get("cpf")
        senha = req.query.get("senha")
        if not cpf or not senha:
            return ft.Response(400, {"error": "CPF e senha são obrigatórios"})
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE cpf=%s AND senha=%s", (cpf, senha))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            if not user:
                return ft.Response(401, {"message": "CPF ou senha inválidos"})
            return ft.Response(200, {"message": "Login realizado com sucesso", "usuario": user})
        except Exception as e:
            return ft.Response(500, {"error": str(e)})

    @page.route("/usuarios", methods=["POST"])
    def cadastro(req):
        data = req.json
        campos = ["nome", "cpf", "data_nascimento", "telefone", "senha"]
        if not all(data.get(c) for c in campos):
            return ft.Response(400, {"error": "Todos os campos são obrigatórios"})
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
            return ft.Response(201, {"message": "Usuário cadastrado com sucesso"})
        except Exception as e:
            return ft.Response(500, {"error": "Erro ao cadastrar usuário: " + str(e)})

ft.app(target=main, port=80)