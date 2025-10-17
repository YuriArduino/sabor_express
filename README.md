# Sabor Express API & CLI

`![cli_menu_principal_1](assets/cli_menu_principal_1.png)`
`![cli_menu_principal_2](assets/cli_menu_principal_2.png)`
`![cli_menu_principal_3](assets/cli_menu_principal_3.png)`
`![cli_menu_api](assets/cli_menu_api.png)`

Uma aplicação completa para gerenciar cardápios de restaurantes, construída com FastAPI e Typer. Este projeto é o resultado da evolução de uma aplicação de curso, refatorada para seguir as melhores práticas de arquitetura de software, incluindo separação de responsabilidades, modelagem de dados com Pydantic e gerenciamento de projeto moderno com `pyproject.toml`.

##  Principais Funcionalidades

- **API Backend Robusta**: Construída com FastAPI, fornecendo endpoints para listar, criar e gerenciar restaurantes e seus cardápios.
- **Cliente de Linha de Comando (CLI) Interativo**: Uma interface de usuário amigável, construída com Typer, que consome a API.
- **Arquitetura Modular**: O código é organizado em uma estrutura `src/` limpa, com responsabilidades bem definidas (API, CLI, Utilitários, Modelos).
- **Classificação Inteligente de Dados**: Um módulo classificador que analisa os itens do cardápio e os agrupa em categorias (Bebidas, Sobremesas, etc.) dinamicamente, sem alterar a fonte de dados original.
- **Gerenciamento de Projeto Moderno**: Utiliza `pyproject.toml` para centralizar todas as dependências, metadados e configurações de ferramentas.

##  Instalação e Setup

### Pré-requisitos
- Python 3.10 ou superior
- `venv` (ou outro gerenciador de ambiente virtual)

### Passos

1.  **Clone o repositório:**
    ```bash
    git clone <url-do-seu-repositorio>
    cd sabor-express
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Criar
    python -m venv venv

    # Ativar (Linux/macOS)
    source venv/bin/activate

    # Ativar (Windows)
    .\venv\Scripts\activate
    ```

3.  **Instale o projeto e suas dependências:**
    O projeto usa `pyproject.toml`. Instale-o em modo editável (`-e`) junto com as dependências de desenvolvimento (`[dev]`):
    ```bash
    pip install -e ".[dev]"
    ```
    Este comando instala a aplicação e cria o ponto de entrada `sabor-express`.

##  Como Usar

A aplicação possui duas partes que rodam em terminais separados: o servidor da API e o cliente CLI.

### 1. Busque os Dados dos Restaurantes
Antes de iniciar a API, popule a pasta `data/` com os arquivos de cardápio.

```bash
sabor-express fetch-data
```

### 2. Inicie o Servidor da API
Este comando iniciará o servidor FastAPI. Mantenha este terminal rodando.

```bash
sabor-express run-api
```
- A API estará disponível em `http://127.0.0.1:8000`.
- A documentação interativa (Swagger UI) estará em `http://127.0.0.1:8000/docs`.

### 3. Use o Cliente CLI
**Abra um novo terminal**, ative o mesmo ambiente virtual e execute o cliente interativo.

```bash
sabor-express run-cli
```
Você verá o menu principal e poderá interagir com a aplicação:
```
1. Listar restaurantes
2. Ver cardápio
3. Cadastrar restaurante
4. Ativar/Desativar restaurante
5. Sair
```

## Estrutura do Projeto

O projeto segue uma arquitetura limpa e desacoplada:

-   `src/api/`: Contém a lógica do FastAPI, com os endpoints separados por recurso.
-   `src/cli/`: Contém a lógica da interface de linha de comando, separada em componentes de UI e cliente da API.
-   `src/core/`: Configurações centrais da aplicação.
-   `src/models/`: Schemas Pydantic para validação e modelagem de dados.
-   `src/utils/`: Módulos de utilidade para buscar, ler e classificar dados.
-   `main.py`: O ponto de entrada da aplicação, que orquestra os comandos da CLI.
-   `pyproject.toml`: Arquivo único para gerenciamento de dependências e configuração do projeto.
