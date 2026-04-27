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

    def _traduzir_sql_pg(sql):
        import re
        sql = sql.replace("?", "%s")
        sql = sql.replace("date('now')", "CURRENT_DATE")
        sql = re.sub(r"date\('now',\s*'start of month'\)", "DATE_TRUNC('month', CURRENT_DATE)", sql)
        sql = re.sub(r"date\('now',\s*'start of month',\s*'-1 day'\)", "(DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '1 day')", sql)
        sql = re.sub(r"date\('now',\s*'start of month',\s*'-1 month'\)", "DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')", sql)
        sql = re.sub(r"date\('now',\s*'start of month',\s*'-2 months'\)", "DATE_TRUNC('month', CURRENT_DATE - INTERVAL '2 months')", sql)
        sql = re.sub(r"date\('now',\s*'start of year'\)", "DATE_TRUNC('year', CURRENT_DATE)", sql)
        sql = re.sub(r"date\('now',\s*'(-?\d+)\s*(day|days|month|months|year|years)'\)",
            lambda m: f"(CURRENT_DATE - INTERVAL '{abs(int(m.group(1)))} {m.group(2)}')", sql)
        sql = re.sub(r"date\('now',\s*'\+(\d+)\s*(day|days)'\)",
            lambda m: f"(CURRENT_DATE + INTERVAL '{m.group(1)} {m.group(2)}')", sql)
        sql = re.sub(r"strftime\('%Y-%m',\s*([^)]+)\)",
            lambda m: f"TO_CHAR({m.group(1).strip()}::DATE, 'YYYY-MM')", sql)
        sql = re.sub(r"strftime\('%Y',\s*([^)]+)\)",
            lambda m: f"TO_CHAR({m.group(1).strip()}::DATE, 'YYYY')", sql)
        sql = re.sub(r"strftime\('%m',\s*([^)]+)\)",
            lambda m: f"TO_CHAR({m.group(1).strip()}::DATE, 'MM')", sql)
        sql = re.sub(r"printf\('%02d',\s*([^)]+)\)",
            lambda m: f"LPAD(CAST({m.group(1).strip()} AS TEXT), 2, '0')", sql)
        sql = re.sub(r"CAST\(julianday\('now'\)\s*-\s*julianday\(([^)]+)\)\s*AS\s*INTEGER\)",
            lambda m: f"EXTRACT(DAY FROM (CURRENT_DATE - {m.group(1).strip()}::DATE))::INTEGER", sql)
        sql = re.sub(r"julianday\('now'\)\s*-\s*julianday\(([^)]+)\)",
            lambda m: f"EXTRACT(DAY FROM (CURRENT_DATE - {m.group(1).strip()}::DATE))", sql)
        sql = re.sub(r"GROUP_CONCAT\(([^,)]+),\s*'([^']+)'\)",
            lambda m: f"STRING_AGG({m.group(1).strip()}, '{m.group(2)}')", sql)
        sql = re.sub(r"GROUP_CONCAT\(([^)]+)\)",
            lambda m: f"STRING_AGG({m.group(1).strip()}, ',')", sql)
        sql = sql.replace("IFNULL(", "COALESCE(")
        result = []; i = 0; sql_up = sql.upper()
        while i < len(sql):
            if sql_up[i:i+6] == "ROUND(":
                result.append("ROUND(("); i += 6
                depth = 1; inner = []
                while i < len(sql) and depth > 0:
                    c = sql[i]
                    if c == "(": depth += 1
                    elif c == ")": depth -= 1
                    if depth > 0: inner.append(c)
                    i += 1
                inner_str = "".join(inner)
                d = 0; comma_pos = -1
                for j, c in enumerate(inner_str):
                    if c == "(": d += 1
                    elif c == ")": d -= 1
                    elif c == "," and d == 0: comma_pos = j; break
                if comma_pos >= 0:
                    result.append(f"{inner_str[:comma_pos]})::NUMERIC{inner_str[comma_pos:]})")
                else:
                    result.append(f"{inner_str})::NUMERIC)")
            else:
                result.append(sql[i]); i += 1
        return "".join(result)


    def conectar():
        """Retorna conexao PostgreSQL (Supabase)."""
        conn = psycopg2.connect(_get_pg_url(), connect_timeout=10)
        return conn

    def _executar_pg(conn, sql, params=()):
        """Executa SQL no PostgreSQL adaptando ROUND para double precision."""
        sql_pg = sql.replace("?", "%s")
        # Substitui ROUND(expr, n) por ROUND(expr::NUMERIC, n) de forma segura
        # usando split por token em vez de regex
        sql_pg = _traduzir_sql_pg(sql_pg)
        cur = conn.cursor()
        cur.execute(sql_pg, params)
        return cur


    def conectar():
        """Retorna conexao PostgreSQL (Supabase)."""
        conn = psycopg2.connect(_get_pg_url(), connect_timeout=10)
        return conn

    def _executar_pg(conn, sql, params=()):
        """Executa SQL no PostgreSQL adaptando ROUND para double precision."""
        sql_pg = sql.replace("?", "%s")
        # Substitui ROUND(expr, n) por ROUND(expr::NUMERIC, n) de forma segura
        # usando split por token em vez de regex
        sql_pg = _traduzir_sql_pg(sql_pg)
        cur = conn.cursor()
        cur.execute(sql_pg, params)
        return cur

    def _traduzir_sql_pg(sql):
        """Substitui ROUND( por ROUND(( e adiciona )::NUMERIC antes da virgula/fecha."""
        if "ROUND(" not in sql.upper():
            return sql
        result = []
        i = 0
        sql_up = sql.upper()
        while i < len(sql):
            if sql_up[i:i+6] == "ROUND(":
                result.append("ROUND((")
                i += 6
                depth = 1
                inner = []
                while i < len(sql) and depth > 0:
                    c = sql[i]
                    if c == "(": depth += 1
                    elif c == ")": depth -= 1
                    if depth > 0:
                        inner.append(c)
                    i += 1
                inner_str = "".join(inner)
                # Verifica se tem segundo argumento (virgula no nivel 0)
                d = 0
                comma_pos = -1
                for j, c in enumerate(inner_str):
                    if c == "(": d += 1
                    elif c == ")": d -= 1
                    elif c == "," and d == 0:
                        comma_pos = j; break
                if comma_pos >= 0:
                    expr  = inner_str[:comma_pos]
                    resto = inner_str[comma_pos:]
                    result.append(f"{expr})::NUMERIC{resto})")
                else:
                    result.append(f"{inner_str})::NUMERIC)")
            else:
                result.append(sql[i]); i += 1
        return "".join(result)

    def _adaptar_sql_pg(sql):
        """Adapta SQL SQLite para PostgreSQL — apenas troca placeholders."""
        return sql.replace("?", "%s")

    def query(sql, params=()):
        """Executa SELECT e retorna lista de tuplas."""
        sql_pg = _traduzir_sql_pg(sql)
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
        cur.execute(sql.replace("?", "%s"), params)
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
