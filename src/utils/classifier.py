"""
Módulo de Classificação de Itens de Cardápio.

Responsável por analisar o nome de um item e atribuir-lhe uma categoria
com base em um conjunto de regras e palavras-chave.
"""

# Usar sets para uma busca de palavras-chave um pouco mais eficiente
CATEGORIAS = {
    "BEBIDA": {
        "small",
        "medium",
        "large",
        "child",
        "fl oz",
        "oz cup",
        "cup",
        "liter",
        "l",
        "soda",
        "coca",
        "sprite",
        "fanta",
        "pepsi",
        "mountain dew",
        "shake",
        "latte",
        "coffee",
        "tea",
        "juice",
        "milk",
        "water",
        "mochaccino",
        "capuccino",
        "mccafe",
        "frappe",
    },
    "SOBREMESA": {
        "pie",
        "flurry",
        "ice cream",
        "parfait",
        "sundae",
        "cookie",
        "muffin",
        "apple slice",
        "cone",
        "dessert",
        "caramel",
        "chocolate chip",
        "m&m’s",
        "oreo",
    },
    "OPÇÃO SAUDÁVEL": {
        "salad",
        "wrap",
        "grilled",
        "oatmeal",
        "yogurt",
        "fruit",
        "vinaigrette",
        "garden",
        "veggie",
        "light",
    },
    "SANDUÍCHE/PRINCIPAL": {
        "burger",
        "sandwi",
        "mac",
        "whopper",
        "big n’ tasty",
        "mcdouble",
        "pizza",
        "taco",
        "burrito",
        "sandwich",
        "hotdog",
        "quarter pounder",
        "breakfast",
        "pancake",
        "hotcakes",
        "biscuit",
    },
    "ACOMPANHAMENTO": {
        "fries",
        "ring",
        "nuggets",
        "pc",
        "piece",
        "side",
        "ketchup",
        "sauce",
        "dip",
        "strips",
        "gizzards",
        "livers",
        "chicken",
        "popcorn",
        "wings",
        "taco shell",
        "crispy",
    },
}


def classify_item(item_name: str) -> str:
    """
    Classifica um item de cardápio em uma categoria com base em seu nome.

    Args:
        item_name: O nome do item a ser classificado.

    Returns:
        A categoria do item como uma string.
    """
    if not item_name:
        return "OUTROS"

    lower_item_name = item_name.lower()

    for categoria, keywords in CATEGORIAS.items():
        if any(keyword in lower_item_name for keyword in keywords):
            return categoria

    return "OUTROS"
