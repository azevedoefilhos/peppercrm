# CHANGELOG — PepperCRM
# Registro de correções e melhorias aplicadas
# IMPORTANTE: Atualizar após cada sessão de desenvolvimento
# Em caso de git reset, reaplicar todas as correções listadas aqui

---

## ⚠️ REGRA MAIS CRÍTICA DO PROJETO

### Streamlit — NUNCA fixar abaixo de 1.58.0
- Streamlit 1.58.0+ usa Uvicorn (assíncrono) → dashboard carrega normalmente
- Streamlit 1.55.0 usa Tornado (síncrono) → dashboard bloqueia por minutos
- requirements.txt deve ter `streamlit` SEM versão fixada
- Esta regra custou dias de debugging — NUNCA ignorar

---

## [2026-06-10] — Sessão atual

### Causa raiz do dashboard lento identificada e corrigida
- Problema: fixamos streamlit==1.55.0 pensando resolver compatibilidade mobile
- Efeito: Tornado (1.55.0) bloqueia thread durante queries → dashboard trava por minutos
- Solução: `streamlit` sem versão → Railway instala 1.58.0+ com Uvicorn assíncrono
- Dashboard voltou a funcionar normalmente no celular e desktop

### railway.toml — causa raiz do problema mobile identificada
- startCommand estava na seção [build] em vez de [deploy]
- Correto:
  [deploy]
  startCommand = "python keepalive.py & streamlit run crm_app.py ..."

---

## [2026-06-08] — Sessão

### Bugs corrigidos
- **contatos.py** — PDF mostrava "0 interações"
  - Causa 1: r['ativo'] não funciona com _DictRow → usar r[6] (índice)
  - Causa 2: query filtrava por ci.fornecedor_id que não existe na tabela contato_interacao
  - Fix: remover filtro de fornecedor_id da query do PDF; usar índice r[6]
  - Padrão: NUNCA usar r['coluna'] — sempre r[índice]

### Apresentação criada
- PepperCRM_Apresentacao.pptx — 7 slides para a consultora Gigi (Sebrae)
- Pendente para próxima versão: scanner de código de barras + roteiros de visitas

---

## [2026-06-04/05] — Sessão de estabilização

### Causa raiz do problema mobile
- railway.toml com startCommand na seção [build] em vez de [deploy]
- Nixpacks deprecado pelo Railway causava comportamento errático

### Bugs corrigidos
- **relatorios.py** — texto git corrompido na linha 1607 removido
- **catalogo.py** — aba Mensagens WhatsApp removida (já existe em Contatos)
- **analise_competitiva.py** — botão "Meu produto vs" → "Meu produto vs concorrentes"
- **configuracao.py** — tabela configuracao criada automaticamente se não existir
- Sequences PostgreSQL desincronizadas corrigidas via corrigir_sequence.py

---

## [2026-05-31] — Sessão principal de desenvolvimento

### Funcionalidades implementadas
- **resultado_operacional.py** — painel confronto comissões × despesas
- **B4** — mensagem de sucesso ao editar PDV
- **B3** — filtro de fornecedor em Contatos pré-seleciona no painel
- **metas.py** — N+1 queries eliminadas com batch
- **relatorios.py** — datas hardcoded substituídas por cálculo Python dinâmico

### Migrações de banco
- comissao_pagamento.data_pagamento_original TEXT
- comissao_pagamento.motivo_prorrogacao TEXT
- Sequences corrigidas
- Tipos de PDV corrigidos: Empório, Sacolão, Açougue, Clube/Associação

### Índices criados no PostgreSQL
- idx_pedido_data, idx_pedido_status, idx_pedido_fornecedor
- idx_pedido_item_pedido, idx_pedido_item_status, idx_comissao_fornecedor

---

## Padrões críticos de código

### Acesso a resultados de query()
```python
# ERRADO — falha silenciosamente com _DictRow
r['nome_coluna']
# CORRETO
r[0], r[1], r[2]
```

### ROUND() no PostgreSQL
```python
# ERRADO
ROUND(SUM(valor), 2)
# CORRETO
ROUND(SUM(valor)::NUMERIC, 2)
```

### GROUP BY no PostgreSQL
```python
# ERRADO — PostgreSQL exige coluna no GROUP BY ou em agregação
SELECT p.comissao_percentual, SUM(pi.valor) FROM pedido p ... GROUP BY p.pedido_id
# CORRETO
SELECT MAX(p.comissao_percentual), SUM(pi.valor) FROM pedido p ... GROUP BY p.pedido_id
```

### comissao.ativo no PostgreSQL
```python
# ERRADO — ativo é INTEGER, não BOOLEAN
com.ativo = TRUE
# CORRETO
com.ativo = 1
```

### railway.toml
```toml
# ERRADO
[build]
builder = "nixpacks"
startCommand = "..."

# CORRETO
[deploy]
startCommand = "python keepalive.py & streamlit run crm_app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true"
restartPolicyType = "on_failure"
restartPolicyMaxRetries = 3
```
