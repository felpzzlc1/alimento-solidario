import flet as ft

def main(page: ft.Page):
    page.title = "Alimento Solidário"
    page.add(ft.Text("Bem-vindo ao Alimento Solidário!"))

    def navigate_to(page_name):
        page.views.clear()
        page.views.append(ft.View(
            controls=[
                ft.Text(f"Carregando página: {page_name}"),
                ft.WebView(src=f"/{page_name}.html")
            ]
        ))

    page.add(
        ft.Column(
            controls=[
                ft.Button("Home", on_click=lambda _: navigate_to("home")),
                ft.Button("Login", on_click=lambda _: navigate_to("login")),
                ft.Button("Realizar Doação", on_click=lambda _: navigate_to("realizar-doacao")),
            ]
        )
    )

ft.app(target=main)
