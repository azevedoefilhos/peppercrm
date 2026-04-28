"""
database.py -- PepperCRM
Em producao (Streamlit Cloud): usa Supabase via Session Pooler (IPv4)
Em desenvolvimento (local):    usa SQLite
"""

import os
import sqlite3

TIPOS_PONTO_EXTRA = ["Ponta de gondola","Ilha","Check-stand","Clip strip","Display"]

_USE_SUPABASE = bool(os.environ.get("SUPABASE_URL"))

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

    def _extrair_expr_parenteses(s, start):
        depth = 1
        i = start
        buf = []
        while i < len(s) and depth > 0:
            c = s[i]
            if c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
            if depth > 0:
                buf.append(c)
            i += 1
        return "".join(buf), i

    def _traduzir_julianday(sql):
        """Traduz julianday SQLite -> diferenca de datas PostgreSQL.
        No PostgreSQL, DATE - DATE retorna INTEGER diretamente.
        Nao usar EXTRACT(DAY FROM ...) pois nao aceita integer.
        """
        import re
        out = []
        i = 0
        while i < len(sql):
            # CAST(julianday('now') - julianday(EXPR) AS INTEGER)
            m = re.match(r"CAST\(julianday\('now'\)\s*-\s*julianday\(", sql[i:], re.IGNORECASE)
            if m:
                i += m.end()
                expr, i = _extrair_expr_parenteses(sql, i)
                rest = re.match(r"\s*AS\s*INTEGER\)", sql[i:], re.IGNORECASE)
                if rest:
                    i += rest.end()
                out.append(f"(CURRENT_DATE - ({expr.strip()})::DATE)")
                continue
            # julianday('now') - julianday(EXPR)
            m2 = re.match(r"julianday\('now'\)\s*-\s*julianday\(", sql[i:], re.IGNORECASE)
            if m2:
                i += m2.end()
                expr, i = _extrair_expr_parenteses(sql, i)
                out.append(f"(CURRENT_DATE - ({expr.strip()})::DATE)")
                continue
            out.append(sql[i])
            i += 1
        return "".join(out)

    def _traduzir_sql_pg(sql):
        import re
        sql = sql.replace("?", "%s")
        sql = re.sub(r"date\('now',\s*'start of month',\s*'-1 day'\)",
            "(DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '1 day')", sql)
        sql = re.sub(r"date\('now',\s*'start of month',\s*'-1 month'\)",
            "DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')", sql)
        sql = re.sub(r"date\('now',\s*'start of month',\s*'-2 months'\)",
            "DATE_TRUNC('month', CURRENT_DATE - INTERVAL '2 months')", sql)
        sql = re.sub(r"date\('now',\s*'start of month'\)",
            "DATE_TRUNC('month', CURRENT_DATE)", sql)
        sql = re.sub(r"date\('now',\s*'start of year'\)",
            "DATE_TRUNC('year', CURRENT_DATE)", sql)
        sql = re.sub(r"date\('now',\s*'(-?\d+)\s*(day|days|month|months|year|years)'\)",
            lambda m: f"(CURRENT_DATE - INTERVAL '{abs(int(m.group(1)))} {m.group(2)}')", sql)
        sql = re.sub(r"date\('now',\s*'\+(\d+)\s*(day|days)'\)",
            lambda m: f"(CURRENT_DATE + INTERVAL '{m.group(1)} {m.group(2)}')", sql)
        sql = sql.replace("date('now')", "CURRENT_DATE")
        sql = re.sub(r"strftime\('%Y-%m',\s*([^)]+)\)",
            lambda m: f"TO_CHAR({m.group(1).strip()}::DATE, 'YYYY-MM')", sql)
        sql = re.sub(r"strftime\('%Y',\s*([^)]+)\)",
            lambda m: f"TO_CHAR({m.group(1).strip()}::DATE, 'YYYY')", sql)
        sql = re.sub(r"strftime\('%m',\s*([^)]+)\)",
            lambda m: f"TO_CHAR({m.group(1).strip()}::DATE, 'MM')", sql)
        sql = re.sub(r"printf\('%02d',\s*([^)]+)\)",
            lambda m: f"LPAD(CAST({m.group(1).strip()} AS TEXT), 2, '0')", sql)
        sql = _traduzir_julianday(sql)
        sql = re.sub(r"GROUP_CONCAT\(([^,)]+),\s*'([^']+)'\)",
            lambda m: f"STRING_AGG({m.group(1).strip()}, '{m.group(2)}')", sql)
        sql = re.sub(r"GROUP_CONCAT\(([^)]+)\)",
            lambda m: f"STRING_AGG({m.group(1).strip()}, ',')", sql)
        sql = sql.replace("IFNULL(", "COALESCE(")
        _cols = r"(data_pedido|data_contato|data_pesquisa|data_followup|data_entrega|data_visita|data_pagamento|data_inicio|data_fim|data_registro|data_vigencia|data_upload)"
        sql = re.sub(rf"({_cols})\s*(>=|<=|=|>|<)", r"\1::DATE \3", sql)
        sql = re.sub(rf"({_cols})\s+BETWEEN", r"\1::DATE BETWEEN", sql)
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
                    result.append(f"{inner_str[:comma_pos]})::NUMERIC{inner_str[comma_pos:]}")
                    result.append(")")
                else:
                    result.append(f"{inner_str})::NUMERIC)")
            else:
                result.append(sql[i]); i += 1
        return "".join(result)

    def _get_pg_password():
        return os.environ.get("SUPABASE_DB_PASSWORD", "")

    def conectar():
        return psycopg2.connect(
            host="aws-1-sa-east-1.pooler.supabase.com",
            port=5432,
            dbname="postgres",
            user="postgres.yunzqndswpwttejlgeaa",
            password=_get_pg_password(),
            sslmode="require",
            connect_timeout=15,
        )

    def query(sql, params=()):
        sql_pg = _traduzir_sql_pg(sql)
        conn = conectar()
        try:
            cur = conn.cursor()
            cur.execute(sql_pg, params)
            return cur.fetchall()
        finally:
            conn.close()

    def execute_write(sql, params=()):
        sql_pg = _traduzir_sql_pg(sql)
        conn = conectar()
        try:
            cur = conn.cursor()
            cur.execute(sql_pg, params)
            conn.commit()
            try:
                return cur.fetchone()[0]
            except Exception:
                return None
        finally:
            conn.close()

