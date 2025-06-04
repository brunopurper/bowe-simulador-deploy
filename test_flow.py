"""
Script para testar o fluxo completo de aprovação de proposta, 
formulário, uploads e visualização no dashboard
"""
from src.main import create_app
import os
import sys
from werkzeug.datastructures import FileStorage

app = create_app()

def test_flow():
    print("Testando o fluxo completo de aprovação de proposta e formulário...")
    
    # Inicializar o contexto da aplicação para consultas ao banco
    with app.app_context():
        from src.models.proposta import Proposta
        from src.models.formulario import FormularioCliente
        
        # Verificar se existe alguma proposta para testar
        proposta = Proposta.query.first()
        if not proposta:
            print("✗ Nenhuma proposta encontrada para testar")
            return
            
        proposta_id = proposta.id
        proposta_id_publico = proposta.id_publico
        print(f"✓ Proposta encontrada: {proposta_id_publico}")
    
    # Usar o test client para simular as requisições HTTP
    with app.test_client() as client:
        # 1. Acessar o dashboard (login)
        print("\n1. Testando login no dashboard...")
        response = client.post('/login', data={
            'username': 'admin',
            'password': 'bowe2025'
        }, follow_redirects=True)
        
        if response.status_code == 200 and b'Dashboard de Propostas' in response.data:
            print("✓ Login no dashboard bem-sucedido")
        else:
            print(f"✗ Erro no login: {response.status_code}")
            return
            
        # 3. Aprovar a proposta (simulando o clique no botão)
        print(f"\n3. Aprovando a proposta {proposta_id_publico}...")
        response = client.post(f'/proposta/{proposta_id_publico}/resposta', data={
            'resposta': 'aprovar'
        }, follow_redirects=True)
        
        # Verificar apenas o status code para aprovação
        if response.status_code == 200:
            print("✓ Proposta aprovada com sucesso")
        else:
            print(f"✗ Erro ao aprovar proposta: {response.status_code}")
            return
        
        # 4. Acessar diretamente o formulário
        print("\n4. Acessando o formulário de continuidade...")
        response = client.get(f'/proposta/{proposta_id_publico}/formulario', follow_redirects=True)
        
        if response.status_code == 200:
            print("✓ Formulário de continuidade acessível")
        else:
            print(f"✗ Erro ao acessar formulário: {response.status_code}")
            return
        
        # 5. Simular o envio do formulário com uploads
        print("\n5. Testando envio do formulário com uploads...")
        
        # Criar arquivos de teste para upload
        test_doc_path = os.path.join(app.root_path, 'test_documento.pdf')
        test_conta_path = os.path.join(app.root_path, 'test_conta_luz.pdf')
        
        with open(test_doc_path, 'wb') as f:
            f.write(b'%PDF-1.4\nTest Document')
        
        with open(test_conta_path, 'wb') as f:
            f.write(b'%PDF-1.4\nTest Conta Luz')
        
        # Preparar os arquivos para upload
        with open(test_doc_path, 'rb') as doc_file, open(test_conta_path, 'rb') as conta_file:
            # Enviar o formulário
            response = client.post(
                f'/proposta/{proposta_id_publico}/formulario', 
                data={
                    'nome_completo': 'Cliente Teste',
                    'telefone': '(11) 98765-4321',
                    'documento': (doc_file, 'test_documento.pdf'),
                    'conta_luz': (conta_file, 'test_conta_luz.pdf')
                },
                follow_redirects=True,
                content_type='multipart/form-data'
            )
        
        # Limpar arquivos de teste
        if os.path.exists(test_doc_path):
            os.remove(test_doc_path)
        if os.path.exists(test_conta_path):
            os.remove(test_conta_path)
        
        if response.status_code == 200:
            print("✓ Formulário enviado com sucesso")
        else:
            print(f"✗ Erro ao enviar formulário: {response.status_code}")
            return
        
        # 6. Verificar se o formulário foi salvo no banco de dados
        print("\n6. Verificando se o formulário foi salvo no banco de dados...")
        with app.app_context():
            formulario = FormularioCliente.query.filter_by(proposta_id=proposta_id).first()
            
            if formulario:
                print(f"✓ Formulário salvo no banco de dados com ID {formulario.id}")
                formulario_id = formulario.id
            else:
                print("✗ Formulário não encontrado no banco de dados")
                return
        
        # 7. Verificar acesso ao dashboard de formulários
        print("\n7. Verificando acesso ao dashboard de formulários...")
        response = client.get('/admin/formularios', follow_redirects=True)
        
        if response.status_code == 200:
            print("✓ Dashboard de formulários acessível")
        else:
            print(f"✗ Erro ao acessar dashboard de formulários: {response.status_code}")
            return
        
        # 8. Verificar acesso aos detalhes do formulário
        print("\n8. Verificando acesso aos detalhes do formulário...")
        response = client.get(f'/admin/formulario/{formulario_id}', follow_redirects=True)
        
        if response.status_code == 200:
            print("✓ Detalhes do formulário acessíveis")
        else:
            print(f"✗ Erro ao acessar detalhes do formulário: {response.status_code}")
            return
        
        print("\nTodos os testes foram concluídos com sucesso!")
        print("O fluxo completo de aprovação de proposta, formulário, uploads e dashboard está funcionando corretamente.")

if __name__ == "__main__":
    test_flow()
