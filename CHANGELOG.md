# CHANGELOG — PepperCRM
# Registro de correções e melhorias aplicadas
# IMPORTANTE: Atualizar este arquivo após cada sessão de desenvolvimento
# Em caso de git reset, reaplicar todas as correções listadas aqui

---

## [2026-06-08] — Sessão atual

### Bugs corrigidos
- **contatos.py** — PDF de tópico mostrava "0 interações" mesmo havendo interações
  - Causa: `r['ativo']` não funciona com `_DictRow` do database.py — retorna erro silencioso
  - Correção: substituído por `r[6]` (acesso por índice) em 3 lugares da função `_gerar_pdf_topico`
  - Padrão a evitar: NUNCA usar `r['nome_coluna']` com resultados de `query()` — usar sempre índice `r[0]`, `r[1]`, etc.

### Melhorias
- **requirements.txt** — versões de todos os pacotes fixadas para evitar quebras automáticas
  - streamlit==1.55.0 (versão testada e compatível com celular Android/Chrome)
  - numpy==1.26.4 (1.25.0 não tem wheel para Python 3.12)
  - Demais pacotes com versões fixadas conforme ambiente local

---

## [2026-06-04] — Sessão de estabilização

### Bugs corrigidos
- **railway.toml** — Nixpacks deprecado causava falha de WebSocket no celular
  - Correção: removido `builder = "nixpacks"` da seção `[build]`, mantendo apenas `[deploy]`
- **relatorios.py** — texto de comando git colado acidentalmente na linha 1607
  - Causa: copiar/colar incorreto durante sessão de desenvolvimento
  - Correção: remoção do texto corrompido
- **catalogo.py** — aba "Mensagens WhatsApp" removida do Catálogo
  - Mensagens já existe dentro do módulo Contatos & Negociações
- **resultado_operacional.py** — título duplicado "📊 Resultado Operacional"
  - Correção: removido `st.subheader` de dentro de `tela_resultado_operacional()`
- **corrigir_sequence.py** — sequences do PostgreSQL desincronizadas causando UniqueViolation
  - Rodado em 31/05/2026: contato_interacao, contato_registro, pedido, cliente, pdv

### Melhorias
- **resultado_operacional.py** — cache de 5 minutos adicionado em todas as funções de query
- **crm_app.py** — menu movido para ANTES do dashboard para não bloquear navegação

---

## [2026-05-31] — Sessão principal de desenvolvimento

### Funcionalidades implementadas
- **resultado_operacional.py** — novo módulo: painel confronto comissões × despesas
  - Visão "previsto": comissões de pedidos ENTREGUE com pagto PENDENTE/PAGO_PARCIAL
  - Visão "realizado": comissões pagas por data_pagamento
  - Gráfico barras agrupadas + linha saldo — últimos 12 meses
  - Breakdown por fornecedor e por categoria de despesa
  - Queries bifurcadas: `_q(sql_sqlite, sql_pg, params)` — NÃO usa tradutor automático
- **B4** — mensagem de sucesso ao editar PDV + scroll ao topo (`_pdv_msg_ok`)
- **B3** — filtro de fornecedor em Contatos pré-seleciona fornecedor no painel
  - Parâmetro `forn_presel=` adicionado a `_painel_topico()` e `_painel_topico_completo()`
  - Bug corrigido: parâmetro `fornecedor_id=` renomeado para `forn_presel=`
- **metas.py** — N+1 queries eliminadas com batch por tipo (produto/categoria/linha)
- **relatorios.py** — datas hardcoded (2026-05-18, 2026-01-01) substituídas por cálculo Python dinâmico

### Migrações de banco
- `comissao_pagamento.data_pagamento_original TEXT` — migrado 31/05/2026
- `comissao_pagamento.motivo_prorrogacao TEXT` — migrado 31/05/2026
- Sequences PostgreSQL corrigidas via `corrigir_sequence.py`
- Tipos de PDV corrigidos: Empório, Sacolão, Açougue, Clube/Associação
  - Scripts: `corrigir_emporio.py` e `corrigir_acentos_pdv.py` rodados no Railway

### Índices criados no PostgreSQL
- `idx_pedido_data` ON pedido(data_pedido)
- `idx_pedido_status` ON pedido(status_pedido)
- `idx_pedido_fornecedor` ON pedido(fornecedor_id)
- `idx_pedido_item_pedido` ON pedido_item(pedido_id)
- `idx_pedido_item_status` ON pedido_item(status_item)
- `idx_comissao_fornecedor` ON comissao(fornecedor_id)

---

## Padrões críticos — NUNCA ignorar

### Acesso a resultados de query()
```python
# ERRADO — pode falhar silenciosamente com _DictRow
r['nome_coluna']

# CORRETO — sempre usar índice
r[0], r[1], r[2]...
```

### Queries com ROUND() no PostgreSQL
```python
# ERRADO — PostgreSQL rejeita ROUND(float, int)
ROUND(SUM(valor), 2)

# CORRETO — cast explícito
ROUND(SUM(valor)::NUMERIC, 2)
```

### Queries com GROUP BY no PostgreSQL
```python
# ERRADO — PostgreSQL exige que colunas fora de agregação estejam no GROUP BY
SELECT p.comissao_percentual, SUM(pi.valor) FROM pedido p ... GROUP BY p.pedido_id

# CORRETO — usar MAX() para colunas funcionalmente dependentes
SELECT MAX(p.comissao_percentual), SUM(pi.valor) FROM pedido p ... GROUP BY p.pedido_id
```

### comissao.ativo no PostgreSQL
```python
# ERRADO — ativo é INTEGER no Railway, não BOOLEAN
com.ativo = TRUE

# CORRETO
com.ativo = 1
```

### Encoding de arquivos
- Sempre salvar .py com `encoding='utf-8', newline='\n'` para compatibilidade Linux/Railway
- NUNCA editar crm_app.py manualmente no Windows — usar scripts Python para modificar

### railway.toml
- startCommand deve estar na seção `[deploy]`, não em `[build]`
- Não usar `builder = "nixpacks"` — Nixpacks foi deprecado pelo Railway

---

## Dashboard — status atual
- Dashboard de indicadores DESABILITADO temporariamente no crm_app.py
- Causa: queries de pedidos demoram 3-5s mesmo com índices — trava o celular
- Solução pendente: transformar em página separada acessível por botão
- Índices criados: ver seção acima — reduziram de 5s para 0.45s em condições normais
