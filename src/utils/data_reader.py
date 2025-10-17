"""
Módulo responsável por ler os dados locais e carregá-los em modelos Pydantic.
Combina metadados dos restaurantes com seus respectivos cardápios.
"""

import json
from typing import Dict
from pydantic import ValidationError
from core.config import settings
from models.schemas import Restaurante, ItemCardapio
from utils.classifier import classify_item


def carregar_dados_restaurantes() -> Dict[str, Restaurante]:
    """
    Lê o arquivo de metadados e os arquivos de cardápio, combina-os
    e retorna um dicionário de restaurantes prontos para a API.
    """
    restaurantes_carregados: Dict[str, Restaurante] = {}

    # 1. Carregar os metadados primeiro
    metadata_restaurantes = {}
    if settings.METADATA_FILE.exists():
        with open(settings.METADATA_FILE, "r", encoding="utf-8") as f:
            metadata_list = json.load(f)
            for meta in metadata_list:
                nome_normalizado = meta.get("nome", "").title()
                metadata_restaurantes[nome_normalizado] = meta
    else:
        print(
            f"[AVISO] Arquivo de metadados não encontrado em: {settings.METADATA_FILE}"
        )

    # 2. Iterar sobre os arquivos de cardápio
    if not settings.DATA_DIR.exists():
        print(
            f"[AVISO] Diretório de dados de cardápios não encontrado:"
            f" {settings.DATA_DIR}"
        )
        return restaurantes_carregados

    for filepath in settings.DATA_DIR.iterdir():
        if filepath.suffix == ".json":
            nome_restaurante = filepath.stem.replace("_", " ").title()
            metadata = metadata_restaurantes.get(nome_restaurante, {})

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    dados_cardapio_raw = json.load(f)

                cardapio_processado = []
                for item_dict in dados_cardapio_raw:
                    # 1. Classifica o item para obter a categoria
                    categoria_item = classify_item(item_dict.get("item"))

                    # 2. Adiciona a categoria ao dicionário do item
                    item_dict["categoria"] = categoria_item

                    # 3. Agora, valida o dicionário completo (com a categoria)
                    item_validado = ItemCardapio.model_validate(item_dict)
                    cardapio_processado.append(item_validado)

                # Cria a instância do Restaurante com o cardápio já processado
                restaurante = Restaurante(
                    nome=metadata.get("nome", nome_restaurante),
                    categoria=metadata.get("categoria", "Não especificada"),
                    ativo=metadata.get("ativo", False),
                    cardapio=cardapio_processado,  # Usa a lista processada
                )
                restaurantes_carregados[restaurante.nome.title()] = restaurante

            except json.JSONDecodeError:
                print(f"[ERRO] O arquivo JSON '{filepath.name}' está mal formatado.")
            except ValidationError as e:
                print(
                    f"[ERRO] Erro de validação de dados em"
                    f" '{filepath.name}'. Detalhes: {e}"
                )
            except OSError as e:
                print(f"[ERRO] Erro de I/O ao ler o arquivo '{filepath.name}': {e}")

    print(
        f"Carregados dados de {len(restaurantes_carregados)} restaurantes para a API."
    )
    return restaurantes_carregados
