from openai_assistant.coffee import logger_coffee

def_find_available_products = {
    "name": "find_available_products",
    "description": ("Finds available products based on the given input. The result is an array with valid product "
                    "names or an empty array if no products are found."),
    "parameters": {
        "type": "object",
        "properties": {
            "input": {
                "type": "string",
                "description": "The input to use to find available products"
            }
        },
        "required": ["input"]
    }
}


def find_available_products(input: str):
    logger_coffee.debug(f"Finding available products based on input: {input}")

    return {
        "result": "OK",
        "products": [
            "Coffee",
            "Tea",
            "Cappuccino",
            "Espresso",
            "Latte",
            "Mocha",
            "Hot Chocolate"
        ]
    }


def_start_order = {
    "name": "start_order",
    "description": "Start an order, the result is ERROR or OK, you can use this to notify the user",
    "parameters": {
        "type": "object",
        "properties": {
            "visitor_name": {
                "type": "string",
                "description": "The name of the visitor to start the order for"
            }
        },
        "required": ["visitor_name"]
    }
}


def start_order(visitor_name: str):
    logger_coffee.info(f"Starting order for visitor {visitor_name}")

    return {
        "result": "OK"
    }


def_add_product_to_order = {
    "name": "add_product_to_order",
    "description": "Add a product to the order, the result is ERROR or OK, you can use this to notify the user",
    "parameters": {
        "type": "object",
        "properties": {
            "product_name": {
                "type": "string",
                "description": "The name of the product to add to the order"
            },
            "quantity": {
                "type": "integer",
                "description": "The quantity of the product to add to the order"
            }
        },
        "required": ["product_name", "quantity"]
    }
}


def add_product_to_order(product_name: str, quantity: int):
    logger_coffee.info(f"Adding {quantity}x {product_name} to the order")

    return {
        "result": "OK"
    }


def_remove_product_from_order = {
    "name": "remove_product_from_order",
    "description": "Remove a product from the order, the result is ERROR or OK, you can use this to notify the user",
    "parameters": {
        "type": "object",
        "properties": {
            "product_name": {
                "type": "string",
                "description": "The name of the product to remove from the order"
            },
            "quantity": {
                "type": "integer",
                "description": "The quantity of the product to remove from the order"
            }
        },
        "required": ["product_name", "quantity"]
    }
}


def remove_product_from_order(product_name: str, quantity: int):
    logger_coffee.info(f"Removing {quantity}x {product_name} from the order")

    return {
        "result": "OK"
    }


def_checkout_order = {
    "name": "checkout_order",
    "description": "Checkout the order, the result is ERROR or OK, you can use this to notify the user",
}


def checkout_order():
    logger_coffee.info(f"Checking out the order")

    return {
        "result": "OK"
    }


def_suggest_product_based_on_ingredients = {
    "name": "suggest_product_based_on_ingredients",
    "description": ("Suggests a product based on the given ingredients. The result is a valid product name or an empty "
                    "string if no products are found."),
    "parameters": {
        "type": "object",
        "properties": {
            "ingredients": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "The ingredients to use to suggest a product"
            }
        },
        "required": ["ingredients"]
    }
}


def suggest_product_based_on_ingredients(ingredients: list):
    logger_coffee.debug(f"Suggesting product based on ingredients: {ingredients}")

    return {
        "result": "OK",
        "product": "Coffee Americano"
    }
