#!/usr/bin/env python3
"""
Deduplicar marcas concorrentes no Supabase.
Migra produtos e pesquisas das duplicatas para a marca principal,
depois desativa as duplicatas.
"""
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

# Definicao das deduplicacoes:
# (manter_id, desativar_ids)
deduplicacoes = [
    # Galla Massas De: manter 77 (tem produto), desativar 76
    (77, [76]),
    # Marca Propria Belmont: manter 19 (mais antigo), migrar 75 e 79
    (19, [75, 79]),
]

for manter_id, desativar_ids in deduplicacoes:
    cur.execute("SELECT marca_concorrente FROM concorrente WHERE concorrente_id=%s", (manter_id,))
    nome = cur.fetchone()[0]
    print(f"\n=== {nome} (mantendo ID {manter_id}) ===")

    for dup_id in desativar_ids:
        print(f"  Migrando ID {dup_id} -> {manter_id}...")

        # 1. Migra produto_concorrente
        cur.execute("""
            UPDATE produto_concorrente
            SET concorrente_id = %s
            WHERE concorrente_id = %s
        """, (manter_id, dup_id))
        print(f"    produto_concorrente: {cur.rowcount} registros migrados")

        # 2. Desativa a marca duplicada
        cur.execute("""
            UPDATE concorrente SET ativo = 0 WHERE concorrente_id = %s
        """, (dup_id,))
        print(f"    concorrente ID {dup_id}: desativado")

conn.commit()

# Verificacao final
print("\n=== Verificacao final ===")
cur.execute("""
    SELECT c.concorrente_id, c.marca_concorrente, c.ativo,
           COUNT(pc.produto_concorrente_id) as produtos
    FROM concorrente c
    LEFT JOIN produto_concorrente pc ON pc.concorrente_id = c.concorrente_id
    WHERE c.marca_concorrente IN ('Galla', 'Marca Própria', 'Marca Pr?pria')
    GROUP BY c.concorrente_id, c.marca_concorrente, c.ativo
    ORDER BY c.marca_concorrente, c.ativo DESC
""")
for row in cur.fetchall():
    status = "ATIVO" if row[2] else "inativo"
    print(f"  ID {row[0]}: {row[1]} ({status}) - {row[3]} produtos")

conn.close()
print("\nPronto!")
