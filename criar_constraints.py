#!/usr/bin/env python3
"""Cria constraints UNIQUE necessarias para ON CONFLICT funcionar no PostgreSQL."""
import os, psycopg2

senha = input("Senha Supabase: ")
conn = psycopg2.connect(
    host="aws-1-sa-east-1.pooler.supabase.com",
    port=5432, dbname="postgres",
    user="postgres.yunzqndswpwttejlgeaa",
    password=senha, sslmode="require", connect_timeout=15,
)
cur = conn.cursor()

constraints = [
    # tabela, nome_constraint, colunas
    ("comissao", "comissao_fornecedor_id_key", "fornecedor_id"),
    ("cliente_fornecedor", "cliente_fornecedor_unique", "cliente_id, fornecedor_id"),
    ("produto_concorrente_relacao", "prod_conc_rel_unique", "produto_id, produto_concorrente_id"),
    ("contato_x_fornecedor", "contato_x_forn_unique", "contato_id, fornecedor_id"),
    ("mix_cliente", "mix_cliente_unique", "cliente_id, produto_id, fornecedor_id"),
]

for tabela, nome, colunas in constraints:
    try:
        cur.execute(f"""
            ALTER TABLE {tabela}
            ADD CONSTRAINT {nome} UNIQUE ({colunas})
        """)
        conn.commit()
        print(f"✅ {tabela}: constraint UNIQUE({colunas}) criada")
    except psycopg2.errors.DuplicateTable:
        conn.rollback()
        print(f"ℹ️  {tabela}: constraint já existe")
    except Exception as e:
        conn.rollback()
        print(f"⚠️  {tabela}: {e}")

conn.close()
print("Pronto!")
