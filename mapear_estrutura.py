from dotenv import load_dotenv; load_dotenv()
import sys; sys.path.insert(0, '.')
from database import query

print("=== TABELA VENDEDOR ===")
cols = query("""SELECT column_name FROM information_schema.columns
    WHERE table_name='vendedor' ORDER BY ordinal_position""")
print("Colunas:", [c[0] for c in (cols or [])])
vends = query("SELECT * FROM vendedor") or []
print(f"Registros: {len(vends)}")
for v in vends:
    print(f"  {v[:6]}")

print("\n=== VINCULOS COM VENDEDOR ===")
for tab in ['pedido','comissao','att_vendedor','meta_fornecedor','cliente']:
    r = query(f"""SELECT COUNT(*) FROM information_schema.columns
        WHERE table_name='{tab}' AND column_name='vendedor_id'""")
    tem = r[0][0] > 0 if r else False
    if tem:
        cnt = query(f"SELECT COUNT(*) FROM {tab} WHERE vendedor_id IS NOT NULL")
        print(f"  {tab}.vendedor_id: {cnt[0][0] if cnt else 0} registros vinculados")

print("\n=== TABELA USUARIO (perfis comerciais) ===")
usu = query("""SELECT usuario_id, nome, email, tipo FROM usuario
    WHERE tipo IN ('REPRESENTANTE_ADM','REPRESENTANTE','VENDEDOR',
                   'PROMOTOR_VENDEDOR','SUPERVISOR','PROMOTOR','MASTER')
    ORDER BY tipo, nome""") or []
for u in usu:
    print(f"  id={u[0]} nome={u[1]} tipo={u[3]}")

print("\n=== TABELA PROMOTOR ===")
proms = query("SELECT promotor_id, nome, usuario_id FROM promotor WHERE nome!='Sem promotor'") or []
print(f"Promotores: {len(proms)}")
for p in proms:
    print(f"  id={p[0]} nome={p[1]} usuario_id={p[2]}")

print("\n=== TABELA SUPERVISOR ===")
sups = query("SELECT supervisor_id, nome, usuario_id FROM supervisor") or []
print(f"Supervisores: {len(sups)}")
for s in sups:
    print(f"  id={s[0]} nome={s[1]} usuario_id={s[2]}")

print("\n=== CONFIGURACAO (colunas) ===")
cols2 = query("""SELECT column_name FROM information_schema.columns
    WHERE table_name='configuracao' ORDER BY ordinal_position""")
print("Colunas:", [c[0] for c in (cols2 or [])])

print("\nOK")
