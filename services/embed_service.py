import os
from datetime import datetime
from werkzeug.utils import secure_filename
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models.vector_db import get_vector_db

TEMP_FOLDER = os.getenv('TEMP_FOLDER')

def allowed_file(filename):
    has_dot = '.' in filename
    is_pdf = filename.rsplit('.', 1)[1].lower() in {'pdf'}
    return has_dot and is_pdf

def save_file(file):
    ct = datetime.now()
    ts = ct.timestamp()
    new_filename = str(ts) + "_" + secure_filename(file.filename)
    file_path = os.path.join(TEMP_FOLDER, new_filename)
    file.save(file_path)
    return file_path

def load_and_split_data(file_path):
    loader = UnstructuredPDFLoader(file_path=file_path)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=7500, chunk_overlap=100)
    chunks = text_splitter.split_documents(data)
    return chunks

def embed_pdf(file):
    if file.filename != '' and file and allowed_file(file.filename):
        file_path = save_file(file)
        chunks = load_and_split_data(file_path)
        db = get_vector_db()
        db.add_documents(chunks)
        os.remove(file_path)
        return True
    return False
