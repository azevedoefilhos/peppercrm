#!/usr/bin/env python3
import pathlib

# ── Fix 1: concorrentes.py linha 1035 ──────────────────────────────────────
CAMINHO = pathlib.Path("concorrentes.py")
src = CAMINHO.read_text(encoding="utf-8")

ANTIGO1 = '''            from database import conectar as _con
            conn = _con()
            # Marca
            if marca_sel == "➕ Nova marca...":
                cur = conn.cursor()
                cur.execute("INSERT INTO concorrente (fornecedor_id, marca_concorrente, ativo) VALUES (?,?,1)",
                            (forn_sel[0], _nome))
                conc_id = cur.lastrowid'''

NOVO1 = '''            from database import conectar as _con, query as _q
            conn = _con()
            # Marca
            if marca_sel == "➕ Nova marca...":
                _dup = _q("SELECT concorrente_id FROM concorrente WHERE LOWER(marca_concorrente)=LOWER(?) AND fornecedor_id=? AND ativo=1",
                          (_nome, forn_sel[0]))
                if _dup:
                    st.error(f"⚠️ A marca **{_nome}** já está cadastrada para este fornecedor.")
                    conn.close(); return
                cur = conn.cursor()
                cur.execute("INSERT INTO concorrente (fornecedor_id, marca_concorrente, ativo) VALUES (?,?,1)",
                            (forn_sel[0], _nome))
                conc_id = cur.lastrowid'''

if ANTIGO1 in src:
    src = src.replace(ANTIGO1, NOVO1, 1)
    CAMINHO.write_text(src, encoding="utf-8")
    print("✅ concorrentes.py linha 1035 protegida")
else:
    print("⚠️  Padrão 1 não encontrado")

# ── Fix 2: pesquisa.py linha 2034 ──────────────────────────────────────────
CAMINHO2 = pathlib.Path("pesquisa.py")
src2 = CAMINHO2.read_text(encoding="utf-8")

ANTIGO2 = '''        if marca_sel == "➕ Nova marca...":
            if not nova_marca.strip():
                st.error("Informe o nome da nova marca.")
                conn.close(); return
            conc_id = execute_write(
                "INSERT INTO concorrente (fornecedor_id, marca_concorrente, ativo) VALUES (?,?,1) RETURNING concorrente_id",
                (forn_id, nova_marca.strip()))'''

NOVO2 = '''        if marca_sel == "➕ Nova marca...":
            if not nova_marca.strip():
                st.error("Informe o nome da nova marca.")
                conn.close(); return
            _dup_m = query("SELECT concorrente_id FROM concorrente WHERE LOWER(marca_concorrente)=LOWER(?) AND fornecedor_id=? AND ativo=1",
                           (nova_marca.strip(), forn_id))
            if _dup_m:
                conc_id = _dup_m[0][0]
            else:
                conc_id = execute_write(
                    "INSERT INTO concorrente (fornecedor_id, marca_concorrente, ativo) VALUES (?,?,1) RETURNING concorrente_id",
                    (forn_id, nova_marca.strip()))'''

if ANTIGO2 in src2:
    src2 = src2.replace(ANTIGO2, NOVO2, 1)
    CAMINHO2.write_text(src2, encoding="utf-8")
    print("✅ pesquisa.py linha 2034 protegida")
else:
    print("⚠️  Padrão 2 não encontrado")
