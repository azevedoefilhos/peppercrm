import pathlib

lines = pathlib.Path("pesquisa.py").read_text(encoding="utf-8").splitlines()

# Encontra o bloco atual na segunda instancia
start = None
end = None
for i in range(3060, 3140):
    if '# CSS' in lines[i] and 'pesquisado' in lines[i] and start is None:
        start = i
    if start and 'st.rerun()' in lines[i] and i > start + 20:
        end = i + 1
        break

print(f"Bloco: {start+1} a {end}")

novo_botoes = [
    '    # CSS: botoes pesquisados em verde elegante',
    '    st.markdown("""<style>',
    '    div[class*="campo_nav_"] button[kind="primary"] {',
    '        background-color: #2E7D32 !important;',
    '        border-color: #2E7D32 !important;',
    '        color: white !important;',
    '    }',
    '    div[class*="campo_nav_"] button[kind="primary"]:hover {',
    '        background-color: #1B5E20 !important;',
    '    }',
    '    </style>""", unsafe_allow_html=True)',
    '',
    '    if nossos:',
    '        st.markdown("**\U0001f7e2 Nossos:**")',
    '        for pid, desc, marca in nossos:',
    '            _label = _lbl("n", pid, marca, desc)',
    '            _pesquisado = _mp.get(("n", pid)) is not None',
    '            if st.button(_label, key=f"campo_nav_n_{pq_id}_{pid}",',
    '                        use_container_width=True,',
    '                        type="primary" if _pesquisado else "secondary"):',
    '                resultado = {"tipo":"nosso","produto_id":pid,',
    '                            "descricao":desc,"marca":marca,"ean":None,"pc_id":None}',
    '                st.session_state[f"nav_produto_pendente_{pq_id}"] = {',
    '                    "resultado": resultado, "ean": ""}',
    '                st.rerun()',
    '',
    '    if concs:',
    '        st.markdown("**\U0001f534 Concorrentes:**")',
    '        for pc_id, desc, marca, ean in concs:',
    '            _label = _lbl("c", pc_id, marca, desc)',
    '            _pesquisado = _mp.get(("c", pc_id)) is not None',
    '            if st.button(_label, key=f"campo_nav_c_{pq_id}_{pc_id}",',
    '                        use_container_width=True,',
    '                        type="primary" if _pesquisado else "secondary"):',
    '                resultado = {"tipo":"conc","pc_id":pc_id,',
    '                            "descricao":desc,"marca":marca,',
    '                            "ean":ean,"auditavel":1}',
    '                st.session_state[f"nav_produto_pendente_{pq_id}"] = {',
    '                    "resultado": resultado, "ean": ean or ""}',
    '                st.rerun()',
]

new_lines = lines[:start] + novo_botoes + lines[end:]
pathlib.Path("pesquisa.py").write_text('\n'.join(new_lines), encoding="utf-8")
print(f"OK: {end-start} -> {len(novo_botoes)} linhas")
