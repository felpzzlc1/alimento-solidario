import flet as ft
from dotenv import load_dotenv
import os
import pymysql

# Carrega .env
load_dotenv()

def get_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        cursorclass=pymysql.cursors.DictCursor
    )

def main(page: ft.Page):
    page.title = "Alimento Solidário - Login e Cadastro"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    def exibir_mensagem(msg):
        page.snack_bar = ft.SnackBar(ft.Text(msg))
        page.snack_bar.open = True
        page.update()

    def fazer_login(e):
        try:
            conn = get_connection()
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios WHERE cpf=%s AND senha=%s", (cpf.value, senha.value))
                result = cursor.fetchone()
            conn.close()

            if result:
                exibir_mensagem("Login realizado com sucesso!")
            else:
                exibir_mensagem("CPF ou senha inválidos")
        except Exception as err:
            exibir_mensagem(f"Erro: {err}")

    def fazer_cadastro(e):
        if not all([nome.value, cpf.value, data_nascimento.value, telefone.value, senha.value]):
            exibir_mensagem("Preencha todos os campos!")
            return
        try:
            conn = get_connection()
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO usuarios (nome, cpf, data_nascimento, telefone, senha)
                    VALUES (%s, %s, %s, %s, %s)
                """, (nome.value, cpf.value, data_nascimento.value, telefone.value, senha.value))
                conn.commit()
            conn.close()
            exibir_mensagem("Usuário cadastrado com sucesso!")
        except Exception as err:
            exibir_mensagem(f"Erro: {err}")

    nome = ft.TextField(label="Nome completo")
    cpf = ft.TextField(label="CPF")
    data_nascimento = ft.TextField(label="Data de nascimento", hint_text="AAAA-MM-DD")
    telefone = ft.TextField(label="Telefone")
    senha = ft.TextField(label="Senha", password=True, can_reveal_password=True)

    btn_login = ft.ElevatedButton("Login", on_click=fazer_login)
    btn_cadastro = ft.ElevatedButton("Cadastrar", on_click=fazer_cadastro)

    page.add(
        ft.Column([
            ft.Text("Alimento Solidário", size=30, weight=ft.FontWeight.BOLD),
            nome,
            cpf,
            data_nascimento,
            telefone,
            senha,
            ft.Row([btn_login, btn_cadastro], alignment=ft.MainAxisAlignment.CENTER),
        ],
        width=400,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

if __name__ == "__main__":
    ft.app(target=main)
