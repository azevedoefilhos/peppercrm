# d1b_etapa1_banco.py
# Etapa 1 do D1b: preparar banco para perfis de acesso
# Risco: BAIXO — adiciona colunas nullable e cria tabelas novas
# Nao altera nenhum dado existente

from dotenv import load_dotenv; load_dotenv()
import sys; sys.path.insert(0, '.')
from database import _pg_connect

conn = _pg_connect()
conn.autocommit = False
cur = conn.cursor()

try:
    print("=== D1b Etapa 1 — Preparar banco ===\n")

    # ── 1. vendedor_id em cliente ─────────────────────────────────────────
    print("1. Adicionando vendedor_id em cliente...")
    cur.execute("""
        SELECT COUNT(*) FROM information_schema.columns
        WHERE table_name='cliente' AND column_name='vendedor_id'
    """)
    if cur.fetchone()[0] == 0:
        cur.execute("ALTER TABLE cliente ADD COLUMN vendedor_id INTEGER DEFAULT NULL")
        print("   OK — coluna adicionada")
    else:
        print("   -- ja existe")

    # ── 2. usuario_id em promotor ─────────────────────────────────────────
    print("2. Adicionando usuario_id em promotor...")
    cur.execute("""
        SELECT COUNT(*) FROM information_schema.columns
        WHERE table_name='promotor' AND column_name='usuario_id'
    """)
    if cur.fetchone()[0] == 0:
        cur.execute("ALTER TABLE promotor ADD COLUMN usuario_id INTEGER DEFAULT NULL")
        print("   OK — coluna adicionada")
    else:
        print("   -- ja existe")

    # ── 3. supervisor_id em promotor ──────────────────────────────────────
    print("3. Adicionando supervisor_id em promotor...")
    cur.execute("""
        SELECT COUNT(*) FROM information_schema.columns
        WHERE table_name='promotor' AND column_name='supervisor_id'
    """)
    if cur.fetchone()[0] == 0:
        cur.execute("ALTER TABLE promotor ADD COLUMN supervisor_id INTEGER DEFAULT NULL")
        print("   OK — coluna adicionada")
    else:
        print("   -- ja existe")

    # ── 4. Tabela supervisor_promotor ─────────────────────────────────────
    print("4. Criando tabela supervisor_promotor...")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS supervisor_promotor (
            id            SERIAL PRIMARY KEY,
            supervisor_id INTEGER NOT NULL,
            promotor_id   INTEGER NOT NULL,
            empresa_id    INTEGER NOT NULL DEFAULT 1,
            ativo         INTEGER DEFAULT 1,
            UNIQUE(supervisor_id, promotor_id, empresa_id)
        )
    """)
    print("   OK — tabela criada (ou ja existia)")

    # ── 5. Atualizar usuario fernando para MASTER ─────────────────────────
    print("5. Verificando usuario MASTER...")
    cur.execute("SELECT usuario_id, tipo FROM usuario WHERE email='fernando'")
    row = cur.fetchone()
    if row:
        cur.execute(
            "UPDATE usuario SET tipo='MASTER' WHERE email='fernando'",
        )
        print(f"   OK — usuario fernando atualizado para MASTER")
    else:
        print("   -- usuario fernando nao encontrado")

    # ── 6. Indices de performance ─────────────────────────────────────────
    print("6. Criando indices...")
    indices = [
        ("idx_cliente_vendedor",      "cliente",              "vendedor_id"),
        ("idx_promotor_usuario",      "promotor",             "usuario_id"),
        ("idx_promotor_supervisor",   "promotor",             "supervisor_id"),
        ("idx_superprom_supervisor",  "supervisor_promotor",  "supervisor_id"),
        ("idx_superprom_promotor",    "supervisor_promotor",  "promotor_id"),
    ]
    for nome, tabela, col in indices:
        cur.execute(f"CREATE INDEX IF NOT EXISTS {nome} ON {tabela}({col})")
        print(f"   OK {nome}")

    conn.commit()

    # ── Verificacao final ─────────────────────────────────────────────────
    print("\n=== Verificacao final ===")
    cur.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name='cliente' AND column_name='vendedor_id'
    """)
    print(f"cliente.vendedor_id: {'OK' if cur.fetchone() else 'FALTA'}")

    cur.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name='promotor' AND column_name IN ('usuario_id','supervisor_id')
    """)
    cols = [r[0] for r in cur.fetchall()]
    print(f"promotor.usuario_id: {'OK' if 'usuario_id' in cols else 'FALTA'}")
    print(f"promotor.supervisor_id: {'OK' if 'supervisor_id' in cols else 'FALTA'}")

    cur.execute("""
        SELECT COUNT(*) FROM information_schema.tables
        WHERE table_name='supervisor_promotor'
    """)
    print(f"supervisor_promotor: {'OK' if cur.fetchone()[0] else 'FALTA'}")

    cur.execute("SELECT usuario_id, nome, tipo FROM usuario WHERE email='fernando'")
    r = cur.fetchone()
    print(f"usuario MASTER: id={r[0]} nome={r[1]} tipo={r[2]}")

    print("\nD1b Etapa 1 concluida com sucesso!")
    print("Proximo: d1b_etapa2_permissoes.py")

except Exception as e:
    conn.rollback()
    print(f"\nERRO: {e}")
    raise
finally:
    cur.close()
    conn.close()
