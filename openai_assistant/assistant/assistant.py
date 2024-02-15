from openai import OpenAI, NotFoundError


class Assistant:
    def __init__(self, client: OpenAI, assistant_id: str):
        self.client = client
        self.assistant_id = assistant_id
        self.__load_assistant()

    def register_function(self, tool: dict):
        function_tool = {
            "type": "function",
            "function": tool
        }
        self.client.beta.assistants.update(self.assistant_id, tools=[function_tool])
        print(f"Registered function {tool['name']}")

    def __load_assistant(self):
        try:
            assistant = self.client.beta.assistants.retrieve(self.assistant_id)
            print(f"Obtained assistant '{assistant.name}'")
        except NotFoundError as err:
            print(f"Assistant {self.assistant_id} not found")
            raise err

    @staticmethod
    def create_assistant(client: OpenAI):
        assistant = client.beta.assistants.create(
            name="Jettro's Assistant",
            instructions="You are my assistant to take care of small tasks for me. I will ask you to do something for me, "
                         "this can be a question, a task or something else. You will then try to do this for me. If you "
                         "can't do it, you will let me know. If you need more information, you will ask me for it. If you "
                         "need to make a decision, you will ask me for it. If you need to do something, you will do it. ",
            tools=[{"type": "code_interpreter"}],
            model="gpt-4-turbo-preview"
        )
        return Assistant(client=client, assistant_id=assistant.id)

    @staticmethod
    def list_assistants(client: OpenAI):
        assistants = [{"id": assistant.id, "name": assistant.name} for assistant in client.beta.assistants.list()]
        for assistant in assistants:
            print(f"Assistant id: {assistant['id']}, name: {assistant['name']}")
        return assistants