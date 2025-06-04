"""
Script para verificar as tabelas do banco de dados e validar a integração do SQLAlchemy
"""
from src.models import db
from src.main import create_app

app = create_app()

with app.app_context():
    # Verificar tabelas existentes
    print('Tabelas no banco de dados:', db.metadata.tables.keys())
    
    # Verificar se as tabelas têm registros
    from src.models.proposta import Proposta
    try:
        from src.models.formulario import FormularioCliente
        has_formulario = True
    except ImportError:
        has_formulario = False
    
    print(f'Total de propostas: {Proposta.query.count()}')
    
    if has_formulario:
        print(f'Total de formulários: {FormularioCliente.query.count()}')
    
    print('Verificação do banco de dados concluída com sucesso!')
