import os
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Subclasse para ajustar o model_config
from langchain_community.embeddings import GPT4AllEmbeddings

class CustomGPT4AllEmbeddings(GPT4AllEmbeddings):
    model_config = {'protected_namespaces': ()}

criar_db = True  # Alterado para True

def open_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            contents = file.read()
        return contents
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"Error: {e}"

if criar_db:
    arquivo = "edital.txt"
    texto = open_file(arquivo)
    filename = os.path.basename(arquivo)
    metadatas = [{"nome do arquivo": filename}]

    chunk_size = 500  # Ajuste conforme necessário
    percentual_overlap = 0.2

    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=chunk_size,
                                          chunk_overlap=int(chunk_size * percentual_overlap),
                                          length_function=len,
                                          )
    all_splits = text_splitter.create_documents([texto], metadatas=metadatas)

    vectorstore = Chroma.from_documents(documents=all_splits,
                                        embedding=OpenAIEmbeddings(),
                                        persist_directory="chroma")
    vectorstore.persist()
else:
    print("Não criou o BD")
    vectorstore = Chroma(embedding_function=OpenAIEmbeddings(), persist_directory="chroma")

question = "Quando será a prova"

docs = vectorstore.similarity_search_with_score(question, k=4)

# Extrai o conteúdo dos documentos
contexto = "\n".join([doc.page_content for doc, score in docs])

def enviar_pergunta(pergunta):
    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-4",  # Certifique-se de que tem acesso ao GPT-4
            messages=[
                {"role": "user", "content": pergunta}
            ]
        )
        resposta_texto = resposta.choices[0].message.content
        return resposta_texto
    except Exception as e:
        return f"Ocorreu um erro: {e}"

# Formata a pergunta com o contexto
pergunta_formatada = f"{question}\n\nUse os dados a seguir como referência para a resposta:\n{contexto}"

# Envia a pergunta formatada
resposta = enviar_pergunta(pergunta_formatada)

print("Resposta:", resposta)
