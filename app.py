"""
Arquivo de inicialização para o Simulador Bowe
Este arquivo deve ser executado a partir da raiz do projeto
"""
import os
import sys

# Adiciona o diretório atual ao path do Python para permitir importações relativas
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Importa a função create_app em vez da instância app
from src.main import create_app

# Cria uma nova instância da aplicação usando a função factory
app = create_app()

if __name__ == "__main__":
    print("Iniciando o Simulador Bowe...")
    app.run(host='0.0.0.0', port=5000, debug=True)
