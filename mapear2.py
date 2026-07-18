from dotenv import load_dotenv; load_dotenv()
import sys; sys.path.insert(0, '.')
from database import query

# Vendedor
cols = query("SELECT column_name FROM information_schema.columns WHERE table_name='vendedor' ORDER BY ordinal_position")
print("VENDEDOR colunas:", [c[0] for c in (cols or [])])
vends = query("SELECT vendedor_id, nome, email, fone FROM vendedor")
print("VENDEDOR registros:", vends)

# Vinculos
for tab in ['pedido','comissao','att_vendedor','cliente']:
    cnt = query(f"SELECT COUNT(*) FROM {tab} WHERE vendedor_id IS NOT NULL")
    print(f"{tab}.vendedor_id nao nulo:", cnt[0][0] if cnt else 0)

# Usuarios comerciais
usu = query("SELECT usuario_id, nome, tipo FROM usuario WHERE tipo NOT IN ('MASTER') ORDER BY tipo, nome")
print("USUARIOS:", usu)

# Promotores
proms = query("SELECT promotor_id, nome, usuario_id FROM promotor WHERE nome!='Sem promotor'")
print("PROMOTORES:", proms)

# Supervisores
sups = query("SELECT supervisor_id, nome, usuario_id FROM supervisor")
print("SUPERVISORES:", sups)

# Configuracao
cols2 = query("SELECT column_name FROM information_schema.columns WHERE table_name='configuracao' ORDER BY ordinal_position")
print("CONFIGURACAO colunas:", [c[0] for c in (cols2 or [])])
