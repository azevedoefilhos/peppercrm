# d1b_etapa5_equipe.py — Prepara banco para modulo Equipe
from dotenv import load_dotenv; load_dotenv()
import sys; sys.path.insert(0, '.')
from database import _pg_connect

conn = _pg_connect()
conn.autocommit = False
cur = conn.cursor()

try:
    print("=== D1b Etapa 5 — Equipe ===\n")

    # 1. usuario_id em vendedor
    print("1. Adicionando usuario_id em vendedor...")
    cur.execute("""SELECT COUNT(*) FROM information_schema.columns
        WHERE table_name='vendedor' AND column_name='usuario_id'""")
    if cur.fetchone()[0] == 0:
        cur.execute("ALTER TABLE vendedor ADD COLUMN usuario_id INTEGER DEFAULT NULL")
        print("   OK")
    else:
        print("   -- ja existe")

    # 2. Vincular Fernando (vendedor) ao Fernando (usuario) pelo nome
    print("2. Vinculando vendedor Fernando ao usuario Fernando...")
    cur.execute("""SELECT v.vendedor_id, v.nome FROM vendedor v
        WHERE v.usuario_id IS NULL ORDER BY v.vendedor_id""")
    vends = cur.fetchall()
    for v in vends:
        vid, vnome = v
        # Busca usuario com nome parecido
        cur.execute("""SELECT usuario_id, nome FROM usuario
            WHERE LOWER(nome) LIKE LOWER(%s) AND ativo=1 LIMIT 1""",
            (f"%{vnome.split()[0]}%",))
        u = cur.fetchone()
        if u:
            cur.execute("UPDATE vendedor SET usuario_id=%s WHERE vendedor_id=%s",
                        (u[0], vid))
            print(f"   OK: vendedor '{vnome}' -> usuario '{u[1]}' (id={u[0]})")
        else:
            print(f"   -- vendedor '{vnome}': nenhum usuario encontrado")

    # 3. Adicionar whatsapp em vendedor se nao existir
    print("3. Verificando whatsapp em vendedor...")
    cur.execute("""SELECT COUNT(*) FROM information_schema.columns
        WHERE table_name='vendedor' AND column_name='whatsapp'""")
    if cur.fetchone()[0] == 0:
        cur.execute("ALTER TABLE vendedor ADD COLUMN whatsapp TEXT DEFAULT NULL")
        print("   OK")
    else:
        print("   -- ja existe")

    # 4. Atualizar modo_operacao na configuracao para novos valores
    print("4. Verificando modo_operacao em configuracao...")
    cur.execute("SELECT modo_operacao FROM configuracao LIMIT 1")
    row = cur.fetchone()
    if row and row[0] == 'REPRESENTANTE':
        cur.execute("UPDATE configuracao SET modo_operacao='REPRESENTACAO'")
        print("   OK: REPRESENTANTE -> REPRESENTACAO")
    else:
        print("   -- sem alteracao necessaria")

    conn.commit()
    print("\nD1b Etapa 5 concluida!")

except Exception as e:
    conn.rollback()
    print(f"\nERRO: {e}")
    raise
finally:
    cur.close()
    conn.close()
