from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA

CHROMA_PATH = "data"

def answer_question(query: str):
    print("[qa_agent] Lendo banco vetorial de:", CHROMA_PATH)

    db = Chroma(
        persist_directory=CHROMA_PATH,
        collection_name="pdf_collection",
        embedding_function=OpenAIEmbeddings()
    )
    retriever = db.as_retriever()

    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model_name="gpt-3.5-turbo-0125"),
        retriever=retriever,
        return_source_documents=False
    )

    result = qa_chain.invoke({"query": query})
    print("[qa_agent] Resultado:", result["result"])
    return result["result"]
