"""
Módulo principal da API Sabor Express.

Responsável por:
- Criar a instância principal do FastAPI.
- Gerenciar o ciclo de vida (lifespan) da aplicação (ex: carregar o 'db').
- Incluir os routers dos diferentes endpoints.
"""

from contextlib import asynccontextmanager
from typing import Dict
from fastapi import FastAPI
from models.schemas import Restaurante
from utils.data_reader import carregar_dados_restaurantes
from .endpoints import restaurants

# "Banco de dados" em memória
db: Dict[str, Restaurante] = {}


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Gerenciador de contexto para eventos de inicialização e finalização da API."""
    print("INFO:     Aplicação iniciando... Populando o banco de dados em memória.")
    dados_carregados = carregar_dados_restaurantes()
    db.clear()
    db.update(dados_carregados)
    print("INFO:     Banco de dados populado com sucesso.")
    yield
    print("INFO:     Aplicação finalizando... Limpando recursos.")
    db.clear()


app = FastAPI(
    title="Sabor Express API",
    description="API para gerenciar restaurantes e seus cardápios.",
    version="1.0.0",
    lifespan=lifespan,
)


# ===================================================================
#  Injeção de Dependência (A FORMA CORRETA)
# ===================================================================
def get_db_dependency() -> Dict[str, Restaurante]:
    """Fornece o dicionário 'db' como uma dependência para os endpoints."""
    return db


# CORREÇÃO: Usamos o método oficial do FastAPI para substituir a dependência.
# Isso garante que, sempre que FastAPI encontrar 'restaurants.get_db', ele usará
# a nossa função 'get_db_dependency' em vez da placeholder.
app.dependency_overrides[restaurants.get_db] = get_db_dependency

# A linha antiga 'restaurants.get_db = get_db_dependency' foi REMOVIDA.

# ===================================================================
#  Inclusão dos Routers
# ===================================================================
app.include_router(
    restaurants.router, prefix="/api/restaurantes", tags=["Restaurantes"]
)


# ===================================================================
#  Endpoint Raiz
# ===================================================================
@app.get("/", summary="Endpoint Raiz", include_in_schema=False)
def read_root():
    """Endpoint raiz que fornece uma mensagem de boas-vindas."""
    return {"message": "Bem-vindo à API Sabor Express!", "docs_url": "/docs"}
