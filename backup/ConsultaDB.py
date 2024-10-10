import chromadb
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
os.environ["TOKENIZERS_PARALLELISM"] = "false"
questao = input("Como posso lhe ajudar?")
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

chroma_client = chromadb.Client()
chroma_client = chromadb.PersistentClient(path="db")
collection = chroma_client.get_or_create_collection(name="artigo")

results = collection.query(query_texts=questao, n_results=10)
conteudo = results["documents"][0][0] + results["documents"][0][9]

prompt = """
Você é um assistente  de IA. Você está conversando com um usuário que está procurando por informações sobre um determinado.
Use o o seguinte contexto para responder a questão, não use nenhuma informação adicional, se não houver informação  suficiente para responder a questão, diga que não temos informações suficientes.
"""

chat_completion = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=[
        {
            "role": "system",
            "content": prompt,
        },
        {"role": "system", "content": conteudo},
        {"role": "system", "content": questao},
    ],
    
)

print(chat_completion.choices[0].message.content)