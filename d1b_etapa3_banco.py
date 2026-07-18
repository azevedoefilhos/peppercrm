# d1b_etapa3_banco.py
# Etapa 3 do D1b: estrutura para Promotor Vendedor, Supervisor e tipo de visita
from dotenv import load_dotenv; load_dotenv()
import sys; sys.path.insert(0, '.')
from database import _pg_connect

conn = _pg_connect()
conn.autocommit = False
cur = conn.cursor()

try:
    print("=== D1b Etapa 3 — Banco ===\n")

    # 1. tipo_visita em visita_cliente
    print("1. Adicionando tipo_visita em visita_cliente...")
    cur.execute("""SELECT COUNT(*) FROM information_schema.columns
        WHERE table_name='visita_cliente' AND column_name='tipo_visita'""")
    if cur.fetchone()[0] == 0:
        cur.execute("""ALTER TABLE visita_cliente
            ADD COLUMN tipo_visita TEXT DEFAULT 'promotor'""")
        print("   OK")
    else:
        print("   -- ja existe")

    # 2. promotor_vendedor_id em pdv
    print("2. Adicionando promotor_vendedor_id em pdv...")
    cur.execute("""SELECT COUNT(*) FROM information_schema.columns
        WHERE table_name='pdv' AND column_name='promotor_vendedor_id'""")
    if cur.fetchone()[0] == 0:
        cur.execute("ALTER TABLE pdv ADD COLUMN promotor_vendedor_id INTEGER DEFAULT NULL")
        print("   OK")
    else:
        print("   -- ja existe")

    # 3. supervisor_id em pdv (atribuicao direta supervisor -> pdv)
    print("3. Adicionando supervisor_id em pdv...")
    cur.execute("""SELECT COUNT(*) FROM information_schema.columns
        WHERE table_name='pdv' AND column_name='supervisor_id'""")
    if cur.fetchone()[0] == 0:
        cur.execute("ALTER TABLE pdv ADD COLUMN supervisor_id INTEGER DEFAULT NULL")
        print("   OK")
    else:
        print("   -- ja existe")

    # 4. Tabela supervisor_pdv (atribuicao direta)
    print("4. Criando tabela supervisor_pdv...")
    cur.execute("""CREATE TABLE IF NOT EXISTS supervisor_pdv (
        id            SERIAL PRIMARY KEY,
        supervisor_id INTEGER NOT NULL,
        pdv_id        INTEGER NOT NULL,
        empresa_id    INTEGER NOT NULL DEFAULT 1,
        ativo         INTEGER DEFAULT 1,
        UNIQUE(supervisor_id, pdv_id, empresa_id)
    )""")
    print("   OK")

    # 5. Promotor "Sem promotor" como registro padrao
    print("5. Verificando promotor 'Sem promotor'...")
    cur.execute("""SELECT promotor_id FROM promotor
        WHERE nome='Sem promotor' AND empresa_id=1""")
    row = cur.fetchone()
    if not row:
        cur.execute("""INSERT INTO promotor (nome, ativo, empresa_id)
            VALUES ('Sem promotor', 1, 1) RETURNING promotor_id""")
        pid = cur.fetchone()[0]
        print(f"   OK — criado com promotor_id={pid}")
    else:
        print(f"   -- ja existe (promotor_id={row[0]})")

    # 6. Indices
    print("6. Criando indices...")
    indices = [
        ("idx_pdv_prom_vend", "pdv", "promotor_vendedor_id"),
        ("idx_pdv_supervisor", "pdv", "supervisor_id"),
        ("idx_vis_tipo", "visita_cliente", "tipo_visita"),
        ("idx_sup_pdv_sup", "supervisor_pdv", "supervisor_id"),
        ("idx_sup_pdv_pdv", "supervisor_pdv", "pdv_id"),
    ]
    for nome, tab, col in indices:
        cur.execute(f"CREATE INDEX IF NOT EXISTS {nome} ON {tab}({col})")
        print(f"   OK {nome}")

    conn.commit()
    print("\nD1b Etapa 3 concluida com sucesso!")

except Exception as e:
    conn.rollback()
    print(f"\nERRO: {e}")
    raise
finally:
    cur.close()
    conn.close()
