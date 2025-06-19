from agents.memory_agent import MemoryAgent
from agents.refinement_agent import refine_response
from agents.qa_agent import answer_question
from agents.upload_agent import upload_and_index
import streamlit as st

from dotenv import load_dotenv
load_dotenv()


st.set_page_config(page_title="Tutor via PDF", page_icon="🤖")
st.title("📚 Tutor de Estudos via PDF")

# Inicializa o agente de memória (apenas uma vez)
if "memory_agent" not in st.session_state:
    st.session_state.memory_agent = MemoryAgent()
if "pdf_carregado" not in st.session_state:
    st.session_state.pdf_carregado = False

# Upload e Indexação
uploaded_file = st.file_uploader("📄 Faça upload de um PDF", type="pdf")

if uploaded_file and not st.session_state.pdf_carregado:
    with st.spinner("📖 Lendo e indexando o documento..."):
        success = upload_and_index(uploaded_file)
        if success:
            st.success("✅ Documento processado com sucesso!")
            st.session_state.pdf_carregado = True

# Consulta e resposta
if st.session_state.pdf_carregado:
    user_query = st.text_input("🔎 O que você quer saber?")
    if user_query:
        with st.spinner("🤔 Pensando na resposta..."):
            raw_answer = answer_question(user_query)
            final_answer = refine_response(raw_answer, user_query)
            st.write("💬 **Resposta:**", final_answer)

            # Armazena na memória
            st.session_state.memory_agent.add_to_memory(
                user_query, final_answer)

    # Histórico
    if st.session_state.memory_agent.get_memory():
        with st.expander("🧠 Histórico da Conversa"):
            for time, q, a in st.session_state.memory_agent.get_memory():
                st.markdown(f"**{time}** — **Pergunta:** {q}")
                st.markdown(f"📘 Resposta: {a}")
                st.markdown("---")
else:
    st.info("⏳ Faça upload de um PDF para iniciar.")
