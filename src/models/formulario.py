from datetime import datetime
import os
from src.models import db

class FormularioCliente(db.Model):
    __tablename__ = 'formularios_cliente'
    
    id = db.Column(db.Integer, primary_key=True)
    proposta_id = db.Column(db.Integer, db.ForeignKey('propostas.id'), nullable=False)
    data_submissao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Dados pessoais
    nome_completo = db.Column(db.String(150), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(150), nullable=True)
    estado_civil = db.Column(db.String(50), nullable=True)
    cpf = db.Column(db.String(20), nullable=True)
    rg = db.Column(db.String(20), nullable=True)
    naturalidade = db.Column(db.String(100), nullable=True)
    
    # Arquivos
    documento_filename = db.Column(db.String(255), nullable=False)
    conta_luz_filename = db.Column(db.String(255), nullable=False)
    
    # Relacionamento com a proposta
    proposta = db.relationship('Proposta', backref=db.backref('formulario', uselist=False))
    
    def __init__(self, **kwargs):
        super(FormularioCliente, self).__init__(**kwargs)
    
    def to_dict(self):
        return {
            'id': self.id,
            'proposta_id': self.proposta_id,
            'data_submissao': self.data_submissao.strftime('%Y-%m-%d %H:%M:%S'),
            'nome_completo': self.nome_completo,
            'telefone': self.telefone,
            'email': self.email,
            'estado_civil': self.estado_civil,
            'cpf': self.cpf,
            'rg': self.rg,
            'naturalidade': self.naturalidade,
            'documento_filename': self.documento_filename,
            'conta_luz_filename': self.conta_luz_filename
        }
