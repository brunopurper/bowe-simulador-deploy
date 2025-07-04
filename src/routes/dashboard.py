from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from src.routes.forms import PropostaForm
from src.models.proposta import Proposta
from datetime import datetime
import uuid
import pytz
from functools import wraps

dashboard_bp = Blueprint('dashboard', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Acesso restrito. Por favor, faça login.', 'error')
            return redirect(url_for('dashboard.login'))
        return f(*args, **kwargs)
    return decorated_function

@dashboard_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'bowe2025':
            session['logged_in'] = True
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash('Credenciais inválidas. Tente novamente.', 'error')
    return render_template('login.html')

@dashboard_bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('dashboard.login'))

@dashboard_bp.route('/dashboard')
@login_required
def index():
    from sqlalchemy import extract
    import datetime
    propostas = Proposta.query.order_by(Proposta.data_criacao.desc()).all()

    total_propostas = len(propostas)
    propostas_aprovadas = sum(1 for p in propostas if p.status == 'Aprovada')
    propostas_recusadas = sum(1 for p in propostas if p.status == 'Recusada')
    propostas_pendentes = total_propostas - propostas_aprovadas - propostas_recusadas

    hoje = datetime.datetime.now()
    meses = []
    dados_mensais = []

    for i in range(5, -1, -1):
        data_mes = hoje.replace(day=1) - datetime.timedelta(days=i*30)
        mes_ano = data_mes.strftime('%m/%Y')
        meses.append(mes_ano)

        mes = data_mes.month
        ano = data_mes.year
        count = Proposta.query.filter(
            extract('month', Proposta.data_criacao) == mes,
            extract('year', Proposta.data_criacao) == ano
        ).count()
        dados_mensais.append(count)

    return render_template('dashboard.html',
                           propostas=propostas,
                           total_propostas=total_propostas,
                           propostas_aprovadas=propostas_aprovadas,
                           propostas_recusadas=propostas_recusadas,
                           propostas_pendentes=propostas_pendentes,
                           meses=meses,
                           dados_mensais=dados_mensais)

@dashboard_bp.route('/nova-proposta', methods=['GET', 'POST'])
@login_required
def nova_proposta():
    form = PropostaForm()
    if form.validate_on_submit():
        id_publico = str(uuid.uuid4())
        consumo = float(form.consumo_indicado.data)
        taxa_concessionaria = float(form.taxa_concessionaria.data)
        taxa_bandeira = float(form.taxa_bandeira.data or 0)
        percentual_desconto = float(form.percentual_desconto.data) / 100

        pagar_energisa = consumo * taxa_concessionaria
        pagar_energisa_mais_bandeira = pagar_energisa + (consumo * taxa_bandeira)
        pagar_enersim = pagar_energisa_mais_bandeira * (1 - percentual_desconto)
        economia = pagar_energisa_mais_bandeira - pagar_enersim
        economia_anual = economia * 12

        nova_proposta = Proposta(
            id_publico=id_publico,
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
            consumo_indicado=consumo,
            tipo_rede=form.tipo_rede.data,
            mes_atual=form.mes_atual.data,
            taxa_concessionaria=taxa_concessionaria,
            taxa_bandeira=taxa_bandeira,
            percentual_desconto=percentual_desconto * 100,
            modelo_contrato=form.modelo_contrato.data,
            pagar_energisa=pagar_energisa,
            pagar_energisa_mais_bandeira=pagar_energisa_mais_bandeira,
            pagar_enersim=pagar_enersim,
            economia=economia,
            economia_anual=economia_anual,
            status='Pendente',
            data_criacao=datetime.now(pytz.UTC)
        )

        from src.models import db
        db.session.add(nova_proposta)
        db.session.commit()

        flash('Proposta criada com sucesso!', 'success')
        return redirect(url_for('proposta.compartilhar', id_publico=id_publico))
    return render_template('nova_proposta.html', form=form)

@dashboard_bp.route('/excluir-proposta/<int:id>', methods=['POST'])
@login_required
def excluir_proposta(id):
    from src.models.proposta import Proposta, db
    proposta = Proposta.query.get_or_404(id)
    try:
        db.session.delete(proposta)
        db.session.commit()
        flash('Proposta excluída com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir proposta: {str(e)}', 'error')
    return redirect(url_for('dashboard.index'))

# 🔥 REMOVI qualquer endpoint que mudasse status para 'Aprovada' diretamente aqui
