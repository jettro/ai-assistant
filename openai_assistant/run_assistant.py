import logging
import os
import sys

from openai import OpenAI

from openai_assistant.assistant import logger_assistant
from openai_assistant.assistant.assistant import Assistant
from openai_assistant.thread import logger_thread
from openai_assistant.thread.thread import Thread


def_add_grocery_to_shopping_list = {
    "name": "add_grocery_to_shopping_list",
    "description": "Add a grocery item to the shopping list. The shopping list is a list that I use when going to the "
                   "store to buy stuff. The result is ERROR or OK, you can use this to notify the user",
    "parameters": {
        "type": "object",
        "properties": {
            "grocery_name": {
                "type": "string",
                "description": "The grocery item to add to the shopping list"
            },
            "quantity": {
                "type": "integer",
                "description": "The quantity of the grocery item to add to the shopping list"
            }
        },
        "required": ["grocery_name", "quantity"]
    }
}


def_set_alarm_clock = {
    "name": "set_alarm_clock",
    "description": "Set an alarm clock, the result is ERROR or OK, you can use this to notify the user",
    "parameters": {
        "type": "object",
        "properties": {
            "time": {
                "type": "string",
                "description": "The time to set the alarm to in the format HH:MM, examples are 09:00, 21:30"
            },
            "date": {
                "type": "string",
                "description": "The date to set the alarm to in the format YYYY-MM-DD, examples are 2022-12-31, 2023-01-01"
            }
        },
        "required": ["time"]
    }
}


def_order_food_delivery = {
    "name": "order_food_delivery",
    "description": "Order food or drinks for delivery, the result is ERROR or OK, you can use this to notify the user",
    "parameters": {
        "type": "object",
        "properties": {
            "product_name": {
                "type": "string",
                "description": "The name of the product to order"
            },
            "quantity": {
                "type": "integer",
                "description": "The quantity of the product to order"
            }
        },
        "required": ["product_name", "quantity"]
    }
}


def_finalize_order_food_delivery = {
    "name": "finalize_order_food_delivery",
    "description": "Finalize the order of food or drinks for delivery, the result is ERROR or OK, you can use this to "
                   "notify the user",
}


def set_alarm_clock(time: str, date: str = None):
    logger_assistant.info(f"Setting alarm clock to {time} on {date}")
    return "OK"


def add_grocery_to_shopping_list(grocery_name: str, quantity: int):
    logger_assistant.info(f"Adding {quantity} {grocery_name} to the shopping list")
    return "OK"


def order_food_delivery(product_name: str, quantity: int):
    logger_assistant.info(f"Ordering {quantity} {product_name}")
    return "OK"


def finalize_order_food_delivery():
    logger_assistant.info(f"Finalizing order")
    return "OK"


def create_assistant():
    name = "Jettro's Assistant"
    instructions = ("You are my assistant to take care of small tasks for me. I will ask you to do something for me, "
                    "this can be a question, a task or something else. You will then try to do this for me. If you "
                    "can't do it, you will let me know. Use your knowledge about products. Tell me if I try to "
                    "order something that is not in the list. If you need more information, you will ask me for "
                    "it. If you need to make a decision, you will ask me for it. If you need to do something, "
                    "you will do it. ")

    return Assistant.create_assistant(client=client, name=name, instructions=instructions)


def add_tools_to_assistant(assistant: Assistant):
    # assistant.register_functions([def_add_grocery_to_shopping_list, def_set_alarm_clock, def_order_food_delivery, def_finalize_order_food_delivery])
    assistant.register_function(def_add_grocery_to_shopping_list)
    assistant.register_function(def_set_alarm_clock)
    assistant.register_function(def_order_food_delivery)
    assistant.register_function(def_finalize_order_food_delivery)


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

    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    assistant = Assistant.load_assistant_by_name(client=client, name="Jettro's Assistant",
                                                 tools_module_name="openai_assistant.run_assistant")
    # add_tools_to_assistant(assistant)

    thread = Thread(client=client, thread_id="thread_l9OFcoJw0uKYakpbVrhePtpG", assistant=assistant)
    thread.cancel_runs()
    message_id = thread.add_new_message("Tomorrow I have a late appointment, therefore I can sleep longer, please set my alarm.")
    thread.run_against_assistant()

    thread.print_messages(before=message_id)
