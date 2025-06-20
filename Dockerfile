FROM python:3.10.5

WORKDIR /app

#Corrige problemas de repositório e instala dependências
RUN apt-get update -y --fix-missing && \
    apt-get install -y git && \
    apt-get install sqlite3 libsqlite3-dev
    


#Clona o repositório privado
RUN git clone https://github.com/Luscaswolf/Rag_tutor .

#Copia e instala as dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

#Atualiza o repositório e roda a aplicação no contêiner
CMD ["sh", "-c", "git reset --hard && git pull https://github.com/Luscaswolf/Rag_tutor && pip install -r requirements.txt && python app.py"]