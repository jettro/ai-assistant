import json
import time

from openai import OpenAI, NotFoundError
from openai.types.beta.threads import Run

from openai_assistant.assistant import logger_thread
from openai_assistant.assistant.assistant import Assistant


class Thread:
    def __init__(self, client: OpenAI, thread_id: str, assistant: Assistant):
        self.client = client
        self.thread_id = thread_id
        self.assistant = assistant
        self.__load_thread()

    def print_messages(self, before: str = None):
        messages = self.client.beta.threads.messages.list(self.thread_id, limit=4, before=before)
        for message in messages:
            logger_thread.info(f"Message: {message}")

    def load_messages(self, limit: int = 10, before: str = None):
        messages = self.client.beta.threads.messages.list(self.thread_id, limit=limit, before=before)

        chat_messages = []
        for message in messages:
            content = message.content[0].text.value
            role = message.role
            chat_messages.append({"role": role, "content": content})

        return chat_messages

    def add_new_message(self, message: str):
        logger_thread.debug(f"Adding message '{message}' to thread {self.thread_id}")
        thread_message = self.client.beta.threads.messages.create(thread_id=self.thread_id, role="user",
                                                                  content=message)
        return thread_message.id

    def run_against_assistant(self):
        logger_thread.debug(f"Running assistant against thread {self.thread_id}")
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread_id,
            assistant_id=self.assistant.assistant_id
        )
        return self.__handle_run(run=run)

    def cancel_runs(self):
        runs = self.client.beta.threads.runs.list(thread_id=self.thread_id)
        for run in runs:
            if run.status not in ["cancelled", "completed", "expired"]:
                logger_thread.debug(f"Canceling run {run.id} with status {run.status}")
                self.client.beta.threads.runs.cancel(run_id=run.id, thread_id=self.thread_id)

    def print_run_info(self, run_id: str):
        run = self.client.beta.threads.runs.retrieve(run_id=run_id, thread_id=self.thread_id)
        logger_thread.info(f"Run: {run}")

    def __handle_run(self, run: Run) -> Run:
        run = self.__verify_run(run_id=run.id)

        while run.status == "requires_action":
            logger_thread.debug(f"Run {run.id} requires action")
            tools_calls = run.required_action.submit_tool_outputs.tool_calls

            tool_outputs = []
            for tool_call in tools_calls:
                logger_thread.info(
                    f"Calling function {tool_call.function.name} with arguments {tool_call.function.arguments}")
                result = self.assistant.call_tool(tool_call.function.name, json.loads(tool_call.function.arguments))
                logger_thread.debug(f"Result of call: {result}")
                tool_outputs.append({
                    "tool_call_id": tool_call.id,
                    "output": result
                })
            run = self.client.beta.threads.runs.submit_tool_outputs(
                run_id=run.id,
                thread_id=self.thread_id,
                tool_outputs=tool_outputs
            )
            run = self.__verify_run(run_id=run.id)

        logger_thread.info(f"Handle run {run.id} completed with result: {run}")
        return run

    def __verify_run(self, run_id: str):
        """
        Verify the status of the run, if it is still in progress, wait for a second and try again
        :param run_id: identifier of the run
        :return: the run
        """
        run = self.client.beta.threads.runs.retrieve(run_id=run_id, thread_id=self.thread_id)
        logger_thread.debug(f"Run: {run.id}, status: {run.status}")
        if run.status not in ["in_progress", "queued"]:
            return run
        time.sleep(1)
        return self.__verify_run(run_id=run.id)

    def __load_thread(self):
        """
        Load the thread from the OpenAI API using the thread_id to see if it exists
        :return: Nothing
        """
        try:
            thread = self.client.beta.threads.retrieve(self.thread_id)
            logger_thread.debug(f"Obtained thread '{thread.id}'")
        except NotFoundError as err:
            logger_thread.warn(f"Thread {self.thread_id} not found")
            raise err

    @staticmethod
    def create_thread(client: OpenAI, assistant: Assistant):
        """
        Create a new Thread object wrapping the OpenAI thread using the OpenAI API.
        :param client: client to talk to the OpenAI API
        :param assistant: the assistant to run against
        :return: Thread object was a wrapper for the OpenAI thread
        """
        thread = client.beta.threads.create()
        logger_thread.info(f"Created thread {thread.id}")
        return Thread(client=client, thread_id=thread.id, assistant=assistant)
