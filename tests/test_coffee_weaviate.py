import logging
import sys

from openai_assistant.coffee import logger_coffee
from openai_assistant.coffee.tools import suggest_coffee_based_on_description, find_available_products
from openai_assistant.store import logger_store

if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    logger_store.setLevel(logging.DEBUG)
    logger_coffee.setLevel(logging.DEBUG)

    result = suggest_coffee_based_on_description("dark coffee")

    logger_store.info(f"Result: {result}")

    coffees = find_available_products()

    logger_store.info(f"Coffees: {coffees}")