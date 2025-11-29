import os
import logging
import certifi
from pymongo import MongoClient, ASCENDING
from pymongo.errors import PyMongoError

URL = os.getenv("URL_CONNECTION_MONGODB")
DATABASE_NAME = os.getenv("DATABASE_NAME", "aprovia_db")
ASSISTANT_COLLECTION = os.getenv("ASSISTANT_COLLECTION", "assistant")

client = None
db = None
collection = None

def _connect_mongo():
    global client, db, collection
    if client is not None:
        return

    if not URL:
        logging.warning("URL_CONNECTION_MONGODB não definido. MongoDB desabilitado.")
        return

    try:
        # usa certifi para o CA bundle e timeout curto para não travar a importação
        client = MongoClient(
            URL,
            tls=True,
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=10000,
            connectTimeoutMS=10000,
            socketTimeoutMS=20000,
        )
        # teste rápido de conexão
        client.admin.command("ping")
        db = client[DATABASE_NAME]
        collection = db[ASSISTANT_COLLECTION]
        try:
            collection.create_index(
                [("user_id", ASCENDING), ("chat_id", ASCENDING)],
                unique=True,
                name="user_chat_unique",
            )
        except Exception as e:
            logging.warning(f"Não foi possível criar índice (continuando): {e}")
        logging.info("Conexão com MongoDB estabelecida com sucesso.")
    except PyMongoError as e:
        logging.error(f"Falha ao conectar no MongoDB: {e}")
        client = None
        db = None
        collection = None

# tenta conectar na importação, mas sem levantar exceção não tratada
try:
    _connect_mongo()
except Exception as e:
    logging.exception("Erro inesperado ao inicializar conexão MongoDB")

def get_collection():
    """
    Retorna a collection ou None se o MongoDB não estiver disponível.
    Use checagem em quem chamar: if get_collection() is None: fallback...
    """
    return collection
