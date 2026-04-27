"""
database.py — PepperCRM
Camada de acesso ao banco de dados.
Em producao (Streamlit Cloud): usa Supabase (PostgreSQL via psycopg2)
Em desenvolvimento (local):    usa SQLite (comportamento atual)
"""

import os
import sqlite3

# ── Constantes globais usadas pelos modulos ──────────────────────────────
TIPOS_PONTO_EXTRA = ["Ponta de gondola","Ilha","Check-stand","Clip strip","Display"]

# ── Detecta ambiente de forma segura ─────────────────────────────────────
# Usa APENAS variavel de ambiente — sem tentar ler st.secrets no import
# O Streamlit Cloud define SUPABASE_URL automaticamente via secrets
_USE_SUPABASE = bool(os.environ.get("SUPABASE_URL"))

# Tenta carregar do secrets.toml apenas se existir (sem crashar)
if not _USE_SUPABASE:
    try:
        import streamlit as st
        _url = st.secrets.get("SUPABASE_URL", "")
        if _url:
            os.environ["SUPABASE_URL"] = _url
            os.environ["SUPABASE_DB_PASSWORD"] = st.secrets.get("SUPABASE_DB_PASSWORD", "")
            _USE_SUPABASE = True
    except Exception:
        _USE_SUPABASE = False

if _USE_SUPABASE:
    import psycopg2
    import urllib.parse

    def _get_pg_url():
        url   = os.environ.get("SUPABASE_URL", "")
        senha = urllib.parse.quote(os.environ.get("SUPABASE_DB_PASSWORD", ""))
        host  = url.replace("https://","").replace("http://","")
        return f"postgresql://postgres:{senha}@db.{host}:5432/postgres"

    def conectar():
        """Retorna conexao PostgreSQL (Supabase)."""
        return psycopg2.connect(_get_pg_url(), connect_timeout=10)

    def query(sql, params=()):
        """Executa SELECT e retorna lista de tuplas."""
        sql_pg = sql.replace("?", "%s")
        conn   = conectar()
        try:
            cur = conn.cursor()
            cur.execute(sql_pg, params)
            return cur.fetchall()
        finally:
            conn.close()

else:
    # ── Modo SQLite (desenvolvimento local) ──────────────────────────────
    _DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "peppercrm.db")

    def conectar():
        """Retorna conexao SQLite."""
        conn = sqlite3.connect(_DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def query(sql, params=()):
        """Executa SELECT e retorna lista de tuplas."""
        conn = conectar()
        try:
            return conn.execute(sql, params).fetchall()
        finally:
            conn.close()


# ── Funcoes auxiliares ────────────────────────────────────────────────────

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
    extra  = "AND m.pdv_id=?" if pdv_id else ""
    params = (cliente_id, fornecedor_id, pdv_id) if pdv_id else (cliente_id, fornecedor_id)
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
        cur = conn.cursor()
        cur.execute(sql.replace("?","%s"), params)
    else:
        conn.execute(sql, params)

def criar_tabelas():
    """Compatibilidade — em producao as tabelas ja existem no Supabase."""
    pass

def _migrar_todos():
    """Compatibilidade — migracao ja foi feita pelo script dedicado."""
    pass

def get_nome_empresa():
    r = query("SELECT empresa_nome FROM configuracao LIMIT 1")
    return r[0][0] if r and r[0][0] else "PepperCRM"
