"""
database.py -- PepperCRM
Lazy connection: só conecta ao banco quando query() é chamada pela primeira vez.
"""
import os

TIPOS_PONTO_EXTRA = ["Ponta de gondola","Ilha","Check-stand","Clip strip","Display"]

# Lazy: nao verifica secrets durante import
_USE_SUPABASE = None  # None = ainda nao verificado

def _check_supabase():
    """Verifica se deve usar Supabase. Chamado apenas quando necessario."""
    global _USE_SUPABASE
    if _USE_SUPABASE is not None:
        return _USE_SUPABASE
    if os.environ.get("SUPABASE_URL"):
        _USE_SUPABASE = True
        return True
    try:
        import streamlit as st
        url = st.secrets.get("SUPABASE_URL", "")
        if url:
            os.environ["SUPABASE_URL"] = url
            os.environ["SUPABASE_DB_PASSWORD"] = st.secrets.get("SUPABASE_DB_PASSWORD", "")
            _USE_SUPABASE = True
            return True
    except Exception:
        pass
    _USE_SUPABASE = False
    return False


class _DictRow:
    __slots__ = ("_row", "_cols")
    def __init__(self, row, cols):
        self._row  = row
        self._cols = cols
    def __getitem__(self, key):
        if isinstance(key, str):
            return self._row[self._cols[key]]
        return self._row[key]
    def __bool__(self):    return self._row is not None
    def __contains__(self, k): return k in self._cols
    def __iter__(self):    return iter(self._row)
    def __len__(self):     return len(self._row)
    def keys(self):        return self._cols.keys()


def _conv_row(row):
    from decimal import Decimal
    return tuple(float(v) if isinstance(v, Decimal) else v for v in row)


def _make_dict_rows(cur):
    rows = cur.fetchall()
    if rows and cur.description:
        cols = {d[0]: i for i, d in enumerate(cur.description)}
        return [_DictRow(_conv_row(r), cols) for r in rows]
    return rows


def _make_dict_row(cur):
    row = cur.fetchone()
    if row and cur.description:
        cols = {d[0]: i for i, d in enumerate(cur.description)}
        return _DictRow(_conv_row(row), cols)
    return row


# ── Traducoes SQLite -> PostgreSQL ──────────────────────────────────────────

def _extrair_expr_parenteses(s, start):
    depth = 1; i = start; buf = []
    while i < len(s) and depth > 0:
        c = s[i]
        if c == "(": depth += 1
        elif c == ")": depth -= 1
        if depth > 0: buf.append(c)
        i += 1
    return "".join(buf), i


def _traduzir_julianday(sql):
    import re
    out = []; i = 0
    while i < len(sql):
        m = re.match(r"CAST\(julianday\('now'\)\s*-\s*julianday\(", sql[i:], re.IGNORECASE)
        if m:
            i += m.end()
            expr, i = _extrair_expr_parenteses(sql, i)
            rest = re.match(r"\s*AS\s*INTEGER\)", sql[i:], re.IGNORECASE)
            if rest: i += rest.end()
            out.append(f"(CURRENT_DATE - ({expr.strip()})::DATE)")
            continue
        m2 = re.match(r"julianday\('now'\)\s*-\s*julianday\(", sql[i:], re.IGNORECASE)
        if m2:
            i += m2.end()
            expr, i = _extrair_expr_parenteses(sql, i)
            out.append(f"(CURRENT_DATE - ({expr.strip()})::DATE)")
            continue
        out.append(sql[i]); i += 1
    return "".join(out)


