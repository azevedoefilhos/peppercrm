#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
lines = src.splitlines()

toggle = [
    '',
    '        # Coleta por Kg',
    '        _col_un, _col_peso, _col_pkg = st.columns([1, 1.5, 1.5])',
    '        unidade_coleta = _col_un.selectbox("Unidade", ["UN", "Kg"], key=f"{k}_un")',
    '        peso_coleta = None',
    '        preco_kg = None',
    '        if unidade_coleta == "Kg":',
    '            peso_coleta = _col_peso.number_input("Peso (Kg)",',
    '                min_value=0.001, value=1.0, step=0.001,',
    '                format="%.3f", key=f"{k}_peso")',
    '            if peso_coleta and preco > 0:',
    '                preco_kg = round(preco / peso_coleta, 2)',
    '                _col_pkg.metric("Preco/Kg", f"R$ {preco_kg:.2f}")',
]

# Insere apos linha 3335 (index 3334) - apos _rup_val
new_lines = lines[:3336] + toggle + lines[3336:]
pathlib.Path("pesquisa.py").write_text('\n'.join(new_lines), encoding="utf-8")
print("OK - toggle inserido na segunda funcao")

# Remove debug da primeira funcao
src2 = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
src2 = src2.replace('        st.write("DEBUG: chegou aqui")\n', '')
pathlib.Path("pesquisa.py").write_text(src2, encoding="utf-8")
print("OK - debug removido")
