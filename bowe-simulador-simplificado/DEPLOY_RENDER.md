# Guia de Deploy no Render.com

Este guia explica como fazer o deploy gratuito do Bowe Simulador de Propostas no Render.com.

## Pré-requisitos

1. Uma conta no [Render.com](https://render.com) (você pode se cadastrar gratuitamente)
2. O código do projeto Bowe Simulador (arquivo zip que você recebeu)

## Passo a Passo para Deploy

### 1. Preparação do Projeto

O projeto já está configurado para deploy com os seguintes arquivos:
- `Procfile` - Instruções para o servidor web
- `requirements.txt` - Dependências atualizadas incluindo gunicorn
- `.env.example` - Exemplo de variáveis de ambiente

### 2. Criar uma Conta no Render.com

1. Acesse [render.com](https://render.com)
2. Clique em "Sign Up" e crie uma conta (pode usar GitHub, GitLab ou email)
3. Confirme seu email se necessário

### 3. Criar um Novo Web Service

1. No Dashboard do Render, clique em "New +" e selecione "Web Service"
2. Escolha a opção "Build and deploy from a Git repository"
3. Você terá duas opções:
   - Conectar com GitHub/GitLab (recomendado)
   - Upload manual via .zip (alternativa)

#### Opção A: Deploy via GitHub/GitLab (Recomendado)

1. Crie um repositório no GitHub ou GitLab
2. Faça upload dos arquivos do projeto para o repositório
3. No Render, conecte sua conta GitHub/GitLab
4. Selecione o repositório do projeto

#### Opção B: Deploy Manual (Alternativa)

1. No Render, escolha "Upload Files Manually"
2. Faça upload do arquivo zip do projeto

### 4. Configurar o Web Service

Preencha os seguintes campos:
- **Name**: bowe-simulador (ou outro nome de sua preferência)
- **Region**: Escolha a região mais próxima do Brasil (geralmente US East)
- **Branch**: main (ou master, dependendo do seu repositório)
- **Runtime**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn src.main:app`
- **Plan**: Free

### 5. Configurar Variáveis de Ambiente

1. Expanda a seção "Advanced" ou "Environment"
2. Adicione as seguintes variáveis:
   - `SECRET_KEY`: uma string aleatória para segurança
   - `FLASK_ENV`: production
   - `ADMIN_USERNAME`: admin (ou outro usuário de sua preferência)
   - `ADMIN_PASSWORD`: bowe2025 (ou outra senha de sua preferência)

### 6. Iniciar o Deploy

1. Clique em "Create Web Service"
2. Aguarde o processo de build e deploy (pode levar alguns minutos)
3. Quando concluído, você receberá uma URL no formato `https://seu-app.onrender.com`

### 7. Acessar o Aplicativo

1. Acesse a URL fornecida pelo Render
2. Você será redirecionado para a página de login
3. Faça login com as credenciais configuradas (admin/bowe2025 por padrão)

## Observações Importantes

- O plano gratuito do Render pode "adormecer" após períodos de inatividade
- O primeiro acesso após um período de inatividade pode ser mais lento
- Para uso em produção com alto tráfego, considere atualizar para um plano pago

## Solução de Problemas

Se encontrar problemas durante o deploy:
1. Verifique os logs no dashboard do Render
2. Confirme se todas as variáveis de ambiente estão configuradas corretamente
3. Verifique se o banco de dados SQLite está funcionando corretamente em produção

Para qualquer dúvida adicional, consulte a [documentação oficial do Render](https://render.com/docs).
