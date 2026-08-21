from dotenv import load_dotenv; load_dotenv()
import sys; sys.path.insert(0,'.')
from database import query

print("=== Todos os usuarios ===")
r = query("SELECT usuario_id, nome, email, tipo, ativo FROM usuario ORDER BY tipo, nome")
for u in (r or []):
    print(f"  id={u[0]} nome={u[1]} tipo={u[3]} ativo={u[4]}")

print("\n=== Sessoes ativas ===")
s = query("""SELECT s.usuario_id, u.nome, u.tipo, s.ativo
    FROM sessao_token s JOIN usuario u ON u.usuario_id=s.usuario_id
    WHERE s.ativo=1 ORDER BY s.usuario_id""")
for t in (s or []):
    print(f"  uid={t[0]} nome={t[1]} tipo={t[2]}")
