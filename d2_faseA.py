# d2_faseA.py — com lock_timeout para evitar deadlock
from dotenv import load_dotenv; load_dotenv()
import sys; sys.path.insert(0, '.')
from database import _pg_connect

TABELAS = [
    "fornecedor", "cliente", "produto", "categoria", "linha", "marca",
    "associacao", "central_compras", "vendedor", "promotor", "representante",
    "pdv", "tabela_preco", "tabela_preco_item", "comissao", "comissao_pagamento",
    "pedido", "pedido_item", "pedido_historico",
    "contato_registro", "contato_interacao", "contato_cliente", "contato_fornecedor",
    "contato_fornecedor_topico", "contato_x_fornecedor",
    "pesquisa_preco", "pesquisa_preco_item", "pesquisa_foto",
    "historico_preco", "concorrente", "produto_concorrente", "produto_concorrente_relacao",
    "meta_fornecedor", "meta_mix", "mix_cliente", "despesa",
    "visita_cliente", "att_promotor", "att_vendedor",
    "negociacao", "interacao", "cliente_fornecedor", "produto_codigo_cliente",
    "mensagem_modelo", "usuario", "configuracao",
]

print("=== FASE A - Adicionar empresa_id (com lock_timeout=5s) ===\n")
ok = 0; ja_existe = 0; travadas = []

for tabela in TABELAS:
    conn = _pg_connect()
    conn.autocommit = False
    cur = conn.cursor()
    try:
        # Verifica se ja existe
        cur.execute("""SELECT COUNT(*) FROM information_schema.columns
            WHERE table_name=%s AND column_name='empresa_id'""", (tabela,))
        if cur.fetchone()[0] > 0:
            print(f"  -- {tabela}: ja existe")
            ja_existe += 1
            conn.commit(); cur.close(); conn.close()
            continue

        # Timeout de 5 segundos para obter lock
        cur.execute("SET lock_timeout = '5s'")
        cur.execute(f"ALTER TABLE {tabela} ADD COLUMN empresa_id INTEGER DEFAULT 1")
        cur.execute(f"UPDATE {tabela} SET empresa_id=1 WHERE empresa_id IS NULL")
        conn.commit()
        print(f"  OK {tabela}")
        ok += 1

    except Exception as e:
        conn.rollback()
        if 'lock' in str(e).lower() or 'timeout' in str(e).lower():
            print(f"  TRAVADA {tabela} — tente novamente com Streamlit fechado")
            travadas.append(tabela)
        else:
            print(f"  ERRO {tabela}: {e}")
    finally:
        try: cur.close(); conn.close()
        except: pass

# Indices
print("\n=== Criando indices ===")
conn = _pg_connect(); conn.autocommit = True; cur = conn.cursor()
for nome, tab in [
    ("idx_emp_cliente","cliente"), ("idx_emp_fornecedor","fornecedor"),
    ("idx_emp_pedido","pedido"), ("idx_emp_contato","contato_registro"),
    ("idx_emp_produto","produto"), ("idx_emp_usuario","usuario"),
]:
    try:
        cur.execute(f"CREATE INDEX IF NOT EXISTS {nome} ON {tab}(empresa_id)")
        print(f"  OK {nome}")
    except Exception as e:
        print(f"  ERRO {nome}: {e}")
cur.close(); conn.close()

print(f"\nOK: {ok} | Ja existiam: {ja_existe} | Travadas: {len(travadas)}")
if travadas:
    print("Tabelas travadas (rodar novamente com Streamlit fechado):")
    for t in travadas: print(f"  - {t}")
else:
    print("FASE A concluida com sucesso!")
