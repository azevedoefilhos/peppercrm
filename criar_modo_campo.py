#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
original = src

# 1. Substitui os 3 botoes de modo por 2 (Classico + Campo)
OLD_BOTOES = '''    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        if st.button(
            "📋 Clássico" if st.session_state[modo_key] != "classico" else "📋 Clássico ✓",
            use_container_width=True,
            type="primary" if st.session_state[modo_key] == "classico" else "secondary",
            key="btn_modo_classico",
            help="Seleciona produto de referência e coleta concorrentes vinculados"
        ):
            st.session_state[modo_key] = "classico"; st.rerun()
    with col_m2:
        if st.button(
            "⚡ Rápido" if st.session_state[modo_key] != "rapido" else "⚡ Rápido ✓",
            use_container_width=True,
            type="primary" if st.session_state[modo_key] == "rapido" else "secondary",
            key="btn_modo_rapido",
            help="Navega por categoria e marca — nossos e concorrentes numa lista"
        ):
            st.session_state[modo_key] = "rapido"; st.rerun()
    with col_m3:
        if st.button(
            "🔢 Por EAN" if st.session_state[modo_key] != "ean" else "🔢 Por EAN ✓",
            use_container_width=True,
            type="primary" if st.session_state[modo_key] == "ean" else "secondary",
            key="btn_modo_ean",
            help="Digite o EAN-13 — app identifica o produto automaticamente"
        ):
            st.session_state[modo_key] = "ean"; st.rerun()'''

NEW_BOTOES = '''    col_m1, col_m2 = st.columns(2)
    with col_m1:
        if st.button(
            "📋 Clássico" if st.session_state[modo_key] != "classico" else "📋 Clássico ✓",
            use_container_width=True,
            type="primary" if st.session_state[modo_key] == "classico" else "secondary",
            key="btn_modo_classico",
            help="Seleciona produto de referência e coleta concorrentes vinculados"
        ):
            st.session_state[modo_key] = "classico"; st.rerun()
    with col_m2:
        if st.button(
            "⚡ Campo" if st.session_state[modo_key] != "campo" else "⚡ Campo ✓",
            use_container_width=True,
            type="primary" if st.session_state[modo_key] == "campo" else "secondary",
            key="btn_modo_campo",
            help="Escanear EAN ou buscar por nome/categoria — modo campo unificado"
        ):
            st.session_state[modo_key] = "campo"; st.rerun()'''

if OLD_BOTOES in src:
    src = src.replace(OLD_BOTOES, NEW_BOTOES, 1)
    print("✅ Botões substituídos")
else:
    print("⚠️  Botões não encontrados")

# 2. Substitui o dispatch dos modos
OLD_DISPATCH = '''    if st.session_state[modo_key] == "classico":
        _coleta_modo_classico(pq_id, forn_id)
    elif st.session_state[modo_key] == "rapido":
        _coleta_modo_rapido(pq_id, forn_id)
    else:
        _coleta_modo_ean(pq_id, forn_id)'''

NEW_DISPATCH = '''    if st.session_state[modo_key] == "classico":
        _coleta_modo_classico(pq_id, forn_id)
    else:
        # Modo campo: padrao para novas pesquisas
        if st.session_state[modo_key] not in ("campo", "classico"):
            st.session_state[modo_key] = "campo"
        _coleta_modo_campo(pq_id, forn_id)'''

if OLD_DISPATCH in src:
    src = src.replace(OLD_DISPATCH, NEW_DISPATCH, 1)
    print("✅ Dispatch atualizado")
else:
    print("⚠️  Dispatch não encontrado")

# 3. Muda o modo padrao de "classico" para "campo"
OLD_DEFAULT = '        st.session_state[modo_key] = "classico"'
NEW_DEFAULT = '        st.session_state[modo_key] = "campo"'

if OLD_DEFAULT in src:
    src = src.replace(OLD_DEFAULT, NEW_DEFAULT, 1)
    print("✅ Modo padrão alterado para campo")
else:
    print("⚠️  Modo padrão não encontrado")

if src != original:
    pathlib.Path("pesquisa.py").write_text(src, encoding="utf-8")
    print("Arquivo salvo")
