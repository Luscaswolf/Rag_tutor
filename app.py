from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from agents.upload_agent import upload_and_index
from agents.qa_agent import answer_question
from agents.refinement_agent import refine_response
from dotenv import load_dotenv
import shutil
import os

load_dotenv()

app = FastAPI()
UPLOAD_FOLDER = "data"


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        # 🟡 Lê e salva o conteúdo do arquivo corretamente
        with open(file_path, "wb") as buffer:
            content = await file.read()  # <- await obrigatório para UploadFile
            buffer.write(content)

        # ✅ Passa apenas o caminho do arquivo
        success = upload_and_index(file_path)
        if success:
            return {"message": "PDF carregado e indexado com sucesso."}
        else:
            return JSONResponse(status_code=500, content={"error": "Falha ao indexar o PDF."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/pergunta")
async def responder(pergunta: str = Form(...)):
    try:
        print("[main_api] Pergunta recebida:", pergunta)

        resposta_bruta = answer_question(pergunta)
        print("[main_api] Resposta bruta:", resposta_bruta)

        resposta_final = refine_response(resposta_bruta, pergunta)
        print("[main_api] Resposta refinada:", resposta_final)

        return {"resposta": resposta_final}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
