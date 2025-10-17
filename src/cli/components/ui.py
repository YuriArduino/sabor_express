"""
Componente de Interface do Usuário (UI).

Responsável por toda a interação visual com o usuário no console.
Não contém nenhuma lógica de negócio ou de comunicação com a API.
"""

import os
from typing import List, Optional, Dict, Any


class MenuUI:
    """Responsável por toda a interação visual com o usuário no console."""

    @staticmethod
    def clear_screen():
        """Limpa o console."""
        os.system("cls" if os.name == "nt" else "clear")

    # ===================================================================
    #  MÉTODO CORRIGIDO
    # ===================================================================
    @staticmethod
    def display_subtitle(subtitle: str):
        """Mostra um subtítulo formatado."""
        # CORREÇÃO: Chamamos o método estático diretamente pela classe.
        MenuUI.clear_screen()
        line = "*" * (len(subtitle) + 4)
        print(f"{line}\n  {subtitle}  \n{line}\n")

    # ===================================================================

    @staticmethod
    def display_header():
        """Mostra o título da aplicação."""
        print("Sabor Express CLI\n")

    @staticmethod
    def display_options(options: dict):
        """Mostra as opções do menu a partir de um dicionário."""
        for key, (text, _) in options.items():
            print(f"{key}. {text}")

    @staticmethod
    def prompt_return_to_menu():
        """Aguarda o usuário para continuar."""
        input("\nPressione Enter para voltar ao menu principal.")

    @staticmethod
    def display_restaurant_list(restaurants: list):
        """Formata e exibe a lista de restaurantes."""
        if not restaurants:
            print("Nenhum restaurante cadastrado.")
            return

        print(
            f'{"Nome do Restaurante".ljust(25)} | {"Categoria".ljust(25)} | {"Status"}'
        )
        for r in restaurants:
            nome = r.get("nome", "N/A").ljust(25)
            categoria = r.get("categoria", "N/A").ljust(25)
            ativo = "Ativado" if r.get("ativo", False) else "Desativado"
            print(f"- {nome} | {categoria} | {ativo}")

    @staticmethod
    def prompt_for_category(categories: List[str]) -> Optional[str]:
        """Exibe uma lista numerada de categorias e solicita a escolha do usuário."""
        print("\nSelecione uma categoria para ver os itens:")
        for i, category in enumerate(categories, 1):
            print(f"  {i}. {category}")

        try:
            choice = int(input("\nEscolha uma opção: "))
            if 1 <= choice <= len(categories):
                return categories[choice - 1]
        except (ValueError, IndexError):
            return None
        return None

    @staticmethod
    def display_category_items(category_name: str, items: List[Dict[str, Any]]):
        """Exibe os itens de uma categoria específica de forma formatada."""
        MenuUI.display_subtitle(f"Itens da Categoria: {category_name}")

        if not items:
            print("Não há itens para exibir nesta categoria.")
            return

        for item in items:
            nome_item = item.get("item", "Item não informado")
            preco = item.get("price", 0.0)
            descricao = item.get("description", "Sem descrição.")

            print(f"  - {nome_item.ljust(30)} | R$ {preco:.2f}")
            print(f"    Descrição: {descricao}\n")

    @staticmethod
    def display_message(message: str, is_error: bool = False):
        """Exibe uma mensagem de sucesso ou erro."""
        prefix = "[ERRO]" if is_error else "[SUCESSO]"
        print(f"\n{prefix} {message}")
