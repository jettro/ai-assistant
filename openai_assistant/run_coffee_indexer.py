import logging
import os
import sys
import pandas as pd

from openai_assistant.store import logger_store
from openai_assistant.store.access_weaviate import AccessWeaviate
from openai_assistant.store.coffee_collection import coffee_weaviate_properties


def load_coffee_data():
    return pd.read_csv('../data/coffee_bar_product_list.csv')


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
    logger_store.setLevel(logging.DEBUG)

    weaviate = AccessWeaviate(url=os.getenv("WEAVIATE_URL"),
                              access_key=os.getenv("WEAVIATE_ACCESS_KEY"),
                              openai_api_key=os.getenv("OPENAI_API_KEY"))
    weaviate.force_create_collection(collection_name="coffee", properties=coffee_weaviate_properties())

    df = load_coffee_data()
    for index, row in df.iterrows():
        document = row.to_dict()
        weaviate.add_document(collection_name="coffee", properties=document)

    weaviate.close()
