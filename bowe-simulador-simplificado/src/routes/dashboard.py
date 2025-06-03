from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps

dashboard_bp = Blueprint('dashboard', __name__)

# Credenciais de login (em produção, isso deveria estar em um banco de dados)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "bowe2025"

# Decorator para verificar se o usuário está logado
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
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash('Usuário ou senha incorretos.', 'error')
    
    return render_template('login.html')

@dashboard_bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('dashboard.login'))

@dashboard_bp.route('/dashboard')
@login_required
def index():
    from src.models.proposta import Proposta
    propostas = Proposta.query.order_by(Proposta.data_criacao.desc()).all()
    
    # Calcular estatísticas para o dashboard
    total_propostas = len(propostas)
    propostas_aprovadas = sum(1 for p in propostas if p.status == 'Aprovada')
    propostas_recusadas = sum(1 for p in propostas if p.status == 'Recusada')
    propostas_pendentes = total_propostas - propostas_aprovadas - propostas_recusadas
    
    return render_template('dashboard.html', 
                          propostas=propostas,
                          total_propostas=total_propostas,
                          propostas_aprovadas=propostas_aprovadas,
                          propostas_recusadas=propostas_recusadas,
                          propostas_pendentes=propostas_pendentes)
