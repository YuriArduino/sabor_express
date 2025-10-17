"""
Módulo principal e ponto de entrada para a CLI interativa.

Responsável por orquestrar os componentes (ApiClient, MenuUI)
para criar e executar a aplicação de menu.
"""

from typing import Callable, Dict, List, Optional, Tuple

from .components.api_client import ApiClient, ApiClientError
from .components.ui import MenuUI


# --- Camada de Lógica da Aplicação ---


class MenuFlowError(Exception):
    """Exceção customizada para erros de fluxo no menu."""


class MenuApp:
    """Orquestra a aplicação, conectando a API com a UI."""

    Option = Tuple[str, Callable[[], Optional[bool]]]

    def __init__(self) -> None:
        self.api_client = ApiClient()
        # mapping: tecla -> (descrição, handler)
        self.options: Dict[str, MenuApp.Option] = {
            "1": ("Listar restaurantes", self.handle_list_restaurants),
            "2": ("Ver cardápio", self.handle_view_menu),
            "3": ("Cadastrar restaurante", self.handle_register_restaurant),
            "4": ("Ativar/Desativar restaurante", self.handle_change_status),
            "5": ("Sair", self.handle_exit),
        }

    # ----- Helpers internos -----
    def _prompt_non_empty(
        self, prompt: str, allow_empty: bool = False
    ) -> Optional[str]:
        """Lê input do usuário, faz strip e valida não vazio (por padrão)."""
        raw = input(prompt)
        if raw is None:
            return None
        value = raw.strip()
        if not value and not allow_empty:
            MenuUI.display_message("Entrada inválida: valor vazio.", is_error=True)
            return None
        return value

    def _get_restaurants(self) -> List[dict]:
        """Obtém lista de restaurantes da API, garantindo lista como retorno."""
        try:
            restaurants = self.api_client.get_restaurants() or []
        except ApiClientError as e:
            MenuUI.display_message(str(e), is_error=True)
            return []
        return restaurants

    # ----- Handlers das opções -----
    def handle_list_restaurants(self) -> None:
        """Lida com a lógica de listar todos os restaurantes."""
        MenuUI.display_subtitle("Listando os restaurantes")
        restaurants = self._get_restaurants()
        if not restaurants:
            MenuUI.display_message("Não há restaurantes cadastrados para exibir.")
            return
        MenuUI.display_restaurant_list(restaurants)

    def handle_view_menu(self) -> None:
        """
        Lida com o fluxo interativo de selecionar um restaurante,
        depois uma categoria, e então ver os itens.
        """
        MenuUI.display_subtitle("Ver Cardápio de um Restaurante")
        try:
            restaurants = self._get_restaurants()
            if not restaurants:
                raise MenuFlowError("Não há restaurantes cadastrados para exibir.")

            MenuUI.display_restaurant_list(restaurants)

            nome_restaurante = self._prompt_non_empty(
                "\nDigite o nome do restaurante que deseja ver o cardápio: "
            )
            if not nome_restaurante:
                return

            restaurant_details = self.api_client.get_restaurant_details(
                nome_restaurante
            )
            if not restaurant_details:
                raise MenuFlowError(
                    f"Não foi possível obter os detalhes para o restaurante "
                    f"'{nome_restaurante}'."
                )

            cardapio = restaurant_details.get("cardapio") or []
            if not cardapio:
                raise MenuFlowError("Este restaurante não possui itens no cardápio.")

            available_categories = sorted(
                {item.get("categoria") for item in cardapio if item.get("categoria")}
            )
            if not available_categories:
                raise MenuFlowError("Não há categorias disponíveis neste cardápio.")

            chosen_category = MenuUI.prompt_for_category(available_categories)
            if not chosen_category:
                raise MenuFlowError("Seleção de categoria inválida.")

            items_to_display = [
                item for item in cardapio if item.get("categoria") == chosen_category
            ]
            MenuUI.display_category_items(chosen_category, items_to_display)
        except (ApiClientError, MenuFlowError) as e:
            MenuUI.display_message(str(e), is_error=True)

    def handle_register_restaurant(self) -> None:
        """Lida com a lógica de registrar um novo restaurante."""
        MenuUI.display_subtitle("Cadastro de novo restaurante")
        nome = self._prompt_non_empty("Digite o nome do restaurante: ")
        if not nome:
            return
        categoria = self._prompt_non_empty("Digite a categoria do restaurante: ")
        if not categoria:
            return

        try:
            self.api_client.create_restaurant(nome, categoria)
        except ApiClientError as e:
            MenuUI.display_message(str(e), is_error=True)
            return

        MenuUI.display_message(f"Restaurante '{nome}' cadastrado com sucesso!")

    def handle_change_status(self) -> None:
        """Lida com a lógica de alterar o status de um restaurante."""
        MenuUI.display_subtitle("Alterando status do restaurante")
        nome = self._prompt_non_empty(
            "Digite o nome do restaurante que deseja alterar o status: "
        )
        if not nome:
            return

        try:
            restaurant = self.api_client.toggle_restaurant_status(nome)
        except ApiClientError as e:
            MenuUI.display_message(str(e), is_error=True)
            return

        if restaurant:
            status = "Ativado" if restaurant.get("ativo") else "Desativado"
            MenuUI.display_message(f"O restaurante '{nome}' foi {status} com sucesso!")
        else:
            MenuUI.display_message(
                "Não foi possível obter o novo status do restaurante.", is_error=True
            )

    def handle_exit(self) -> bool:
        """Lida com a saída da aplicação."""
        MenuUI.display_subtitle("Finalizando aplicação...")
        print("Obrigado por usar o Sabor Express! Até logo!\n")
        return False

    # ----- Loop principal -----
    def run(self) -> None:
        """Executa o loop principal do menu."""
        running = True
        while running:
            MenuUI.display_subtitle("Menu Principal")
            MenuUI.display_header()
            MenuUI.display_options(self.options)

            choice = input("\nEscolha uma opção: ").strip()
            action_tuple = self.options.get(choice)

            if action_tuple:
                _, handler = action_tuple
                try:
                    result = handler()
                    # handler pode retornar False para pedir saída
                    if result is False:
                        running = False
                except ApiClientError as e:
                    MenuUI.display_message(str(e), is_error=True)

                if running:
                    MenuUI.prompt_return_to_menu()
            else:
                MenuUI.display_message("Opção inválida!", is_error=True)
                MenuUI.prompt_return_to_menu()


# --- Ponto de Entrada ---


def main() -> None:
    """Função principal que inicia a aplicação do menu."""
    app = MenuApp()
    app.run()


if __name__ == "__main__":
    main()
