# teste_pg_direto.py — versão com dotenv embutido
from dotenv import load_dotenv
load_dotenv()

import os, sys
pasta = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, pasta)

import psycopg2
db_url = os.environ.get("DATABASE_URL", "")
if not db_url:
    print("DATABASE_URL não encontrada no .env")
    sys.exit(1)

print(f"Conectando ao Railway...")
conn = psycopg2.connect(db_url, sslmode="prefer", connect_timeout=8)
cur = conn.cursor()

d_ini, d_fim = "2025-12-01", "2026-05-31"

print("\n=== Query nova (subquery com MAX) ===")
try:
    cur.execute("""
        SELECT ROUND(SUM(sub.base * sub.perc / 100.0)::NUMERIC, 2)
        FROM (
            SELECT
                SUM(pi.quantidade * pi.preco_final
                    * (1 - COALESCE(p.desconto_geral, 0) / 100.0)) AS base,
                COALESCE(MAX(p.comissao_percentual), MAX(com.percentual), 0) AS perc
            FROM pedido p
            JOIN pedido_item pi ON p.pedido_id = pi.pedido_id
                AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO','CANCELADO')
            LEFT JOIN comissao com ON p.fornecedor_id = com.fornecedor_id AND com.ativo = TRUE
            LEFT JOIN comissao_pagamento cpag ON p.pedido_id = cpag.pedido_id
            WHERE p.status_pedido = 'ENTREGUE'
              AND COALESCE(cpag.status_pagamento, 'PENDENTE') IN ('PENDENTE','PAGO_PARCIAL')
              AND COALESCE(p.data_entrega_realizada, p.data_pedido) BETWEEN %s AND %s
            GROUP BY p.pedido_id
        ) sub
    """, (d_ini, d_fim))
    print(f"Resultado: {cur.fetchone()}")
except Exception as e:
    print(f"ERRO: {e}")
    conn.rollback()

print("\n=== Arquivo resultado_operacional.py em disco ===")
arq = os.path.join(pasta, "resultado_operacional.py")
with open(arq, encoding="utf-8") as f:
    conteudo = f.read()
print(f"  Linhas:             {len(conteudo.splitlines())}")
print(f"  Tem _q(?):          {'SIM' if '_q(' in conteudo else 'NAO — arquivo antigo!'}")
print(f"  Tem MAX comissao?:  {'SIM' if 'MAX(p.comissao_percentual)' in conteudo else 'NAO — arquivo antigo!'}")
print(f"  Tem strftime?:      {'SIM' if 'strftime' in conteudo else 'NAO'}")

conn.close()
print("\nTeste concluído.")
