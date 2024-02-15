import os

from openai import OpenAI

from openai_assistant.assistant.assistant import Assistant
from openai_assistant.assistant.assistant_functions import set_alarm_clock
from openai_assistant.thread.thread import Thread

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    assistants = Assistant.list_assistants(client=client)
    assistant = Assistant(client=client, assistant_id=assistants[0]["id"])
    # assistant.register_function(add_grocery_to_shopping_list)
    assistant.register_function(set_alarm_clock)

    thread = Thread(client=client, thread_id="thread_l9OFcoJw0uKYakpbVrhePtpG")
    thread.cancel_runs()
    thread.add_new_message("I need to wake up tomorrow at seven in the morning, i need coffee but I am all out.")

    run = thread.run_against_assistant(assistant_id=assistant.assistant_id)

    print(run)

    thread.print_messages()