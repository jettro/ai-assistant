import logging
import os
import sys

from openai import OpenAI

from openai_assistant.assistant import logger_assistant, logger_thread
from openai_assistant.assistant.assistant import Assistant, AssistantNotFoundError
from openai_assistant.coffee import logger_coffee
from openai_assistant.coffee.tools import def_find_available_products, def_start_order, def_add_product_to_order, \
    def_checkout_order, def_remove_product_from_order, def_suggest_coffee_based_on_description
from openai_assistant.store import logger_store


def create_assistant():
    name = "Coffee Assistant"
    instructions = ("You are a barista in a coffee shop. You help users choose the products the shop has to offer. "
                    "You have tools available to help you with this task. You can answer questions of visitors, ."
                    "you should answer with short answers. You can ask questions to the visitor if you need more "
                    "information. If a visitor knows what he wants, you can add the product to the order. If a visitor "
                    "wants to remove a product from the order, you can do that. If a visitor wants to checkout, you "
                    "can do that. If a visitor asks for a suggestion, you can do that. If a visitor asks for the "
                    "available products, you can do that. Always be polite and helpful. A happy customer is more "
                    "important than a fast customer and higher valued orders.")

    return Assistant.create_assistant(client=client,
                                      name=name,
                                      instructions=instructions,
                                      tools_module_name="openai_assistant.coffee.tools")


def add_tools_to_assistant(assistant: Assistant):
    assistant.register_functions(
        [def_find_available_products, def_start_order, def_add_product_to_order, def_checkout_order,
         def_remove_product_from_order, def_suggest_coffee_based_on_description])


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
        add_tools_to_assistant(assistant)
    except AssistantNotFoundError as exp:
        logging.error(f"Assistant not found: {exp}")
        assistant = create_assistant()
        add_tools_to_assistant(assistant)
