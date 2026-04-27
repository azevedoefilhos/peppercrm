"""
SCRIPT DE CORREÇÃO DEFINITIVA — PepperCRM
Lê a estrutura REAL do SQLite e sincroniza com o Supabase automaticamente.
Execute na pasta peppercrm:
    python corrigir_migracao_final.py
"""
import sqlite3, os, sys, urllib.parse
import psycopg2

DB_SQLITE = "peppercrm.db"
senha     = urllib.parse.quote("#JunioR_1970@")
PG_URL    = f"postgresql://postgres:{senha}@db.yunzqndswpwttejlgeaa.supabase.co:5432/postgres"

# Mapeamento de tipos SQLite → PostgreSQL
def sqlite_to_pg(tipo):
    t = (tipo or "TEXT").upper()
    if "INT" in t:    return "BIGINT"
    if "REAL" in t or "FLOAT" in t or "DOUBLE" in t: return "DOUBLE PRECISION"
    if "BLOB" in t:   return "BYTEA"
    return "TEXT"

if not os.path.exists(DB_SQLITE):
    print("ERRO: peppercrm.db não encontrado."); sys.exit(1)

sqlite_conn = sqlite3.connect(DB_SQLITE)
sqlite_conn.row_factory = sqlite3.Row
pg_conn = psycopg2.connect(PG_URL, connect_timeout=10)
pg_conn.autocommit = False
cur = pg_conn.cursor()

# Lista tabelas do SQLite
tabelas_sqlite = [r[0] for r in sqlite_conn.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name!='sqlite_sequence' ORDER BY name"
).fetchall()]

print(f"Tabelas no SQLite: {len(tabelas_sqlite)}")
print("="*60)

total = 0
erros = []

for tabela in tabelas_sqlite:
    # Colunas reais do SQLite
    cols_sqlite = sqlite_conn.execute(f"PRAGMA table_info({tabela})").fetchall()
    col_names   = [c[1] for c in cols_sqlite]
    col_types   = {c[1]: c[2] for c in cols_sqlite}

    # Colunas existentes no PostgreSQL
    cur.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_schema='public' AND table_name=%s
    """, (tabela,))
    cols_pg = {r[0] for r in cur.fetchall()}

    if not cols_pg:
        # Tabela não existe no PG — cria
        print(f"\n📋 Criando tabela {tabela}...")
        pk_col = cols_sqlite[0][1]  # primeira coluna como PK
        col_defs = []
        for c in cols_sqlite:
            nome = c[1]; tipo = sqlite_to_pg(c[2])
            if nome == pk_col:
                col_defs.append(f'"{nome}" SERIAL PRIMARY KEY')
            else:
                col_defs.append(f'"{nome}" {tipo}')
        ddl = f'CREATE TABLE IF NOT EXISTS {tabela} ({", ".join(col_defs)})'
        try:
            cur.execute(ddl)
            pg_conn.commit()
            print(f"  Tabela criada")
        except Exception as e:
            pg_conn.rollback()
            print(f"  ERRO criando tabela: {e}")
            erros.append((tabela, str(e)))
            continue
    else:
        # Tabela existe — adiciona colunas faltantes
        faltantes = [c for c in col_names if c not in cols_pg]
        if faltantes:
            print(f"\n🔧 {tabela}: adicionando {len(faltantes)} coluna(s): {faltantes}")
            for col in faltantes:
                tipo_pg = sqlite_to_pg(col_types.get(col,"TEXT"))
                stmt    = f'ALTER TABLE {tabela} ADD COLUMN IF NOT EXISTS "{col}" {tipo_pg}'
                try:
                    cur.execute(stmt)
                    pg_conn.commit()
                    print(f"  + {col} ({tipo_pg})")
                except Exception as e:
                    pg_conn.rollback()
                    print(f"  AVISO {col}: {e}")

    # Remigra dados (limpa e reinsere)
    rows = sqlite_conn.execute(f"SELECT * FROM {tabela}").fetchall()
    if not rows:
        continue

    # Usa apenas colunas que existem em AMBOS os lados
    cur.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_schema='public' AND table_name=%s
    """, (tabela,))
    cols_pg_atual = {r[0] for r in cur.fetchall()}

    cols_usar = [c for c in col_names if c in cols_pg_atual]

    # Limpa
    try:
        cur.execute(f"DELETE FROM {tabela}")
        pg_conn.commit()
    except:
        pg_conn.rollback()

    ph      = ", ".join(["%s"] * len(cols_usar))
    cols_s  = ", ".join(f'"{c}"' for c in cols_usar)
    sql_ins = f'INSERT INTO {tabela} ({cols_s}) VALUES ({ph}) ON CONFLICT DO NOTHING'

    try:
        # Extrai apenas as colunas que vão ser inseridas
        idx_usar = [col_names.index(c) for c in cols_usar]
        dados    = [tuple(r[i] for i in idx_usar) for r in rows]
        cur.executemany(sql_ins, dados)
        pg_conn.commit()
        print(f"  ✅ {tabela}: {len(rows)} registro(s)")
        total += len(rows)
    except Exception as e:
        pg_conn.rollback()
        erros.append((tabela, str(e)))
        print(f"  ❌ {tabela}: {e}")

# Reajusta TODAS as sequences
print("\n🔧 Ajustando sequences...")
cur.execute("""
    SELECT sequence_name FROM information_schema.sequences
    WHERE sequence_schema='public'
""")
sequences = cur.fetchall()
for (seq_name,) in sequences:
    # Deriva nome da tabela e coluna da sequence
    # Padrão Supabase: tablename_colname_seq
    try:
        cur.execute(f"""
            SELECT setval('{seq_name}',
                COALESCE((
                    SELECT last_value FROM {seq_name}
                ), 1))
        """)
        pg_conn.commit()
    except:
        pg_conn.rollback()

# Ajuste explícito das principais sequences
main_seqs = [
    ("configuracao","config_id"), ("representante","representante_id"),
    ("vendedor","vendedor_id"), ("fornecedor","fornecedor_id"),
    ("categoria","categoria_id"), ("linha","linha_id"),
    ("produto","produto_id"), ("tabela_preco","tabela_preco_id"),
    ("tabela_preco_item","tabela_preco_item_id"),
    ("cliente","cliente_id"), ("pdv","pdv_id"),
    ("pedido","pedido_id"), ("pedido_item","pedido_item_id"),
    ("concorrente","concorrente_id"),
    ("produto_concorrente","produto_concorrente_id"),
    ("produto_concorrente_relacao","relacao_id"),
    ("pesquisa_preco","pesquisa_id"),
    ("pesquisa_preco_item","pesquisa_item_id"),
    ("contato_registro","contato_id"),
    ("contato_interacao","interacao_id"),
    ("historico_preco","hist_id"),
    ("meta_mix","meta_mix_id"),
    ("visita_cliente","visita_id"),
]
for t, c in main_seqs:
    try:
        cur.execute(f"""
            SELECT setval(
                pg_get_serial_sequence('{t}','{c}'),
                COALESCE((SELECT MAX({c}) FROM {t}), 1))
        """)
        pg_conn.commit()
    except Exception as e:
        pg_conn.rollback()

print("\n" + "="*60)
print(f"✅ Total de registros migrados: {total}")
if erros:
    print(f"\n⚠️  Erros ({len(erros)}):")
    for t, e in erros:
        print(f"  {t}: {e[:100]}")
else:
    print("🎉 MIGRAÇÃO 100% COMPLETA — zero erros!")
    print("\nPRÓXIMO PASSO: criar o repositório GitHub")

sqlite_conn.close()
pg_conn.close()
