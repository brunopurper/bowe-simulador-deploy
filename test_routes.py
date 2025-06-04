"""
Script para testar as principais rotas da aplicação
"""
from src.main import create_app
import requests

app = create_app()

def test_routes():
    print("Testando rotas principais da aplicação...")
    
    with app.test_client() as client:
        # Testar rota principal (login)
        print("\n1. Testando acesso à página de login...")
        response = client.get('/')
        if response.status_code == 200 or response.status_code == 302:
            print(f"✓ Página de login acessível (status: {response.status_code})")
        else:
            print(f"✗ Erro ao acessar página de login: {response.status_code}")
        
        # Testar login
        print("\n2. Testando login no dashboard...")
        response = client.post('/login', data={
            'username': 'admin',
            'password': 'bowe2025'
        }, follow_redirects=True)
        
        if response.status_code == 200 and b'Dashboard de Propostas' in response.data:
            print("✓ Login e acesso ao dashboard funcionando")
        else:
            print(f"✗ Erro no login ou acesso ao dashboard: {response.status_code}")
        
        # Testar acesso ao dashboard após login
        print("\n3. Testando acesso direto ao dashboard...")
        response = client.get('/dashboard', follow_redirects=True)
        if response.status_code == 200 and b'Dashboard de Propostas' in response.data:
            print("✓ Acesso ao dashboard funcionando")
        else:
            print(f"✗ Erro ao acessar dashboard: {response.status_code}")
        
        # Testar acesso a uma proposta existente (se houver)
        print("\n4. Testando acesso a uma proposta existente...")
        # Usar o app_context() fora do with do test_client
        with app.app_context():
            from src.models.proposta import Proposta
            proposta = Proposta.query.first()
            
        if proposta:
            response = client.get(f'/proposta/{proposta.id_publico}')
            if response.status_code == 200:
                print(f"✓ Acesso à proposta {proposta.id_publico} funcionando")
            else:
                print(f"✗ Erro ao acessar proposta: {response.status_code}")
        else:
            print("! Nenhuma proposta encontrada para testar")
        
        print("\nTestes de rotas concluídos!")

if __name__ == "__main__":
    test_routes()
