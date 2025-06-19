from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
import os

CHROMA_PATH = "embeddings"


def load_documents():
    documents = []
    for filename in os.listdir("data"):
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(f"data/{filename}")
            documents.extend(loader.load())
    return documents


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200)
    return splitter.split_documents(documents)


def create_vector_store():
    docs = load_documents()
    chunks = split_documents(docs)
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=OpenAIEmbeddings(),
        persist_directory=CHROMA_PATH
    )
    vectordb.persist()


if __name__ == "__main__":
    create_vector_store()
