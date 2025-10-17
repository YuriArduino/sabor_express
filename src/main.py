"""
Ponto de entrada principal da aplicação Sabor Express.

Este módulo utiliza Typer para criar uma Interface de Linha de Comando (CLI)
que gerencia a execução dos diferentes componentes do sistema, como
iniciar o servidor da API.
"""

import typer
import uvicorn
from cli import menu as cli_menu
from utils.data_fetcher import process_and_save_restaurants

# Cria uma instância do Typer app. É o nosso orquestrador de comandos.
cli_app = typer.Typer()


@cli_app.command()
def fetch_data():
    """
    Busca os dados de restaurantes da fonte original na internet
    e salva-os localmente na pasta 'data/restaurants'.
    """
    typer.echo("Iniciando a busca e salvamento dos dados dos restaurantes...")
    process_and_save_restaurants()
    typer.echo("Operação concluída.")


@cli_app.command()
def run_api(
    host: str = typer.Option("127.0.0.1", help="O endereço do host para expor a API."),
    port: int = typer.Option(8000, help="A porta para expor a API."),
    reload: bool = typer.Option(
        True, help="Habilita o recarregamento automático ao detectar mudanças."
    ),
):
    """
    Inicia o servidor da API Sabor Express usando Uvicorn.
    """
    typer.echo(f"Iniciando a API Sabor Express em http://{host}:{port}")
    # A string para uvicorn agora deve refletir o novo local do router
    uvicorn.run("api.router:app", host=host, port=port, reload=reload)


@cli_app.command()
def run_cli():
    """
    Inicia a interface de linha de comando interativa (o menu).
    """
    typer.echo("Iniciando o menu interativo do Sabor Express...")
    cli_menu.main()


# Este é o ponto de entrada quando o script é executado diretamente.
if __name__ == "__main__":
    cli_app()
