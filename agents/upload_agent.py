import os
import shutil
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

CHROMA_PATH = "data"

def upload_and_index(file_path):
    #  Apaga o diretório do banco vetorial se ele já existir
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    #  Carrega o conteúdo do PDF
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    #  Divide em pedaços menores
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(documents)

    #  Log dos chunks extraídos
    print(f"[upload_agent] Total de chunks: {len(chunks)}")
    for i, chunk in enumerate(chunks[:3]):
        print(f"[chunk {i+1}] {chunk.page_content[:300]}")

    #  Cria ou recria o banco vetorial
    db = Chroma(
        collection_name="pdf_collection",
        embedding_function=OpenAIEmbeddings(),
        persist_directory=CHROMA_PATH
    )

    #  Adiciona os documentos ao banco
    db.add_documents(chunks)

    return True