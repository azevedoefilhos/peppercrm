#!/usr/bin/env python3
import os, psycopg2

os.environ.setdefault("SUPABASE_DB_PASSWORD", input("Senha Supabase: "))

conn = psycopg2.connect(
    host="aws-1-sa-east-1.pooler.supabase.com",
    port=5432, dbname="postgres",
    user="postgres.yunzqndswpwttejlgeaa",
    password=os.environ["SUPABASE_DB_PASSWORD"],
    sslmode="require", connect_timeout=15,
)
cur = conn.cursor()

# Deleta as duplicatas inativas sem produtos nem pesquisas
ids_deletar = [75, 76, 79]
cur.execute("DELETE FROM concorrente WHERE concorrente_id = ANY(%s)", (ids_deletar,))
print(f"✅ {cur.rowcount} marca(s) duplicada(s) deletada(s): IDs {ids_deletar}")

# Agora cria o indice unico
cur.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS concorrente_forn_marca_unique
    ON concorrente (fornecedor_id, marca_concorrente)
    WHERE ativo = 1
""")
print("✅ Índice UNIQUE criado — novas duplicatas ativas serão impedidas")

conn.commit()
conn.close()
print("Pronto!")
