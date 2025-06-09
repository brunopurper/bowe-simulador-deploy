from flask import Flask, flash, request, redirect, render_template
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # DON'T CHANGE THIS !!!

from src.models import db
from src.routes.formulario import formulario_bp
from src.routes.proposta import proposta_bp
from src.routes.dashboard import dashboard_bp
from src.models.proposta import Proposta  # necessário para o errohandler

def create_app():
    app = Flask(__name__)
    
    # Configuração do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bowe_simulador.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'bowe-simulador-secret-key')
    
    # Configuração para uploads de arquivos
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 6 * 1024 * 1024  # 6 MB

    
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
    
    # Tratar erro de Request Entity Too Large (413)
    @app.errorhandler(413)
    def request_entity_too_large(error):
        flash('O arquivo enviado excede o limite de 3 MB.', 'error')
        # Pega o id_publico da URL, que está no formato: /proposta/<id_publico>/formulario
        id_publico = request.url.split('/')[4]
        proposta = Proposta.query.filter_by(id_publico=id_publico).first()
        return render_template('formulario.html', proposta=proposta), 413
    
    return app

# Criar a aplicação para o Gunicorn
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
