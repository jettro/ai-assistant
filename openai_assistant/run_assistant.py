import logging
import os
import sys

from openai import OpenAI

from openai_assistant.assistant import logger_assistant
from openai_assistant.assistant.assistant import Assistant
from openai_assistant.assistant.assistant_functions import def_set_alarm_clock, def_add_grocery_to_shopping_list, \
    def_order_food_delivery, def_finalize_order_food_delivery
from openai_assistant.thread import logger_thread
from openai_assistant.thread.thread import Thread


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
    assistant.register_functions(def_add_grocery_to_shopping_list)
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
                                                 tools_module_name="openai_assistant.assistant.assistant_functions")
    # add_tools_to_assistant(assistant)

    thread = Thread(client=client, thread_id="thread_l9OFcoJw0uKYakpbVrhePtpG", assistant=assistant)
    thread.cancel_runs()
    message_id = thread.add_new_message("Tomorrow I have a late appointment, therefore I can sleep longer, please set my alarm.")
    thread.run_against_assistant()

    thread.print_messages(before=message_id)
