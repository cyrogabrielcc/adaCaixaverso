# Usa uma imagem base oficial do Python, igual à da aplicação web
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o script ETL para dentro do container
COPY etl.py .

# Define o comando padrão (o que o container fará se for iniciado sem um comando específico)
CMD ["python", "etl.py"]