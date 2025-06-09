from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from src.models.proposta import Proposta
from datetime import datetime
import pytz

proposta_bp = Blueprint('proposta', __name__)

def convert_to_brasilia_time(utc_dt):
    if utc_dt is None:
        return None
    utc_timezone = pytz.timezone('UTC')
    brasilia_timezone = pytz.timezone('America/Sao_Paulo')
    utc_dt = utc_timezone.localize(utc_dt)
    brasilia_dt = utc_dt.astimezone(brasilia_timezone)
    return brasilia_dt

@proposta_bp.route('/proposta/<id_publico>')
def visualizar(id_publico):
    proposta = Proposta.query.filter_by(id_publico=id_publico).first_or_404()
    proposta.data_criacao_brasilia = convert_to_brasilia_time(proposta.data_criacao)
    return render_template('proposta.html', proposta=proposta)

@proposta_bp.route('/proposta/<id_publico>/resposta', methods=['POST'])
def resposta(id_publico):
    proposta = Proposta.query.filter_by(id_publico=id_publico).first_or_404()
    
    resposta = request.form.get('resposta')
    if resposta == 'aprovar':
        flash('Aprovação registrada! Agora envie os documentos para validar a proposta.', 'success')
        # 🔥 🔥 🔥 Removi a linha que mudava o status aqui!
        return redirect(url_for('formulario.formulario', id_publico=id_publico))
    elif resposta == 'recusar':
        proposta.status = 'Recusada'
        flash('Proposta recusada.', 'info')
    else:
        flash('Resposta inválida.', 'error')
        return redirect(url_for('proposta.visualizar', id_publico=id_publico))
    
    from src.models import db
    db.session.commit()
    return redirect(url_for('proposta.visualizar', id_publico=id_publico))

@proposta_bp.route('/proposta/<id_publico>/compartilhar')
def compartilhar(id_publico):
    proposta = Proposta.query.filter_by(id_publico=id_publico).first_or_404()
    link_completo = f"{request.host_url}proposta/{id_publico}"
    return render_template('compartilhar.html', proposta=proposta, link_completo=link_completo)
