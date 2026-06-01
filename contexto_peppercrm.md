# PepperCRM — Contexto para continuação da sessão de desenvolvimento

## Infraestrutura
- Railway: https://peppercrm-production.up.railway.app
- GitHub: https://github.com/azevedoefilhos/peppercrm.git (branch main)
- PostgreSQL Railway (ÚNICO banco): host=postgres.railway.internal, port=5432
- Conexão externa: kodama.proxy.rlwy.net:49266, user=postgres, db=railway
- Password: hCjlbzeKMkHIcifEnAMtlcHlONfrCdQx
- Arquivo .env local com DATABASE_URL apontando para Railway
- Plano Railway Hobby $5/mês
- Desenvolvimento local via PyCharm

## Arquivos principais
crm_app.py, database.py, cadastros.py, catalogo.py, contatos.py,
pedido.py, ver_pedidos.py, visitas.py, relatorios.py, analise_competitiva.py,
metas.py, mix_analise.py, keepalive.py, despesas.py, scanner_ean.py,
pesquisa.py, nixpacks.toml, railway.toml, requirements.txt,
cache_helpers.py, comissoes.py, concorrentes.py, configuracao.py,
sincronizar_banco.py, IniciarPepperCRM.vbs, atualizar.ps1,
resultado_operacional.py

## Padrões importantes do código
- PostgreSQL: usar %s como placeholder, True/False para boolean, ativo IS NOT FALSE
- SQLite: usar ? como placeholder, 1/0 para boolean
- _check_supabase() retorna True quando DATABASE_URL existe (Railway)
- _pg_connect() usa apenas DATABASE_URL — sem fallback Supabase (removido)
- execute_write() traduz ? para %s automaticamente via _traduzir_sql_pg()
- query() também traduz automaticamente
- NUNCA usar julianday() — calcular datas em Python e passar como parâmetro
- NUNCA usar f-string com {where_sql} dentro de query() — o tradutor pg pode corromper
- width="stretch" em todos os widgets (use_container_width DEPRECIADO e removido)
- Exportar campos vazios como '' (string vazia), nunca '—'
- Importadores: applymap converte '—','–','-','--' para None antes de gravar
- comissao.ativo é INTEGER no Railway — usar com.ativo = 1, NUNCA com.ativo = TRUE
- Queries com ROUND() + GROUP BY no PostgreSQL: colunas fora de agregação devem
  estar no GROUP BY ou usar MAX()/SUM() — PostgreSQL é mais estrito que SQLite
- resultado_operacional.py: queries bifurcadas com _q(sql_sqlite, sql_pg, params)
  pois strftime() do SQLite não é traduzido corretamente dentro de COALESCE()
- NUNCA mexer no crm_app.py sem testar localmente primeiro — arquivo crítico
- Streamlit local: versão 1.55.0 — Railway fixado em 1.55.0 no requirements.txt

## Ferramentas de trabalho
- atualizar.ps1: copia arquivos .py atualizados, faz git commit e push para Railway
  - Coloque arquivos .py na mesma pasta do .ps1 e execute com botão direito → PowerShell
  - Se reportar "Nada para commitar", confirme que o download foi copiado corretamente
- IniciarPepperCRM.vbs: abre o app local (localhost:8501)
- Para ver logs/erros: abrir PyCharm terminal e rodar `streamlit run crm_app.py`
- Reiniciar Streamlit obrigatório após substituir arquivos: Ctrl+C → streamlit run crm_app.py
- Sequences do PostgreSQL: rodar corrigir_sequence.py se aparecer UniqueViolation

## Estrutura de navegação
- Módulos com _ir() padronizado com _scroll_topo = True em todos os módulos
- _RESET_ABAS em crm_app.py: ao navegar, abas do módulo destino resetam automaticamente
- Menu no dashboard: Cadastros (col1) + Comercial (col2) — ANTES do dashboard
- Dashboard fica DEPOIS do menu para não bloquear navegação durante carregamento

## Tipos de PDV e perfil de cliente — lista padronizada (com acentos corretos)
Empório, Supermercado, Hipermercado, Atacadista, Mini Mercado, Mercearia,
Sacolão, Hortifruti, Açougue, Casa de Carnes, Peixaria, Padaria, Confeitaria,
Delicatessen, Hamburgueria, Restaurante, Lanchonete, Bar / Boteco,
Clube / Associação, Outro
- Banco Railway já corrigido (corrigir_emporio.py e corrigir_acentos_pdv.py rodados)

