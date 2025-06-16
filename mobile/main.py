import flet as ft

def main(page: ft.Page):
    page.title = "Alimento Solidário"
    page.add(
        ft.WebView(
            src="http://54.233.212.218:3000",
            expand=True
        )
    )

ft.app(target=main)