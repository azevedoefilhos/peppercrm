#!/usr/bin/env python3
"""
Aplica cache @st.cache_data nas queries mais frequentes do dashboard (crm_app.py).
O dashboard é carregado em cada interação — cachear aqui tem maior impacto.
"""
import pathlib

CAMINHO = pathlib.Path("crm_app.py")
src = CAMINHO.read_text(encoding="utf-8")

# Verifica se ja tem cache
if '@st.cache_data' in src:
    print("Cache já presente em crm_app.py")
else:
    # Adiciona cache nas queries do dashboard
    # A funcao _dashboard() é chamada a cada renderizacao
    # Vamos cachear as queries pesadas com TTL de 2 minutos

    ANTIGO = '''    # ── Coleta todos os dados ─────────────────────────────────────────────────
    def _q1(sql, p=()):
        r = query(sql, p); return r[0][0] if r else 0'''

    NOVO = '''    # ── Coleta todos os dados ─────────────────────────────────────────────────
    @st.cache_data(ttl=120, show_spinner=False)
    def _q1_cached(sql, p=()):
        r = query(sql, p); return r[0][0] if r else 0

    def _q1(sql, p=()):
        return _q1_cached(sql, p)'''

    if ANTIGO in src:
        src2 = src.replace(ANTIGO, NOVO, 1)
        CAMINHO.write_text(src2, encoding="utf-8")
        print("✅ Cache adicionado no dashboard _q1")
    else:
        print("⚠️  Padrão _q1 não encontrado — verifique manualmente")

# Verifica imports
src = CAMINHO.read_text(encoding="utf-8")
print(f"@st.cache_data presente: {'@st.cache_data' in src}")
