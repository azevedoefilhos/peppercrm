#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
original = src

# Fix: salvar produto selecionado no session_state ao clicar
# e verificar no inicio da _campo_navegacao se ha produto pendente

OLD_NAV_NOSSO = '''    if nossos:
        st.markdown("**\U0001f7e2 Nossos:**")
        for pid, desc, marca in nossos:
            if st.button(f"{marca} \u2014 {desc}",
                        key=f"campo_nav_n_{pq_id}_{pid}",
                        use_container_width=True):
                resultado = {"tipo":"nosso","produto_id":pid,
                            "descricao":desc,"marca":marca,"ean":None,"pc_id":None}
                _coleta_ean_produto_encontrado(pq_id, forn_id, resultado, "")

    if concs:
        st.markdown("**\U0001f534 Concorrentes:**")
        for pc_id, desc, marca, ean in concs:'''

NEW_NAV_NOSSO = '''    # Verifica se ha produto pendente (apos rerun do confirmar)
    _prod_pendente = st.session_state.get(f"nav_produto_pendente_{pq_id}")
    if _prod_pendente:
        st.session_state.pop(f"nav_produto_pendente_{pq_id}", None)
        _coleta_ean_produto_encontrado(pq_id, forn_id, _prod_pendente["resultado"],
                                       _prod_pendente["ean"])
        return

    if nossos:
        st.markdown("**\U0001f7e2 Nossos:**")
        for pid, desc, marca in nossos:
            if st.button(f"{marca} \u2014 {desc}",
                        key=f"campo_nav_n_{pq_id}_{pid}",
                        use_container_width=True):
                resultado = {"tipo":"nosso","produto_id":pid,
                            "descricao":desc,"marca":marca,"ean":None,"pc_id":None}
                st.session_state[f"nav_produto_pendente_{pq_id}"] = {
                    "resultado": resultado, "ean": ""}
                st.rerun()

    if concs:
        st.markdown("**\U0001f534 Concorrentes:**")
        for pc_id, desc, marca, ean in concs:'''

if OLD_NAV_NOSSO in src:
    src = src.replace(OLD_NAV_NOSSO, NEW_NAV_NOSSO, 1)
    print("✅ Fix nossos aplicado")
else:
    print("⚠️  Padrão nossos não encontrado")

# Fix concs tambem
OLD_NAV_CONCS = '''            if st.button(f"{marca} \u2014 {desc}",
                        key=f"campo_nav_c_{pq_id}_{pc_id}",
                        use_container_width=True):
                resultado = {"tipo":"conc","pc_id":pc_id,
                            "descricao":desc,"marca":marca,
                            "ean":ean,"auditavel":1}
                _coleta_ean_produto_encontrado(pq_id, forn_id, resultado,
                                               ean or "")'''

NEW_NAV_CONCS = '''            if st.button(f"{marca} \u2014 {desc}",
                        key=f"campo_nav_c_{pq_id}_{pc_id}",
                        use_container_width=True):
                resultado = {"tipo":"conc","pc_id":pc_id,
                            "descricao":desc,"marca":marca,
                            "ean":ean,"auditavel":1}
                st.session_state[f"nav_produto_pendente_{pq_id}"] = {
                    "resultado": resultado, "ean": ean or ""}
                st.rerun()'''

if OLD_NAV_CONCS in src:
    src = src.replace(OLD_NAV_CONCS, NEW_NAV_CONCS, 1)
    print("✅ Fix concs aplicado")
else:
    print("⚠️  Padrão concs não encontrado")

if src != original:
    pathlib.Path("pesquisa.py").write_text(src, encoding="utf-8")
    print("Salvo")
