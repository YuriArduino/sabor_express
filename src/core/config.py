"""Módulo para centralizar as configurações da aplicação."""

from pathlib import Path
from pydantic import computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Define as configurações da aplicação de forma robusta e centralizada.
    Utiliza pathlib para manipulação de caminhos e Pydantic V2 para validação.
    """

    # Define a raiz do projeto de forma robusta, subindo dois níveis
    # a partir deste arquivo (src/core/ -> src/ -> /)
    # Path(__file__) -> /caminho/completo/para/src/core/config.py
    # .resolve() -> Garante que o caminho é absoluto
    # .parents[2] -> Sobe 2 níveis na hierarquia de pastas
    PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]

    @computed_field
    @property
    def DATA_DIR(self) -> Path:
        """
        Deriva o caminho para o diretório de dados a partir da raiz do projeto.
        Este campo é calculado dinamicamente e garante
        que o caminho esteja sempre correto.
        """

        return self.PROJECT_ROOT / "data" / "restaurants"

    @computed_field
    @property
    def METADATA_FILE(self) -> Path:
        """Aponta para o arquivo de metadados dos restaurantes."""
        return self.PROJECT_ROOT / "data" / "restaurants_metadata.json"


# Instância única das configurações para ser usada em toda a aplicação
settings = Settings()

# Pequeno teste para garantir que os caminhos estão corretos ao executar diretamente
if __name__ == "__main__":
    print(f"Raiz do Projeto: {settings.PROJECT_ROOT}")
    print(f"Diretório de Dados: {settings.DATA_DIR}")
    print(
        f"Diretório de dados existe? {'Sim' if settings.DATA_DIR.exists() else 'Não'}"
    )
