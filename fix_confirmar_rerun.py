#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
original = src

# Fix: adiciona rerun apos confirmar + muda logica para nao mostrar form antes
OLD = '''    if _ja_existe:
        _preco_ant = _ja_existe[0][1]
        _preco_fmt = f"R$ {_preco_ant:,.2f}".replace(",","X").replace(".",",").replace("X",".")  if _preco_ant else "Ruptura"
        _confirmar_key = f"{k}_confirmar_update"
        st.warning(f"\u26a0\ufe0f **{label}** j\u00e1 foi pesquisado nesta visita (pre\u00e7o: {_preco_fmt}). Deseja atualizar?")
        col_s, col_n = st.columns(2)
        if col_s.button("\u2705 Sim, atualizar", key=f"{k}_sim", use_container_width=True):
            st.session_state[_confirmar_key] = True
        if col_n.button("\u274c N\u00e3o, pr\u00f3ximo", key=f"{k}_nao", use_container_width=True):
            st.session_state.pop(f"ean_input_{pq_id}", None)
            st.session_state.pop(f"campo_busca_{pq_id}", None)
            st.rerun()
        if not st.session_state.get(_confirmar_key):
            return'''

NEW = '''    _confirmar_key = f"{k}_confirmar_update"
    if _ja_existe and not st.session_state.get(_confirmar_key):
        _preco_ant = _ja_existe[0][1]
        _preco_fmt = f"R$ {_preco_ant:,.2f}".replace(",","X").replace(".",",").replace("X",".")  if _preco_ant else "Ruptura"
        st.warning(f"\u26a0\ufe0f **{label}** j\u00e1 foi pesquisado nesta visita (pre\u00e7o: {_preco_fmt}). Deseja atualizar?")
        col_s, col_n = st.columns(2)
        if col_s.button("\u2705 Sim, atualizar", key=f"{k}_sim", use_container_width=True):
            st.session_state[_confirmar_key] = True
            st.rerun()
        if col_n.button("\u274c N\u00e3o, pr\u00f3ximo", key=f"{k}_nao", use_container_width=True):
            st.session_state.pop(f"ean_input_{pq_id}", None)
            st.session_state.pop(f"campo_busca_{pq_id}", None)
            st.rerun()
        return'''

if OLD in src:
    src = src.replace(OLD, NEW, 1)
    print("OK")
else:
    # Tenta localizar e mostrar contexto
    idx = src.find('_confirmar_key = f"{k}_confirmar_update"')
    if idx >= 0:
        print("Encontrado em posicao diferente, corrigindo...")
        # Substitui apenas a linha do rerun faltante
        src = src.replace(
            '            st.session_state[_confirmar_key] = True\n        if col_n.button',
            '            st.session_state[_confirmar_key] = True\n            st.rerun()\n        if col_n.button'
        )
        # Muda a logica para nao mostrar form antes do rerun
        src = src.replace(
            '        if not st.session_state.get(_confirmar_key):\n            return',
            ''
        )
        src = src.replace(
            '    if _ja_existe:\n        _preco_ant',
            '    if _ja_existe and not st.session_state.get(_confirmar_key):\n        _preco_ant'
        )
        # Adiciona return no final do bloco
        src = src.replace(
            '            st.rerun()\n        if not st.session_state.get',
            '            st.rerun()\n        return\n        if not st.session_state.get'
        )
        print("Corrigido via fallback")
    else:
        print("NAO ENCONTRADO")

if src != original:
    pathlib.Path("pesquisa.py").write_text(src, encoding="utf-8")
    print("Salvo")
