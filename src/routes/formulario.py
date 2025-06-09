from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app, send_from_directory, session
import os
import uuid
from werkzeug.utils import secure_filename
from src.models.proposta import Proposta
from src.models.formulario import FormularioCliente
from src.models import db

formulario_bp = Blueprint('formulario', __name__)

def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def save_file(file, subfolder):
    if not file:
        return None
    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4()}_{filename}"
    upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, unique_filename)
    file.save(file_path)
    return unique_filename

@formulario_bp.route('/proposta/<id_publico>/formulario', methods=['GET', 'POST'])
def formulario(id_publico):
    proposta = Proposta.query.filter_by(id_publico=id_publico).first_or_404()
    
    if proposta.status != 'Aprovada' and proposta.status != 'Pendente':
        flash('Esta proposta não pode ser processada neste momento.', 'warning')
        return redirect(url_for('proposta.visualizar', id_publico=id_publico))
    
    formulario_existente = FormularioCliente.query.filter_by(proposta_id=proposta.id).first()
    if formulario_existente:
        flash('O formulário já foi preenchido para esta proposta.', 'info')
        return redirect(url_for('proposta.visualizar', id_publico=id_publico))
    
    if request.method == 'POST':
        nome_completo = request.form.get('nome_completo')
        telefone = request.form.get('telefone')
        email = request.form.get('email')
        estado_civil = request.form.get('estado_civil')
        cpf = request.form.get('cpf')
        rg = request.form.get('rg')
        naturalidade = request.form.get('naturalidade')
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
        else:
            documento.seek(0, os.SEEK_END)
            if documento.tell() > 6 * 1024 * 1024:
                errors.append('Documento excede o limite de 6 MB.')
            documento.seek(0)
        
        if not conta_luz:
            errors.append('Conta de luz atualizada é obrigatória.')
        elif not allowed_file(conta_luz.filename, {'pdf', 'jpg', 'jpeg', 'png'}):
            errors.append('Conta de luz deve ser um arquivo PDF, JPG ou PNG.')
        else:
            conta_luz.seek(0, os.SEEK_END)
            if conta_luz.tell() > 6 * 1024 * 1024:
                errors.append('Conta de luz excede o limite de 6 MB.')
            conta_luz.seek(0)
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('formulario.html', proposta=proposta)
        
        try:
            documento_filename = save_file(documento, 'documentos')
            conta_luz_filename = save_file(conta_luz, 'contas_luz')
            
            novo_formulario = FormularioCliente(
                proposta_id=proposta.id,
                nome_completo=nome_completo,
                telefone=telefone,
                email=email,
                estado_civil=estado_civil,
                cpf=cpf,
                rg=rg,
                naturalidade=naturalidade,
                documento_filename=documento_filename,
                conta_luz_filename=conta_luz_filename
            )
            
            # Atualizar o status da proposta para Aprovada
            proposta.status = 'Aprovada'
            
            db.session.add(novo_formulario)
            db.session.commit()
            return render_template('formulario_sucesso.html', proposta=proposta)
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao processar o formulário: {str(e)}', 'error')
    
    return render_template('formulario.html', proposta=proposta)

@formulario_bp.route('/admin/formularios')
def admin_formularios():
    if 'logged_in' not in session:
        flash('Acesso restrito. Por favor, faça login.', 'error')
        return redirect(url_for('dashboard.login'))
    formularios = FormularioCliente.query.order_by(FormularioCliente.data_submissao.desc()).all()
    return render_template('admin_formularios.html', formularios=formularios)

@formulario_bp.route('/admin/formulario/<int:id>')
def admin_formulario_detalhe(id):
    if 'logged_in' not in session:
        flash('Acesso restrito. Por favor, faça login.', 'error')
        return redirect(url_for('dashboard.login'))
    formulario = FormularioCliente.query.get_or_404(id)
    return render_template('admin_formulario_detalhe.html', formulario=formulario)

@formulario_bp.route('/admin/formulario/excluir/<int:id>', methods=['POST'])
def excluir_formulario(id):
    if 'logged_in' not in session:
        flash('Acesso restrito. Por favor, faça login.', 'error')
        return redirect(url_for('dashboard.login'))

    username = request.form.get('username')
    password = request.form.get('password')

    if username != 'admin' or password != 'bowe2025':
        flash('Usuário ou senha incorretos. Exclusão não autorizada.', 'error')
        return redirect(url_for('formulario.admin_formularios'))

    formulario = FormularioCliente.query.get_or_404(id)
    try:
        db.session.delete(formulario)
        db.session.commit()
        flash('Formulário excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir formulário: {str(e)}', 'error')

    return redirect(url_for('formulario.admin_formularios'))

@formulario_bp.route('/uploads/<tipo>/<filename>')
def view_file(tipo, filename):
    if 'logged_in' not in session:
        flash('Acesso restrito. Por favor, faça login.', 'error')
        return redirect(url_for('dashboard.login'))
    if tipo not in ['documentos', 'contas_luz']:
        abort(404)
    upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], tipo)
    return send_from_directory(upload_folder, filename)

@formulario_bp.route('/download/<tipo>/<filename>')
def download_file(tipo, filename):
    if 'logged_in' not in session:
        flash('Acesso restrito. Por favor, faça login.', 'error')
        return redirect(url_for('dashboard.login'))
    if tipo not in ['documentos', 'contas_luz']:
        abort(404)
    upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], tipo)
    return send_from_directory(upload_folder, filename, as_attachment=True)
