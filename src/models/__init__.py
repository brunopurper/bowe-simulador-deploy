from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Importar modelos após criar a instância db
from src.models.proposta import Proposta
from src.models.formulario import FormularioCliente
