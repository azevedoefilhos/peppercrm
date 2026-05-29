"""
Sincroniza TODAS as tabelas do Supabase para Railway
Usa INSERT ... ON CONFLICT DO UPDATE para não perder dados existentes
"""
import psycopg2

src = psycopg2.connect(
    host="aws-1-sa-east-1.pooler.supabase.com",
    port=5432,
    dbname="postgres",
    user="postgres.yunzqndswpwttejlgeaa",
    password="#JunioR_1970@",
    sslmode="require"
)

dst = psycopg2.connect(
    "postgresql://postgres:hCjlbzeKMkHIcifEnAMtlcHlONfrCdQx@kodama.proxy.rlwy.net:49266/railway"
)

src_cur = src.cursor()
dst_cur = dst.cursor()

# Tabelas para sincronizar com suas PKs
TABELAS = [
    ("cliente",                "cliente_id"),
    ("pdv",                    "pdv_id"),
    ("contato_cliente",        "contato_cliente_id"),
    ("mix_cliente",            "mix_id"),
    ("pesquisa_preco",         "pesquisa_id"),
    ("pesquisa_preco_item",    "pesquisa_item_id"),
    ("pesquisa_foto",          "foto_id"),
    ("contato_registro",       "contato_id"),
    ("contato_interacao",      "interacao_id"),
    ("contato_x_fornecedor",   "cxf_id"),
    ("visita_cliente",         "visita_id"),
    ("pedido",                 "pedido_id"),
    ("pedido_item",            "pedido_item_id"),
    ("historico_preco",        "historico_id"),
    ("despesa",                "despesa_id"),
]

for tabela, pk in TABELAS:
    try:
        # Busca todos do Supabase
        src_cur.execute(f"SELECT * FROM {tabela} ORDER BY {pk}")
        rows = src_cur.fetchall()
        if not rows:
            print(f"⚪ {tabela}: vazio")
            continue

        cols = [d[0] for d in src_cur.description]
        col_names = ",".join(cols)
        placeholders = ",".join(["%s"] * len(cols))
        update_cols = ",".join([f"{c}=EXCLUDED.{c}" for c in cols if c != pk])

        count_new = 0
        for row in rows:
            dst_cur.execute(
                f"""INSERT INTO {tabela} ({col_names})
                    VALUES ({placeholders})
                    ON CONFLICT ({pk}) DO UPDATE SET {update_cols}""",
                row
            )
            if dst_cur.rowcount > 0:
                count_new += 1

        dst.commit()
        print(f"✅ {tabela}: {len(rows)} registros sincronizados ({count_new} atualizados)")

    except Exception as e:
        dst.rollback()
        print(f"❌ {tabela}: {e}")

# Atualiza sequências
print("\nAtualizando sequências...")
seq_map = {
    "cliente": "cliente_cliente_id_seq",
    "pdv": "pdv_pdv_id_seq",
    "pesquisa_preco": "pesquisa_preco_pesquisa_id_seq",
    "pesquisa_preco_item": "pesquisa_preco_item_pesquisa_item_id_seq",
    "despesa": "despesa_despesa_id_seq",
}
for tabela, seq in seq_map.items():
    try:
        dst_cur.execute(f"SELECT setval('{seq}', COALESCE((SELECT MAX({list(filter(lambda x: 'id' in x, [c for r in [dst_cur.execute(f\"SELECT column_name FROM information_schema.columns WHERE table_name=%(t)s AND column_name LIKE %(p)s\", {\"t\":tabela,\"p\":\"%%id%%\"}) or [] for r in [dst_cur.fetchall()]])][0][:1]}), 1)))")
    except:
        pass

# Forma mais simples para sequências
for tabela, pk in TABELAS[:5]:
    try:
        seq = f"{tabela}_{pk}_seq"
        dst_cur.execute(f"SELECT setval('{seq}', COALESCE((SELECT MAX({pk}) FROM {tabela}), 1))")
        dst.commit()
    except:
        dst.rollback()

src.close()
dst.close()
print("\n✅ Sincronização completa!")