def _traduzir_sql_pg(sql):
    import re
    sql = sql.replace("?", "%s")
    # Traduz strftime do SQLite para TO_CHAR do PostgreSQL
    # strftime SQLite -> TO_CHAR PostgreSQL
    # Regex restrito: captura apenas nomes de campo simples (sem espacos ou virgulas)
    def _conv_strftime(fmt, campo):
        pg_fmt = fmt.replace('%Y-%m-%d','YYYY-MM-DD').replace('%Y-%m','YYYY-MM')\
                    .replace('%Y','YYYY').replace('%m','MM').replace('%d','DD')
        return f"TO_CHAR(({campo})::date, '{pg_fmt}')"
    sql = re.sub(
        r"strftime\('([^']+)',\s*([a-zA-Z0-9_.]+)\)",
        lambda m: _conv_strftime(m.group(1), m.group(2)), sql)
    # PostgreSQL: ILIKE e case-insensitive (equivalente ao LIKE do SQLite)
    import re as _re
    sql = _re.sub(r'\bLIKE\b', 'ILIKE', sql)
    # Escapa % literais no SQL (nao sao parametros)
    # Nota: %s ja foi inserido, entao escapamos apenas os outros %
    import re
    sql = re.sub(r'%(?!s)', '%%', sql)
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
    had_or_ignore = bool(re.search(r"INSERT\s+OR\s+IGNORE\s+INTO", sql, re.IGNORECASE))
    sql = re.sub(r"INSERT\s+OR\s+(?:IGNORE|REPLACE)\s+INTO", "INSERT INTO", sql, flags=re.IGNORECASE)
    if had_or_ignore:
        sql = sql.rstrip() + " ON CONFLICT DO NOTHING"
    sql = re.sub(r"INTEGER\s+PRIMARY\s+KEY\s+AUTOINCREMENT", "SERIAL PRIMARY KEY", sql, flags=re.IGNORECASE)
    sql = re.sub(r"INTEGER\s+AUTOINCREMENT", "SERIAL", sql, flags=re.IGNORECASE)
    _cols = r"data_pedido|data_contato|data_pesquisa|data_followup|data_entrega|data_visita|data_pagamento|data_inicio|data_fim|data_registro|data_vigencia|data_upload"
    sql = re.sub(rf"\b({_cols})\b(\s*)(>=|<=|=|>|<)", r"\1::DATE\2\3", sql)
    sql = re.sub(rf"\b({_cols})\b(\s+)BETWEEN\b", r"\1::DATE\2BETWEEN", sql)
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


# ── Conexao PostgreSQL (lazy) ────────────────────────────────────────────────

def _pg_connect():
    import psycopg2
    return psycopg2.connect(
        host="aws-1-sa-east-1.pooler.supabase.com",
        port=5432,
        dbname="postgres",
        user="postgres.yunzqndswpwttejlgeaa",
        password=os.environ.get("SUPABASE_DB_PASSWORD", ""),
        sslmode="require",
        connect_timeout=15,
    )


def _get_session_conn():
    """Conexao persistente por sessao Streamlit."""
    try:
        import streamlit as st
        if "db_conn" not in st.session_state or st.session_state["db_conn"].closed:
            st.session_state["db_conn"] = _pg_connect()
        conn = st.session_state["db_conn"]
        try:
            conn.cursor().execute("SELECT 1")
            return conn
        except Exception:
            try: conn.close()
            except: pass
            st.session_state["db_conn"] = _pg_connect()
            return st.session_state["db_conn"]
    except Exception:
        return _pg_connect()


class _PgCursor:
    def __init__(self, pg_cur):
        self._cur = pg_cur
        self.lastrowid = None
    def execute(self, sql, params=()):
        sql_pg = _traduzir_sql_pg(sql)
        self._cur.execute(sql_pg, params)
        self.lastrowid = None
    def fetchall(self): return _make_dict_rows(self._cur)
    def fetchone(self): return _make_dict_row(self._cur)


class _PgConn:
    def __init__(self):
        self._conn = _pg_connect()
    def cursor(self): return _PgCursor(self._conn.cursor())
    def execute(self, sql, params=()):
        cur = self.cursor(); cur.execute(sql, params); return cur
    def commit(self): self._conn.commit()
    def close(self): self._conn.close()
    def __enter__(self): return self
    def __exit__(self, *a):
        self._conn.commit(); self._conn.close()


# ── SQLite (desenvolvimento local) ───────────────────────────────────────────