else:
    _DB_PATH = os.path.join(os.path.dirname(__file__), "peppercrm.db")

    def conectar():
        conn = sqlite3.connect(_DB_PATH)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        return conn

    def query(sql, params=()):
        conn = conectar()
        try:
            cur = conn.execute(sql, params)
            return cur.fetchall()
        finally:
            conn.close()

    def execute_write(sql, params=()):
        conn = conectar()
        try:
            cur = conn.execute(sql, params)
            conn.commit()
            return cur.lastrowid
        finally:
            conn.close()

def get_percentual_comissao(fornecedor_id):
    r = query("SELECT percentual FROM comissao WHERE fornecedor_id=? AND ativo=1 LIMIT 1",
              (fornecedor_id,))
    return float(r[0][0]) if r else 0.0

def get_fornecedores_do_cliente(cliente_id):
    return query("""
        SELECT DISTINCT f.fornecedor_id, f.nome_fantasia
        FROM cliente_fornecedor cf
        JOIN fornecedor f ON cf.fornecedor_id=f.fornecedor_id
        WHERE cf.cliente_id=? AND cf.ativo=1 AND f.ativo=1
        ORDER BY f.nome_fantasia
    """, (cliente_id,))

def get_mix_com_preco(cliente_id, fornecedor_id, pdv_id=None):
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

def get_produtos_por_fornecedor(fornecedor_id):
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
    pass

def _migrar_todos():
    pass

def get_nome_empresa():
    r = query("SELECT empresa_nome FROM configuracao LIMIT 1")
    return r[0][0] if r and r[0][0] else "PepperCRM"
