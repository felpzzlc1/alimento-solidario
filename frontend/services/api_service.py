import requests
import os
from dotenv import load_dotenv

load_dotenv()

class ApiService:
    def __init__(self):
        self.base_url = os.getenv("API_BASE_URL")

    def _make_request(self, method, endpoint, data=None):
        url = f"{self.base_url}{endpoint}"
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=data
            )
            return response.json(), response.status_code
        except requests.RequestException as e:
            return {"error": str(e)}, 500

    def login(self, cpf, senha):
        return self._make_request("POST", "/auth/login", {"cpf": cpf, "password": senha})

    def cadastrar_usuario(self, dados_usuario):
        return self._make_request("POST", "/users", dados_usuario)