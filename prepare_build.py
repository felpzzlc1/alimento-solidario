import os
import shutil
import subprocess

def prepare_build():
    subprocess.run(["pip", "install", "-r", "requirements.txt", "--target", "libs"], check=True)
    subprocess.run(["pip", "install", "flet", "--target", "libs"], check=True)

    if not os.path.exists("libs"):
        os.makedirs("libs")
    shutil.copytree("libs", "site/libs", dirs_exist_ok=True)

    print("Dependências preparadas com sucesso!")

if __name__ == "__main__":
    prepare_build()