import os

from openai import OpenAI

from openai_assistant.assistant.assistant import Assistant
from openai_assistant.assistant.assistant_functions import def_set_alarm_clock, def_add_grocery_to_shopping_list, \
    add_grocery_to_shopping_list, set_alarm_clock, def_order_food_delivery, order_food_delivery, \
    def_finalize_order_food_delivery, finalize_order_food_delivery
from openai_assistant.thread.thread import Thread

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    assistants = Assistant.list_assistants(client=client)
    assistant = Assistant(client=client, assistant_id=assistants[0]["id"])
    assistant.register_function(def_add_grocery_to_shopping_list, add_grocery_to_shopping_list)
    assistant.register_function(def_set_alarm_clock, set_alarm_clock)
    assistant.register_function(def_order_food_delivery, order_food_delivery)
    assistant.register_function(def_finalize_order_food_delivery, finalize_order_food_delivery)

    thread = Thread(client=client, thread_id="thread_l9OFcoJw0uKYakpbVrhePtpG", assistant=assistant)
    thread.cancel_runs()
    thread.add_new_message("I need to wake up tomorrow at seven in the morning, i need coffee but I am all out, "
                           "so please or it for delivery and order a cheese sandwith to go with the coffee. I do not "
                           "need to order anything else for delivery")

    run = thread.run_against_assistant()

    print(run)

    thread.print_messages()