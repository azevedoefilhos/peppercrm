#!/usr/bin/env python3
"""
Corrige sequences PostgreSQL que ficaram dessincronizadas apos migracao do SQLite.
Executa: SELECT setval('tabela_coluna_seq', MAX(coluna)) para cada tabela com PK serial.
"""
import os, psycopg2

os.environ.setdefault("SUPABASE_DB_PASSWORD", input("Senha Supabase: "))

conn = psycopg2.connect(
    host="aws-1-sa-east-1.pooler.supabase.com",
    port=5432,
    dbname="postgres",
    user="postgres.yunzqndswpwttejlgeaa",
    password=os.environ["SUPABASE_DB_PASSWORD"],
    sslmode="require",
    connect_timeout=15,
)

# Tabelas e suas PKs que podem ter sequences dessincronizadas
tabelas = [
    ("pedido_historico", "historico_id"),
    ("pedido", "pedido_id"),
    ("pedido_item", "pedido_item_id"),
    ("cliente", "cliente_id"),
    ("fornecedor", "fornecedor_id"),
    ("produto", "produto_id"),
    ("pesquisa_preco", "pesquisa_id"),
    ("pesquisa_preco_item", "item_id"),
    ("contato_registro", "contato_id"),
    ("contato_interacao", "interacao_id"),
    ("comissao_pagamento", "pagamento_id"),
    ("concorrente", "concorrente_id"),
    ("produto_concorrente", "produto_concorrente_id"),
    ("tabela_preco", "tabela_preco_id"),
    ("tabela_preco_item", "tabela_preco_item_id"),
    ("mix_cliente", "mix_id"),
    ("pdv", "pdv_id"),
    ("representante", "representante_id"),
    ("vendedor", "vendedor_id"),
    ("categoria", "categoria_id"),
    ("configuracao", "config_id"),
]

cur = conn.cursor()
for tabela, pk in tabelas:
    try:
        # Verifica se a tabela existe
        cur.execute(f"SELECT MAX({pk}) FROM {tabela}")
        max_id = cur.fetchone()[0]
        if max_id is None:
            print(f"  {tabela}: vazia, ignorando")
            continue
        # Reseta a sequence
        cur.execute(f"SELECT setval(pg_get_serial_sequence('{tabela}', '{pk}'), {max_id})")
        novo = cur.fetchone()[0]
        print(f"✅ {tabela}.{pk}: sequence resetada para {novo}")
    except Exception as e:
        conn.rollback()
        print(f"⚠️  {tabela}.{pk}: {e}")

conn.commit()
conn.close()
print("\nPronto! Sequences corrigidas.")
