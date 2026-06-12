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
resultado_operacional.py, CHANGELOG.md

## ⚠️ REGRAS CRÍTICAS — NUNCA IGNORAR

### Streamlit
- NUNCA fixar versão do Streamlit abaixo de 1.58.0
- Streamlit 1.58.0+ usa Uvicorn (assíncrono) → dashboard carrega sem bloquear
- Streamlit 1.55.0 usa Tornado (síncrono) → dashboard bloqueia tudo por minutos
- requirements.txt deve ter `streamlit` SEM versão fixada (instala o mais recente)

### railway.toml
- startCommand DEVE estar na seção [deploy], não em [build]
- Não usar builder = "nixpacks" — Nixpacks foi deprecado pelo Railway
- Formato correto:
  [deploy]
  startCommand = "python keepalive.py & streamlit run crm_app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true"
  restartPolicyType = "on_failure"
  restartPolicyMaxRetries = 3

### Acesso a resultados de query()
- NUNCA usar r['nome_coluna'] — pode falhar silenciosamente com _DictRow
- SEMPRE usar índice: r[0], r[1], r[2]...

### PostgreSQL vs SQLite
- PostgreSQL: %s como placeholder, ROUND()::NUMERIC, com.ativo = 1 (INTEGER)
- SQLite: ? como placeholder
- NUNCA usar julianday() — calcular datas em Python
- NUNCA usar f-string com {where_sql} dentro de query()

### Encoding de arquivos
- Salvar .py com encoding='utf-8', newline='\n' para compatibilidade Linux/Railway
- NUNCA editar crm_app.py manualmente no Windows — usar scripts Python

### Desenvolvimento seguro
- SEMPRE testar local antes de subir via atualizar.ps1
- SEMPRE testar no celular antes de confirmar deploy
- Manter CHANGELOG.md atualizado após cada sessão

## Ferramentas de trabalho
- atualizar.ps1: copia arquivos .py, faz git commit e push para Railway
- IniciarPepperCRM.vbs: abre o app local (localhost:8501)
- Para ver logs: abrir PyCharm terminal e rodar `streamlit run crm_app.py`
- Reiniciar Streamlit após substituir arquivos: Ctrl+C → streamlit run crm_app.py

## Estrutura de navegação
- Menu na home: Cadastros (col1) + Comercial (col2) — ANTES do dashboard
- Dashboard de indicadores: abaixo do menu, carrega assincronamente (Uvicorn)
- _RESET_ABAS em crm_app.py: ao navegar, abas do módulo destino resetam

## Tipos de PDV — lista padronizada (com acentos corretos)
Empório, Supermercado, Hipermercado, Atacadista, Mini Mercado, Mercearia,
Sacolão, Hortifruti, Açougue, Casa de Carnes, Peixaria, Padaria, Confeitaria,
Delicatessen, Hamburgueria, Restaurante, Lanchonete, Bar / Boteco,
Clube / Associação, Outro
- Banco Railway já corrigido

## Módulos implementados
1. Clientes & PDVs — cadastro completo com geolocalização
2. Pedidos — emissão e acompanhamento
3. Contatos & Negociações — histórico com PDF exportável
4. Comissões — controle por fornecedor com prorrogação
5. Resultado Operacional — comissões × despesas = margem líquida
6. Pesquisa de Preços — com scanner de código de barras (OpenCV)
7. Metas — faturamento e mix por fornecedor
8. Relatórios — análise competitiva e ranking
9. Despesas — com foto de comprovante (base64)
10. Catálogo PDF — geração por fornecedor
11. Visitas — roteiros e promotores
12. Concorrentes & Inteligência Competitiva

## Banco — migrações realizadas
- comissao_pagamento.data_pagamento_original TEXT
- comissao_pagamento.motivo_prorrogacao TEXT
- Sequences corrigidas via corrigir_sequence.py
- Índices criados: idx_pedido_data, idx_pedido_status, idx_pedido_fornecedor,
  idx_pedido_item_pedido, idx_pedido_item_status, idx_comissao_fornecedor

## Resultado Operacional
- Arquivo: resultado_operacional.py
- Queries bifurcadas: _q(sql_sqlite, sql_pg, params) — NÃO usa tradutor automático
- com.ativo = 1 (não TRUE) no PostgreSQL
- Cache de 5min em todas as funções de query

## Fotos de gôndola
- Salvas como base64 inline no campo foto_path da tabela pesquisa_foto
- Fotos antigas com path local não aparecem no Railway (migração pendente)

## Mensagens WhatsApp (módulo Contatos)
- [cliente] substitui nome do cliente na mensagem
- Pendente: saudação automática por horário (Bom dia/Boa tarde/Boa noite)

## Próximas etapas (em ordem de prioridade)
1. **C1 — Auditoria Railway** — varredura módulo a módulo em produção
2. **D1 — Níveis de acesso** — 6 perfis de usuário
   - Representante ADM — acesso total
   - Vendedor ADM — sem financeiro
   - Representante Usuário — sem configurações
   - Vendedor Usuário — operacional
   - Promotor Vendedor — só pesquisa e visitas
   - Promotor — só pesquisa
3. **B1 — Mensagens por fornecedor** — saudação automática por horário
4. **D2 — Multi-tenant** — múltiplos representantes com dados isolados
5. **D3 — Modelo de negócio** — planos, cobrança, onboarding

## Bugs conhecidos pendentes
- Fotos de gôndola antigas (path local) não aparecem no Railway
- Scroll ao topo nos módulos — funciona no desktop, irregular no mobile

## requirements.txt atual
streamlit (sem versão — OBRIGATÓRIO para manter Uvicorn)
psycopg2-binary==2.9.12
pandas==2.2.3
plotly==5.24.1
reportlab==4.4.10
requests==2.31.0
openpyxl==3.1.2
Pillow==12.1.1
opencv-python-headless==4.10.0.84
numpy==1.26.4
python-dotenv==1.2.2
