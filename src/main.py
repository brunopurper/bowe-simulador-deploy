from flask import Flask
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # DON'T CHANGE THIS !!!

from src.models import db
from src.routes.formulario import formulario_bp
from src.routes.proposta import proposta_bp
from src.routes.dashboard import dashboard_bp

def create_app():
    app = Flask(__name__)
    
    # Configuração do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bowe_simulador.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'bowe-simulador-secret-key')
    
    # Configuração para uploads de arquivos
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
    
    # Criar diretórios de upload se não existirem
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'documentos'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'contas_luz'), exist_ok=True)
    
    # Inicializar extensões
    db.init_app(app)
    
    # Registrar blueprints
    app.register_blueprint(formulario_bp)
    app.register_blueprint(proposta_bp)
    app.register_blueprint(dashboard_bp)
    
    # Criar tabelas do banco de dados
    with app.app_context():
        db.create_all()
    
    return app

# Criar a aplicação para o Gunicorn
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
