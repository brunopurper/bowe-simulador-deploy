# Campos do Formulário Simplificado para o Simulador de Propostas Bowe

## Dados do Vendedor (Ocultos)
*Todos os campos do vendedor serão ocultos conforme solicitado, mas mantidos no backend para uso futuro.*

1. **NomeVendedor** (string)
   - Obrigatório: Sim (valor padrão no backend)
   - Descrição: Nome completo do vendedor/promotor
   - Status: Oculto

2. **TelefoneVendedor** (string)
   - Obrigatório: Sim (valor padrão no backend)
   - Descrição: Número de telefone do vendedor
   - Status: Oculto

3. **ChavePix** (string)
   - Obrigatório: Não (valor padrão no backend)
   - Descrição: Chave PIX do vendedor para recebimento
   - Status: Oculto

4. **CidadeIndicador** (string)
   - Obrigatório: Não (valor padrão no backend)
   - Descrição: Cidade do indicador/vendedor
   - Status: Oculto

5. **Lider** (string)
   - Obrigatório: Não (valor padrão no backend)
   - Descrição: Nome do líder ou supervisor do vendedor
   - Status: Oculto

6. **CPFIndicador** (string)
   - Obrigatório: Não (valor padrão no backend)
   - Descrição: CPF do indicador
   - Status: Oculto

## Dados do Cliente
7. **NomeIndicado** (string)
   - Obrigatório: Sim
   - Descrição: Nome da empresa/cliente indicado
   - Status: Visível

8. **TelefoneIndicado** (string)
   - Obrigatório: Não
   - Descrição: Telefone do cliente
   - Status: Oculto

9. **EmailIndicado** (string)
   - Obrigatório: Não
   - Descrição: Email do cliente
   - Status: Oculto

10. **UnidadeConsumidora** (string)
    - Obrigatório: Sim
    - Descrição: Número da unidade consumidora
    - Status: Visível

## Dados de Consumo
11. **ConsumoIndicado** (number)
    - Obrigatório: Sim
    - Descrição: Consumo em kWh
    - Status: Visível

12. **TipoRede** (string)
    - Obrigatório: Sim
    - Descrição: Tipo de rede elétrica
    - Opções: "Monofásica", "Bifásica", "Trifásica"
    - Status: Visível

13. **MesAtual** (string)
    - Obrigatório: Sim
    - Descrição: Mês de referência da proposta
    - Formato: "Mês/Ano"
    - Status: Visível

## Dados de Tarifas (Simplificados)
14. **TaxaConcessionaria** (number)
    - Obrigatório: Sim
    - Descrição: Tarifa da concessionária com tributos (R$/kWh)
    - Status: Visível
    - Novo nome: "Tarifa com Tributos"

15. **TaxaBandeira** (number)
    - Obrigatório: Não
    - Descrição: Taxa adicional de bandeira em R$/kWh
    - Status: Visível (opcional)

16. **PercentualDesconto** (number)
    - Obrigatório: Sim
    - Descrição: Percentual de desconto a ser aplicado
    - Opções: Select com valores de 15% a 30% (incrementos de 1%)
    - Status: Visível
    - Substitui: TaxaEnersim

## Valores Calculados
17. **PagarEnergisa** (number)
    - Calculado: Sim
    - Descrição: Valor a pagar para concessionária (sem bandeira)
    - Fórmula: ConsumoIndicado * TaxaConcessionaria

18. **PagarEnergisaMaisBandeira** (number)
    - Calculado: Sim
    - Descrição: Valor a pagar para concessionária (com bandeira)
    - Fórmula: PagarEnergisa + (ConsumoIndicado * TaxaBandeira)

19. **PagarBowe** (number)
    - Calculado: Sim
    - Descrição: Valor a pagar para Bowe
    - Fórmula: PagarEnergisaMaisBandeira * (1 - (PercentualDesconto / 100))

20. **Economia** (number)
    - Calculado: Sim
    - Descrição: Economia mensal
    - Fórmula: PagarEnergisaMaisBandeira - PagarBowe

21. **EconomiaAnual** (number)
    - Calculado: Sim
    - Descrição: Economia anual
    - Fórmula: Economia * 12

22. **PorcentagemEconomia** (number)
    - Calculado: Sim
    - Descrição: Percentual de economia
    - Fórmula: PercentualDesconto (mesmo valor do select)

## Outros Campos
23. **ModeloContrato** (string)
    - Obrigatório: Não
    - Descrição: Modelo de contrato a ser utilizado
    - Status: Visível

24. **IdPublico** (string)
    - Obrigatório: Não
    - Descrição: Identificador público da proposta
    - Observação: Será gerado automaticamente pelo sistema
    - Status: Oculto

## Campos Adicionais para o Sistema
25. **DataCriacao** (datetime)
    - Calculado: Sim
    - Descrição: Data e hora de criação da proposta
    - Gerado automaticamente pelo sistema
    - Status: Oculto

26. **Status** (string)
    - Calculado: Sim
    - Descrição: Status da proposta
    - Valores possíveis: "Pendente", "Aprovada", "Recusada"
    - Valor padrão: "Pendente"
    - Status: Oculto