def _sqlite_connect():
    import sqlite3
    db_path = os.path.join(os.path.dirname(__file__), "peppercrm.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


# ── API publica ──────────────────────────────────────────────────────────────

def conectar():
    if _check_supabase():
        return _PgConn()
    return _sqlite_connect()


def query(sql, params=()):
    if _check_supabase():
        sql_pg = _traduzir_sql_pg(sql)
        try:
            conn = _get_session_conn()
            cur = conn.cursor()
            cur.execute(sql_pg, params)
            return _make_dict_rows(cur)
        except Exception:
            conn2 = _pg_connect()
            try:
                cur = conn2.cursor()
                cur.execute(sql_pg, params)
                return _make_dict_rows(cur)
            finally:
                conn2.close()
    else:
        conn = _sqlite_connect()
        try:
            cur = conn.execute(sql, params)
            return cur.fetchall()
        finally:
            conn.close()


def execute_write(sql, params=()):
    if _check_supabase():
        sql_pg = _traduzir_sql_pg(sql)
        conn = _pg_connect()
        try:
            cur = conn.cursor()
            cur.execute(sql_pg, params)
            conn.commit()
            try: return cur.fetchone()[0]
            except Exception: return None
        finally:
            conn.close()
    else:
        conn = _sqlite_connect()
        try:
            cur = conn.execute(sql, params)
            conn.commit()
            return cur.lastrowid
        finally:
            conn.close()


# ── Helpers ──────────────────────────────────────────────────────────────────

def get_percentual_comissao(fornecedor_id):
    r = query("SELECT percentual FROM comissao WHERE fornecedor_id=? AND ativo=1 LIMIT 1",
              (fornecedor_id,))
    return float(r[0][0]) if r else 0.0


def get_fornecedores_do_cliente(cliente_id):
    return query("""
        SELECT cf.cliente_fornecedor_id, f.fornecedor_id, f.nome_fantasia,
               tp.tabela_preco_id, tp.nome_tabela, tp.tipo_tabela,
               tp.prazo_pagamento, tp.frete
        FROM cliente_fornecedor cf
        JOIN fornecedor f ON cf.fornecedor_id=f.fornecedor_id
        LEFT JOIN tabela_preco tp ON cf.tabela_preco_id=tp.tabela_preco_id
        WHERE cf.cliente_id=? AND cf.ativo=1 AND f.ativo=1
        ORDER BY f.nome_fantasia
    """, (cliente_id,))


def get_mix_com_preco(cliente_id, fornecedor_id, pdv_id=None):
    extra  = "AND m.pdv_id=?" if pdv_id else ""
    params = (cliente_id, fornecedor_id) + ((pdv_id,) if pdv_id else ()) + \
             (cliente_id, fornecedor_id) + ((pdv_id,) if pdv_id else ())
    return query(f"""
        SELECT p.produto_id, p.codigo_produto, p.descricao_curta, p.descricao,
               p.unidades_caixa, p.unidade_medida,
               COALESCE(tpi.preco_caixa, 0) AS preco_caixa,
               COALESCE(tpi.desconto_maximo, 0) AS desconto_max,
               p.ean, ult.quantidade AS ultima_qtd, ult.data_pedido AS ultima_data
        FROM mix_cliente m
        JOIN produto p ON m.produto_id=p.produto_id
        LEFT JOIN cliente_fornecedor cf
               ON cf.cliente_id=m.cliente_id AND cf.fornecedor_id=m.fornecedor_id AND cf.ativo=1
        LEFT JOIN tabela_preco_item tpi
               ON tpi.tabela_preco_id=cf.tabela_preco_id AND tpi.produto_id=p.produto_id
        LEFT JOIN (
               SELECT pi.produto_id, pi.quantidade, ped.data_pedido
               FROM pedido_item pi JOIN pedido ped ON pi.pedido_id=ped.pedido_id
               WHERE ped.cliente_id=? AND ped.fornecedor_id=?
                 AND ped.status_pedido NOT IN ('CANCELADO','RECUSADO')
               ORDER BY ped.data_pedido DESC LIMIT 1
        ) ult ON ult.produto_id=p.produto_id
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
    conn.execute(sql, (pedido_id, datetime.now().isoformat(), campo,
                       str(valor_antes) if valor_antes is not None else None,
                       str(valor_depois) if valor_depois is not None else None, obs))


def criar_tabelas(): pass
def _migrar_todos(): pass


def get_nome_empresa():
    r = query("SELECT empresa_nome FROM configuracao LIMIT 1")
    return r[0][0] if r and r[0][0] else "PepperCRM"


def _cache_clientes():
    try:
        import streamlit as st
        @st.cache_data(ttl=300, show_spinner=False)
        def _fn(): return get_clientes_ativos()
        return _fn()
    except Exception: return get_clientes_ativos()


def _cache_fornecedores():
    try:
        import streamlit as st
        @st.cache_data(ttl=300, show_spinner=False)
        def _fn(): return query("SELECT fornecedor_id, nome_fantasia FROM fornecedor WHERE ativo=1 ORDER BY nome_fantasia")
        return _fn()
    except Exception: return query("SELECT fornecedor_id, nome_fantasia FROM fornecedor WHERE ativo=1 ORDER BY nome_fantasia")


def _cache_categorias():
    try:
        import streamlit as st
        @st.cache_data(ttl=600, show_spinner=False)
        def _fn(): return query("SELECT categoria_id, nome_categoria FROM categoria WHERE ativo=1 ORDER BY nome_categoria")
        return _fn()
    except Exception: return query("SELECT categoria_id, nome_categoria FROM categoria WHERE ativo=1 ORDER BY nome_categoria")
