import importlib

from openai import OpenAI, NotFoundError

from openai_assistant.assistant import logger_assistant
from openai_assistant.files.file import File


class Assistant:
    def __init__(self, client: OpenAI, assistant_id: str,
                 tools_module_name: str = "openai_assistant.assistant.assistant_functions"):
        self.client = client
        self.assistant_id = assistant_id
        self.available_tools = []
        self.tools_module_name = tools_module_name
        self.__load_assistant()

    def register_functions(self, tool_definitions: list[dict]):
        tools = []
        for tool_definition in tool_definitions:
            function_tool = {
                "type": "function",
                "function": tool_definition
            }
            tools.append(function_tool)
            self.available_tools.append(tool_definition["name"])
            logger_assistant.info(f"Registered function {tool_definition['name']}")

        self.client.beta.assistants.update(self.assistant_id, tools=tools)

    def register_function(self, tool_definition: dict):
        function_tool = {
            "type": "function",
            "function": tool_definition
        }
        logger_assistant.info(f"Registered function {tool_definition['name']}")
        self.available_tools.append(tool_definition["name"])

        self.client.beta.assistants.update(self.assistant_id, tools=[function_tool])

    def register_file(self, file_name: str):
        file = File.load_file_by_name(client=self.client, filename=file_name)
        self.client.beta.assistants.files.create(assistant_id=self.assistant_id, file_id=file.file_id)

    def call_tool(self, tool_name: str, arguments: dict):
        if tool_name not in self.available_tools:
            logger_assistant.warning(f"Tool {tool_name} is not available")
            return "ERROR: Tool not available, do not use unknown tools."

        module = importlib.import_module(self.tools_module_name)
        if tool_name in dir(module) and callable(getattr(module, tool_name)):
            tool = getattr(module, tool_name)
            return tool(**arguments)
        else:
            logger_assistant.warning(f"Tool {tool_name} is not available")
            return "ERROR: Tool not available"

    def __load_assistant(self):
        try:
            assistant = self.client.beta.assistants.retrieve(self.assistant_id)
            self.available_tools = [tool.function.name for tool in assistant.tools if tool.type == "function"]
            logger_assistant.debug(f"Obtained assistant '{assistant.name}'")
        except NotFoundError as err:
            logger_assistant.warning(f"Assistant {self.assistant_id} not found")
            raise err

    def add_retrieval_tool(self):
        self.client.beta.assistants.update(self.assistant_id, tools=[{"type": "retrieval"}])

    @staticmethod
    def create_assistant(client: OpenAI, name: str, instructions: str, tools_module_name: str = None,
                         model: str = "gpt-4-turbo-preview"):
        assistant = client.beta.assistants.create(
            name=name,
            instructions=instructions,
            model=model
        )
        return Assistant(client=client, assistant_id=assistant.id, tools_module_name=tools_module_name)

    @staticmethod
    def load_assistant_by_name(client: OpenAI, name: str, tools_module_name: str = None):
        assistants = Assistant.list_assistants(client=client)
        for assistant in assistants:
            if assistant["name"] == name:
                return Assistant(client=client, assistant_id=assistant["id"], tools_module_name=tools_module_name)

        raise FileNotFoundError(f"Assistant {name} not found")

    @staticmethod
    def list_assistants(client: OpenAI):
        assistants = [{"id": assistant.id, "name": assistant.name} for assistant in client.beta.assistants.list()]
        for assistant in assistants:
            logger_assistant.debug(f"Assistant id: {assistant['id']}, name: {assistant['name']}")
        return assistants
