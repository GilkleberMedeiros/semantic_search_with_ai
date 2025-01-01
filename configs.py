import os
import getpass
from random import randint


class ConfigObj:
    """
    Temporary config class
    """
    def __init__(self) -> None:
        self.model_chat = "gemini-1.5-pro"
        self.chat_model_temperature = 0.7
        self.chat_model_top_p = None
        self.chat_model_top_k = None
        self.model_embeddings = "models/embedding-001"

        self.text_splitter_chunk_size = 1000
        self.text_splitter_chunk_overlap = 50
        self.text_splitter_length_function = len

        self.vector_store_search_k = 1
        self.vector_store_search_fetch_k = 20

        self.retrieval_chain_type = "stuff"

        self.google_api_key_name = "GOOGLE_AISTUDIO_API_KEY"


__configs: ConfigObj | None = None

def get_configs() -> ConfigObj:
    global __configs

    __configs = __configs or ConfigObj()

    return __configs

def get_google_api_key() -> str:
    configs = get_configs()
    GOOGLE_API_KEY = os.environ.get(configs.google_api_key_name, "")

    if not GOOGLE_API_KEY:
        GOOGLE_API_KEY = getpass.getpass("Provide your google ai api key: ")

    return GOOGLE_API_KEY 