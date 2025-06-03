from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from src.models import db
from src.models.proposta import Proposta
from src.routes.forms import PropostaForm
from functools import wraps

formulario_bp = Blueprint('formulario', __name__)

# Decorator para verificar se o usuário está logado
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Acesso restrito. Por favor, faça login.', 'error')
            return redirect(url_for('dashboard.login'))
        return f(*args, **kwargs)
    return decorated_function

@formulario_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = PropostaForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        # Criar nova proposta com os dados do formulário
        proposta = Proposta(
            nome_vendedor=form.nome_vendedor.data,
            telefone_vendedor=form.telefone_vendedor.data,
            chave_pix=form.chave_pix.data,
            cidade_indicador=form.cidade_indicador.data,
            lider=form.lider.data,
            cpf_indicador=form.cpf_indicador.data,
            nome_indicado=form.nome_indicado.data,
            telefone_indicado=form.telefone_indicado.data,
            email_indicado=form.email_indicado.data,
            unidade_consumidora=form.unidade_consumidora.data,
            consumo_indicado=form.consumo_indicado.data,
            tipo_rede=form.tipo_rede.data,
            mes_atual=form.mes_atual.data,
            taxa_concessionaria=form.taxa_concessionaria.data,
            taxa_bandeira=form.taxa_bandeira.data or 0,
            percentual_desconto=float(form.percentual_desconto.data),
            modelo_contrato=form.modelo_contrato.data,
            # Os campos calculados serão preenchidos automaticamente no modelo
        )
        
        # Salvar no banco de dados
        db.session.add(proposta)
        db.session.commit()
        
        # Redirecionar para a página de compartilhamento da proposta
        return redirect(url_for('proposta.compartilhar', id_publico=proposta.id_publico))
    
    return render_template('formulario.html', form=form)

@formulario_bp.route('/calcular', methods=['POST'])
def calcular():
    """Endpoint para cálculos em tempo real via AJAX"""
    data = request.json
    
    try:
        consumo = float(data.get('consumo_indicado', 0))
        taxa_concessionaria = float(data.get('taxa_concessionaria', 0))
        taxa_bandeira = float(data.get('taxa_bandeira', 0))
        percentual_desconto = float(data.get('percentual_desconto', 0))
        
        # Realizar cálculos
        pagar_energisa = round(consumo * taxa_concessionaria, 2)
        pagar_energisa_mais_bandeira = round(pagar_energisa + (consumo * taxa_bandeira), 2)
        pagar_enersim = round(pagar_energisa_mais_bandeira * (1 - (percentual_desconto / 100)), 2)
        economia = round(pagar_energisa_mais_bandeira - pagar_enersim, 2)
        economia_anual = round(economia * 12, 2)
        porcentagem_economia = percentual_desconto  # Usar diretamente o percentual de desconto
        
        return jsonify({
            'pagar_energisa': pagar_energisa,
            'pagar_energisa_mais_bandeira': pagar_energisa_mais_bandeira,
            'pagar_enersim': pagar_enersim,
            'economia': economia,
            'economia_anual': economia_anual,
            'porcentagem_economia': porcentagem_economia
        })
    except (ValueError, ZeroDivisionError):
        return jsonify({'error': 'Erro nos cálculos. Verifique os valores informados.'}), 400
