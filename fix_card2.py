#!/usr/bin/env python3
import pathlib

lines = pathlib.Path("pesquisa.py").read_text(encoding="utf-8").splitlines()

# Encontra fim do form na segunda instancia
start_c2 = 4160  # linha 4161, index 4160
end_c2 = None
for i in range(start_c2, start_c2 + 40):
    if 'obs = st.text_input' in lines[i]:
        end_c2 = i + 1
        break

print(f"Segunda instancia form: linhas {start_c2+1} a {end_c2+1}")

novo_form2 = [
    '            with st.form(f"form_{key_prefix}"):',
    '                # Linha 1: Preco | Unidade | Frentes',
    '                c1, c2, c3 = st.columns([3, 1.5, 2])',
    '                preco = c1.number_input("\U0001f4b0 Pre\u00e7o (R$) *",',
    '                    min_value=0.0, format="%.2f", value=float(preco_d or 0),',
    '                    step=0.01, key=f"preco_{key_prefix}")',
    '                unidade_coleta = c2.selectbox("Unidade", ["UN", "Kg"],',
    '                    key=f"un_{key_prefix}")',
    '                frentes = c3.number_input("Frentes", min_value=0,',
    '                    value=int(frentes_d or 0), key=f"frentes_{key_prefix}")',
    '',
    '                # Linha 2: Oferta | P.Extra | Ruptura',
    '                c4, c5, c6 = st.columns(3)',
    '                em_oferta = c4.checkbox("\U0001f3f7\ufe0f Oferta", value=bool(oferta_d),',
    '                    key=f"oferta_{key_prefix}")',
    '                pe = c5.checkbox("\U0001f4cc P.Extra", value=bool(pe_d),',
    '                    key=f"pe_{key_prefix}")',
    '                ruptura = c6.checkbox("\u26a0\ufe0f Ruptura", value=bool(ruptura_d),',
    '                    key=f"ruptura_{key_prefix}")',
    '',
    '                # Linha 3: Peso (se Kg) + Tipo ponto extra + Obs',
    '                peso_coleta = None',
    '                preco_kg = None',
    '                if unidade_coleta == "Kg":',
    '                    _cp, _cpkg = st.columns([2, 2])',
    '                    peso_coleta = _cp.number_input("Peso coletado (Kg)",',
    '                        min_value=0.001, value=1.0, step=0.001,',
    '                        format="%.3f", key=f"peso_{key_prefix}")',
    '                    if peso_coleta and preco > 0:',
    '                        preco_kg = round(preco / peso_coleta, 2)',
    '                        _cpkg.metric("Pre\u00e7o/Kg", f"R$ {preco_kg:.2f}")',
    '',
    '                tpe = None',
    '                if pe:',
    '                    tpe = st.selectbox("Tipo de ponto extra", TIPOS_PONTO_EXTRA,',
    '                        index=TIPOS_PONTO_EXTRA.index(tpe_d)',
    '                              if tpe_d in TIPOS_PONTO_EXTRA else 0,',
    '                        key=f"tpe_{key_prefix}")',
    '                obs = st.text_input("Observa\u00e7\u00e3o", value=obs_d or "",',
    '                    key=f"obs_{key_prefix}")',
]

new_lines = lines[:start_c2] + novo_form2 + lines[end_c2:]
pathlib.Path("pesquisa.py").write_text('\n'.join(new_lines), encoding="utf-8")
print(f"OK: {end_c2-start_c2} linhas -> {len(novo_form2)} linhas")
