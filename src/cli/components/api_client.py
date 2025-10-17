"""
Componente Cliente da API.

Responsável por toda a comunicação com a API Sabor Express.
Abstrai os detalhes das requisições HTTP.
"""

import requests


class ApiClientError(Exception):
    """Exceção customizada para erros na comunicação com a API."""


class ApiClient:
    """Responsável por toda a comunicação com a API Sabor Express."""

    def __init__(self, base_url: str = "http://127.0.0.1:8000/api"):
        self.base_url = base_url

    def _make_request(self, method: str, endpoint: str, **kwargs):
        """Método genérico para fazer requisições e tratar erros comuns."""
        try:
            url = f"{self.base_url}/{endpoint}"
            response = requests.request(method, url, timeout=5, **kwargs)
            response.raise_for_status()
            # Retorna None para requisições bem-sucedidas
            #  sem conteúdo (ex: 204 No Content)
            return response.json() if response.status_code != 204 else None
        except requests.HTTPError as e:
            detail = e.response.json().get("detail", "Erro desconhecido do servidor.")
            raise ApiClientError(f"Erro na API: {detail}") from e
        except requests.RequestException as e:
            raise ApiClientError(f"Erro de conexão com a API: {e}") from e

    def get_restaurants(self):
        """Busca a lista de todos os restaurantes."""
        return self._make_request("get", "restaurantes")

    def get_restaurant_details(self, name: str):
        """Busca os detalhes completos, incluindo o cardápio, de um restaurante."""
        # A URL será, por exemplo, /restaurantes/Burger%20King
        return self._make_request("get", f"restaurantes/{name}")

    def create_restaurant(self, name: str, category: str):
        """Envia dados para criar um novo restaurante."""
        payload = {"nome": name, "categoria": category, "ativo": False}
        return self._make_request("post", "restaurantes", json=payload)

    def toggle_restaurant_status(self, name: str):
        """Solicita a alteração de status de um restaurante."""
        return self._make_request("patch", f"restaurantes/{name}/toggle_status")
