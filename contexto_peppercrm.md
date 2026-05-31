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
- use_container_width=True DEPRECIADO — usar width="stretch" em todos os widgets
- Exportar campos vazios como '' (string vazia), nunca '—'
- Importadores: applymap converte '—','–','-','--' para None antes de gravar
- comissao.ativo é INTEGER no Railway — usar com.ativo = 1, NUNCA com.ativo = TRUE
- Queries com ROUND() + GROUP BY no PostgreSQL: colunas fora de agregação devem
  estar no GROUP BY ou usar MAX()/SUM() — PostgreSQL é mais estrito que SQLite
- Módulo resultado_operacional.py: queries bifurcadas com _q(sql_sqlite, sql_pg, params)
  pois strftime() do SQLite não é traduzido corretamente pelo tradutor quando dentro
  de COALESCE() ou EXTRACT()

## Ferramentas de trabalho
- atualizar.ps1: copia arquivos .py atualizados, faz git commit e push para Railway
  - Coloque arquivos .py na mesma pasta do .ps1 e execute com botão direito → PowerShell
  - Não reinicia o app local — use IniciarPepperCRM.vbs para isso
  - Se reportar "Nada para commitar", o arquivo em disco é idêntico ao do git —
    confirme que o download foi copiado corretamente antes de rodar
- IniciarPepperCRM.vbs: abre o app local (localhost:8501)
- Para ver logs/erros: abrir PyCharm terminal e rodar `streamlit run crm_app.py`
- Reiniciar Streamlit obrigatório após substituir arquivos: Ctrl+C → streamlit run crm_app.py

## Estrutura de navegação
- Módulos com _ir() padronizado com _scroll_topo = True em todos os módulos
- _RESET_ABAS em crm_app.py: ao navegar, abas do módulo destino resetam automaticamente
- Catálogo e Despesas adicionados ao menu principal
- resultado_operacional adicionado ao menu principal entre Despesas e Visitas

## Export/Import — padrão estabelecido
- Export e template usam MESMOS nomes amigáveis (ex: "Nome Fantasia", não "nome_fantasia")
- Importador normaliza: str.lower().str.replace(r'\s+','_') → "Nome Fantasia" vira "nome_fantasia"
- Export de clientes: ID, Nome Fantasia, Razao Social, Perfil, Fone, CNPJ, Site, Instagram,
  Endereco, Bairro, Cidade, Estado, Associacao, Status, Observacao (sem PDVs)
- Export de PDVs: ID, Cliente, Nr Loja, Nome Loja, Tipo PDV, Setor, Endereco, Bairro,
  Cidade, Estado, CNPJ, Gerente, Fone Gerente, Horario Recebimento, Status, Observacao,
  Latitude, Longitude
- Importador de clientes: busca por ID primeiro (se válido no banco), fallback por nome
- Importador de PDVs: busca por ID+cliente primeiro, fallback por cliente+nome_loja
- Templates ficam na própria aba de importação (não numa aba separada)
- row.get("associacao") — não mais "associacao_nome"
- row.get("cliente") — não mais "cliente_nome"
- row.get("nr_loja") — não mais "numero_loja"

## Tipos de PDV e perfil de cliente — lista padronizada (com acentos corretos)
Empório, Supermercado, Hipermercado, Atacadista, Mini Mercado, Mercearia,
Sacolão, Hortifruti, Açougue, Casa de Carnes, Peixaria, Padaria, Confeitaria,
Delicatessen, Hamburgueria, Restaurante, Lanchonete, Bar / Boteco,
Clube / Associação, Outro
- Banco Railway já corrigido (scripts corrigir_emporio.py e corrigir_acentos_pdv.py rodados)

