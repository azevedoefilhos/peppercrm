# d1b_etapa4_supervisor.py
# Cria tabela supervisor e ajusta supervisor_promotor e supervisor_pdv
from dotenv import load_dotenv; load_dotenv()
import sys; sys.path.insert(0, '.')
from database import _pg_connect

conn = _pg_connect()
conn.autocommit = False
cur = conn.cursor()

try:
    print("=== D1b Etapa 4 — Tabela Supervisor ===\n")

    # 1. Criar tabela supervisor
    print("1. Criando tabela supervisor...")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS supervisor (
            supervisor_id  SERIAL PRIMARY KEY,
            nome           TEXT NOT NULL,
            fone           TEXT,
            whatsapp       TEXT,
            email          TEXT,
            cpf            TEXT,
            cidade         TEXT,
            estado         TEXT,
            bairro         TEXT,
            endereco       TEXT,
            observacao     TEXT,
            usuario_id     INTEGER DEFAULT NULL,
            empresa_id     INTEGER DEFAULT 1,
            ativo          INTEGER DEFAULT 1
        )
    """)
    print("   OK")

    # 2. Ajustar supervisor_promotor para usar supervisor.supervisor_id
    print("2. Verificando supervisor_promotor...")
    cur.execute("""
        SELECT COUNT(*) FROM information_schema.columns
        WHERE table_name='supervisor_promotor' AND column_name='supervisor_id'
    """)
    print("   OK — supervisor_id ja existe")

    # 3. Ajustar supervisor_pdv
    print("3. Verificando supervisor_pdv...")
    cur.execute("""
        SELECT COUNT(*) FROM information_schema.tables
        WHERE table_name='supervisor_pdv'
    """)
    if cur.fetchone()[0] == 0:
        cur.execute("""
            CREATE TABLE supervisor_pdv (
                id            SERIAL PRIMARY KEY,
                supervisor_id INTEGER NOT NULL,
                pdv_id        INTEGER NOT NULL,
                empresa_id    INTEGER NOT NULL DEFAULT 1,
                ativo         INTEGER DEFAULT 1,
                UNIQUE(supervisor_id, pdv_id, empresa_id)
            )
        """)
        print("   OK — criada")
    else:
        print("   -- ja existe")

    # 4. usuario_id em supervisor
    print("4. Verificando usuario_id em supervisor...")
    cur.execute("""
        SELECT COUNT(*) FROM information_schema.columns
        WHERE table_name='supervisor' AND column_name='usuario_id'
    """)
    if cur.fetchone()[0] == 0:
        cur.execute("ALTER TABLE supervisor ADD COLUMN usuario_id INTEGER DEFAULT NULL")
        print("   OK")
    else:
        print("   -- ja existe")

    # 5. RLS na nova tabela
    print("5. Ativando RLS em supervisor...")
    cur.execute("ALTER TABLE supervisor ENABLE ROW LEVEL SECURITY")
    cur.execute("DROP POLICY IF EXISTS empresa_isolation ON supervisor")
    cur.execute("""
        CREATE POLICY empresa_isolation ON supervisor
        USING (empresa_id = COALESCE(current_setting('app.empresa_id',true)::integer,1))
        WITH CHECK (empresa_id = COALESCE(current_setting('app.empresa_id',true)::integer,1))
    """)
    print("   OK")

    # 6. Indices
    print("6. Criando indices...")
    for nome, tab, col in [
        ("idx_supervisor_usuario", "supervisor", "usuario_id"),
        ("idx_supervisor_empresa", "supervisor", "empresa_id"),
        ("idx_sup_prom_sup2",      "supervisor_promotor", "supervisor_id"),
        ("idx_sup_pdv_sup2",       "supervisor_pdv", "supervisor_id"),
    ]:
        try:
            cur.execute(f"CREATE INDEX IF NOT EXISTS {nome} ON {tab}({col})")
            print(f"   OK {nome}")
        except Exception as e:
            print(f"   -- {nome}: {e}")

    conn.commit()
    print("\nD1b Etapa 4 concluida!")

except Exception as e:
    conn.rollback()
    print(f"\nERRO: {e}")
    raise
finally:
    cur.close()
    conn.close()
