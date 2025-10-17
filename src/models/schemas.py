"""Módulo de schemas Pydantic para validação e modelagem de dados."""

from typing import List, Optional
from pydantic import BaseModel, Field


class Avaliacao(BaseModel):
    """Schema para uma avaliação de cliente."""

    cliente: str
    # Adiciona validação para que a nota esteja entre 0 e 5.
    nota: float = Field(ge=0, le=5)


class ItemCardapio(BaseModel):
    """Schema para um item do cardápio, baseado no JSON."""

    item: str
    price: float
    description: Optional[str] = None
    categoria: str

    class Config:
        """Configurações adicionais para o Pydantic."""

        populate_by_name = True


class Restaurante(BaseModel):
    """Schema principal para um restaurante."""

    nome: str
    categoria: str = "Não especificada"  # Pode se definir um padrão
    ativo: bool = False
    cardapio: List[ItemCardapio] = []
    avaliacoes: List[Avaliacao] = []

    @property
    def media_avaliacoes(self) -> float:
        """Calcula a média das avaliações do restaurante."""
        if not self.avaliacoes:
            return 0.0
        total_notas = sum(avaliacao.nota for avaliacao in self.avaliacoes)
        return round(total_notas / len(self.avaliacoes), 1)
