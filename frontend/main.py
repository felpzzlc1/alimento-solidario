import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "libs"))
sys.path.append(os.path.join(os.path.dirname(__file__), "services"))

import flet as ft
from api_service import ApiService

class AlimentoSolidarioApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.api_service = ApiService()
        self.setup_page()

    def setup_page(self):
        self.page.title = "Alimento Solidário"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.show_login()

    def show_login(self):
        self.cpf_field = ft.TextField(
            label="CPF",
            autofocus=True,
            width=300
        )
        self.senha_field = ft.TextField(
            label="Senha",
            password=True,
            width=300
        )

        self.page.views.clear()
        self.page.views.append(
            ft.View(
                "/login",
                [
                    ft.Text("Login", size=30, weight=ft.FontWeight.BOLD),
                    self.cpf_field,
                    self.senha_field,
                    ft.ElevatedButton("Entrar", on_click=self.do_login),
                    ft.TextButton("Criar conta", on_click=lambda _: self.show_cadastro())
                ],
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        self.page.update()

    async def do_login(self, e):
        # Mostrar loading
        self.page.show_snack_bar(ft.SnackBar(content=ft.Text("Fazendo login...")))
        
        response, status_code = self.api_service.login(
            self.cpf_field.value, 
            self.senha_field.value
        )

        if status_code == 200:
            # Login bem sucedido
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text("Login realizado com sucesso!")))
            self.show_home()
        else:
            # Login falhou
            self.page.show_snack_bar(
                ft.SnackBar(content=ft.Text(response.get("error", "Erro ao fazer login")))
            )

    def show_cadastro(self):
        # Implementar tela de cadastro similar ao login
        pass

    def show_home(self):
        self.page.views.clear()
        self.page.views.append(
            ft.View(
                "/home",
                [
                    ft.Text("Bem-vindo ao Alimento Solidário!", size=30),
                    ft.ElevatedButton("Realizar Doação", on_click=lambda _: self.show_realizar_doacao()),
                    ft.ElevatedButton("Minhas Doações", on_click=lambda _: self.show_minhas_doacoes()),
                ],
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        self.page.update()

def main(page: ft.Page):
    app = AlimentoSolidarioApp(page)

ft.app(target=main)
