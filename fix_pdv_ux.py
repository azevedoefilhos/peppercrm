#!/usr/bin/env python3
import pathlib

src = pathlib.Path("cadastros.py").read_text(encoding="utf-8")
original = src

# Fix 1: Cliente para novo PDV nao deve pre-selecionar o primeiro
# Adiciona opcao vazia e exige selecao
OLD1 = '''    cli_novo_opts = [(c[0],c[1]) for c in clientes_all] if clientes_all else []
    if not cli_novo_opts:
        st.info("Cadastre um cliente primeiro."); return
    cli_novo_idx = next((i for i,c in enumerate(cli_novo_opts) if c[0]==cli_fil[0]), 0)
    cli_novo = st.selectbox("Cliente para novo PDV", cli_novo_opts,
                            index=cli_novo_idx,
                            format_func=lambda x: x[1], key="pdv_cli_novo")
    st.subheader("Novo PDV")
    _form_novo_pdv(cli_novo[0])'''

NEW1 = '''    # Novo PDV - cliente deve ser selecionado explicitamente
    st.subheader("➕ Novo PDV")
    cli_novo_opts = [(None, "— Selecione o cliente —")] + [(c[0],c[1]) for c in clientes_all] if clientes_all else []
    if not cli_novo_opts or len(cli_novo_opts) <= 1:
        st.info("Cadastre um cliente primeiro."); return
    cli_novo = st.selectbox("Cliente *", cli_novo_opts,
                            index=0,
                            format_func=lambda x: x[1], key="pdv_cli_novo")
    if not cli_novo or not cli_novo[0]:
        st.warning("⚠️ Selecione o cliente antes de cadastrar o PDV.")
    else:
        _form_novo_pdv(cli_novo[0])'''

if OLD1 in src:
    src = src.replace(OLD1, NEW1, 1)
    print("✅ Fix 1: cliente obrigatório no novo PDV")
else:
    print("⚠️  Fix 1 não encontrado")

# Fix 2: Form de edição só abre quando usuário clicar em "Editar"
OLD2 = '''        if st.session_state.get("pdv_excluir_id") == sel[0]:
            _confirmacao_excluir_pdv(sel[0], sel[1])
        elif sel:
            _form_editar_pdv(sel[0])'''

NEW2 = '''        if st.session_state.get("pdv_excluir_id") == sel[0]:
            _confirmacao_excluir_pdv(sel[0], sel[1])
        elif sel:
            _editar_key = f"pdv_editar_{sel[0]}"
            if st.session_state.get(_editar_key):
                _form_editar_pdv(sel[0])
                if st.button("✖️ Fechar edição", key=f"fechar_pdv_{sel[0]}"):
                    st.session_state.pop(_editar_key, None)
                    st.rerun()
            else:
                if st.button("✏️ Editar PDV selecionado", key=f"btn_editar_pdv_{sel[0]}",
                             type="primary", use_container_width=True):
                    st.session_state[_editar_key] = True
                    st.rerun()'''

if OLD2 in src:
    src = src.replace(OLD2, NEW2, 1)
    print("✅ Fix 2: edição só abre ao clicar")
else:
    print("⚠️  Fix 2 não encontrado")

# Fix 3: Adiciona campo status no form novo PDV
OLD3 = '''        obs    = st.text_area("Observacao")
        salvar = st.form_submit_button("Salvar PDV", type="primary")'''

NEW3 = '''        status_pdv = st.selectbox("Status do PDV *",
                                   ["Prospecto", "Ativo", "Inativo", "Bloqueado"],
                                   index=0,
                                   key="pdv_status_novo",
                                   help="Prospecto = cliente em prospecção, ainda não compra")
        obs    = st.text_area("Observacao")
        salvar = st.form_submit_button("Salvar PDV", type="primary")'''

if OLD3 in src:
    src = src.replace(OLD3, NEW3, 1)
    print("✅ Fix 3: campo status adicionado")
else:
    print("⚠️  Fix 3 não encontrado")

# Fix 4: Usar status_pdv no INSERT em vez de ativo=1 fixo
OLD4 = '''             horario_recebimento, setor, cluster, tamanho_pdv, observacao, ativo)'''
NEW4 = '''             horario_recebimento, setor, cluster, tamanho_pdv, observacao, status, ativo)'''

if OLD4 in src:
    src = src.replace(OLD4, NEW4, 1)
    print("✅ Fix 4: status no INSERT")
else:
    print("⚠️  Fix 4 não encontrado")

# Ver o VALUES do INSERT para completar
lines = src.splitlines()
for i, l in enumerate(lines, 1):
    if 'horario_recebimento, setor, cluster' in l and 'VALUES' in lines[i] if i < len(lines) else False:
        print(f"Linha {i+1}: {lines[i][:85]}")

if src != original:
    pathlib.Path("cadastros.py").write_text(src, encoding="utf-8")
    print("Salvo")
