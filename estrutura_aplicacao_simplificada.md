# Estrutura da Aplicação Web Simplificada - Simulador de Propostas Bowe

## Ajustes na Arquitetura

A estrutura básica da aplicação permanecerá a mesma, utilizando Flask como tecnologia principal. No entanto, serão necessários alguns ajustes para acomodar as novas solicitações:

1. **Modelo de Dados**: 
   - Manter todos os campos originais no modelo `Proposta`
   - Adicionar campo `percentual_desconto` para substituir `taxa_enersim`
   - Ajustar a lógica de cálculo para usar o percentual de desconto

2. **Formulário**:
   - Ocultar campos do vendedor, mantendo valores padrão no backend
   - Ocultar campos de telefone e email do cliente
   - Simplificar campos de tarifas
   - Adicionar select para percentual de desconto

3. **Lógica de Cálculo**:
   - Modificar a fórmula de cálculo do valor a pagar para Bowe
   - Ajustar o cálculo de economia com base no percentual de desconto

## Estrutura de Arquivos Atualizada

```
bowe-simulador/
├── venv/                      # Ambiente virtual Python
├── src/                       # Código-fonte da aplicação
│   ├── main.py                # Ponto de entrada da aplicação (sem alterações)
│   ├── models/                # Modelos de dados
│   │   ├── __init__.py        # (sem alterações)
│   │   └── proposta.py        # Modelo para propostas (ajustado)
│   ├── routes/                # Rotas e controladores
│   │   ├── __init__.py        # (sem alterações)
│   │   ├── formulario.py      # Rotas para o formulário (ajustado)
│   │   ├── proposta.py        # Rotas para visualização (ajustado)
│   │   └── dashboard.py       # Rotas para o dashboard (sem alterações)
│   ├── static/                # Arquivos estáticos (sem alterações)
│   └── templates/             # Templates HTML
│       ├── base.html          # Template base (sem alterações)
│       ├── formulario.html    # Página do formulário (ajustado)
│       ├── proposta.html      # Página de visualização (ajustado)
│       └── dashboard.html     # Página do dashboard (sem alterações)
└── requirements.txt           # Dependências do projeto (sem alterações)
```

## Ajustes no Modelo de Dados

O modelo `Proposta` será ajustado para incluir o novo campo `percentual_desconto`:

```python
class Proposta(db.Model):
    # Campos existentes...
    
    # Novo campo
    percentual_desconto = db.Column(db.Float, nullable=False)
    
    # Ajuste no método __init__
    def __init__(self, **kwargs):
        super(Proposta, self).__init__(**kwargs)
        # Lógica existente...
        
        # Nova lógica de cálculo
        if not self.pagar_enersim and self.pagar_energisa_mais_bandeira and self.percentual_desconto:
            self.pagar_enersim = round(self.pagar_energisa_mais_bandeira * (1 - (self.percentual_desconto / 100)), 2)
```

## Ajustes no Formulário

O formulário será modificado para ocultar campos e adicionar o select de percentual de desconto:

```python
class PropostaForm(FlaskForm):
    # Campos do vendedor ocultos (valores padrão no backend)
    nome_vendedor = HiddenField(default="Bowe Energia")
    telefone_vendedor = HiddenField(default="(00) 0000-0000")
    chave_pix = HiddenField()
    cidade_indicador = HiddenField()
    lider = HiddenField()
    cpf_indicador = HiddenField()
    
    # Dados do cliente (telefone e email ocultos)
    nome_indicado = StringField('Nome do Cliente', validators=[DataRequired()])
    telefone_indicado = HiddenField()
    email_indicado = HiddenField()
    unidade_consumidora = StringField('Unidade Consumidora', validators=[DataRequired()])
    
    # Dados de consumo (sem alterações)
    consumo_indicado = FloatField('Consumo (kWh)', validators=[DataRequired(), NumberRange(min=1)])
    tipo_rede = SelectField('Tipo de Rede', choices=[
        ('Monofásica', 'Monofásica'),
        ('Bifásica', 'Bifásica'),
        ('Trifásica', 'Trifásica')
    ], validators=[DataRequired()])
    mes_atual = StringField('Mês de Referência', validators=[DataRequired()])
    
    # Dados de tarifas (simplificados)
    taxa_concessionaria = FloatField('Tarifa com Tributos (R$/kWh)', validators=[DataRequired(), NumberRange(min=0.001)])
    taxa_bandeira = FloatField('Taxa Bandeira (R$/kWh)', validators=[Optional(), NumberRange(min=0)])
    
    # Novo campo para percentual de desconto
    percentual_desconto = SelectField('Percentual de Desconto', 
                                     choices=[(str(i), f"{i}%") for i in range(15, 31)],
                                     validators=[DataRequired()])
    
    # Outros campos
    modelo_contrato = StringField('Modelo de Contrato', validators=[Optional()])
    
    # Campos calculados (sem alterações)
    pagar_energisa = HiddenField()
    pagar_energisa_mais_bandeira = HiddenField()
    pagar_enersim = HiddenField()
    economia = HiddenField()
    economia_anual = HiddenField()
    porcentagem_economia = HiddenField()
```

