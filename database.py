"""
database_supabase.py — PepperCRM
Camada de acesso ao banco de dados.
Em produção (Streamlit Cloud): usa Supabase (PostgreSQL via psycopg2)
Em desenvolvimento (local):    usa SQLite (comportamento atual)
"""

import os
import sqlite3

# ── Constantes globais usadas pelos módulos ─────────────────────────────
TIPOS_PONTO_EXTRA = ["Ponta de gôndola","Ilha","Check-stand","Clip strip","Display"]

# ── Detecta ambiente ─────────────────────────────────────────────────────
# Quando rodando no Streamlit Cloud, a variável SUPABASE_URL estará definida
# nos secrets do app. Localmente usa SQLite normalmente.
_USE_SUPABASE = bool(os.environ.get("SUPABASE_URL") or
                     (hasattr(__import__('streamlit'), 'secrets') and
                      __import__('streamlit').secrets.get("SUPABASE_URL")))

if _USE_SUPABASE:
    import psycopg2
    import psycopg2.extras
    import urllib.parse

    def _get_pg_url():
        import streamlit as st
        url      = st.secrets["SUPABASE_URL"]
        senha    = urllib.parse.quote(st.secrets["SUPABASE_DB_PASSWORD"])
        host     = url.replace("https://","").replace("http://","")
        db_host  = f"db.{host}"
        return f"postgresql://postgres:{senha}@{db_host}:5432/postgres"

    def conectar():
        """Retorna conexão PostgreSQL (Supabase)."""
        return psycopg2.connect(_get_pg_url(), connect_timeout=10)

    def query(sql, params=()):
        """Executa SELECT e retorna lista de tuplas — compatível com SQLite."""
        # Converte placeholders ? → %s (diferença SQLite vs PostgreSQL)
        sql_pg = sql.replace("?", "%s")
        conn   = conectar()
        try:
            cur = conn.cursor()
            cur.execute(sql_pg, params)
            rows = cur.fetchall()
            return rows
        finally:
            conn.close()

else:
    # ── Modo SQLite (desenvolvimento local) ──────────────────────────────
    _DB_PATH = os.path.join(os.path.dirname(__file__), "peppercrm.db")

    def conectar():
        """Retorna conexão SQLite."""
        conn = sqlite3.connect(_DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def query(sql, params=()):
        """Executa SELECT e retorna lista de tuplas."""
        conn = conectar()
        try:
            rows = conn.execute(sql, params).fetchall()
            return rows
        finally:
            conn.close()


# ── Funções auxiliares (idênticas independente do banco) ─────────────────

def get_percentual_comissao(fornecedor_id: int) -> float:
    r = query("SELECT percentual FROM comissao WHERE fornecedor_id=? AND ativo=1 LIMIT 1",
              (fornecedor_id,))
    return float(r[0][0]) if r else 0.0

def get_fornecedores_do_cliente(cliente_id: int):
    return query("""
        SELECT DISTINCT f.fornecedor_id, f.nome_fantasia
        FROM cliente_fornecedor cf
        JOIN fornecedor f ON cf.fornecedor_id=f.fornecedor_id
        WHERE cf.cliente_id=? AND cf.ativo=1 AND f.ativo=1
        ORDER BY f.nome_fantasia
    """, (cliente_id,))

def get_mix_com_preco(cliente_id: int, fornecedor_id: int, pdv_id=None):
    extra = "AND m.pdv_id=?" if pdv_id else ""
    params= (cliente_id, fornecedor_id, pdv_id) if pdv_id else (cliente_id, fornecedor_id)
    return query(f"""
        SELECT p.produto_id, p.descricao_curta, p.descricao,
               p.codigo_produto, p.ean,
               p.peso, p.unidade_medida, p.unidades_caixa,
               COALESCE(tpi.preco_caixa, 0) AS preco_caixa,
               m.mix_id
        FROM mix_cliente m
        JOIN produto p ON m.produto_id=p.produto_id
        LEFT JOIN cliente_fornecedor cf
               ON cf.cliente_id=m.cliente_id AND cf.fornecedor_id=m.fornecedor_id AND cf.ativo=1
        LEFT JOIN tabela_preco_item tpi
               ON tpi.tabela_preco_id=cf.tabela_preco_id AND tpi.produto_id=p.produto_id
        WHERE m.cliente_id=? AND m.fornecedor_id=? AND m.ativo=1 {extra}
        ORDER BY p.descricao_curta
    """, params)

def get_clientes_ativos():
    return query("SELECT cliente_id, nome_fantasia FROM cliente WHERE ativo=1 ORDER BY nome_fantasia")

def get_produtos_por_fornecedor(fornecedor_id: int):
    return query("""
        SELECT produto_id, descricao_curta, descricao, codigo_produto,
               peso, unidade_medida, unidades_caixa, ean
        FROM produto WHERE fornecedor_id=? AND ativo=1 ORDER BY descricao_curta
    """, (fornecedor_id,))

def registrar_historico(conn, pedido_id, campo, valor_antes, valor_depois, obs=None):
    from datetime import datetime
    sql = """INSERT INTO pedido_historico
             (pedido_id, data_hora, campo, valor_antes, valor_depois, observacao)
             VALUES (?,?,?,?,?,?)"""
    params = (pedido_id, datetime.now().isoformat(), campo,
              str(valor_antes) if valor_antes is not None else None,
              str(valor_depois) if valor_depois is not None else None, obs)
    if _USE_SUPABASE:
        sql_pg = sql.replace("?", "%s")
        cur = conn.cursor()
        cur.execute(sql_pg, params)
    else:
        conn.execute(sql, params)


# ── Mantém compatibilidade com código existente ───────────────────────────
# O database.py original tem criar_tabelas() e _migrar_todos()
# Em produção (Supabase) essas funções não fazem nada —
# a estrutura foi criada pelo script de migração

def criar_tabelas():
    """Compatibilidade — em produção as tabelas já existem no Supabase."""
    pass

def _migrar_todos():
    """Compatibilidade — migração já foi feita pelo script dedicado."""
    pass

def get_nome_empresa():
    """Retorna o nome da empresa da configuração."""
    r = query("SELECT empresa_nome FROM configuracao LIMIT 1")
    return r[0][0] if r and r[0][0] else "PepperCRM"
