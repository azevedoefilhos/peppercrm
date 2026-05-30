"""
Sincroniza TODAS as tabelas do Supabase para Railway
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

TABELAS = [
    ("cliente",             "cliente_id"),
    ("pdv",                 "pdv_id"),
    ("contato_cliente",     "contato_cliente_id"),
    ("mix_cliente",         "mix_id"),
    ("pesquisa_preco",      "pesquisa_id"),
    ("pesquisa_preco_item", "pesquisa_item_id"),
    ("pesquisa_foto",       "foto_id"),
    ("contato_registro",    "contato_id"),
    ("contato_interacao",   "interacao_id"),
    ("contato_x_fornecedor","cxf_id"),
    ("visita_cliente",      "visita_id"),
    ("pedido",              "pedido_id"),
    ("pedido_item",         "pedido_item_id"),
    ("historico_preco",     "historico_id"),
]

for tabela, pk in TABELAS:
    try:
        src_cur.execute("SELECT * FROM " + tabela + " ORDER BY " + pk)
        rows = src_cur.fetchall()
        if not rows:
            print("⚪ " + tabela + ": vazio")
            continue

        cols = [d[0] for d in src_cur.description]
        col_names = ",".join(cols)
        placeholders = ",".join(["%s"] * len(cols))
        update_set = ",".join([c + "=EXCLUDED." + c for c in cols if c != pk])

        for row in rows:
            sql = ("INSERT INTO " + tabela + " (" + col_names + ") "
                   "VALUES (" + placeholders + ") "
                   "ON CONFLICT (" + pk + ") DO UPDATE SET " + update_set)
            dst_cur.execute(sql, row)

        dst.commit()
        print("✅ " + tabela + ": " + str(len(rows)) + " registros")

    except Exception as e:
        dst.rollback()
        print("❌ " + tabela + ": " + str(e)[:100])

# Atualiza sequências principais
print("\nAtualizando sequências...")
seqs = [
    ("cliente",             "cliente_id",          "cliente_cliente_id_seq"),
    ("pdv",                 "pdv_id",               "pdv_pdv_id_seq"),
    ("pesquisa_preco",      "pesquisa_id",          "pesquisa_preco_pesquisa_id_seq"),
    ("pesquisa_preco_item", "pesquisa_item_id",     "pesquisa_preco_item_pesquisa_item_id_seq"),
]
for tabela, pk, seq in seqs:
    try:
        dst_cur.execute("SELECT setval(%s, COALESCE((SELECT MAX(" + pk + ") FROM " + tabela + "), 1))", (seq,))
        dst.commit()
        print("  ✅ " + seq)
    except Exception as e:
        dst.rollback()
        print("  ❌ " + seq + ": " + str(e)[:80])

src.close()
dst.close()
print("\n✅ Sincronização completa!")
