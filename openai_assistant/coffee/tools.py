import os

import streamlit as st

from openai_assistant.coffee import logger_coffee
from openai_assistant.store.access_weaviate import AccessWeaviate

def_find_available_products = {
    "name": "find_available_products",
    "description": ("Finds available products. The result is an string with valid product names separated by a comma. "
                    "If no products are found an empty string is returned."),
}


def find_available_products():
    logger_coffee.debug(f"Finding available products.")

    weaviate = AccessWeaviate(url=os.getenv("WEAVIATE_URL"),
                              access_key=os.getenv("WEAVIATE_ACCESS_KEY"),
                              openai_api_key=os.getenv("OPENAI_API_KEY"))

    result = weaviate.loop_over_collection(collection_name="coffee", properties=["name"])

    weaviate.close()

    return ",".join([item['name'] for item in result])


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
    st.session_state.basket = []
    return "OK"


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
        "required": ["thread_id", "product_name", "quantity"]
    }
}


def add_product_to_order(product_name: str, quantity: int):
    logger_coffee.info(f"Adding {quantity}x {product_name} to the order")
    st.session_state.basket.append({"product_name": product_name, "quantity": quantity})
    return "OK"


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

    return "OK"


def_checkout_order = {
    "name": "checkout_order",
    "description": "Checkout the order, the result is ERROR or OK, you can use this to notify the user",
}


def checkout_order():
    logger_coffee.info(f"Checking out the order")
    basket = st.session_state.basket
    for item in basket:
        logger_coffee.info(f"{item['quantity']}x {item['product_name']}")
    st.session_state.basket = []

    return "OK"


def_suggest_coffee_based_on_description = {
    "name": "suggest_coffee_based_on_description",
    "description": ("Suggests a product based on the given ingredients. The result is a valid product name or an empty "
                    "string if no products are found."),
    "parameters": {
        "type": "object",
        "properties": {
            "input": {
                "type": "string",
                "description": "Description of the coffee to suggest a coffee for"
            }
        },
        "required": ["input"]
    }
}


def suggest_coffee_based_on_description(input: str):
    logger_coffee.debug(f"Suggesting coffee based on user input: {input}")

    weaviate = AccessWeaviate(url=os.getenv("WEAVIATE_URL"),
                              access_key=os.getenv("WEAVIATE_ACCESS_KEY"),
                              openai_api_key=os.getenv("OPENAI_API_KEY"))

    result = weaviate.query_collection(question=input, collection_name="coffee")

    for obj in result.objects:
        logger_coffee.debug(f"Name: {obj.properties['name']}")
        logger_coffee.debug(f"Score: {obj.metadata.score}")

    weaviate.close()

    if len(result.objects) == 0:
        logger_coffee.warning("No products found")
        return ""

    return result.objects[0].properties["name"]