## Export/Import — padrão estabelecido
- Export e template usam MESMOS nomes amigáveis (ex: "Nome Fantasia", não "nome_fantasia")
- Importador normaliza: str.lower().str.replace(r'\s+','_')
- row.get("associacao"), row.get("cliente"), row.get("nr_loja")
- Templates ficam na própria aba de importação

## Ver Pedidos — melhorias implementadas (30/05/2026)
- Data de entrega prevista e efetiva separadas
- Prazo de pagamento herdado da tabela de preço
- Vencimento do boleto calculado automaticamente
- Prorrogação de comissão: salva data_pagamento_original, nova data e motivo

## Banco — colunas e migrações realizadas
- comissao_pagamento.data_pagamento_original TEXT (migrado 31/05/2026)
- comissao_pagamento.motivo_prorrogacao TEXT (migrado 31/05/2026)
- corrigir_sequence.py: corrige sequences desincronizadas (UniqueViolation)

## Resultado Operacional (implementado 31/05/2026)
- Arquivo: resultado_operacional.py
- Acesso: menu principal + aba em Comissões + aba em Despesas
- Visão "previsto": comissões ENTREGUE com pagto PENDENTE/PAGO_PARCIAL
- Visão "realizado": comissões pagas por data_pagamento
- Queries bifurcadas: _q(sql_sqlite, sql_pg, params)
- Gráfico barras agrupadas + linha saldo — últimos 12 meses
- Breakdown por fornecedor e por categoria de despesa

## Fotos de gôndola
- Salvas como base64 inline no campo foto_path da tabela pesquisa_foto
- Fotos antigas com path local não aparecem no Railway (migração pendente)

## Dashboard — PROBLEMA CRÍTICO PENDENTE
- Dashboard desabilitado temporariamente no crm_app.py (linha: `pass`)
- Causa: query de pedidos demora 3.4s no Railway — total 6-7s travava o app
- Solução necessária ANTES de reabilitar:
  1. Criar índices no PostgreSQL Railway:
     CREATE INDEX IF NOT EXISTS idx_pedido_data ON pedido(data_pedido);
     CREATE INDEX IF NOT EXISTS idx_pedido_status ON pedido(status_pedido);
     CREATE INDEX IF NOT EXISTS idx_pedido_item_pedido ON pedido_item(pedido_id);
  2. Reabilitar _dashboard() no crm_app.py após confirmar que query < 1s
- Menu já foi movido para ANTES do dashboard (navegação funciona mesmo sem dashboard)

## Concluído na sessão 31/05/2026
- Migração colunas comissao_pagamento no Railway
- Resultado Operacional: painel confronto comissões × despesas
- B4: mensagem de sucesso ao editar PDV + scroll ao topo
- B3: filtro de fornecedor em Contatos pré-seleciona no painel de interações
  (também corrigido bug: parâmetro fornecedor_id= renomeado para forn_presel=)
- Correção ortográfica tipos de PDV: Empório, Sacolão, Açougue, Clube/Associação
- Metas: N+1 queries eliminadas (batch por tipo produto/categoria/linha)
- Relatórios: datas hardcoded substituídas por cálculo Python dinâmico
- requirements.txt: streamlit==1.55.0, python-dotenv adicionado
- crm_app.py: menu movido para antes do dashboard

## Próximas etapas (em ordem de prioridade)
1. **URGENTE — Criar índices no Railway e reabilitar dashboard**
   - Script: criar_indices.py com os 3 CREATE INDEX acima
   - Após confirmar query < 1s, reabilitar _dashboard() no crm_app.py
2. **C1 — Auditoria Railway** — varredura módulo a módulo em produção
3. **B1 — Aba Mensagens por fornecedor** — reformular WhatsApp por tópico
4. **C3 — Performance adicional** — outras queries lentas identificadas
5. **D1 — Níveis de acesso** — 6 perfis de usuário
6. **D2 — Multi-tenant** — múltiplos representantes isolados
7. **D3 — Modelo de negócio** — planos, cobrança, onboarding

## Bugs conhecidos pendentes
- Dashboard desabilitado (ver seção acima)
- Fotos de gôndola antigas (path local) não aparecem no Railway
- Sequences PostgreSQL podem desincronizar — rodar corrigir_sequence.py se UniqueViolation

## requirements.txt atual
streamlit==1.55.0, psycopg2-binary, pandas, plotly, reportlab, requests,
Pillow, opencv-python-headless, numpy, openpyxl, python-dotenv