## Ver Pedidos — melhorias implementadas (30/05/2026)
- Data de entrega prevista e data de entrega efetiva separadas (campos date_input)
- Data efetiva retroativa: max_value=hoje, pode informar data passada
- Prazo de pagamento herdado automaticamente da tabela de preço vinculada ao pedido
- Vencimento do boleto calculado automaticamente (extrai dias do prazo, soma à entrega)
- Ao confirmar status ENTREGUE: campo de data efetiva + checkbox de prorrogação de comissão
- Prorrogação de comissão: salva data_pagamento_original, nova data e motivo
- Migração necessária: migrar_comissao_prorrogacao.py (já rodado no Railway em 31/05/2026)

## Banco — colunas adicionadas
- comissao_pagamento.data_pagamento_original TEXT (migrado em 31/05/2026)
- comissao_pagamento.motivo_prorrogacao TEXT (migrado em 31/05/2026)

## Resultado Operacional (novo módulo — 31/05/2026)
- Arquivo: resultado_operacional.py
- Acesso: menu principal ("📊 Resultado Operacional") + aba em Comissões + aba em Despesas
- Visão "previsto": comissões de pedidos ENTREGUE com pagto PENDENTE/PAGO_PARCIAL
- Visão "realizado": comissões efetivamente pagas (status PAGO/PAGO_PARCIAL por data_pagamento)
- Queries bifurcadas: _q(sql_sqlite, sql_pg, params) — NÃO usa tradutor para este módulo
- PostgreSQL: usa subquery com MAX(p.comissao_percentual) para resolver GROUP BY
- Tabela despesa criada automaticamente se não existir (_garantir_tabela_despesa)
- Gráfico: barras agrupadas (comissões x despesas) + linha de saldo — últimos 12 meses fixos
- Breakdown por fornecedor e por categoria de despesa com gráfico de pizza

## Fotos de gôndola
- Salvas como base64 inline no campo foto_path da tabela pesquisa_foto
- Função _foto_para_b64() em pesquisa.py centraliza a leitura (base64 ou path local)
- Fotos antigas com path local (C:\Users\...) funcionam só localmente — no Railway não aparecem
- Pendente: script de migração das fotos antigas para base64 (baixa prioridade)

## Concluído na sessão 31/05/2026
- Migração colunas comissao_pagamento no Railway (data_pagamento_original, motivo_prorrogacao)
- Resultado Operacional: painel confronto comissões × despesas (novo módulo)
- B4: mensagem de sucesso ao editar PDV + scroll ao topo após salvar
- B3: filtro de fornecedor em Contatos → pré-seleciona fornecedor no painel de interações
  ao abrir tópico com filtro de fornecedor ativo na lista de Registros
  Também corrigido bug: chamada com fornecedor_id= renomeada para forn_presel=
- Correção ortográfica nos tipos de PDV: Empório, Sacolão, Açougue, Clube / Associação
  (cadastros.py + banco Railway corrigidos)

## Próximas etapas (em ordem de prioridade)
1. **C1 — Auditoria Railway** — varredura com olhar de novo usuário em todos os módulos
   (deixada para utilização na semana — 02/06/2026 em diante)
2. **B1 — Aba Mensagens por fornecedor** — reformular WhatsApp adaptado à estrutura
   de tópicos por fornecedor
3. **C3 — Performance** — N+1 queries em metas.py, queries lentas em relatorios.py
4. **D1 — Níveis de acesso** — 6 perfis de usuário (mais trabalhoso e estratégico)
   - Representante (dono) — acesso total
   - Vendedor interno — sem financeiro
   - Promotor — só pesquisa e visitas
   - Cliente — só pedidos
   - Fornecedor — só relatórios
   - Admin — configurações
5. **D2 — Multi-tenant** — múltiplos representantes com dados isolados
6. **D3 — Modelo de negócio** — planos, cobrança, onboarding

## Bugs conhecidos pendentes
- Fotos de gôndola antigas (path local) não aparecem no Railway
- Migração fotos antigas para base64 pendente (baixa prioridade)

## requirements.txt atual
streamlit, psycopg2-binary, pandas, plotly, reportlab, requests,
Pillow, opencv-python-headless, numpy, openpyxl, python-dotenv
