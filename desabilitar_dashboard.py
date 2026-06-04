# desabilitar_dashboard.py
f = open('crm_app.py', encoding='utf-8').read()

old = '''    # ── Dashboard DEPOIS do menu ───────────────────────────────────────────
    with st.spinner("Carregando indicadores..."):
        _dashboard()'''

new = '''    # ── Dashboard desabilitado temporariamente ────────────────────────────
    # (otimização pendente — queries muito lentas para mobile)
    pass'''

if old in f:
    f = f.replace(old, new, 1)
    open('crm_app.py', 'w', encoding='utf-8', newline='\n').write(f)
    print("OK - dashboard desabilitado")
else:
    print("ERRO - trecho nao encontrado")
