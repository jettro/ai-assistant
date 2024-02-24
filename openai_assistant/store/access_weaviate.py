import uuid

import weaviate
import weaviate.classes as wvc

from openai_assistant.store import logger_store


class AccessWeaviate:

    def __init__(self, url, access_key, openai_api_key: str):
        logger_store.debug(f"Connecting to Weaviate at {url}")
        self.client = weaviate.connect_to_wcs(
            cluster_url=url,
            auth_credentials=weaviate.auth.AuthApiKey(access_key),
            headers={"X-OpenAI-Api-Key": openai_api_key}
        )

    def does_collection_exist(self, collection_name):
        exists = self.client.collections.exists(collection_name)

        if not exists:
            logger_store.debug(f"Collection {collection_name} does not exist")

        return exists

    def add_document(self, collection_name: str,  properties: dict):
        logger_store.debug(f"Adding document to collection {collection_name}")
        self.client.collections.get(collection_name).data.insert(
            uuid=uuid.uuid4(),
            properties=properties
        )

    def delete_collection(self, collection_name: str):
        logger_store.debug(f"Deleting collection {collection_name}")
        self.client.collections.delete(collection_name)

    def create_collection(self, collection_name: str, properties: list):
        logger_store.debug(f"Creating collection {collection_name}")

        self.client.collections.create(
            name=collection_name,
            properties=properties,
            vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(
                model="text-embedding-3-small",
                type_="text",
            )
        )

    def force_create_collection(self, collection_name: str, properties: list):
        logger_store.debug(f"Force creating collection {collection_name}")
        if self.does_collection_exist(collection_name):
            self.delete_collection(collection_name)

        self.create_collection(collection_name, properties)

    def close(self):
        logger_store.debug("Closing Weaviate connection")
        self.client.close()

    def print_meta(self, collection_name: str):
        meta = self.client.get_meta()
        print(f"Version: {meta['version']}")
        collections = self.client.collections.list_all(simple=False)
        for collection in collections:
            print(f"Available collection: {collection}")
        print(self.client.collections.export_config(name=collection_name))
