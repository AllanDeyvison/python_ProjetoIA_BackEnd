import os
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

CHROMA_PATH = os.getenv('CHROMA_PATH')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')
TEXT_EMBEDDING_MODEL = os.getenv('TEXT_EMBEDDING_MODEL')

def get_vector_db():
    embbeding = OllamaEmbeddings(model=TEXT_EMBEDDING_MODEL)
    db = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_PATH,
        embedding_function=embbeding
    )
    return db
