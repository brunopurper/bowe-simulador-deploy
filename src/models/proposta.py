from datetime import datetime
import uuid
from src.models import db

class Proposta(db.Model):
    __tablename__ = 'propostas'
    
    id = db.Column(db.Integer, primary_key=True)
    id_publico = db.Column(db.String(36), unique=True, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Pendente')
    
    # Dados do Vendedor
    nome_vendedor = db.Column(db.String(100), nullable=False, default="Bowe Energia")
    telefone_vendedor = db.Column(db.String(20), nullable=False, default="(00) 0000-0000")
    chave_pix = db.Column(db.String(100))
    cidade_indicador = db.Column(db.String(100))
    lider = db.Column(db.String(100))
    cpf_indicador = db.Column(db.String(14))
    
    # Dados do Cliente
    nome_indicado = db.Column(db.String(100), nullable=False)
    telefone_indicado = db.Column(db.String(20))
    email_indicado = db.Column(db.String(100))
    unidade_consumidora = db.Column(db.String(20), nullable=False)
    
    # Dados de Consumo
    consumo_indicado = db.Column(db.Float, nullable=False)
    tipo_rede = db.Column(db.String(20), nullable=False)
    mes_atual = db.Column(db.String(20), nullable=False)
    
    # Dados de Tarifas
    taxa_concessionaria = db.Column(db.Float, nullable=False)
    taxa_bandeira = db.Column(db.Float, default=0)
    taxa_enersim = db.Column(db.Float)  # Mantido para compatibilidade
    percentual_desconto = db.Column(db.Float, nullable=False)  # Novo campo
    
    # Valores Calculados
    pagar_energisa = db.Column(db.Float, nullable=False)
    pagar_energisa_mais_bandeira = db.Column(db.Float, nullable=False)
    pagar_enersim = db.Column(db.Float, nullable=False)
    economia = db.Column(db.Float, nullable=False)
    economia_anual = db.Column(db.Float, nullable=False)
    porcentagem_economia = db.Column(db.Float, nullable=False)
    
    # Outros Campos
    modelo_contrato = db.Column(db.String(100))
    
    def __init__(self, **kwargs):
        super(Proposta, self).__init__(**kwargs)
        if not self.id_publico:
            self.id_publico = str(uuid.uuid4())
        
        # Calcular valores automaticamente se não fornecidos
        if not self.pagar_energisa and self.consumo_indicado and self.taxa_concessionaria:
            self.pagar_energisa = round(self.consumo_indicado * self.taxa_concessionaria, 2)
            
        if not self.pagar_energisa_mais_bandeira and self.pagar_energisa and self.consumo_indicado and self.taxa_bandeira:
            self.pagar_energisa_mais_bandeira = round(self.pagar_energisa + (self.consumo_indicado * self.taxa_bandeira), 2)
        elif not self.pagar_energisa_mais_bandeira and self.pagar_energisa:
            self.pagar_energisa_mais_bandeira = self.pagar_energisa
            
        # Nova lógica de cálculo usando percentual de desconto
        if not self.pagar_enersim and self.pagar_energisa_mais_bandeira and self.percentual_desconto:
            self.pagar_enersim = round(self.pagar_energisa_mais_bandeira * (1 - (self.percentual_desconto / 100)), 2)
            
        if not self.economia and self.pagar_energisa_mais_bandeira and self.pagar_enersim:
            self.economia = round(self.pagar_energisa_mais_bandeira - self.pagar_enersim, 2)
            
        if not self.economia_anual and self.economia:
            self.economia_anual = round(self.economia * 12, 2)
            
        if not self.porcentagem_economia and self.percentual_desconto:
            self.porcentagem_economia = self.percentual_desconto
    
    def to_dict(self):
        return {
            'id': self.id,
            'id_publico': self.id_publico,
            'data_criacao': self.data_criacao.strftime('%Y-%m-%d %H:%M:%S'),
            'status': self.status,
            'nome_vendedor': self.nome_vendedor,
            'telefone_vendedor': self.telefone_vendedor,
            'chave_pix': self.chave_pix,
            'cidade_indicador': self.cidade_indicador,
            'lider': self.lider,
            'cpf_indicador': self.cpf_indicador,
            'nome_indicado': self.nome_indicado,
            'telefone_indicado': self.telefone_indicado,
            'email_indicado': self.email_indicado,
            'unidade_consumidora': self.unidade_consumidora,
            'consumo_indicado': self.consumo_indicado,
            'tipo_rede': self.tipo_rede,
            'mes_atual': self.mes_atual,
            'taxa_concessionaria': self.taxa_concessionaria,
            'taxa_bandeira': self.taxa_bandeira,
            'percentual_desconto': self.percentual_desconto,
            'pagar_energisa': self.pagar_energisa,
            'pagar_energisa_mais_bandeira': self.pagar_energisa_mais_bandeira,
            'pagar_enersim': self.pagar_enersim,
            'economia': self.economia,
            'economia_anual': self.economia_anual,
            'porcentagem_economia': self.porcentagem_economia,
            'modelo_contrato': self.modelo_contrato
        }
