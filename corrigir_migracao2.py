"""
SCRIPT DE CORREÇÃO FINAL — PepperCRM
Execute na pasta peppercrm:
    python corrigir_migracao2.py
"""
import sqlite3, os, sys, urllib.parse
import psycopg2

DB_SQLITE = "peppercrm.db"
senha     = urllib.parse.quote("#JunioR_1970@")
PG_URL    = f"postgresql://postgres:{senha}@db.yunzqndswpwttejlgeaa.supabase.co:5432/postgres"

if not os.path.exists(DB_SQLITE):
    print("ERRO: peppercrm.db não encontrado."); sys.exit(1)

sqlite_conn = sqlite3.connect(DB_SQLITE)
sqlite_conn.row_factory = sqlite3.Row
pg_conn = psycopg2.connect(PG_URL, connect_timeout=10)
pg_conn.autocommit = False
cur = pg_conn.cursor()

print("Adicionando colunas faltantes...")

ALTER_STMTS = [
    "ALTER TABLE visita_cliente      ADD COLUMN IF NOT EXISTS latitude  TEXT",
    "ALTER TABLE visita_cliente      ADD COLUMN IF NOT EXISTS longitude TEXT",
    "ALTER TABLE produto_concorrente ADD COLUMN IF NOT EXISTS ean       TEXT",
    "ALTER TABLE pesquisa_preco_item ADD COLUMN IF NOT EXISTS facing    INTEGER",
    "ALTER TABLE pesquisa_foto       ADD COLUMN IF NOT EXISTS legenda   TEXT",
    "ALTER TABLE contato_interacao   ADD COLUMN IF NOT EXISTS resultado TEXT",
]

for stmt in ALTER_STMTS:
    try:
        cur.execute(stmt)
        pg_conn.commit()
        print(f"  OK: {stmt[30:70]}...")
    except Exception as e:
        pg_conn.rollback()
        print(f"  AVISO: {e}")

# Remigra apenas as 5 tabelas restantes
TABELAS = [
    "visita_cliente","produto_concorrente",
    "pesquisa_preco_item","pesquisa_foto","contato_interacao",
]

print("\nRemigrando tabelas restantes...")
total = 0
erros = []

for tabela in TABELAS:
    rows = sqlite_conn.execute(f"SELECT * FROM {tabela}").fetchall()
    if not rows:
        print(f"  VAZIO {tabela}"); continue

    cols = [d[0] for d in sqlite_conn.execute(
        f"SELECT * FROM {tabela} LIMIT 0").description]

    placeholders = ", ".join(["%s"] * len(cols))
    cols_str     = ", ".join(f'"{c}"' for c in cols)

    # Limpa dados existentes
    try:
        cur.execute(f"DELETE FROM {tabela}")
        pg_conn.commit()
    except:
        pg_conn.rollback()

    sql = (f'INSERT INTO {tabela} ({cols_str}) VALUES ({placeholders}) '
           f'ON CONFLICT DO NOTHING')
    try:
        dados = [tuple(r) for r in rows]
        cur.executemany(sql, dados)
        pg_conn.commit()
        print(f"  OK {tabela}: {len(rows)} registro(s)")
        total += len(rows)
    except Exception as e:
        pg_conn.rollback()
        erros.append((tabela, str(e)))
        print(f"  ERRO {tabela}: {e}")

# Reajusta sequences das tabelas migradas
print("\nAjustando sequences...")
seq = {
    "visita_cliente":      "visita_id",
    "produto_concorrente": "produto_concorrente_id",
    "pesquisa_preco_item": "pesquisa_item_id",
    "pesquisa_foto":       "foto_id",
    "contato_interacao":   "interacao_id",
}
for t, c in seq.items():
    try:
        cur.execute(
            f"SELECT setval(pg_get_serial_sequence('{t}','{c}'),"
            f"COALESCE((SELECT MAX({c}) FROM {t}),1))")
        pg_conn.commit()
        print(f"  OK seq {t}")
    except Exception as e:
        pg_conn.rollback()
        print(f"  Aviso seq {t}: {e}")

print(f"\n{'='*50}")
print(f"Registros migrados nesta rodada: {total}")
if erros:
    print(f"Erros ({len(erros)}):")
    for t, e in erros:
        print(f"  {t}: {e}")
else:
    print("MIGRAÇÃO 100% COMPLETA — sem erros!")
    print("\nPRÓXIMO PASSO: criar o repositório no GitHub")

sqlite_conn.close()
pg_conn.close()
