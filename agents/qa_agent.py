from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

CHROMA_PATH = "data"


def answer_question(query: str):
    db = Chroma(persist_directory=CHROMA_PATH,
                embedding_function=OpenAIEmbeddings())
    retriever = db.as_retriever()

    qa_chain = RetrievalQA.from_chain_type(
        # 🔺 aqui está o modelo mais barato
        llm=ChatOpenAI(model_name="gpt-3.5-turbo-0125"),
        retriever=retriever,
        return_source_documents=False
    )

    result = qa_chain.invoke({"query": query})
    return result['result']  # 🔺 Só retorna o texto puro
