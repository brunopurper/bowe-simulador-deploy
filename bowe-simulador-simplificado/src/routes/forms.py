from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, HiddenField
from wtforms.validators import DataRequired, Email, Optional, NumberRange

class PropostaForm(FlaskForm):
    # Dados do Vendedor (ocultos)
    nome_vendedor = HiddenField('Nome do Vendedor', default="Bowe Energia")
    telefone_vendedor = HiddenField('Telefone do Vendedor', default="(00) 0000-0000")
    chave_pix = HiddenField('Chave PIX')
    cidade_indicador = HiddenField('Cidade do Indicador')
    lider = HiddenField('Líder')
    cpf_indicador = HiddenField('CPF do Indicador')
    
    # Dados do Cliente (telefone e email ocultos)
    nome_indicado = StringField('Nome do Cliente', validators=[DataRequired()])
    telefone_indicado = HiddenField('Telefone do Cliente')
    email_indicado = HiddenField('Email do Cliente')
    unidade_consumidora = StringField('Unidade Consumidora', validators=[DataRequired()])
    
    # Dados de Consumo
    consumo_indicado = FloatField('Consumo (kWh)', validators=[DataRequired(), NumberRange(min=1)])
    tipo_rede = SelectField('Tipo de Rede', choices=[
        ('Monofásica', 'Monofásica'),
        ('Bifásica', 'Bifásica'),
        ('Trifásica', 'Trifásica')
    ], validators=[DataRequired()])
    mes_atual = StringField('Mês de Referência', validators=[DataRequired()])
    
    # Dados de Tarifas (simplificados)
    taxa_concessionaria = FloatField('Tarifa com Tributos (R$/kWh)', validators=[DataRequired(), NumberRange(min=0.001)])
    taxa_bandeira = FloatField('Taxa Bandeira (R$/kWh)', validators=[Optional(), NumberRange(min=0)])
    
    # Novo campo para percentual de desconto
    percentual_desconto = SelectField('Percentual de Desconto', 
                                     choices=[(str(i), f"{i}%") for i in range(15, 31)],
                                     validators=[DataRequired()])
    
    # Outros Campos
    modelo_contrato = StringField('Modelo de Contrato', validators=[Optional()])
    
    # Campos calculados (hidden)
    pagar_energisa = HiddenField()
    pagar_energisa_mais_bandeira = HiddenField()
    pagar_enersim = HiddenField()
    economia = HiddenField()
    economia_anual = HiddenField()
    porcentagem_economia = HiddenField()
