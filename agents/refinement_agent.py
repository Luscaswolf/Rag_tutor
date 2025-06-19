from langchain_community.chat_models import ChatOpenAI


def refine_response(raw_answer, question):
    llm = ChatOpenAI(model_name="gpt-3.5-turbo-0125",
                     temperature=0.3)  # 🔺 usa o mesmo modelo barato
    prompt = f"""
Você é um assistente responsável por revisar respostas geradas por um sistema de recuperação de informação.
Pergunta: {question}
Resposta inicial: {raw_answer}
Revise ou melhore a resposta se necessário, mantendo-a clara e correta.
"""
    return llm.invoke(prompt).content  # 🔺 Extrai apenas o conteúdo puro
