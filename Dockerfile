# Usa a imagem oficial do Python como base
FROM python:3.11-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos da aplicação para o contêiner
COPY . .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Cria a pasta de uploads (caso não exista) e define as permissões
RUN mkdir -p static/uploads && chmod -R 777 static/uploads

# Expõe a porta 5000 para acesso à aplicação
EXPOSE 5000

# Usa Gunicorn para rodar o Flask em produção
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "agriapp:app"]
