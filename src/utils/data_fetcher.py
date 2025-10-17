"""
Módulo responsável por buscar dados de fontes externas e salvá-los localmente.
Sua única responsabilidade é o ETL (Extract, Transform, Load) inicial dos dados.
"""

import json
import requests
from core.config import settings


def process_and_save_restaurants():
    """
    Carrega dados de restaurantes de uma URL, processa e salva em arquivos JSON
    separados por restaurante no diretório 'data/restaurants'.
    """
    url = (
        "https://raw.githubusercontent.com/YuriArduino/Estudos_Artificial_Intelligence/"
        "refs/heads/Dados/restaurantes.json"
    )
    timeout = 10

    print("Iniciando download dos dados dos restaurantes...")
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        dados_json = response.json()
        print("Download concluído com sucesso.")

        restaurantes_agrupados = {}
        for item in dados_json:
            company_name = item.get("Company")
            if not company_name:
                continue

            if company_name not in restaurantes_agrupados:
                restaurantes_agrupados[company_name] = []

            restaurantes_agrupados[company_name].append(
                {
                    "item": item.get("Item"),
                    "price": item.get("price"),
                    "description": item.get("description"),
                }
            )

        settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
        print(f"Verificando/criando diretório de dados em: {settings.DATA_DIR}")

        for nome, dados in restaurantes_agrupados.items():
            file_name = f'{nome.replace(" ", "_").lower()}.json'
            file_path = settings.DATA_DIR / file_name

            print(f"Salvando dados de '{nome}' em '{file_path}'...")
            with open(file_path, "w", encoding="utf-8") as arquivo:
                json.dump(dados, arquivo, indent=4, ensure_ascii=False)

        print("\nProcesso de salvamento de dados concluído.")

    except requests.RequestException as e:
        print(f"[ERRO] Erro ao fazer a requisição HTTP: {e}")
    except json.JSONDecodeError as e:
        print(f"[ERRO] Erro ao decodificar o JSON: {e}")
    except OSError as e:
        print(f"[ERRO] Erro de I/O ao salvar o arquivo: {e}")
