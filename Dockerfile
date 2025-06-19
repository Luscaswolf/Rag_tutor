FROM python:3.10.5
WORKDIR /app

# Corrige problemas de repositório e instala dependências
RUN apt-get update -y --fix-missing && \
    apt-get install -y git
# Argumentos para autenticação no GitHub
# Clona o repositório privado
RUN git clone https://${GITHUB_USERNAME}:${GITHUB_TOKEN}@https://github.com/Luscaswolf/Rag_tutor .
# Instala dependências Python
COPY  requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080
CMD git reset --hard && \
    git pull https://${GITHUB_USERNAME}:${GITHUB_TOKEN}@https://github.com/Luscaswolf/Rag_tutor && \
    pip install -r requirements.txt && \
    python main.py