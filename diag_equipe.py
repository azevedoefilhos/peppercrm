from dotenv import load_dotenv; load_dotenv()
import sys; sys.path.insert(0, '.')
from database import query

print("=== USUARIOS comerciais ===")
usu = query("""SELECT usuario_id, nome, email, tipo, empresa_id, ativo
    FROM usuario ORDER BY tipo, nome""") or []
for u in usu:
    print(f"  id={u[0]} nome={u[1]} tipo={u[3]} empresa_id={u[4]} ativo={u[5]}")

print("\n=== VENDEDORES tabela vendedor ===")
vends = query("SELECT vendedor_id, nome, usuario_id, empresa_id, ativo FROM vendedor") or []
for v in vends:
    print(f"  id={v[0]} nome={v[1]} usuario_id={v[2]} empresa_id={v[3]} ativo={v[4]}")

print("\n=== PROMOTORES ===")
proms = query("SELECT promotor_id, nome, usuario_id, empresa_id FROM promotor WHERE nome!='Sem promotor'") or []
for p in proms:
    print(f"  id={p[0]} nome={p[1]} usuario_id={p[2]} empresa_id={p[3]}")

print("\n=== SUPERVISORES ===")
sups = query("SELECT supervisor_id, nome, usuario_id, empresa_id FROM supervisor") or []
for s in sups:
    print(f"  id={s[0]} nome={s[1]} usuario_id={s[2]} empresa_id={s[3]}")
