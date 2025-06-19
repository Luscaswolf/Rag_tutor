import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

CHROMA_PATH = "data"


def upload_and_index(file):
    os.makedirs(CHROMA_PATH, exist_ok=True)

    temp_path = f"{CHROMA_PATH}/{file.name}"
    with open(temp_path, "wb") as f:
        f.write(file.getbuffer())

    loader = PyPDFLoader(temp_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(documents)

    db = Chroma.from_documents(
        documents=chunks, embedding=OpenAIEmbeddings(), persist_directory=CHROMA_PATH)
    db.persist()
    return True
