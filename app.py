
import os
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, jsonify, request
from flask_cors import CORS
from query import query
from embed import embed
# from addDocuments import addDocs

TEMP_FOLDER = os.getenv('TEMP_FOLDER')
os.makedirs(TEMP_FOLDER, exist_ok=True)

app = Flask(__name__)
CORS(app) # Isso habilita o CORS para todas as rotas

@app.route('/embed', methods=['POST'])
def route_embed():
    if 'file' not in request.files:
        return jsonify({"error" : "No file part"}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({"error" : "No selected file"}), 400
    
    embedded = embed(file)

    if embedded:
        return jsonify({"success" : "File added successfuly"}), 200
    
    return jsonify({"error" : "File added unsuccessfully"}), 400

@app.route('/query', methods=['POST'])
def route_query():
    data = request.get_json()
    response = query(data.get('message'))

    if response:
        return jsonify({"answer": response}), 200
    else:
        return jsonify({"error": "Something went wrong"}), 400



if __name__ == "__main__":
    app.run()