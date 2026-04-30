"""
SCRIPT DE CORREÇÃO DA MIGRAÇÃO — PepperCRM
Execute na pasta peppercrm APÓS o migrar_para_supabase.py:
    python corrigir_migracao.py
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

print("Corrigindo colunas faltantes no Supabase...")

# Adiciona colunas que faltaram no DDL original
ALTER_STMTS = [
    # produto
    "ALTER TABLE produto ADD COLUMN IF NOT EXISTS shelf_life_resfriado INTEGER",
    "ALTER TABLE produto ADD COLUMN IF NOT EXISTS shelf_life_congelado  INTEGER",
    # tabela_preco_item
    "ALTER TABLE tabela_preco_item ADD COLUMN IF NOT EXISTS peso_unidade REAL",
    # pedido
    "ALTER TABLE pedido ADD COLUMN IF NOT EXISTS data_entrega_realizada TEXT",
    # visita_cliente
    "ALTER TABLE visita_cliente ADD COLUMN IF NOT EXISTS pesquisa_preco_id INTEGER",
    # produto_concorrente
    "ALTER TABLE produto_concorrente ADD COLUMN IF NOT EXISTS unidades_caixa INTEGER",
    # pesquisa_preco
    "ALTER TABLE pesquisa_preco ADD COLUMN IF NOT EXISTS foto_path TEXT",
    # pesquisa_preco_item
    "ALTER TABLE pesquisa_preco_item ADD COLUMN IF NOT EXISTS preco_proprio REAL",
    # pesquisa_foto
    "ALTER TABLE pesquisa_foto ADD COLUMN IF NOT EXISTS foto_path TEXT",
    # contato_interacao
    "ALTER TABLE contato_interacao ADD COLUMN IF NOT EXISTS contato_cliente_id INTEGER",
    # contato_x_fornecedor — a PK estava com nome diferente
    "ALTER TABLE contato_x_fornecedor ADD COLUMN IF NOT EXISTS cxf_id INTEGER",
]

for stmt in ALTER_STMTS:
    try:
        cur.execute(stmt)
        pg_conn.commit()
        print(f"  OK: {stmt[:60]}...")
    except Exception as e:
        pg_conn.rollback()
        print(f"  AVISO: {e}")

# Remigra as tabelas que falharam
TABELAS_ERRO = [
    "produto","tabela_preco_item","pedido","visita_cliente",
    "produto_concorrente","pesquisa_preco","pesquisa_preco_item",
    "pesquisa_foto","contato_interacao","contato_x_fornecedor",
]

print("\nRemigrando tabelas com erro...")
total = 0
erros = []
for tabela in TABELAS_ERRO:
    existe = sqlite_conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (tabela,)).fetchone()
    if not existe:
        print(f"  SKIP {tabela}: não existe no SQLite"); continue

    rows = sqlite_conn.execute(f"SELECT * FROM {tabela}").fetchall()
    if not rows:
        print(f"  VAZIO {tabela}"); continue

    cols = [d[0] for d in sqlite_conn.execute(
        f"SELECT * FROM {tabela} LIMIT 0").description]
    
    placeholders = ", ".join(["%s"] * len(cols))
    cols_str     = ", ".join(f'"{c}"' for c in cols)
    
    # Limpa dados existentes para evitar duplicatas
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

# Reajusta sequences
print("\nAjustando sequences...")
seq = {
    "produto":"produto_id","tabela_preco_item":"tabela_preco_item_id",
    "pedido":"pedido_id","visita_cliente":"visita_id",
    "produto_concorrente":"produto_concorrente_id",
    "pesquisa_preco":"pesquisa_id","pesquisa_preco_item":"pesquisa_item_id",
    "pesquisa_foto":"foto_id","contato_interacao":"interacao_id",
}
for t, c in seq.items():
    try:
        cur.execute(
            f"SELECT setval(pg_get_serial_sequence('{t}','{c}'),"
            f"COALESCE((SELECT MAX({c}) FROM {t}),1))")
        pg_conn.commit()
    except Exception as e:
        pg_conn.rollback()
        print(f"  Aviso seq {t}: {e}")

print(f"\n=== CORREÇÃO CONCLUÍDA ===")
print(f"Registros adicionais migrados: {total}")
if erros:
    print(f"Erros restantes ({len(erros)}):")
    for t,e in erros: print(f"  {t}: {e}")
else:
    print("Sem erros! Migração completa.")

sqlite_conn.close()
pg_conn.close()
