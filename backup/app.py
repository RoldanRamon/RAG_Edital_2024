# app.py

import streamlit as st
from ChatbotDB import get_response

# Configurações da aplicação Streamlit
st.set_page_config(page_title="Chatbot de Assistente de IA", layout="centered")

# Injetar CSS para personalizar a sidebar e adicionar elementos adicionais
st.markdown(
    """
    <style>
    /* Reduzir a largura da sidebar */
    [data-testid="stSidebar"] {
        width: 50px;
    }

    /* Estilizar o rodapé da sidebar */
    .sidebar-footer {
        position: fixed;
        bottom: 20px;
        width: 230px;
        text-align: center;
        font-size: 14px;
        color: #555;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Título e descrição
st.title("Chatbot de PDF")
st.write("Faça suas perguntas sobre o edital do Dataprev e receba respostas baseadas no conteúdo disponível.")

# Definir os modelos disponíveis
available_models = [
    "gemma2-9b-it",
    "llama3-groq-70b-8192-tool-use-preview",
    "llama-3.1-70b-versatile",
    "llama-3.2-90b-vision-preview"
    # Adicione outros modelos conforme disponíveis na sua API Groq
]

# Inicializa o histórico de conversas na sessão
if 'history' not in st.session_state:
    st.session_state.history = []

# Função para adicionar uma nova interação ao histórico
def add_to_history(pergunta, resposta, max_history=20):
    st.session_state.history.append({"role": "user", "content": pergunta})
    st.session_state.history.append({"role": "assistant", "content": resposta})
    
    # Limita o histórico ao número máximo de mensagens
    if len(st.session_state.history) > max_history:
        st.session_state.history = st.session_state.history[-max_history:]

import streamlit as st

# Adicionar a imagem no sidebar, centralizada no topo
st.sidebar.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        display: flex;
        justify-content: center;
        align-items: center;
        padding-top: 5px; /* Ajuste o padding para controlar a distância do topo */
    }
    img {
        width: 50%;
        display: block;
        margin: 0 auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.image("logo.jpg")


# Caixa de seleção para escolher o modelo na sidebar
st.sidebar.header("Configurações do Chatbot")
selected_model = st.sidebar.selectbox(
    "Escolha o modelo de linguagem:",
    options=available_models,
    index=0,  # Índice do modelo padrão
)

# Adicionar rodapé na sidebar com hiperlink ativo
st.sidebar.markdown("""
    <div class="sidebar-footer">
        Criado por <a href="https://www.linkedin.com/in/ramon-roldan-de-lara/" target="_blank">Ramon de Lara</a>
    </div>
    """,
    unsafe_allow_html=True
)

# Caixa de entrada para o usuário dentro de um formulário
with st.form(key='chat_form', clear_on_submit=True):
    questao = st.text_input("Digite sua pergunta:", "")
    submit_button = st.form_submit_button(label='Enviar')

    if submit_button and questao.strip() != "":
        with st.spinner("Processando sua pergunta..."):
            # Passa o histórico para a função get_response
            resposta = get_response(questao, model=selected_model, history=st.session_state.history)
        # Adiciona a interação ao histórico com limitação
        add_to_history(questao, resposta)

# Exibe o histórico de conversas em ordem reversa (últimas interações no topo)
st.markdown("### Histórico de Conversas")
for chat in reversed(st.session_state.history):
    if chat['role'] == "user":
        st.markdown(f"""<div class="user-message">
                        <strong>Usuário:</strong> {chat['content']}
                      </div>""",
                    unsafe_allow_html=True)
    elif chat['role'] == "assistant":
        st.markdown(f"""<div class="assistant-message">
                        <strong>Assistente:</strong> {chat['content']}
                      </div>""",
                    unsafe_allow_html=True)
    st.write("---")
