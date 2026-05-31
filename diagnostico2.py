# diagnostico2.py
import sqlite3, os
from datetime import date, timedelta

DB = os.path.join(os.path.dirname(__file__), "peppercrm.db")
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row

def q(label, sql, params=()):
    print(f"\n{'='*60}")
    print(f">>> {label}")
    print(f"    params: {params}")
    try:
        rows = conn.execute(sql, params).fetchall()
        if not rows:
            print("    (sem resultados)")
        for r in rows:
            print("   ", dict(r))
    except Exception as e:
        print(f"    ERRO: {e}")

# Datas que o app manda para o semestre
hoje = date.today()
d_ini = (hoje - timedelta(days=180)).replace(day=1)
d_fim = hoje
print(f"\nHoje: {hoje}")
print(f"Semestre d_ini: {d_ini.isoformat()}")
print(f"Semestre d_fim: {d_fim.isoformat()}")

# Pedido do banco — cai dentro do semestre?
q("Pedido ENTREGUE — data e se cai no semestre",
  """SELECT pedido_id, data_pedido, data_entrega_realizada,
            COALESCE(data_entrega_realizada, data_pedido) AS competencia,
            CASE WHEN COALESCE(data_entrega_realizada, data_pedido)
                      BETWEEN ? AND ?
                 THEN 'SIM — dentro do período'
                 ELSE 'NÃO — fora do período'
            END AS no_periodo
     FROM pedido WHERE status_pedido='ENTREGUE'""",
  (d_ini.isoformat(), d_fim.isoformat()))

# Query completa de totais com o período real
q("Total comissões PREVISTO — período semestre real",
  """SELECT ROUND(SUM(
        pi.quantidade * pi.preco_final
        * (1 - COALESCE(p.desconto_geral, 0) / 100.0)
    ) * COALESCE(p.comissao_percentual, COALESCE(com.percentual, 0)) / 100.0, 2) AS total
    FROM pedido p
    JOIN pedido_item pi ON p.pedido_id = pi.pedido_id
        AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO','CANCELADO')
    LEFT JOIN comissao com ON p.fornecedor_id = com.fornecedor_id AND com.ativo = 1
    LEFT JOIN comissao_pagamento cpag ON p.pedido_id = cpag.pedido_id
    WHERE p.status_pedido = 'ENTREGUE'
      AND COALESCE(cpag.status_pagamento, 'PENDENTE') IN ('PENDENTE','PAGO_PARCIAL')
      AND COALESCE(p.data_entrega_realizada, p.data_pedido) BETWEEN ? AND ?""",
  (d_ini.isoformat(), d_fim.isoformat()))

# Tabela despesa existe?
q("Tabelas existentes no banco",
  "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")

conn.close()
print("\n" + "="*60)
print("Diagnóstico 2 concluído.")
