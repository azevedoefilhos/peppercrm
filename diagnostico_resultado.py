# diagnostico_resultado.py
# Cole na pasta peppercrm e rode: python diagnostico_resultado.py
# Mostra exatamente o que o banco retorna para cada query do Resultado Operacional

import sqlite3, os

DB = os.path.join(os.path.dirname(__file__), "peppercrm.db")
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row

def q(label, sql, params=()):
    print(f"\n{'='*60}")
    print(f">>> {label}")
    try:
        rows = conn.execute(sql, params).fetchall()
        if not rows:
            print("    (sem resultados)")
        for r in rows:
            print("   ", dict(r))
    except Exception as e:
        print(f"    ERRO: {e}")

# ── 1. Estrutura das tabelas relevantes ──────────────────────────────────────
q("Colunas de pedido",
  "PRAGMA table_info(pedido)")

q("Colunas de comissao_pagamento",
  "PRAGMA table_info(comissao_pagamento)")

q("Colunas de despesa",
  "PRAGMA table_info(despesa)")

# ── 2. Dados brutos: pedidos ENTREGUE ────────────────────────────────────────
q("Pedidos ENTREGUE (amostra)",
  """SELECT pedido_id, status_pedido, data_pedido,
            data_entrega_realizada, comissao_percentual
     FROM pedido WHERE status_pedido='ENTREGUE' LIMIT 10""")

q("Comissao_pagamento (amostra)",
  """SELECT pedido_id, status_pagamento, data_pagamento, valor_pago
     FROM comissao_pagamento LIMIT 10""")

q("Despesas (amostra)",
  """SELECT despesa_id, data_despesa, valor, ativo
     FROM despesa LIMIT 10""")

# ── 3. Query de totais — visão previsto ──────────────────────────────────────
q("Total comissões PREVISTO (semestre)",
  """SELECT ROUND(SUM(
        pi.quantidade * pi.preco_final
        * (1 - COALESCE(p.desconto_geral, 0) / 100.0)
    ) * COALESCE(p.comissao_percentual, COALESCE(com.percentual, 0)) / 100.0, 2)
    FROM pedido p
    JOIN pedido_item pi ON p.pedido_id = pi.pedido_id
        AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO','CANCELADO')
    LEFT JOIN comissao com ON p.fornecedor_id = com.fornecedor_id AND com.ativo = 1
    LEFT JOIN comissao_pagamento cpag ON p.pedido_id = cpag.pedido_id
    WHERE p.status_pedido = 'ENTREGUE'
      AND COALESCE(cpag.status_pagamento, 'PENDENTE') IN ('PENDENTE','PAGO_PARCIAL')
      AND COALESCE(p.data_entrega_realizada, p.data_pedido) BETWEEN ? AND ?""",
  ("2025-12-01", "2026-05-31"))

# ── 4. Verifica o filtro de status_pagamento ─────────────────────────────────
q("Status pagamento dos pedidos ENTREGUE",
  """SELECT p.pedido_id, COALESCE(cpag.status_pagamento, 'PENDENTE') as st_pag
     FROM pedido p
     LEFT JOIN comissao_pagamento cpag ON p.pedido_id = cpag.pedido_id
     WHERE p.status_pedido = 'ENTREGUE'""")

# ── 5. Pedido_item: status dos itens ─────────────────────────────────────────
q("Status dos itens dos pedidos ENTREGUE",
  """SELECT pi.pedido_id, pi.status_item, COUNT(*) as qtd
     FROM pedido_item pi
     JOIN pedido p ON pi.pedido_id = p.pedido_id
     WHERE p.status_pedido = 'ENTREGUE'
     GROUP BY pi.pedido_id, pi.status_item""")

# ── 6. strftime funciona? ────────────────────────────────────────────────────
q("Teste strftime nos pedidos ENTREGUE",
  """SELECT pedido_id, data_pedido,
            strftime('%Y', data_pedido) as ano,
            strftime('%m', data_pedido) as mes
     FROM pedido WHERE status_pedido='ENTREGUE' LIMIT 5""")

# ── 7. Query por mês ─────────────────────────────────────────────────────────
q("Comissões por mês — visão previsto",
  """SELECT
        CAST(strftime('%Y', COALESCE(p.data_entrega_realizada, p.data_pedido)) AS INTEGER) AS ano,
        CAST(strftime('%m', COALESCE(p.data_entrega_realizada, p.data_pedido)) AS INTEGER) AS mes,
        ROUND(SUM(
            pi.quantidade * pi.preco_final
            * (1 - COALESCE(p.desconto_geral, 0) / 100.0)
        ) * COALESCE(p.comissao_percentual, COALESCE(com.percentual, 0)) / 100.0, 2) AS valor_com
    FROM pedido p
    JOIN pedido_item pi ON p.pedido_id = pi.pedido_id
        AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO','CANCELADO')
    LEFT JOIN comissao com ON p.fornecedor_id = com.fornecedor_id AND com.ativo = 1
    LEFT JOIN comissao_pagamento cpag ON p.pedido_id = cpag.pedido_id
    WHERE p.status_pedido = 'ENTREGUE'
      AND COALESCE(cpag.status_pagamento, 'PENDENTE') IN ('PENDENTE','PAGO_PARCIAL')
    GROUP BY ano, mes""")

# ── 8. Comissão calculada no módulo comissoes.py (query de referência) ───────
q("Referência: query do módulo Comissões (Total comissao R$111,35)",
  """SELECT
        ROUND(SUM(pi.quantidade * pi.preco_final
                  * (1 - COALESCE(p.desconto_geral, 0) / 100.0))
              * COALESCE(p.comissao_percentual, COALESCE(com.percentual, 0)) / 100.0, 2) AS valor_com,
        COALESCE(cpag.status_pagamento, 'PENDENTE') AS st_pag
    FROM pedido p
    JOIN pedido_item pi ON p.pedido_id = pi.pedido_id
        AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO','CANCELADO')
    LEFT JOIN comissao com ON p.fornecedor_id = com.fornecedor_id AND com.ativo = 1
    LEFT JOIN comissao_pagamento cpag ON p.pedido_id = cpag.pedido_id
    WHERE p.status_pedido = 'ENTREGUE'
    GROUP BY cpag.status_pagamento""")

conn.close()
print("\n" + "="*60)
print("Diagnóstico concluído. Cole o resultado acima no chat.")
