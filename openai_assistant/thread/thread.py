import json
import time

from openai import OpenAI, NotFoundError

from openai_assistant.assistant.assistant import Assistant


# TODO Maybe we should add the available tools to the thread, so we can use them in the run_against_assistant method


class Thread:
    def __init__(self, client: OpenAI, thread_id: str, assistant: Assistant):
        self.client = client
        self.thread_id = thread_id
        self.assistant = assistant
        self.__load_thread()

    def print_messages(self):
        messages = self.client.beta.threads.messages.list(self.thread_id)
        for message in messages:
            print(f"Message: {message}")

    def add_new_message(self, message: str):
        self.client.beta.threads.messages.create(
            thread_id=self.thread_id,
            role="user",
            content=message
        )

    def run_against_assistant(self):
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread_id,
            assistant_id=self.assistant.assistant_id
        )
        run = self.__verify_run(run_id=run.id)
        if run.status == "requires_action":
            print(f"Run {run.id} requires action")
            tools_calls = run.required_action.submit_tool_outputs.tool_calls
            for tool_call in tools_calls:
                print(f"Tool call: {tool_call}")
            tool_outputs = []
            for tool_call in tools_calls:
                if tool_call.function.name in self.assistant.tools.keys():
                    tool = self.assistant.tools[tool_call.function.name]
                    arguments = json.loads(tool_call.function.arguments)
                    result = tool(**arguments)
                    tool_outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": result
                    })
                else:
                    print(f"Tool {tool_call.function.name} is not available: {tool_call}")

                    tool_outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": "ERROR: Tool not available"
                    })
            run = self.client.beta.threads.runs.submit_tool_outputs(
                run_id=run.id,
                thread_id=self.thread_id,
                tool_outputs=tool_outputs
            )
            self.__verify_run(run_id=run.id)
        else:
            print(f"Run {run.id} completed with result: {run}")
            return run

    def cancel_runs(self):
        runs = self.client.beta.threads.runs.list(thread_id=self.thread_id)
        for run in runs:
            if run.status not in ["cancelled", "completed", "expired"]:
                print(f"Canceling run {run.id} with status {run.status}")
                self.client.beta.threads.runs.cancel(run_id=run.id, thread_id=self.thread_id)

    def __verify_run(self, run_id: str):
        run = self.client.beta.threads.runs.retrieve(run_id=run_id, thread_id=self.thread_id)
        print(f"Run: {run.id}, status: {run.status}")
        if run.status not in ["in_progress", "queued"]:
            return run
        time.sleep(1)
        return self.__verify_run(run_id=run.id)

    def __load_thread(self):
        try:
            thread = self.client.beta.threads.retrieve(self.thread_id)
            print(f"Obtained thread '{thread.id}'")
        except NotFoundError as err:
            print(f"Thread {self.thread_id} not found")
            raise err

    @staticmethod
    def create_thread(client: OpenAI):
        thread = client.beta.threads.create()
        print(f"Created thread {thread.id}")
        return Thread(client=client, thread_id=thread.id)
