#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
lines = src.splitlines()

# Fix: inserir unidade_coleta selectbox na linha 3321 (dentro do form, apos col1,col2,col3)
# e mover o preco para ficar ao lado do selectbox

OLD = '''    with st.form(key=f"{k}_form", border=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            preco = st.number_input(
                "? Pre?o (R$) *",
                min_value=0.0, format="%.2f",
                value=_v_preco,
                step=0.01, key=f"{k}_preco")
        with col2:
            frentes = st.number_input(
                "Frentes", min_value=0,
                value=_v_frentes, step=1, key=f"{k}_frt")
        with col3:
            col_of, col_pe = st.columns(2)
            oferta    = col_of.checkbox("Oferta", value=_v_oferta, key=f"{k}_of")
            ponto_extra = col_pe.checkbox("P.Extra", value=_v_pe, key=f"{k}_pe")

        ruptura = st.checkbox("?? Ruptura (sem estoque)", value=_v_ruptura, key=f"{k}_rup"

        # Nota: em st.form, os valores dos checkboxes sao lidos do session_state
        # apos submit para garantir valores corretos
        _oferta_val = st.session_state.get(f"{k}_of", oferta)
        _pe_val = st.session_state.get(f"{k}_pe", ponto_extra)
        _rup_val = st.session_state.get(f"{k}_rup", ruptura)


        # Coleta por Kg - peso aparece abaixo quando Kg selecionado
        peso_coleta = None
        preco_kg = None
        if unidade_coleta == "Kg":'''

# Busca esta sequencia no arquivo
idx = src.find('        # Coleta por Kg - peso aparece abaixo quando Kg selecionado\n        peso_coleta = None\n        preco_kg = None\n        if unidade_coleta == "Kg":')
if idx >= 0:
    # Encontra o inicio do with st.form antes deste bloco
    form_start = src.rfind('    with st.form(key=f"{k}_form"', 0, idx)
    print(f"form_start: {form_start}, kg_block: {idx}")
    
    # Encontra a linha do col1 apos o form
    col1_start = src.find('        col1, col2, col3 = st.columns(3)', form_start)
    preco_block_start = src.find('        with col1:\n            preco = st.number_input(\n                "? Pre?o (R$) *"', col1_start)
    print(f"preco_block: {preco_block_start}")

# Substitui direto: adiciona selectbox de unidade ao lado do preco
# e define unidade_coleta antes do if
OLD2 = '        # Coleta por Kg - peso aparece abaixo quando Kg selecionado\n        peso_coleta = None\n        preco_kg = None\n        if unidade_coleta == "Kg":'

NEW2 = '''        # Coleta por Kg
        _cu_col = st.columns([2, 1, 2])
        unidade_coleta = _cu_col[1].selectbox("Unidade", ["UN", "Kg"], key=f"{k}_un")
        peso_coleta = None
        preco_kg = None
        if unidade_coleta == "Kg":'''

src2 = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
if OLD2 in src2:
    src2 = src2.replace(OLD2, NEW2, 1)
    pathlib.Path("pesquisa.py").write_text(src2, encoding="utf-8")
    print("OK: unidade_coleta definido antes do if")
else:
    print("NAO ENCONTRADO")
