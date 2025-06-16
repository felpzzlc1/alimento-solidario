import requests
from typing import Dict, Any, Tuple
import os
from dotenv import load_dotenv

load_dotenv()

class ApiService:
    def __init__(self):
        self.base_url = os.getenv("API_BASE_URL")

    def _make_request(self, method: str, endpoint: str, data: Dict = None) -> Tuple[Dict, int]:
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Content-Type": "application/json"  # Adicionar header
        }
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,  # Adicionar headers
                json=data
            )
            return response.json(), response.status_code
        except requests.RequestException as e:
            return {"error": str(e)}, 500

    def login(self, cpf: str, senha: str) -> Tuple[Dict, int]:
        return self._make_request(
            "POST",
            "/auth/login",
            {"cpf": cpf, "password": senha}
        )

    def cadastrar_usuario(self, dados_usuario: Dict) -> Tuple[Dict, int]:
        return self._make_request(
            "POST",
            "/users",
            dados_usuario
        )