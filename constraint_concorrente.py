#!/usr/bin/env python3
"""Adiciona constraint UNIQUE em concorrente(fornecedor_id, marca_concorrente)."""
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

try:
    cur.execute("""
        ALTER TABLE concorrente
        ADD CONSTRAINT concorrente_forn_marca_unique
        UNIQUE (fornecedor_id, marca_concorrente)
    """)
    conn.commit()
    print("✅ Constraint UNIQUE(fornecedor_id, marca_concorrente) criada em concorrente")
except Exception as e:
    conn.rollback()
    print(f"⚠️  {e}")

conn.close()
