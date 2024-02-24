import os

from openai import OpenAI, NotFoundError


class File:

    def __init__(self, client: OpenAI, file_id: str, filename: str):
        self.client = client
        self.file_id = file_id
        self.filename = filename

    @staticmethod
    def load_file_by_name(client: OpenAI, filename: str):
        files = File.list_files(client=client)
        for file in files:
            if file["name"] == filename:
                return File(client=client, file_id=file["id"], filename=filename)

        raise FileNotFoundError(f"File {filename} not found")

    @staticmethod
    def load_file_by_id(client: OpenAI, file_id: str):
        try:
            file = client.files.retrieve(file_id)
            return File(client=client, file_id=file.id, filename=file.filename)
        except NotFoundError as err:
            raise FileNotFoundError(f"File {file_id} not found")

    @staticmethod
    def list_files(client: OpenAI):
        return [{"id": file.id, "name": file.filename,"purpose": file.purpose} for file in client.files.list()]
