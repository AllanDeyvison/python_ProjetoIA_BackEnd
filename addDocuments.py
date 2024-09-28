from langchain_community.vectorstores import Chroma
from langchain_community import embeddings
from langchain.text_splitter import CharacterTextSplitter
import pandas as pd


def addDocs(docs):
    df = pd.read_excel(docs)

    # 1. Dividir os dados em partes
    # Definir as Chunks (partes)
    text_splitter=CharacterTextSplitter.from_tiktoken_encoder(chunk_size=7500, chunk_overlap=100)
    # O overlap (espaço) entre as partes é o chunk_overlap

    # Dividir os documentos a partir do tamanho das chunks
    docs_splits = text_splitter.split_documents(df) # --> ($documento a ser dividido)


    # 2. Converter os documentos em Embeddings e guardar eles
    vectorstore = Chroma.from_documents(
        documents=docs_splits, # Documentos que quer mandar
        collection_name='local_data', # Nome da coleção de arquivos
        embedding=embeddings.OllamaEmbeddings(model='nomic-embed-text') #Qual o programa para embedding, nesse caso, um modelo LLM do ollama
    )

    return True