import logging
import os
import sys

from openai import OpenAI

from openai_assistant.assistant import logger_assistant, logger_thread
from openai_assistant.assistant.assistant import Assistant, AssistantNotFoundError
from openai_assistant.assistant.thread import Thread
from openai_assistant.coffee import logger_coffee
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
    logger_assistant.setLevel(logging.DEBUG)
    logger_thread.setLevel(logging.DEBUG)
    logger_coffee.setLevel(logging.DEBUG)
    logger_store.setLevel(logging.DEBUG)

    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    try:
        assistant = Assistant.load_assistant_by_name(client=client, name="Coffee Assistant",
                                                     tools_module_name="openai_assistant.coffee.tools")
        logging.info(f"Tools available: {assistant.available_tools}")
    except AssistantNotFoundError as exp:
        logging.error(f"Assistant not found: {exp}")
        raise exp

    # For new user create a new Thread, else use existing thread
    # thread = Thread.create_thread(client=client, assistant=assistant)
    # logging.error(f"Thread created: {thread}")

    thread_id = "thread_1xxZYhCXBixBc6rT5TbHXVq1"
    thread = Thread(client=client, thread_id=thread_id, assistant=assistant)
    thread.cancel_runs()

    # message_id = thread.add_new_message("I would like to have a strong coffee, what would you suggest?")
    message_id = thread.add_new_message("Please add a strong coffee to my order.")
    thread.run_against_assistant()

    thread.print_messages(before=message_id)
