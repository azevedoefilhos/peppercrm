# diagnostico3.py
import sqlite3, os, sys

pasta = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(pasta, "peppercrm.db")
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

d_ini, d_fim = "2025-12-01", "2026-05-31"

# 1. O pedido passa pelo filtro de status_pagamento?
q("1. Pedido ENTREGUE + LEFT JOIN comissao_pagamento",
  """SELECT p.pedido_id, p.status_pedido,
            cpag.pedido_id as cpag_ped, cpag.status_pagamento,
            COALESCE(cpag.status_pagamento, 'PENDENTE') AS st_coalesce
     FROM pedido p
     LEFT JOIN comissao_pagamento cpag ON p.pedido_id = cpag.pedido_id
     WHERE p.status_pedido = 'ENTREGUE'""")

# 2. O filtro IN ('PENDENTE','PAGO_PARCIAL') passa?
q("2. Com filtro IN PENDENTE/PAGO_PARCIAL",
  """SELECT p.pedido_id,
            COALESCE(cpag.status_pagamento, 'PENDENTE') AS st_pag
     FROM pedido p
     LEFT JOIN comissao_pagamento cpag ON p.pedido_id = cpag.pedido_id
     WHERE p.status_pedido = 'ENTREGUE'
       AND COALESCE(cpag.status_pagamento, 'PENDENTE') IN ('PENDENTE','PAGO_PARCIAL')""")

# 3. Com filtro de data também
q("3. Com filtro de data (semestre)",
  """SELECT p.pedido_id,
            COALESCE(p.data_entrega_realizada, p.data_pedido) AS competencia
     FROM pedido p
     LEFT JOIN comissao_pagamento cpag ON p.pedido_id = cpag.pedido_id
     WHERE p.status_pedido = 'ENTREGUE'
       AND COALESCE(cpag.status_pagamento, 'PENDENTE') IN ('PENDENTE','PAGO_PARCIAL')
       AND COALESCE(p.data_entrega_realizada, p.data_pedido) BETWEEN ? AND ?""",
  (d_ini, d_fim))

# 4. Com JOIN pedido_item
q("4. Com JOIN pedido_item",
  """SELECT p.pedido_id, pi.pedido_id as pi_ped, pi.status_item,
            pi.quantidade, pi.preco_final
     FROM pedido p
     JOIN pedido_item pi ON p.pedido_id = pi.pedido_id
        AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO','CANCELADO')
     LEFT JOIN comissao_pagamento cpag ON p.pedido_id = cpag.pedido_id
     WHERE p.status_pedido = 'ENTREGUE'
       AND COALESCE(cpag.status_pagamento, 'PENDENTE') IN ('PENDENTE','PAGO_PARCIAL')
       AND COALESCE(p.data_entrega_realizada, p.data_pedido) BETWEEN ? AND ?""",
  (d_ini, d_fim))

# 5. Com LEFT JOIN comissao
q("5. Com LEFT JOIN comissao",
  """SELECT p.pedido_id, com.percentual, p.comissao_percentual,
            COALESCE(p.comissao_percentual, COALESCE(com.percentual, 0)) AS perc_final
     FROM pedido p
     JOIN pedido_item pi ON p.pedido_id = pi.pedido_id
        AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO','CANCELADO')
     LEFT JOIN comissao com ON p.fornecedor_id = com.fornecedor_id AND com.ativo = 1
     LEFT JOIN comissao_pagamento cpag ON p.pedido_id = cpag.pedido_id
     WHERE p.status_pedido = 'ENTREGUE'
       AND COALESCE(cpag.status_pagamento, 'PENDENTE') IN ('PENDENTE','PAGO_PARCIAL')
       AND COALESCE(p.data_entrega_realizada, p.data_pedido) BETWEEN ? AND ?""",
  (d_ini, d_fim))

# 6. Query completa — sem ROUND para ver o valor bruto
q("6. Query completa SEM ROUND",
  """SELECT SUM(
        pi.quantidade * pi.preco_final
        * (1 - COALESCE(p.desconto_geral, 0) / 100.0)
    ) * COALESCE(p.comissao_percentual, COALESCE(com.percentual, 0)) / 100.0 AS total_bruto
    FROM pedido p
    JOIN pedido_item pi ON p.pedido_id = pi.pedido_id
        AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO','CANCELADO')
    LEFT JOIN comissao com ON p.fornecedor_id = com.fornecedor_id AND com.ativo = 1
    LEFT JOIN comissao_pagamento cpag ON p.pedido_id = cpag.pedido_id
    WHERE p.status_pedido = 'ENTREGUE'
      AND COALESCE(cpag.status_pagamento, 'PENDENTE') IN ('PENDENTE','PAGO_PARCIAL')
      AND COALESCE(p.data_entrega_realizada, p.data_pedido) BETWEEN ? AND ?""",
  (d_ini, d_fim))

# 7. Verifica: database.py usa _check_supabase() — tem DATABASE_URL no env?
import os as _os
db_url = _os.environ.get("DATABASE_URL", "")
print(f"\n{'='*60}")
print(f">>> DATABASE_URL presente? {'SIM — usando PostgreSQL' if db_url else 'NÃO — usando SQLite'}")
if db_url:
    print("    ATENÇÃO: o app está conectando no Railway, não no SQLite local!")
    print("    A query de comissões pode estar falhando no PostgreSQL por outro motivo.")

conn.close()
print("\n" + "="*60)
print("Diagnóstico 3 concluído.")
