# chatbotdb.py

import chromadb
import os
from groq import Groq
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Inicializa o cliente Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Inicializa o cliente ChromaDB e a coleção
chroma_client = chromadb.PersistentClient(path="db")
collection = chroma_client.get_or_create_collection(name="artigo")

# Define o prompt inicial do sistema
PROMPT = """
Você é um assistente de IA conversando com um usuário sobre o edital do Dataprev.
Use o seguinte contexto para responder à questão. Não use nenhuma informação adicional. Responda em português. Se não houver informação suficiente para responder à questão, diga que não temos informações suficientes.
"""

def get_response(questao, model="llama3-8b-8192", history=None):
    """
    Processa a pergunta do usuário e retorna a resposta gerada pelo assistente de IA, considerando o histórico de conversas.

    Args:
        questao (str): A pergunta feita pelo usuário.
        model (str): O modelo de linguagem a ser utilizado para gerar a resposta.
        history (list): Lista de mensagens anteriores no formato [{"role": "user", "content": "Pergunta"}, {"role": "assistant", "content": "Resposta"}].

    Returns:
        str: A resposta do assistente de IA.
    """
    # Log para debug
    print(f"Processando pergunta: {questao}")
    print(f"Usando modelo: {model}")

    # Obtém o contexto relevante do ChromaDB
    results = collection.query(query_texts=[questao], n_results=10)
    conteudos = results["documents"][0] if results["documents"] else []
    conteudo = ' '.join(conteudos)

    # Cria a lista de mensagens iniciando com o prompt do sistema
    messages = [
        {
            "role": "system",
            "content": PROMPT,
        },
        {
            "role": "system",
            "content": conteudo if conteudo else "Nenhum contexto disponível.",
        },
    ]

    # Adiciona o histórico de conversas, se fornecido
    if history:
        for msg in history:
            messages.append({
                "role": msg['role'],
                "content": msg['content'],
            })

    # Adiciona a pergunta atual do usuário
    messages.append({
        "role": "user",
        "content": questao,
    })

    # Gera a resposta do assistente
    try:
        chat_completion = client.chat.completions.create(
            model=model,
            messages=messages,
        )
        resposta = chat_completion.choices[0].message.content.strip()
    except Exception as e:
        resposta = "Desculpe, ocorreu um erro ao processar a sua solicitação."
        # Log do erro
        print(f"Erro: {e}")

    return resposta
