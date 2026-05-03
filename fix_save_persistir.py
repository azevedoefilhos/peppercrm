#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
original = src

# O problema: nav_produto_pendente é lido e removido em _campo_navegacao
# antes de _form_coleta_rapida_ean ser chamado
# Quando o form faz submit (rerun), nav_produto_pendente já foi removido
# entao _campo_navegacao nao chama _form_coleta_rapida_ean novamente

# Fix: nao remover nav_produto_pendente no inicio de _campo_navegacao
# so remover APOS o save bem-sucedido (ja esta no bloco de save)

OLD = '''    # Verifica se ha produto pendente (apos rerun do confirmar)
    _prod_pendente = st.session_state.get(f"nav_produto_pendente_{pq_id}")
    if _prod_pendente:
        st.session_state.pop(f"nav_produto_pendente_{pq_id}", None)
        _coleta_ean_produto_encontrado(pq_id, forn_id, _prod_pendente["resultado"],
                                       _prod_pendente["ean"])
        return'''

NEW = '''    # Verifica se ha produto pendente (apos rerun do confirmar ou submit do form)
    _prod_pendente = st.session_state.get(f"nav_produto_pendente_{pq_id}")
    if _prod_pendente:
        # NAO remove aqui - so remove apos save bem-sucedido
        _coleta_ean_produto_encontrado(pq_id, forn_id, _prod_pendente["resultado"],
                                       _prod_pendente["ean"])
        return'''

if OLD in src:
    src = src.replace(OLD, NEW, 1)
    print("✅ Fix: nav_produto_pendente preservado durante submit")
else:
    print("⚠️  Padrão não encontrado")

if src != original:
    pathlib.Path("pesquisa.py").write_text(src, encoding="utf-8")
    print("Salvo")
