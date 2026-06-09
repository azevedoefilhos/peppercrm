# diagnostico_pdf.py
from dotenv import load_dotenv
load_dotenv()
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database import query

# Tópico #6 — Fornecimento Marca Própria Coop Belmont
cid = 6

print(f"=== Tópico {cid} ===")
cr = query("SELECT contato_id, assunto, status FROM contato_registro WHERE contato_id=?", (cid,))
print(f"Tópico: {cr}")

print(f"\n=== Interações brutas (sem filtro ativo) ===")
ints = query("""
    SELECT ci.interacao_id, ci.data_interacao, ci.ativo, ci.descricao
    FROM contato_interacao ci
    WHERE ci.contato_id=?
    ORDER BY ci.data_interacao ASC
""", (cid,))
print(f"Total: {len(ints) if ints else 0}")
for r in (ints or []):
    print(f"  id={r[0]} data={r[1]} ativo={r[2]} desc={str(r[3])[:40]}")

print(f"\n=== Interações com filtro ativo!=0 ===")
ints2 = query("""
    SELECT ci.interacao_id, ci.data_interacao, ci.ativo
    FROM contato_interacao ci
    WHERE ci.contato_id=? AND ci.ativo!=0
    ORDER BY ci.data_interacao ASC
""", (cid,))
print(f"Total: {len(ints2) if ints2 else 0}")

print(f"\n=== Tipo do campo ativo ===")
if ints:
    r = ints[0]
    print(f"  tipo: {type(r[2])} valor: {r[2]!r}")
    print(f"  r[2] not in (0, False): {r[2] not in (0, False)}")
    print(f"  r[2] is False: {r[2] is False}")
    print(f"  r[2] == False: {r[2] == False}")
