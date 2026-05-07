#!/usr/bin/env python3
import pathlib

lines = pathlib.Path("pesquisa.py").read_text(encoding="utf-8").splitlines()

# === FIX MODO RAPIDO (linhas 3320-3358) ===
# Substitui linhas 3320-3358 (indices 3319-3357) pelo novo layout
novo_rapido = [
    '    with st.form(key=f"{k}_form", border=True):',
    '        # Linha 1: Preco | Unidade | Frentes | Oferta | P.Extra',
    '        c1, c2, c3, c4, c5 = st.columns([2.5, 1.2, 1.5, 1, 1])',
    '        preco = c1.number_input("\U0001f4b0 Preço (R$) *", min_value=0.0,',
    '                    format="%.2f", value=_v_preco, step=0.01, key=f"{k}_preco")',
    '        unidade_coleta = c2.selectbox("Unidade", ["UN", "Kg"], key=f"{k}_un")',
    '        frentes = c3.number_input("Frentes", min_value=0,',
    '                    value=_v_frentes, step=1, key=f"{k}_frt")',
    '        c4.write(""); oferta = c4.checkbox("Oferta", value=_v_oferta, key=f"{k}_of")',
    '        c5.write(""); ponto_extra = c5.checkbox("P.Extra", value=_v_pe, key=f"{k}_pe")',
    '',
    '        # Linha 2: Ruptura + Peso (se Kg)',
    '        _rc, _pc, _pkgc = st.columns([2, 2, 2])',
    '        ruptura = _rc.checkbox("⚠️ Ruptura (sem estoque)", value=_v_ruptura, key=f"{k}_rup")',
    '        peso_coleta = None',
    '        preco_kg = None',
    '        if unidade_coleta == "Kg":',
    '            peso_coleta = _pc.number_input("Peso (Kg)", min_value=0.001, value=1.0,',
    '                step=0.001, format="%.3f", key=f"{k}_peso")',
    '            if peso_coleta and preco > 0:',
    '                preco_kg = round(preco / peso_coleta, 2)',
    '                _pkgc.metric("R$/Kg", f"{preco_kg:.2f}")',
    '',
    '        # Leitura dos checkboxes do session_state',
    '        _oferta_val = st.session_state.get(f"{k}_of", oferta)',
    '        _pe_val     = st.session_state.get(f"{k}_pe", ponto_extra)',
    '        _rup_val    = st.session_state.get(f"{k}_rup", ruptura)',
]

# Encontra inicio e fim do bloco modo rapido
start_r = None
end_r = None
for i, l in enumerate(lines):
    if i > 3300 and '    with st.form(key=f"{k}_form", border=True):' in l and start_r is None:
        start_r = i
    if start_r and i > start_r + 5 and '        _oferta_val = st.session_state.get' in l:
        end_r = i + 3  # inclui as 3 linhas de session_state
        break

print(f"Modo rapido: linhas {start_r+1} a {end_r+1}")

# === FIX MODO CLASSICO (linhas 2270-2295) ===
novo_classico = [
    '            with st.form(f"form_{key_prefix}"):',
    '                # Linha 1: Preco | Unidade | Frentes | Oferta | P.Extra',
    '                c1, c2, c3, c4, c5 = st.columns([2.5, 1.2, 1.5, 1, 1])',
    '                preco = c1.number_input("\U0001f4b0 Preço (R$) *", min_value=0.0,',
    '                    value=float(preco_d or 0), step=0.01, format="%.2f",',
    '                    key=f"preco_{key_prefix}")',
    '                unidade_coleta = c2.selectbox("Unidade", ["UN", "Kg"],',
    '                    key=f"un_{key_prefix}")',
    '                frentes = c3.number_input("Frentes", min_value=0,',
    '                    value=int(frentes_d or 0), key=f"frentes_{key_prefix}")',
    '                c4.write(""); em_oferta = c4.checkbox("Oferta", value=bool(oferta_d),',
    '                    key=f"oferta_{key_prefix}")',
    '                c5.write(""); pe = c5.checkbox("P.Extra", value=bool(pe_d),',
    '                    key=f"pe_{key_prefix}")',
    '',
    '                # Linha 2: Ruptura | Peso (se Kg)',
    '                _rc2, _pc2, _pkgc2 = st.columns([2, 2, 2])',
    '                ruptura = _rc2.checkbox("⚠️ Ruptura (ausente)", value=bool(ruptura_d),',
    '                    key=f"ruptura_{key_prefix}")',
    '                peso_coleta = None',
    '                preco_kg = None',
    '                if unidade_coleta == "Kg":',
    '                    peso_coleta = _pc2.number_input("Peso (Kg)", min_value=0.001,',
    '                        value=1.0, step=0.001, format="%.3f", key=f"peso_{key_prefix}")',
    '                    if peso_coleta and preco > 0:',
    '                        preco_kg = round(preco / peso_coleta, 2)',
    '                        _pkgc2.metric("R$/Kg", f"{preco_kg:.2f}")',
    '',
    '                tpe = None',
    '                if pe:',
    '                    tpe = st.selectbox("Tipo de ponto extra", TIPOS_PONTO_EXTRA,',
    '                                       index=TIPOS_PONTO_EXTRA.index(tpe_d)',
    '                                             if tpe_d in TIPOS_PONTO_EXTRA else 0,',
    '                                       key=f"tpe_{key_prefix}")',
    '                obs = st.text_input("Observação", value=obs_d or "",',
    '                                    key=f"obs_{key_prefix}")',
]

start_c = None
end_c = None
for i, l in enumerate(lines):
    if '            with st.form(f"form_{key_prefix}"):' in l:
        start_c = i
    if start_c and i > start_c + 5 and '                obs = st.text_input' in l:
        end_c = i + 1
        break

print(f"Modo classico: linhas {start_c+1} a {end_c+1}")

# Aplica fixes (do fim para o inicio para nao deslocar indices)
new_lines = lines.copy()

if start_c and end_c:
    new_lines = new_lines[:start_c] + novo_classico + new_lines[end_c:]
    print("OK Fix classico")

if start_r and end_r:
    new_lines = new_lines[:start_r] + novo_rapido + new_lines[end_r:]
    print("OK Fix rapido")

pathlib.Path("pesquisa.py").write_text('\n'.join(new_lines), encoding="utf-8")
print("Salvo!")
