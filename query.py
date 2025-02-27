import ollama

# from langchain_community.chat_models import ChatOllama
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnablePassthrough
# from addDocuments import 

# def query(query):
#     local_model = ChatOllama(model='qwen2')
#     template = '{prompt} -- answer in less than 45 words'
#     prompt = ChatPromptTemplate.from_template(template)
#     chain = prompt | local_model | StrOutputParser()

#     return chain.invoke({'prompt':query})

# def query2(query):
#     local_model = ChatOllama(model='qwen2')
    
#     # Criar um retriever para receber documentos relevantes quando fazemos uma pergunta
#     retriever = vectorstore.as_retriever()

#     rag_template = '''
#     Answer the question based only on the following context: {context}
#     Question: {question} - Answer in less than 60 words
#     '''
#     rag_prompt = ChatPromptTemplate.from_template(rag_template)
#     rag_chain = (
#         {
#             'context' : retriever,
#             'question' : RunnablePassthrough()
#         }
#         | rag_prompt
#         | local_model
#         | StrOutputParser()
#     ) 

#     return rag_chain.invoke(query)


def query(query):
    response = ollama.chat(model='qwen2', messages=[
        {
            'role':'user',
            'content': query + " -- answer in less than 25 words",  
        },
    ])

    return response['message']['content']

