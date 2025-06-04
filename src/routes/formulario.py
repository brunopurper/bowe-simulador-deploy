from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app, send_from_directory, session
import os
import uuid
from werkzeug.utils import secure_filename
from src.models.proposta import Proposta
from src.models.formulario import FormularioCliente
from src.models import db

formulario_bp = Blueprint('formulario', __name__)

# Função para verificar extensões de arquivo permitidas
def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

# Função para salvar arquivo com nome seguro
def save_file(file, subfolder):
    # Verificar se o arquivo existe
    if not file:
        return None
        
    # Criar nome de arquivo seguro com UUID para evitar colisões
    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4()}_{filename}"
    
    # Definir caminho para salvar o arquivo
    upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, unique_filename)
    
    # Salvar o arquivo
    file.save(file_path)
    
    return unique_filename

@formulario_bp.route('/proposta/<id_publico>/formulario', methods=['GET', 'POST'])
def formulario(id_publico):
    # Buscar a proposta pelo ID público
    proposta = Proposta.query.filter_by(id_publico=id_publico).first_or_404()
    
    # Verificar se a proposta foi aprovada
    if proposta.status != 'Aprovada':
        flash('Esta proposta ainda não foi aprovada.', 'warning')
        return redirect(url_for('proposta.visualizar', id_publico=id_publico))
    
    # Verificar se o formulário já foi preenchido para esta proposta
    formulario_existente = FormularioCliente.query.filter_by(proposta_id=proposta.id).first()
    if formulario_existente:
        flash('O formulário já foi preenchido para esta proposta.', 'info')
        return redirect(url_for('proposta.visualizar', id_publico=id_publico))
    
    # Processar o formulário se for um POST
    if request.method == 'POST':
        # Validar campos obrigatórios
        nome_completo = request.form.get('nome_completo')
        telefone = request.form.get('telefone')
        documento = request.files.get('documento')
        conta_luz = request.files.get('conta_luz')
        
        errors = []
        
        if not nome_completo:
            errors.append('Nome completo é obrigatório.')
        
        if not telefone:
            errors.append('Telefone é obrigatório.')
        
        if not documento:
            errors.append('Documento com foto e CPF é obrigatório.')
        elif not allowed_file(documento.filename, {'pdf', 'jpg', 'jpeg', 'png'}):
            errors.append('Documento deve ser um arquivo PDF, JPG ou PNG.')
        
        if not conta_luz:
            errors.append('Conta de luz atualizada é obrigatória.')
        elif not allowed_file(conta_luz.filename, {'pdf', 'jpg', 'jpeg', 'png'}):
            errors.append('Conta de luz deve ser um arquivo PDF, JPG ou PNG.')
        
        # Se houver erros, exibir mensagens e retornar ao formulário
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('formulario.html', proposta=proposta)
        
        try:
            # Salvar os arquivos
            documento_filename = save_file(documento, 'documentos')
            conta_luz_filename = save_file(conta_luz, 'contas_luz')
            
            # Criar novo registro no banco de dados
            novo_formulario = FormularioCliente(
                proposta_id=proposta.id,
                nome_completo=nome_completo,
                telefone=telefone,
                documento_filename=documento_filename,
                conta_luz_filename=conta_luz_filename
            )
            
            db.session.add(novo_formulario)
            db.session.commit()
            
            # Redirecionar para página de sucesso
            return render_template('formulario_sucesso.html', proposta=proposta)
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao processar o formulário: {str(e)}', 'error')
    
    # Exibir o formulário para GET
    return render_template('formulario.html', proposta=proposta)

@formulario_bp.route('/admin/formularios')
def admin_formularios():
    # Verificar autenticação de admin (simplificado)
    if not request.cookies.get('admin_logged_in'):
        return redirect(url_for('dashboard.login'))
    
    # Buscar todos os formulários com suas propostas
    formularios = FormularioCliente.query.order_by(FormularioCliente.data_submissao.desc()).all()
    
    return render_template('admin_formularios.html', formularios=formularios)

@formulario_bp.route('/admin/formulario/<int:id>')
def admin_formulario_detalhe(id):
    # Verificar autenticação de admin (simplificado)
    if not request.cookies.get('admin_logged_in'):
        return redirect(url_for('dashboard.login'))
    
    # Buscar o formulário pelo ID
    formulario = FormularioCliente.query.get_or_404(id)
    
    return render_template('admin_formulario_detalhe.html', formulario=formulario)

@formulario_bp.route('/uploads/<tipo>/<filename>')
def view_file(tipo, filename):
    # Verificar autenticação de admin (simplificado)
    if not request.cookies.get('admin_logged_in'):
        return redirect(url_for('dashboard.login'))
    
    # Verificar se o tipo é válido
    if tipo not in ['documentos', 'contas_luz']:
        abort(404)
    
    # Retornar o arquivo usando send_from_directory
    upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], tipo)
    return send_from_directory(upload_folder, filename)

@formulario_bp.route('/download/<tipo>/<filename>')
def download_file(tipo, filename):
    # Verificar autenticação de admin (simplificado)
    if not request.cookies.get('admin_logged_in'):
        return redirect(url_for('dashboard.login'))
    
    # Verificar se o tipo é válido
    if tipo not in ['documentos', 'contas_luz']:
        abort(404)
    
    # Retornar o arquivo para download
    upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], tipo)
    return send_from_directory(upload_folder, filename, as_attachment=True)
