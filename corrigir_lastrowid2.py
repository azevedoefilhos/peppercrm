#!/usr/bin/env python3
"""Corrige cur.lastrowid para conc_id em pesquisa.py usando execute_write + RETURNING."""
import pathlib, sys

CAMINHO = pathlib.Path("pesquisa.py")
texto = CAMINHO.read_text(encoding="utf-8")

ANTIGO = '''        conn = conectar()
        # Determina conc_id
        if marca_sel == "➕ Nova marca...":
            if not nova_marca.strip():
                st.error("Informe o nome da nova marca.")
                conn.close(); return
            cur = conn.cursor()
            cur.execute("INSERT INTO concorrente (fornecedor_id, marca_concorrente, ativo) VALUES (?,?,1)",
                        (forn_id, nova_marca.strip()))
            conc_id = cur.lastrowid
            conn.commit()'''

NOVO = '''        conn = conectar()
        # Determina conc_id
        if marca_sel == "➕ Nova marca...":
            if not nova_marca.strip():
                st.error("Informe o nome da nova marca.")
                conn.close(); return
            conc_id = execute_write(
                "INSERT INTO concorrente (fornecedor_id, marca_concorrente, ativo) VALUES (?,?,1) RETURNING concorrente_id",
                (forn_id, nova_marca.strip()))'''

if ANTIGO in texto:
    novo = texto.replace(ANTIGO, NOVO, 1)
    CAMINHO.write_text(novo, encoding="utf-8")
    print("✅ conc_id corrigido com execute_write + RETURNING")
else:
    # Busca mais flexível
    import re
    padrao = re.compile(
        r'cur = conn\.cursor\(\)\s*\n\s*cur\.execute\("INSERT INTO concorrente.*?\n.*?conc_id = cur\.lastrowid\s*\n\s*conn\.commit\(\)',
        re.DOTALL
    )
    if padrao.search(texto):
        novo = padrao.sub(
            'conc_id = execute_write(\n                "INSERT INTO concorrente (fornecedor_id, marca_concorrente, ativo) VALUES (?,?,1) RETURNING concorrente_id",\n                (forn_id, nova_marca.strip()))',
            texto, count=1
        )
        CAMINHO.write_text(novo, encoding="utf-8")
        print("✅ conc_id corrigido via regex")
    else:
        print("⚠️  Padrão não encontrado — verifique manualmente linhas 2027-2037")
