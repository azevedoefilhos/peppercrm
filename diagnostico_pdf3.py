# diagnostico_pdf3.py
from dotenv import load_dotenv
load_dotenv()
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database import query

cid = 6

# Fornecedores vinculados ao tópico
print("=== Fornecedores vinculados ao tópico #6 ===")
forns = query("""
    SELECT fn.fornecedor_id, fn.nome_fantasia FROM contato_x_fornecedor cxf
    JOIN fornecedor fn ON cxf.fornecedor_id=fn.fornecedor_id
    WHERE cxf.contato_id=?""", (cid,))
for f in (forns or []):
    print(f"  fornecedor_id={f[0]} nome={f[1]}")

# fornecedor_id das interações
print("\n=== fornecedor_id de cada interação ===")
ints = query("""
    SELECT ci.interacao_id, ci.data_interacao, ci.fornecedor_id, ci.ativo
    FROM contato_interacao ci
    WHERE ci.contato_id=?
    ORDER BY ci.data_interacao ASC""", (cid,))
for r in (ints or []):
    print(f"  interacao_id={r[0]} data={r[1]} fornecedor_id={r[2]} ativo={r[3]}")

# Testa a query com filtro de fornecedor
if forns:
    fid = forns[0][0]
    print(f"\n=== Query com fornecedor_id={fid} (Belmont) ===")
    ints2 = query("""
        SELECT ci.interacao_id, ci.data_interacao, ci.fornecedor_id
        FROM contato_interacao ci
        WHERE ci.contato_id=?
          AND (ci.fornecedor_id=? OR ci.fornecedor_id IS NULL)
        ORDER BY ci.data_interacao ASC""", (cid, fid))
    print(f"  Total com filtro: {len(ints2) if ints2 else 0}")
    for r in (ints2 or []):
        print(f"  id={r[0]} data={r[1]} forn_id={r[2]}")
