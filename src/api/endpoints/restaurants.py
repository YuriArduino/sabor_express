"""
Endpoints para o recurso 'Restaurante'.
"""

from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from models.schemas import Restaurante


# ===================================================================
#  Dependência para obter o banco de dados
# ===================================================================
# Esta é uma função placeholder. O 'db' real será fornecido pelo router principal.
# Isso torna este módulo completamente independente e testável.
def get_db():
    """Esta dependência será sobrescrita no router principal."""
    raise NotImplementedError("get_db dependency not implemented")


# ===================================================================
#  Criação do Router
# ===================================================================
router = APIRouter()

# ===================================================================
#  Endpoints
# ===================================================================


@router.get("", response_model=List[Restaurante], summary="Lista e filtra restaurantes")
def get_restaurantes(
    categoria: Optional[str] = None,
    ativo: Optional[bool] = None,
    nome: Optional[str] = None,
    db: Dict[str, Restaurante] = Depends(get_db),
):
    """Retorna uma lista de todos os restaurantes, com filtros opcionais."""
    resultados = list(db.values())
    if categoria:
        resultados = [r for r in resultados if r.categoria.lower() == categoria.lower()]
    if ativo is not None:
        resultados = [r for r in resultados if r.ativo == ativo]
    if nome:
        resultados = [r for r in resultados if nome.lower() in r.nome.lower()]
    return resultados


@router.get(
    "/{nome_restaurante}",
    response_model=Restaurante,
    summary="Busca um restaurante pelo nome",
)
def get_restaurant(nome_restaurante: str, db: Dict[str, Restaurante] = Depends(get_db)):
    """Retorna os dados de um restaurante específico pelo seu nome."""
    nome_normalizado = nome_restaurante.replace("_", " ").title()
    restaurante = db.get(nome_normalizado)
    if not restaurante:
        raise HTTPException(status_code=404, detail="Restaurante não encontrado")
    return restaurante


@router.post(
    "",
    response_model=Restaurante,
    status_code=201,
    summary="Cadastra um novo restaurante",
)
def create_restaurant(
    restaurante_input: Restaurante, db: Dict[str, Restaurante] = Depends(get_db)
):
    """Recebe os dados de um novo restaurante e o adiciona ao 'banco de dados'."""
    nome_normalizado = restaurante_input.nome.title()
    if nome_normalizado in db:
        raise HTTPException(
            status_code=409, detail="Restaurante com este nome já existe."
        )
    db[nome_normalizado] = restaurante_input
    return restaurante_input


@router.patch(
    "/{nome_restaurante}/toggle_status",
    response_model=Restaurante,
    summary="Ativa ou desativa um restaurante",
)
def toggle_restaurant_status(
    nome_restaurante: str, db: Dict[str, Restaurante] = Depends(get_db)
):
    """Encontra um restaurante pelo nome e inverte seu status 'ativo'."""
    nome_normalizado = nome_restaurante.replace("_", " ").title()
    restaurante = db.get(nome_normalizado)
    if not restaurante:
        raise HTTPException(status_code=404, detail="Restaurante não encontrado")
    restaurante.ativo = not restaurante.ativo
    return restaurante
