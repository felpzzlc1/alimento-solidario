import flet as ft
import os
import shutil

def copy_frontend_files():
    # Criar diretório assets se não existir
    if not os.path.exists("assets"):
        os.makedirs("assets")
    
    # Copiar arquivos do frontend/static para assets
    frontend_static = "../frontend/static"
    if os.path.exists(frontend_static):
        for file in os.listdir(frontend_static):
            src = os.path.join(frontend_static, file)
            dst = os.path.join("assets", file)
            if os.path.isfile(src):
                shutil.copy2(src, dst)

def main(page: ft.Page):
    # Copiar arquivos do frontend
    copy_frontend_files()
    
    page.title = "Alimento Solidário"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # Criar WebView com arquivo local
    webview = ft.WebView(
        src="file:///assets/index.html",
        expand=True
    )
    
    page.add(webview)

ft.app(target=main)