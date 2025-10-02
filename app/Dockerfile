# Usa uma imagem base oficial do Python
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto dos arquivos da aplicação
COPY . .

# Expõe a porta em que a aplicação vai rodar
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["python", "app.py"]