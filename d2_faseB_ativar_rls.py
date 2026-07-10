# d2_faseB_ativar_rls.py
# Ativa Row Level Security nas tabelas de negocio
# O banco filtra empresa_id automaticamente sem mudar codigo

from dotenv import load_dotenv; load_dotenv()
import sys; sys.path.insert(0, '.')
from database import _pg_connect

TABELAS = [
    "fornecedor", "cliente", "produto", "categoria", "linha", "marca",
    "associacao", "central_compras", "vendedor", "promotor", "representante",
    "pdv", "tabela_preco", "tabela_preco_item",
    "comissao", "comissao_pagamento",
    "pedido", "pedido_item", "pedido_historico",
    "contato_registro", "contato_interacao",
    "contato_cliente", "contato_fornecedor",
    "contato_fornecedor_topico", "contato_x_fornecedor",
    "pesquisa_preco", "pesquisa_preco_item", "pesquisa_foto",
    "historico_preco", "concorrente",
    "produto_concorrente", "produto_concorrente_relacao",
    "meta_fornecedor", "meta_mix", "mix_cliente",
    "despesa", "visita_cliente", "att_promotor", "att_vendedor",
    "negociacao", "interacao",
    "cliente_fornecedor", "produto_codigo_cliente",
    "mensagem_modelo",
]

conn = _pg_connect()
conn.autocommit = True
cur = conn.cursor()

print("=== Ativando RLS nas tabelas de negocio ===\n")

ok = 0; erros = []

for tabela in TABELAS:
    try:
        # 1. Ativa RLS na tabela
        cur.execute(f"ALTER TABLE {tabela} ENABLE ROW LEVEL SECURITY")

        # 2. Remove policy antiga se existir
        cur.execute(f"DROP POLICY IF EXISTS empresa_isolation ON {tabela}")

        # 3. Cria policy de isolamento por empresa_id
        # USING: filtra SELECTs
        # WITH CHECK: filtra INSERTs/UPDATEs
        cur.execute(f"""
            CREATE POLICY empresa_isolation ON {tabela}
            USING (
                empresa_id = COALESCE(
                    current_setting('app.empresa_id', true)::integer,
                    1
                )
            )
            WITH CHECK (
                empresa_id = COALESCE(
                    current_setting('app.empresa_id', true)::integer,
                    1
                )
            )
        """)

        print(f"  OK {tabela}")
        ok += 1

    except Exception as e:
        print(f"  ERRO {tabela}: {e}")
        erros.append((tabela, str(e)))

print(f"\nOK: {ok} | Erros: {len(erros)}")
if erros:
    for t, e in erros:
        print(f"  {t}: {e}")

# Verifica RLS ativo
print("\n=== Verificando RLS ===")
cur.execute("""
    SELECT tablename, rowsecurity
    FROM pg_tables
    WHERE schemaname='public' AND rowsecurity=true
    ORDER BY tablename
""")
ativas = cur.fetchall()
print(f"RLS ativo em {len(ativas)} tabelas")

cur.close()
conn.close()

if not erros:
    print("\nFASE B (RLS) concluida!")
    print("Proximo passo: atualizar database.py para injetar empresa_id na conexao")
