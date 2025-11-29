# AprovIA — Backend (API)

API backend em Flask para um assistente de Matemática/Inglês com chat em streaming, persistência local/MongoDB e embeddings de PDFs.

## Sumário
- Visão geral
- Arquitetura e pastas
- Tecnologias e dependências
- Configuração (.env)
- Como rodar (desenvolvimento / produção / Docker)
- Endpoints principais (exemplos)
- Swagger / documentação OpenAPI
- Comportamento de streaming
- Persistência: MongoDB e fallback local
- Embeddings (PDF -> Chroma)
- Troubleshooting
- Próximos passos

## Estrutura (resumida)
- app.py — ponto de entrada e rotas
- configs/swagger_config.py — template do Swagger
- controllers/ — controle das rotas (chat, embed)
- services/ — lógica de negócio (chat_service, embed_service)
- models/ — persistência (mongo_connection, history, vector_db)
- _temp/ — arquivos temporários (definido em .env)
- requirements.txt, .env (não versionar)

## Bibliotecas PyPI necessárias
- Flask
- Flask-CORS
- flasgger
- langchain
- langchain-text-splitters
- langchain-community
- dotenv
- chromadb
- unstructured
- ollama
- pymongo
- certifi
- dnspython

## Instalação (Windows)
1. Criar e ativar ambiente virtual:
```bash
python -m venv venv
venv\Scripts\activate
```

2. Instalar dependências básicas:
```bash
pip install -r requirements.txt
```

Dependências extras para embed/Leitura de PDFs:
```bash
pip install langchain langchain-text-splitters langchain-community langchain-ollama langchain-chroma chromadb unstructured
pip install "unstructured[all-docs]"
```

Para desenvolvimento mínimo (apenas API + Mongo + Ollama):
```bash
pip install Flask Flask-CORS flasgger ollama pymongo python-dotenv
```

## Configuração (.env)
Copie o arquivo de exemplo (sampleenv.txt) para `.env` e preencha:
- TEMP_FOLDER — pasta temporária (ex.: ./_temp)
- CHROMA_PATH — diretório do ChromaDB
- COLLECTION_NAME — coleção Chroma
- LLM_MODEL — modelo Ollama padrão
- TEXT_EMBEDDING_MODEL — modelo de embedding
- URL_CONNECTION_MONGODB — string de conexão (ou deixar vazio para fallback local)
- DATABASE_NAME, ASSISTANT_COLLECTION

Observação: não versionar o `.env` e não colocar credenciais em repositórios públicos.

## Como rodar (desenvolvimento)
```bash
venv\Scripts\activate
python app.py
```
Acesse Swagger UI em: `http://127.0.0.1:5000/swagger/` (ou conforme configuração).

## Notas importantes
- O projeto já implementa fallback local (arquivo JSON) quando o MongoDB não está disponível.
- Timestamps são armazenados como strings ISO para compatibilidade com JSON/Swagger.
- Para streaming via curl use `-N` (ex.: `curl -N ...`) para visualizar chunks.

## Troubleshooting rápido
- Erro SSL/TLS ao conectar Mongo Atlas: atualizar certifi/dnspython/pymongo e verificar firewall/proxy.
- Erro "datetime not JSON serializable": timestamps já estão em ISO strings no histórico.
- Ollama: verifique se o serviço e o modelo estão rodando localmente.

## Exemplos rápidos
Criar novo chat (curl, streaming):
```bash
curl -N -X POST "http://127.0.0.1:5000/chats/new?user_id=test" \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen2-math","message":"Como resolver 2+2?"}'
```

Listar chats:
```bash
curl "http://127.0.0.1:5000/chats?user_id=test"
```

Recuperar chat:
```bash
curl "http://127.0.0.1:5000/chats/{chat_id}?user_id=test"
```

Enviar PDF para embed (exemplo de uso da rota embed):
```bash
curl -F "file=@arquivo.pdf" "http://127.0.0.1:5000/embed?user_id=test"
```
