"""
Módulo para a Interface de Linha de Comando (CLI) interativa do Sabor Express.
Este módulo atua como um cliente para a API Sabor Express.
"""

import os
import requests

# Define a URL base da API para facilitar a manutenção.
API_BASE_URL = "http://127.0.0.1:8000/api"


def print_name():
    """Mostra o título da aplicação."""
    print("Sabor Express CLI\n")


def print_options():
    """Mostra as opções do menu."""
    print("1. Cadastrar restaurante")
    print("2. Listar restaurantes")
    print("3. Ativar/Desativar restaurante")
    print("4. Sair")


def show_subtitle(subtitle):
    """Limpa a tela e mostra um subtítulo formatado."""
    os.system("cls" if os.name == "nt" else "clear")
    line = "*" * (len(subtitle) + 4)
    print(line)
    print(f"  {subtitle}  ")
    print(line)
    print()


def return_to_menu():
    """Aguarda o usuário pressionar uma tecla para voltar ao menu."""
    input("\nPressione Enter para voltar ao menu principal.")


def enlist_restaurants():
    """Busca e exibe a lista de restaurantes a partir da API."""
    show_subtitle("Listando os restaurantes")
    try:
        response = requests.get(f"{API_BASE_URL}/restaurantes")
        response.raise_for_status()  # Lança um erro se a requisição falhar (status != 2xx)

        restaurantes = response.json()

        if not restaurantes:
            print("Nenhum restaurante cadastrado.")
            return

        print(
            f'{"Nome do Restaurante".ljust(25)} | {"Categoria".ljust(25)} | {"Status"}'
        )
        for restaurante in restaurantes:
            nome = restaurante.get("nome", "N/A").ljust(25)
            categoria = restaurante.get("categoria", "N/A").ljust(25)
            # O schema Pydantic converte bool para true/false no JSON
            ativo = "Ativado" if restaurante.get("ativo", False) else "Desativado"
            print(f"- {nome} | {categoria} | {ativo}")

    except requests.RequestException as e:
        print(f"\nErro ao conectar com a API: {e}")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado: {e}")
    finally:
        return_to_menu()


# As funções `register_restaurant` e `change_restaurant_status` são exemplos
# de como o CLI interagiria com a API. Elas requerem que os endpoints
# correspondentes (POST, PATCH) existam na API.


def register_restaurant():
    """
    Envia os dados de um novo restaurante para a API para registro.
    NOTA: Requer um endpoint POST /api/restaurantes na API.
    """
    show_subtitle("Cadastro de novo restaurante")
    nome = input("Digite o nome do restaurante: ")
    categoria = input("Digite a categoria do restaurante: ")

    payload = {"nome": nome, "categoria": categoria, "ativo": False}

    try:
        response = requests.post(f"{API_BASE_URL}/restaurantes", json=payload)
        response.raise_for_status()
        print(f"Restaurante '{nome}' cadastrado com sucesso!")
    except requests.HTTPError as e:
        print(f"Erro ao cadastrar restaurante: {e.response.json().get('detail', e)}")
    except requests.RequestException as e:
        print(f"Erro de conexão com a API: {e}")
    finally:
        return_to_menu()


def change_restaurant_status():
    """
    Solicita a alteração de status (ativar/desativar) de um restaurante via API.
    NOTA: Requer um endpoint PATCH /api/restaurantes/{nome}/status na API.
    """
    show_subtitle("Alterando status do restaurante")
    nome = input("Digite o nome do restaurante que deseja alterar o status: ")

    try:
        # O endpoint ideal seria um PATCH que só altera o status
        response = requests.patch(f"{API_BASE_URL}/restaurantes/{nome}/toggle_status")
        response.raise_for_status()

        restaurante = response.json()
        status = "Ativado" if restaurante.get("ativo") else "Desativado"
        print(f"O restaurante '{nome}' foi {status} com sucesso!")

    except requests.HTTPError as e:
        detail = e.response.json().get("detail", "Erro desconhecido")
        print(f"Erro ao alterar status: {detail}")
    except requests.RequestException as e:
        print(f"Erro de conexão com a API: {e}")
    finally:
        return_to_menu()


def end_app():
    """Finaliza a aplicação."""
    show_subtitle("Finalizando aplicação...")
    print("Obrigado por usar o Sabor Express! Até logo!\n")


def main():
    """Função principal que executa o loop do menu interativo."""
    while True:
        show_subtitle("Menu Principal")
        print_name()
        print_options()

        try:
            opcao = int(input("\nEscolha uma opção: "))
            if opcao == 1:
                register_restaurant()
            elif opcao == 2:
                enlist_restaurants()
            elif opcao == 3:
                change_restaurant_status()
            elif opcao == 4:
                end_app()
                break
            else:
                print("Opção inválida!")
                return_to_menu()
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")
            return_to_menu()


if __name__ == "__main__":
    main()
