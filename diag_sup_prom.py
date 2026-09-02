from dotenv import load_dotenv; load_dotenv()
import sys; sys.path.insert(0,'.')
from database import query

print("=== Supervisores ===")
sups = query("SELECT supervisor_id, nome, usuario_id FROM supervisor WHERE empresa_id=1")
for s in (sups or []):
    print(f"  supervisor_id={s[0]} nome={s[1]} usuario_id={s[2]}")

print("\n=== supervisor_promotor ===")
sp = query("SELECT * FROM supervisor_promotor ORDER BY supervisor_promotor_id")
for r in (sp or []):
    print(f"  {r}")

print("\n=== Promotores ===")
proms = query("SELECT promotor_id, nome, usuario_id FROM promotor WHERE empresa_id=1")
for p in (proms or []):
    print(f"  promotor_id={p[0]} nome={p[1]} usuario_id={p[2]}")
