import logging
import os
import sys

from openai import OpenAI

from openai_assistant.assistant import logger_assistant, logger_thread
from openai_assistant.assistant.assistant import Assistant, AssistantNotFoundError
from openai_assistant.coffee import logger_coffee
from openai_assistant.coffee.tools import def_find_available_products, def_start_order, def_add_product_to_order, \
    def_checkout_order, def_remove_product_from_order, def_suggest_product_based_on_ingredients
from openai_assistant.store import logger_store


def create_assistant():
    name = "Coffee Assistant"
    instructions = ("You are a barista in a coffee shop. You help users choose the products the shop has to offer. "
                    "You have tools available to help you with this task. There are tools to find available products, "
                    "add products, give suggestions based on ingredients, and finalise the order. You are also "
                    "allowed to do small talk with the visitors.")

    return Assistant.create_assistant(client=client,
                                      name=name,
                                      instructions=instructions,
                                      tools_module_name="openai_assistant.coffee.tools")


def add_tools_to_assistant(assistant: Assistant):
    assistant.register_function(def_find_available_products)
    assistant.register_function(def_start_order)
    assistant.register_function(def_add_product_to_order)
    assistant.register_function(def_remove_product_from_order)
    assistant.register_function(def_checkout_order)
    assistant.register_function(def_suggest_product_based_on_ingredients)


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
    logger_assistant.setLevel(logging.INFO)
    logger_thread.setLevel(logging.INFO)
    logger_coffee.setLevel(logging.DEBUG)
    logger_store.setLevel(logging.DEBUG)

    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    try:
        assistant = Assistant.load_assistant_by_name(client=client, name="Coffee Assistant",
                                                     tools_module_name="openai_assistant.coffee.tools")
    except AssistantNotFoundError as exp:
        logging.error(f"Assistant not found: {exp}")
        assistant = create_assistant()
        add_tools_to_assistant(assistant)
