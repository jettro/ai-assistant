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

    # Initialize logging
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

    # Initialize Assistant
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


    import streamlit as st

    st.set_page_config(page_title="Your Coffee Assistant", layout="wide")

    st.title("Coffee Assistant")
    st.write("This is a simple example of using OpenAI Assistant to create a Coffee Assistant.")
    col_content, col_basket = st.columns([0.7,0.3], gap="small")

    if st.session_state.get("basket", None) is None:
        st.session_state.basket = []

    # Initialize chat history
    if "thread_id" not in st.session_state:
        thread = Thread.create_thread(client=client, assistant=assistant)
        st.session_state.thread_id = thread.thread_id
    else:
        thread = Thread(client=client, thread_id=st.session_state.thread_id, assistant=assistant)

    with col_content:
        chat_messages = thread.load_messages()
        if chat_messages:
            chat_messages.reverse()
        with st.container(height=500):
            # Display chat messages from history on app rerun
            for message in chat_messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        if prompt := st.chat_input("Your message"):
            thread.cancel_runs()
            message_id = thread.add_new_message(prompt)
            thread.run_against_assistant()
            chat_messages.append(thread.load_messages(before=message_id))
            st.experimental_rerun()

    with col_basket:
        st.write("Currently in your basket:")
        for item in st.session_state.basket:
            st.write(f"{item['quantity']}x {item['product_name']}")
