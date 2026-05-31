# diagnostico5.py
import os, sys
pasta = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, pasta)

for mod in ["database"]:
    if mod in sys.modules:
        del sys.modules[mod]

from database import _traduzir_sql_pg

sql_com = """
    SELECT ROUND(SUM(
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
      AND COALESCE(p.data_entrega_realizada, p.data_pedido) BETWEEN ? AND ?
"""

sql_mes = """
    SELECT
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
    GROUP BY ano, mes
"""

print("="*60)
print("SQL TOTAIS — TRADUZIDO PARA POSTGRESQL:")
print(_traduzir_sql_pg(sql_com))

print("\n" + "="*60)
print("SQL POR MÊS — TRADUZIDO PARA POSTGRESQL:")
print(_traduzir_sql_pg(sql_mes))

# Agora roda direto no PG para ver o erro real
print("\n" + "="*60)
print("RODANDO DIRETO NO POSTGRESQL:")
import psycopg2
db_url = os.environ.get("DATABASE_URL","")
try:
    conn = psycopg2.connect(db_url, sslmode="prefer", connect_timeout=8)
    cur = conn.cursor()
    sql_pg = _traduzir_sql_pg(sql_com)
    print("Executando query de totais...")
    try:
        cur.execute(sql_pg, ("2025-12-01", "2026-05-31"))
        print(f"Resultado: {cur.fetchall()}")
    except Exception as e:
        print(f"ERRO NA QUERY DE TOTAIS: {e}")

    sql_pg2 = _traduzir_sql_pg(sql_mes)
    print("\nExecutando query por mês...")
    try:
        cur.execute(sql_pg2)
        print(f"Resultado: {cur.fetchall()}")
    except Exception as e:
        print(f"ERRO NA QUERY POR MÊS: {e}")

    conn.close()
except Exception as e:
    print(f"ERRO AO CONECTAR: {e}")

print("\nDiagnóstico 5 concluído.")
