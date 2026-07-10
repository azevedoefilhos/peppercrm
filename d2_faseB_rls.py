# d2_faseB_rls.py
# Fase B alternativa: Row Level Security no PostgreSQL
# O banco filtra empresa_id automaticamente — zero mudanca de codigo
# 
# COMO FUNCIONA:
# 1. Criamos um usuario PostgreSQL por empresa
# 2. RLS garante que cada usuario so ve seus proprios dados
# 3. O app conecta com o usuario da empresa logada
#
# OU — abordagem mais simples para nosso caso:
# Usar SET app.empresa_id = X na conexao, e policies que filtram por isso

from dotenv import load_dotenv; load_dotenv()
import sys; sys.path.insert(0, '.')
from database import _pg_connect

conn = _pg_connect()
conn.autocommit = True
cur = conn.cursor()

# Tabelas principais de negocio
TABELAS_RLS = [
    "fornecedor", "cliente", "produto", "categoria", "linha", "marca",
    "associacao", "central_compras", "vendedor", "promotor",
    "pdv", "tabela_preco", "tabela_preco_item",
    "comissao", "comissao_pagamento",
    "pedido", "pedido_item", "pedido_historico",
    "contato_registro", "contato_interacao",
    "contato_cliente", "contato_fornecedor",
    "pesquisa_preco", "pesquisa_preco_item", "pesquisa_foto",
    "concorrente", "produto_concorrente",
    "meta_fornecedor", "meta_mix", "mix_cliente",
    "despesa", "visita_cliente",
    "mensagem_modelo",
]

print("=== Testando Row Level Security ===\n")

# Verifica se RLS ja esta ativo em alguma tabela
cur.execute("""
    SELECT tablename, rowsecurity 
    FROM pg_tables 
    WHERE schemaname='public' 
    AND tablename IN %s
    ORDER BY tablename
""", (tuple(TABELAS_RLS),))

rows = cur.fetchall()
rls_ativo = [r[0] for r in rows if r[1]]
rls_inativo = [r[0] for r in rows if not r[1]]

print(f"RLS ativo em {len(rls_ativo)} tabelas")
print(f"RLS inativo em {len(rls_inativo)} tabelas")

# Verifica se SET LOCAL funciona (necessario para nossa abordagem)
try:
    cur.execute("SET LOCAL app.empresa_id = '1'")
    cur.execute("SELECT current_setting('app.empresa_id', true)")
    val = cur.fetchone()[0]
    print(f"\nSET app.empresa_id funciona: valor={val}")
    print("Abordagem RLS viavel!")
except Exception as e:
    print(f"\nErro: {e}")

cur.close()
conn.close()
