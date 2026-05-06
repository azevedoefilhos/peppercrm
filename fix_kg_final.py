#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
original = src

OLD = '''        # Coleta por Kg
        col_un, col_peso, col_pkg = st.columns([1, 1.5, 1.5])
        with col_un:
            unidade_coleta = st.selectbox("Unidade", ["UN", "Kg"], key=f"{k}_un")
        peso_coleta = None
        preco_kg = None
        if unidade_coleta == "Kg":
            with col_peso:
                peso_coleta = st.number_input("Peso (Kg)",
                    min_value=0.001, value=1.0, step=0.001,
                    format="%.3f", key=f"{k}_peso")
            with col_pkg:
                if peso_coleta and preco > 0:
                    preco_kg = round(preco / peso_coleta, 2)
                    st.metric("Preco/Kg", f"R$ {preco_kg:.2f}")'''

NEW = '''        # Coleta por Kg
        _col_un, _col_peso, _col_pkg = st.columns([1, 1.5, 1.5])
        unidade_coleta = _col_un.selectbox("Unidade", ["UN", "Kg"], key=f"{k}_un")
        peso_coleta = None
        preco_kg = None
        if unidade_coleta == "Kg":
            peso_coleta = _col_peso.number_input("Peso (Kg)",
                min_value=0.001, value=1.0, step=0.001,
                format="%.3f", key=f"{k}_peso")
            if peso_coleta and preco > 0:
                preco_kg = round(preco / peso_coleta, 2)
                _col_pkg.metric("Preco/Kg", f"R$ {preco_kg:.2f}")'''

if OLD in src:
    src = src.replace(OLD, NEW, 1)
    pathlib.Path("pesquisa.py").write_text(src, encoding="utf-8")
    print("OK")
else:
    print("NAO ENCONTRADO")
