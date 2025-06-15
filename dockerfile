# Use uma imagem base leve de Python
FROM python:3.10-slim

# Crie e use um diretório de trabalho
WORKDIR /app

# Copie as dependências e instale
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie todo o código
COPY . .

# Defina a porta do Flask
EXPOSE 5001

# Comando para rodar usando gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "src.main:app"]
