# PepperCRM — Contexto para continuação da sessão de desenvolvimento

## Infraestrutura
- Railway: https://peppercrm-production.up.railway.app
- GitHub: https://github.com/azevedoefilhos/peppercrm.git (branch main)
- PostgreSQL Railway (ÚNICO banco): host=postgres.railway.internal, port=5432
- Conexão externa: kodama.proxy.rlwy.net:49266, user=postgres, db=railway
- Password: hCjlbzeKMkHIcifEnAMtlcHlONfrCdQx
- Arquivo .env local com DATABASE_URL apontando para Railway
- secrets.toml LOCAL limpo (sem SUPABASE_URL)
- Variáveis Railway: SUPABASE_URL e SUPABASE_DB_PASSWORD REMOVIDAS
- Plano Railway Hobby $5/mês

## Arquivos principais
crm_app.py, database.py, cadastros.py, catalogo.py, contatos.py,
pedido.py, ver_pedidos.py, visitas.py, relatorios.py, analise_competitiva.py,
metas.py, mix_analise.py, keepalive.py, despesas.py, scanner_ean.py,
pesquisa.py, nixpacks.toml, railway.toml, requirements.txt

## Padrões importantes do código
- PostgreSQL: usar %s como placeholder, True/False para boolean, ativo IS NOT FALSE
- SQLite: usar ? como placeholder, 1/0 para boolean
- _check_supabase() retorna True quando DATABASE_URL existe (Railway)
- _pg_connect() usa DATABASE_URL quando disponível
- execute_write() traduz ? para %s automaticamente via _traduzir_sql_pg()
- query() também traduz automaticamente

## Concluído nesta sessão (24-29/05/2026)
- Migração DEFINITIVA Supabase → PostgreSQL Railway (banco único)
- Scanner EAN com OpenCV (sem libzbar)
- Módulo Despesas completo: salvar, listar, editar, excluir, foto base64, PDF
- Editar contato de cliente (aba Contatos em Clientes)
- Botão Voltar no modo Rápido de pesquisa
- Bug pesquisa corrigido: elif no mapa evita produto nosso com preço do concorrente
- Sincronização completa Supabase → Railway (sincronizar_banco.py)
- Templates download 1 clique (sem expander)
- Lista clientes via st.dataframe com seleção de linha
- N+1 queries corrigidas em clientes, contatos, mix_analise
- ativo!=0 → ativo IS NOT FALSE em todos os módulos
- strftime → EXTRACT em metas.py e outros
- Dashboard: follow-ups colapsados por padrão
- Prospecção: multiselect de tipos de estabelecimento

## Próximas etapas (em ordem de prioridade)
1. **Scroll ao topo + reset de abas** ao navegar entre módulos
   - JavaScript via st.markdown não está funcionando no mobile
   - Abas não resetam para a principal ao navegar
2. **Export 1 clique** em Relatórios e Tabelas de Preço
3. **Aba Mensagens** por fornecedor — reformular
4. **Auditoria geral** do app no Railway
5. **Níveis de acesso** — 6 perfis de usuário
6. **Multi-tenant** + modelo de negócio

## Bugs conhecidos pendentes
- Scroll ao topo não funciona consistentemente no mobile
- use_container_width depreciado — substituir por width='stretch' antes de junho
- Fotos de gôndola: salvas como path local, não funcionam no Railway

## requirements.txt atual
streamlit, psycopg2-binary, pandas, plotly, reportlab, requests,
Pillow, opencv-python-headless, numpy, openpyxl, python-dotenv