## Ajustes na Lógica de Cálculo

A função de cálculo em tempo real será ajustada para usar o percentual de desconto:

```javascript
function calcularValores() {
    // Obter valores dos campos
    var consumo = parseFloat($('#consumo_indicado').val()) || 0;
    var taxaConcessionaria = parseFloat($('#taxa_concessionaria').val()) || 0;
    var taxaBandeira = parseFloat($('#taxa_bandeira').val()) || 0;
    var percentualDesconto = parseFloat($('#percentual_desconto').val()) || 0;
    
    // Verificar se temos os valores mínimos necessários
    if (consumo > 0 && taxaConcessionaria > 0 && percentualDesconto > 0) {
        $.ajax({
            url: "/calcular",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                consumo_indicado: consumo,
                taxa_concessionaria: taxaConcessionaria,
                taxa_bandeira: taxaBandeira,
                percentual_desconto: percentualDesconto
            }),
            success: function(data) {
                // Atualizar campos de exibição
                // ...
            }
        });
    }
}
```

E no backend:

```python
@formulario_bp.route('/calcular', methods=['POST'])
def calcular():
    data = request.json
    
    try:
        consumo = float(data.get('consumo_indicado', 0))
        taxa_concessionaria = float(data.get('taxa_concessionaria', 0))
        taxa_bandeira = float(data.get('taxa_bandeira', 0))
        percentual_desconto = float(data.get('percentual_desconto', 0))
        
        # Realizar cálculos
        pagar_energisa = round(consumo * taxa_concessionaria, 2)
        pagar_energisa_mais_bandeira = round(pagar_energisa + (consumo * taxa_bandeira), 2)
        pagar_enersim = round(pagar_energisa_mais_bandeira * (1 - (percentual_desconto / 100)), 2)
        economia = round(pagar_energisa_mais_bandeira - pagar_enersim, 2)
        economia_anual = round(economia * 12, 2)
        porcentagem_economia = percentual_desconto  # Usar diretamente o percentual de desconto
        
        return jsonify({
            'pagar_energisa': pagar_energisa,
            'pagar_energisa_mais_bandeira': pagar_energisa_mais_bandeira,
            'pagar_enersim': pagar_enersim,
            'economia': economia,
            'economia_anual': economia_anual,
            'porcentagem_economia': porcentagem_economia
        })
    except (ValueError, ZeroDivisionError):
        return jsonify({'error': 'Erro nos cálculos. Verifique os valores informados.'}), 400
```

## Considerações para Futuras Atualizações

1. **Reativação de Campos Ocultos**:
   - Todos os campos ocultos permanecerão no modelo de dados
   - Para reativar, bastará ajustar o template HTML e o formulário WTForms
   - Nenhuma migração de banco de dados será necessária

2. **Flexibilidade na Lógica de Cálculo**:
   - A lógica de cálculo poderá ser facilmente ajustada no futuro
   - O percentual de desconto pode ser substituído pela tarifa Bowe original

3. **Compatibilidade com Dados Existentes**:
   - Propostas criadas com a versão anterior permanecerão válidas
   - O dashboard continuará exibindo todas as propostas
