# Bowe Simulador de Propostas - Novo Layout

Este projeto é uma versão atualizada do simulador de propostas da Bowe Energia, com um layout moderno e harmonioso, mantendo todas as funcionalidades originais e adicionando a exportação para PDF.

## Principais Melhorias

1. **Layout Moderno e Harmonioso**
   - Design mais limpo e profissional
   - Melhor organização visual das informações
   - Cards com destaque para valores importantes
   - Cores consistentes e significativas
   - Animações sutis para melhor experiência do usuário

2. **Exportação para PDF**
   - Botão dedicado para exportar a proposta em PDF
   - Mantém o estilo visual do layout web
   - Facilita o compartilhamento com clientes

3. **Responsividade**
   - Layout adaptado para diferentes tamanhos de tela
   - Melhor visualização em dispositivos móveis

## Instalação

1. Descompacte o arquivo zip em seu ambiente de desenvolvimento
2. Crie um ambiente virtual Python:
   ```
   python -m venv venv
   ```
3. Ative o ambiente virtual:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

## Execução

1. Ative o ambiente virtual (se ainda não estiver ativo)
2. Execute o aplicativo Flask:
   ```
   python src/main.py
   ```
3. Acesse no navegador: `http://localhost:5000`

## Observações Importantes

1. **Exportação para PDF**: 
   - A visualização do PDF pode variar dependendo do navegador
   - Recomendamos testar a exportação em diferentes navegadores
   - O WeasyPrint foi atualizado para a versão 65.1 para melhor compatibilidade

2. **Personalização**:
   - O estilo principal está em `src/static/css/new_layout.css`
   - Cores e elementos visuais podem ser facilmente ajustados neste arquivo

3. **Compatibilidade**:
   - Todas as funcionalidades originais foram preservadas
   - O fluxo de aprovação/recusa de propostas permanece o mesmo
   - Os cálculos e lógica de negócio não foram alterados

## Estrutura de Arquivos

- `src/` - Código-fonte da aplicação
  - `static/` - Arquivos estáticos (CSS, JS, imagens)
    - `css/new_layout.css` - Novo estilo visual
    - `js/new_layout_interactions.js` - Interações do novo layout
  - `templates/` - Templates HTML
    - `proposta.html` - Template da proposta com novo layout
  - `routes/` - Rotas da aplicação
    - `proposta.py` - Controlador das propostas (inclui exportação PDF)

## Suporte

Para qualquer dúvida ou problema, entre em contato com a equipe de desenvolvimento.
