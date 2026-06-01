# criar_indices.py
# Cria índices no PostgreSQL Railway para acelerar queries do dashboard
from dotenv import load_dotenv
load_dotenv()
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database import _pg_connect

conn = _pg_connect()
cur = conn.cursor()

indices = [
    ("idx_pedido_data",       "pedido",       "data_pedido"),
    ("idx_pedido_status",     "pedido",       "status_pedido"),
    ("idx_pedido_fornecedor", "pedido",       "fornecedor_id"),
    ("idx_pedido_item_pedido","pedido_item",  "pedido_id"),
    ("idx_pedido_item_status","pedido_item",  "status_item"),
    ("idx_comissao_fornecedor","comissao",    "fornecedor_id"),
]

for nome, tabela, coluna in indices:
    print(f"Criando {nome}...", end=" ")
    try:
        cur.execute(f"CREATE INDEX IF NOT EXISTS {nome} ON {tabela}({coluna})")
        conn.commit()
        print("✅")
    except Exception as e:
        conn.rollback()
        print(f"❌ {e}")

# Testa a query lenta
print("\nTestando query de pedidos após índices...")
t0 = time.time()
cur.execute("""
    SELECT
        COUNT(DISTINCT CASE WHEN p.status_pedido IN ('ABERTO','ENVIADO')
              THEN p.pedido_id END),
        COUNT(DISTINCT CASE WHEN p.status_pedido NOT IN ('CANCELADO','RECUSADO')
              AND p.data_pedido >= '2026-05-01' THEN p.pedido_id END),
        ROUND(COALESCE(SUM(CASE
            WHEN p.status_pedido NOT IN ('CANCELADO','RECUSADO')
             AND p.data_pedido >= '2026-05-01'
            THEN pi.quantidade*pi.preco_final*(1-COALESCE(p.desconto_geral,0)/100.0)
            END),0),2)
    FROM pedido p
    LEFT JOIN pedido_item pi ON pi.pedido_id=p.pedido_id
        AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO','CANCELADO')
""")
t = time.time() - t0
print(f"Resultado: {cur.fetchone()} — tempo: {t:.2f}s")

if t < 1.0:
    print("\n✅ Query rápida! Dashboard pode ser reabilitado.")
else:
    print(f"\n⚠️ Ainda lento ({t:.2f}s). Pode precisar de ANALYZE.")
    cur.execute("ANALYZE pedido")
    cur.execute("ANALYZE pedido_item")
    conn.commit()
    print("ANALYZE executado — tente rodar novamente.")

cur.close()
conn.close()
