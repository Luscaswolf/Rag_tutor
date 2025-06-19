from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

CHROMA_PATH = "data"

def upload_and_index(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(documents)

    print(f"[upload_agent] Total de chunks: {len(chunks)}")
    for i, chunk in enumerate(chunks[:2]):
        print(f"[chunk] {chunk.page_content[:200]}")

    Chroma.from_documents(
        documents=chunks,
        embedding=OpenAIEmbeddings(),
        collection_name="pdf_collection",
        persist_directory=CHROMA_PATH
    )

    return True
