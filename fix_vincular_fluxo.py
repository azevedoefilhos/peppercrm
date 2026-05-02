#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
original = src

OLD = '''                    st.session_state[f"ean_vinculado_{pq_id}"] = sel_vinc[0]
                    st.session_state.pop(f"ean_input_{pq_id}", None)
                    st.success(f"✅ EAN vinculado! Relançando pesquisa...")
                    st.rerun()'''

NEW = '''                    st.session_state[f"ean_vinculado_{pq_id}"] = sel_vinc[0]
                    # Mantém o EAN no campo para que o lookup encontre o produto recém vinculado
                    st.session_state[f"ean_vinc_ok_redirect_{pq_id}"] = ean
                    st.success(f"✅ EAN vinculado! Abrindo campos de preço...")
                    st.rerun()'''

if OLD in src:
    src = src.replace(OLD, NEW, 1)
    print("✅ Fix 1: redirect após vincular")
else:
    print("⚠️  Fix 1 não encontrado")

# Adiciona verificação do redirect no início da função _coleta_modo_ean
OLD2 = '''    # ── LOOKUP LOCAL ──────────────────────────────────────────────────────
    resultado = _lookup_ean_local(ean)'''

NEW2 = '''    # Verifica se veio de uma vinculação recente
    _redirect_ean = st.session_state.pop(f"ean_vinc_ok_redirect_{pq_id}", None)
    if _redirect_ean:
        ean = _redirect_ean

    # ── LOOKUP LOCAL ──────────────────────────────────────────────────────
    resultado = _lookup_ean_local(ean)'''

if OLD2 in src:
    src = src.replace(OLD2, NEW2, 1)
    print("✅ Fix 2: redirect interceptado antes do lookup")
else:
    print("⚠️  Fix 2 não encontrado")

if src != original:
    pathlib.Path("pesquisa.py").write_text(src, encoding="utf-8")
    print("Salvo")
