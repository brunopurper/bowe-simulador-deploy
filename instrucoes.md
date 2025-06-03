# Instruções de Uso e Implantação - Simulador de Propostas Bowe

## Visão Geral

O Simulador de Propostas Bowe é uma aplicação web desenvolvida com Flask que permite:

1. Criar propostas personalizadas para clientes
2. Calcular automaticamente valores de economia
3. Gerar links únicos para compartilhamento
4. Analisar estatísticas e gerenciar propostas via dashboard

## Estrutura do Projeto

```
bowe-simulador/
├── venv/                      # Ambiente virtual Python
├── src/                       # Código-fonte da aplicação
│   ├── main.py                # Ponto de entrada da aplicação
│   ├── models/                # Modelos de dados
│   ├── routes/                # Rotas e controladores
│   ├── static/                # Arquivos estáticos (CSS, JS, imagens)
│   └── templates/             # Templates HTML
└── requirements.txt           # Dependências do projeto
```

## Requisitos

- Python 3.6 ou superior
- Pip (gerenciador de pacotes Python)
- Navegador web moderno

## Instalação e Execução Local

1. Clone o repositório ou extraia os arquivos para uma pasta local
2. Crie e ative um ambiente virtual Python:
   ```
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```
3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
4. Execute a aplicação:
   ```
   cd src
   python main.py
   ```
5. Acesse a aplicação em seu navegador:
   ```
   http://localhost:5000
   ```

## Funcionalidades Principais

### 1. Criação de Propostas

- Acesse a página inicial para criar uma nova proposta
- Preencha todos os campos obrigatórios (marcados com *)
- Os cálculos são realizados automaticamente em tempo real
- Clique em "Gerar Proposta" para salvar e obter o link único

### 2. Visualização de Propostas

- Cada proposta possui um link único no formato:
  ```
  http://seu-dominio.com/proposta/[id_publico]
  ```
- A página de visualização exibe todos os detalhes da proposta
- Opções para aprovar ou recusar a proposta estão disponíveis

### 3. Compartilhamento

- Na página de visualização, clique em "COMPARTILHAR ESSA SIMULAÇÃO"
- Opções disponíveis: copiar link, compartilhar via WhatsApp ou Email

### 4. Dashboard

- Acesse o dashboard através do menu superior
- Visualize estatísticas gerais e gráficos
- Lista completa de propostas com opções de filtro
- Exporte dados para CSV

## Personalização

### Alterando Logotipos e Imagens

1. Substitua os arquivos na pasta `src/static/img/`
2. Principais arquivos de imagem:
   - `logo.png` - Logo principal da Bowe
   - `document-icon.png` - Ícone de documento

### Alterando Estilos

1. Edite o arquivo `src/static/css/style.css`
2. As cores principais podem ser alteradas nas variáveis CSS

### Alterando Textos e Conteúdo

1. Edite os arquivos de template em `src/templates/`
2. Para alterar textos fixos, modifique diretamente os arquivos HTML

## Implantação em Produção

### Opção 1: Servidor Web com WSGI

1. Instale o Gunicorn:
   ```
   pip install gunicorn
   ```
2. Execute a aplicação com Gunicorn:
   ```
   gunicorn -w 4 -b 0.0.0.0:8000 "src.main:create_app()"
   ```
3. Configure um proxy reverso (Nginx ou Apache) para encaminhar as requisições

### Opção 2: Serviços de Hospedagem PaaS

A aplicação é compatível com serviços como Heroku, PythonAnywhere, ou Google App Engine.

## Suporte e Manutenção

### Backup do Banco de Dados

O banco de dados SQLite está localizado em `src/bowe_simulador.db`. Faça backups regulares deste arquivo.

### Atualizações

Para atualizar a aplicação:

1. Faça backup do banco de dados
2. Atualize os arquivos do código-fonte
3. Reinstale as dependências se necessário
4. Reinicie o servidor

## Solução de Problemas

### Erro ao iniciar a aplicação

- Verifique se todas as dependências estão instaladas
- Confirme que o ambiente virtual está ativado
- Verifique permissões de arquivo para o banco de dados

### Cálculos incorretos

- Verifique os valores das tarifas inseridas
- Confirme que os campos numéricos contêm valores válidos

### Problemas de acesso aos links

- Verifique se o servidor está configurado corretamente
- Confirme que as rotas estão registradas em `main.py`
