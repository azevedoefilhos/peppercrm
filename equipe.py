# equipe.py — PepperCRM
# Modulo de gestao da equipe comercial e de campo

import streamlit as st
import hashlib, secrets, string, urllib.parse
from database import query, execute_write, conectar
from permissoes import e_admin, e_master, exigir_admin, empresa_id_atual, usuario_id_atual

def _ir(p):
    st.session_state["pagina"] = p; st.rerun()

def _hash(s):
    return hashlib.sha256(s.encode()).hexdigest()

def _gerar_senha(n=10):
    return "".join(secrets.choice(string.ascii_letters+string.digits+"!@#") for _ in range(n))

def _ufs():
    return ["AC","AL","AM","AP","BA","CE","DF","ES","GO","MA","MG","MS","MT",
            "PA","PB","PE","PI","PR","RJ","RN","RO","RR","RS","SC","SE","SP","TO"]

def _link_wa(fone, msg):
    num = "".join(filter(str.isdigit, fone or ""))
    if not num.startswith("55"): num = "55" + num
    return f"https://wa.me/{num}?text={urllib.parse.quote(msg)}"

def _msg_acesso(nome, login, senha):
    return (f"Ola {nome.split()[0]}! Seu acesso ao *PepperCRM* esta pronto.\n\n"
            f"🌐 https://peppercrm-production.up.railway.app\n"
            f"👤 *Login:* {login}\n🔑 *Senha:* {senha}\n\n"
            f"Salve o link como favorito no celular!")

def tela_equipe():
    exigir_admin()
    st.header("👥 Equipe")
    if st.button("⬅ Voltar"): _ir("home")

    ABAS = {
        "vend": "💼 Vendedores",
        "prom": "👤 Promotores",
        "pv":   "👤💼 Promotor Vendedor",
        "sup":  "🎯 Supervisores",
    }
    if "eq_aba" not in st.session_state: st.session_state["eq_aba"] = "vend"
    cols = st.columns(len(ABAS))
    for col,(k,v) in zip(cols, ABAS.items()):
        ativa = st.session_state["eq_aba"] == k
        if col.button(v, key=f"eqnav_{k}", width="stretch",
                      type="primary" if ativa else "secondary"):
            st.session_state["eq_aba"] = k; st.rerun()
    st.divider()

    a = st.session_state["eq_aba"]
    if a == "vend": _tela_vendedores()
    elif a == "prom": _tela_promotores()
    elif a == "pv":   _tela_promotores_vendedores()
    elif a == "sup":  _tela_supervisores()


# ═══════════════════════════════════════════════════════════════
# VENDEDORES / REPRESENTANTES
# ═══════════════════════════════════════════════════════════════

def _tela_vendedores():
    eid = empresa_id_atual()
    st.subheader("💼 Vendedores / Representantes")
    st.caption("🔑 Com login no app | ⚪ Sem login")

    from permissoes import e_master as _e_master
    _is_master = _e_master()

    # Busca usuarios SEM JOIN — LEFT JOIN com vendedor falha silenciosamente com RLS
    usu_raw = query("""
        SELECT usuario_id, nome, email, whatsapp, tipo, ativo
        FROM usuario
        WHERE empresa_id=%s
          AND (tipo='REPRESENTANTE_ADM' OR tipo='REPRESENTANTE'
               OR tipo='VENDEDOR' OR tipo='MASTER')
        ORDER BY nome
    """, (eid,)) or []

    # Busca vendedores separadamente
    vend_raw = query("""
        SELECT vendedor_id, usuario_id, fone, cidade
        FROM vendedor WHERE empresa_id=%s AND ativo!=0
    """, (eid,)) or []
    vend_map = {v[1]: v for v in vend_raw if v[1]}

    # Combina em memoria sem JOIN
    vends_u = []
    for u in usu_raw:
        uid, nome, email, wa, tipo, ativo = u[0], u[1], u[2], u[3], u[4], u[5]
        v = vend_map.get(uid)
        vends_u.append((uid, nome, email, wa, tipo, ativo,
                        v[0] if v else None,
                        v[2] if v else None,
                        v[3] if v else None))

    # Vendedores legados sem usuario
    vends_leg = query("""
        SELECT vendedor_id, nome, email, whatsapp, fone, cidade
        FROM vendedor WHERE empresa_id=%s AND usuario_id IS NULL AND ativo!=0
        ORDER BY nome
    """, (eid,)) or []

    vends = vends_u

    if st.session_state.get("eq_vend_msg"):
        st.success(st.session_state.pop("eq_vend_msg"))

    if not vends and not vends_leg:
        st.info("Nenhum vendedor/representante cadastrado.")

    if vends:
        for v in vends:
            uid, nome, email, wa, tipo, ativo, vid, fone, cidade = v
            icon = "✅" if ativo else "❌"
            login_icon = "🔑"
            with st.expander(f"{icon} {login_icon} {nome} | {tipo} | {cidade or '—'}"):
                col1, col2, col3 = st.columns(3)
                col1.write(f"**Login:** {email}")
                col2.write(f"**WhatsApp:** {wa or fone or '—'}")
                col3.write(f"**Status:** {'Ativo' if ativo else 'Inativo'}")

                with st.expander("✏️ Editar dados"):
                    e_nome  = st.text_input("Nome", value=nome, key=f"ev_n_{uid}")
                    e_wa    = st.text_input("WhatsApp", value=wa or "", key=f"ev_w_{uid}")
                    e_email = st.text_input("Email/login", value=email, key=f"ev_e_{uid}")
                    e_cidade = st.text_input("Cidade", value=cidade or "", key=f"ev_c_{uid}")
                    if st.button("💾 Salvar", key=f"ev_sv_{uid}", type="primary"):
                        execute_write("UPDATE usuario SET nome=%s, whatsapp=%s, email=%s WHERE usuario_id=%s",
                                      (e_nome.strip(), e_wa.strip() or None, e_email.strip().lower(), uid))
                        if vid:
                            execute_write("UPDATE vendedor SET nome=%s, whatsapp=%s, cidade=%s WHERE vendedor_id=%s",
                                          (e_nome.strip(), e_wa.strip() or None, e_cidade.strip() or None, vid))
                        st.session_state["eq_vend_msg"] = "✅ Dados atualizados."
                        st.rerun()

                col_a, col_b = st.columns(2)
                if ativo:
                    if col_a.button("❌ Desativar", key=f"ev_des_{uid}"):
                        n_cli = (query("SELECT COUNT(*) FROM cliente WHERE vendedor_id=%s", (uid,)) or [[0]])[0][0]
                        if n_cli > 0:
                            st.warning(f"Este vendedor tem {n_cli} cliente(s). Redistribua em Usuários → Carteira.")
                        else:
                            execute_write("UPDATE usuario SET ativo=0 WHERE usuario_id=%s", (uid,))
                            execute_write("UPDATE sessao_token SET ativo=0 WHERE usuario_id=%s", (uid,))
                            st.session_state["eq_vend_msg"] = f"{nome} desativado."
                            st.rerun()
                else:
                    if col_a.button("✅ Reativar", key=f"ev_rea_{uid}"):
                        execute_write("UPDATE usuario SET ativo=1 WHERE usuario_id=%s", (uid,))
                        st.session_state["eq_vend_msg"] = f"{nome} reativado."
                        st.rerun()

                if col_b.button("🔑 Nova senha", key=f"ev_pwd_{uid}"):
                    nova = _gerar_senha()
                    execute_write("UPDATE usuario SET senha_hash=%s WHERE usuario_id=%s",
                                  (_hash(nova), uid))
                    execute_write("UPDATE sessao_token SET ativo=0 WHERE usuario_id=%s", (uid,))
                    wa_num = wa or fone or ""
                    if wa_num:
                        link = _link_wa(wa_num, _msg_acesso(nome, email, nova))
                        st.markdown(f'<a href="{link}" target="_blank"><button style="background:#25D366;color:white;border:none;padding:8px 16px;border-radius:6px;cursor:pointer;width:100%">💬 Enviar nova senha via WhatsApp</button></a>', unsafe_allow_html=True)
                    st.info(f"Nova senha: **{nova}**")
    else:
        st.info("Nenhum vendedor/representante cadastrado.")

    # Vendedores legados (tabela vendedor sem usuario vinculado)
    if vends_leg:
        st.divider()
        st.markdown("**Vendedores sem login vinculado** _(cadastrados anteriormente)_")
        for v in vends_leg:
            vid, nome, email, wa, fone, cidade = v
            with st.expander(f"⚪ {nome} | {cidade or '—'} | {fone or '—'}"):
                st.caption("Este vendedor não tem login. Vincule a um usuário ou crie um login.")
                # Vincular a usuario existente
                usu_disp = query("""SELECT usuario_id, nome FROM usuario
                    WHERE empresa_id=%s AND tipo IN ('REPRESENTANTE_ADM','REPRESENTANTE','VENDEDOR')
                    AND usuario_id NOT IN (SELECT usuario_id FROM vendedor WHERE usuario_id IS NOT NULL)
                    ORDER BY nome""", (eid,)) or []
                if usu_disp:
                    opts = [(None, "— Selecione um usuário —")] + [(u[0], u[1]) for u in usu_disp]
                    usel = st.selectbox("Vincular a usuário existente", opts,
                                        format_func=lambda x: x[1], key=f"vleg_u_{vid}")
                    if usel[0] and st.button("🔗 Vincular", key=f"vleg_btn_{vid}"):
                        execute_write("UPDATE vendedor SET usuario_id=%s WHERE vendedor_id=%s",
                                      (usel[0], vid))
                        st.session_state["eq_vend_msg"] = f"✅ {nome} vinculado!"
                        st.rerun()
                # Criar novo login
                if st.button("🔑 Criar novo login", key=f"vleg_login_{vid}"):
                    st.session_state[f"vleg_criar_{vid}"] = True
                if st.session_state.get(f"vleg_criar_{vid}"):
                    with st.form(f"vleg_form_{vid}"):
                        l_email = st.text_input("Email/login *", value=email or "", key=f"vleg_e_{vid}")
                        l_wa    = st.text_input("WhatsApp", value=wa or fone or "", key=f"vleg_w_{vid}")
                        l_tipo  = st.selectbox("Perfil", ['REPRESENTANTE','VENDEDOR'], key=f"vleg_t_{vid}")
                        l_senha = st.text_input("Senha", value=_gerar_senha(), key=f"vleg_s_{vid}")
                        criar   = st.form_submit_button("✅ Criar login")
                    if criar:
                        existe = query("SELECT 1 FROM usuario WHERE email=%s", (l_email.strip().lower(),))
                        if existe:
                            st.error("Email já cadastrado.")
                        else:
                            execute_write("""INSERT INTO usuario (nome,email,senha_hash,tipo,empresa_id,whatsapp,ativo)
                                VALUES (%s,%s,%s,%s,%s,%s,1)""",
                                (nome, l_email.strip().lower(), _hash(l_senha), l_tipo, eid, l_wa or None))
                            novo_uid = (query("SELECT usuario_id FROM usuario WHERE email=%s",
                                             (l_email.strip().lower(),)) or [[None]])[0][0]
                            if novo_uid:
                                execute_write("UPDATE vendedor SET usuario_id=%s WHERE vendedor_id=%s",
                                              (novo_uid, vid))
                            if l_wa:
                                link = _link_wa(l_wa, _msg_acesso(nome, l_email.strip().lower(), l_senha))
                                st.markdown(f'<a href="{link}" target="_blank"><button style="background:#25D366;color:white;border:none;padding:8px 16px;border-radius:6px;cursor:pointer;width:100%">💬 Enviar via WhatsApp</button></a>', unsafe_allow_html=True)
                            st.session_state[f"vleg_criar_{vid}"] = False
                            st.session_state["eq_vend_msg"] = f"✅ Login criado para {nome}."
                            st.rerun()

    st.divider()
    st.caption("Cria login e cadastro simultaneamente.")

    TIPOS = ['REPRESENTANTE','VENDEDOR']
    n_tipo  = st.selectbox("Tipo", TIPOS, key="nv_tipo",
                           format_func=lambda x: "Representante" if x=="REPRESENTANTE" else "Vendedor")
    n_nome  = st.text_input("Nome completo *", key="nv_nome")
    n_email = st.text_input("Email/login *", key="nv_email")
    n_wa    = st.text_input("WhatsApp", key="nv_wa", placeholder="11 9 9999-9999")
    n_cidade = st.text_input("Cidade", key="nv_cidade")
    n_senha = st.text_input("Senha inicial", key="nv_senha", value=_gerar_senha())

    if st.button("💾 Criar vendedor", key="nv_criar", type="primary"):
        if not n_nome.strip() or not n_email.strip():
            st.error("Nome e email são obrigatórios.")
        else:
            existe = query("SELECT 1 FROM usuario WHERE email=%s", (n_email.strip().lower(),))
            if existe:
                st.error("Email já cadastrado.")
            else:
                execute_write("""INSERT INTO usuario (nome,email,senha_hash,tipo,empresa_id,whatsapp,ativo)
                    VALUES (%s,%s,%s,%s,%s,%s,1)""",
                    (n_nome.strip(), n_email.strip().lower(), _hash(n_senha), n_tipo, eid,
                     n_wa.strip() or None))
                novo_uid = (query("SELECT usuario_id FROM usuario WHERE email=%s",
                                  (n_email.strip().lower(),)) or [[None]])[0][0]
                if novo_uid:
                    execute_write("""INSERT INTO vendedor (nome,whatsapp,cidade,empresa_id,usuario_id,ativo)
                        VALUES (%s,%s,%s,%s,%s,1)""",
                        (n_nome.strip(), n_wa.strip() or None, n_cidade.strip() or None, eid, novo_uid))
                st.session_state["eq_vend_msg"] = f"✅ {n_nome} criado!"
                if n_wa:
                    link = _link_wa(n_wa, _msg_acesso(n_nome, n_email.strip().lower(), n_senha))
                    st.markdown(f'<a href="{link}" target="_blank"><button style="background:#25D366;color:white;border:none;padding:8px 16px;border-radius:6px;cursor:pointer;width:100%">💬 Enviar credenciais via WhatsApp</button></a>', unsafe_allow_html=True)
                    st.info(f"Senha: **{n_senha}**")
                st.rerun()


# ═══════════════════════════════════════════════════════════════
# PROMOTORES
# ═══════════════════════════════════════════════════════════════

def _tela_promotores():
    eid = empresa_id_atual()
    st.subheader("👤 Promotores")
    st.caption("🔑 Com login | ⚪ Sem login")

    if st.session_state.get("eq_prom_msg"):
        st.success(st.session_state.pop("eq_prom_msg"))

    proms = query("""
        SELECT p.promotor_id, p.nome, p.fone, p.cidade, p.ativo, p.usuario_id,
               u.email, u.whatsapp
        FROM promotor p
        LEFT JOIN usuario u ON u.usuario_id=p.usuario_id
        WHERE p.empresa_id=%s AND p.nome != 'Sem promotor'
        ORDER BY p.nome
    """, (eid,)) or []

    for p in proms:
        pid, nome, fone, cidade, ativo, uid, email, wa = p
        icon = "✅" if ativo else "❌"
        login_icon = "🔑" if uid else "⚪"
        with st.expander(f"{icon} {login_icon} {nome} | {cidade or '—'} | {fone or '—'}"):
            if uid: st.caption(f"Login: {email}")

            with st.form(f"ep_{pid}"):
                col1, col2 = st.columns(2)
                with col1:
                    e_nome  = st.text_input("Nome", value=nome, key=f"epn_{pid}")
                    e_fone  = st.text_input("Fone/WhatsApp", value=fone or "", key=f"epf_{pid}")
                with col2:
                    e_cid   = st.text_input("Cidade", value=cidade or "", key=f"epc_{pid}")
                    e_ativo = st.checkbox("Ativo", value=bool(ativo), key=f"epa_{pid}")
                salvar = st.form_submit_button("💾 Salvar", type="primary")
            if salvar:
                execute_write("UPDATE promotor SET nome=%s,fone=%s,cidade=%s,ativo=%s WHERE promotor_id=%s",
                              (e_nome.strip(), e_fone or None, e_cid or None, int(e_ativo), pid))
                if uid:
                    execute_write("UPDATE usuario SET nome=%s WHERE usuario_id=%s", (e_nome.strip(), uid))
                st.session_state["eq_prom_msg"] = "✅ Promotor atualizado."
                st.rerun()

            # Criar login se nao tiver
            if not uid:
                if st.button("🔑 Criar login", key=f"ep_login_{pid}"):
                    st.session_state[f"ep_criar_login_{pid}"] = True
                if st.session_state.get(f"ep_criar_login_{pid}"):
                    with st.form(f"ep_login_form_{pid}"):
                        l_email = st.text_input("Email/login *", key=f"epl_e_{pid}")
                        l_wa    = st.text_input("WhatsApp", key=f"epl_w_{pid}")
                        l_senha = st.text_input("Senha", value=_gerar_senha(), key=f"epl_s_{pid}")
                        criar   = st.form_submit_button("✅ Criar login")
                    if criar:
                        existe = query("SELECT 1 FROM usuario WHERE email=%s", (l_email.strip().lower(),))
                        if existe:
                            st.error("Email já cadastrado.")
                        else:
                            execute_write("""INSERT INTO usuario (nome,email,senha_hash,tipo,empresa_id,whatsapp,ativo)
                                VALUES (%s,%s,%s,'PROMOTOR',%s,%s,1)""",
                                (nome, l_email.strip().lower(), _hash(l_senha), eid, l_wa.strip() or None))
                            novo_uid = (query("SELECT usuario_id FROM usuario WHERE email=%s",
                                             (l_email.strip().lower(),)) or [[None]])[0][0]
                            if novo_uid:
                                execute_write("UPDATE promotor SET usuario_id=%s WHERE promotor_id=%s",
                                              (novo_uid, pid))
                            wa_env = l_wa or fone or ""
                            if wa_env:
                                link = _link_wa(wa_env, _msg_acesso(nome, l_email.strip().lower(), l_senha))
                                st.markdown(f'<a href="{link}" target="_blank"><button style="background:#25D366;color:white;border:none;padding:8px 16px;border-radius:6px;cursor:pointer;width:100%">💬 Enviar via WhatsApp</button></a>', unsafe_allow_html=True)
                            st.session_state[f"ep_criar_login_{pid}"] = False
                            st.session_state["eq_prom_msg"] = f"✅ Login criado para {nome}."
                            st.rerun()
    st.divider()
    st.subheader("➕ Novo promotor")
    with st.form("novo_promotor_eq", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            np_nome  = st.text_input("Nome completo *")
            np_fone  = st.text_input("Fone / WhatsApp")
            np_email = st.text_input("E-mail")
            np_cpf   = st.text_input("CPF")
        with col2:
            np_cid  = st.text_input("Cidade")
            np_uf   = st.selectbox("UF", _ufs())
            np_bair = st.text_input("Bairro")
            np_vei  = st.text_input("Veículo")
        np_obs = st.text_input("Observação")
        salvar = st.form_submit_button("Salvar promotor", type="primary")
    if salvar:
        if not np_nome.strip(): st.error("Nome obrigatório."); return
        execute_write("""INSERT INTO promotor (nome,fone,email,cpf,cidade,estado,bairro,veiculo,observacao,empresa_id,ativo)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,1)""",
            (np_nome.strip(), np_fone or None, np_email or None, np_cpf or None,
             np_cid or None, np_uf, np_bair or None, np_vei or None, np_obs or None, eid))
        st.session_state["eq_prom_msg"] = f"✅ Promotor '{np_nome}' cadastrado!"
        st.rerun()


# ═══════════════════════════════════════════════════════════════
# PROMOTOR VENDEDOR
# ═══════════════════════════════════════════════════════════════

def _tela_promotores_vendedores():
    eid = empresa_id_atual()
    st.subheader("👤💼 Promotores Vendedores")
    st.caption("Profissionais que executam visitas E fazem pedidos. 🔑 Com login | ⚪ Sem login")

    if st.session_state.get("eq_pv_msg"):
        st.success(st.session_state.pop("eq_pv_msg"))

    pvs = query("""
        SELECT u.usuario_id, u.nome, u.email, u.whatsapp, u.ativo
        FROM usuario u
        WHERE u.empresa_id=%s AND u.tipo='PROMOTOR_VENDEDOR' AND u.ativo!=0
        ORDER BY u.nome
    """, (eid,)) or []

    for pv in pvs:
        uid, nome, email, wa, ativo = pv
        with st.expander(f"✅ 🔑 {nome} | {email}"):
            with st.expander("✏️ Editar"):
                e_nome  = st.text_input("Nome", value=nome, key=f"pv_n_{uid}")
                e_wa    = st.text_input("WhatsApp", value=wa or "", key=f"pv_w_{uid}")
                e_email = st.text_input("Email", value=email, key=f"pv_e_{uid}")
                if st.button("💾 Salvar", key=f"pv_sv_{uid}"):
                    execute_write("UPDATE usuario SET nome=%s,whatsapp=%s,email=%s WHERE usuario_id=%s",
                                  (e_nome.strip(), e_wa or None, e_email.strip().lower(), uid))
                    st.session_state["eq_pv_msg"] = "✅ Atualizado."
                    st.rerun()

    if not pvs:
        st.info("Nenhum Promotor Vendedor cadastrado. Crie via botão abaixo.")

    st.divider()
    st.subheader("➕ Novo Promotor Vendedor")
    n_nome  = st.text_input("Nome *", key="npv_nome")
    n_email = st.text_input("Email/login *", key="npv_email")
    n_wa    = st.text_input("WhatsApp", key="npv_wa")
    n_senha = st.text_input("Senha inicial", key="npv_senha", value=_gerar_senha())
    if st.button("💾 Criar", key="npv_criar", type="primary"):
        if not n_nome.strip() or not n_email.strip():
            st.error("Nome e email obrigatórios.")
        else:
            existe = query("SELECT 1 FROM usuario WHERE email=%s", (n_email.strip().lower(),))
            if existe:
                st.error("Email já cadastrado.")
            else:
                execute_write("""INSERT INTO usuario (nome,email,senha_hash,tipo,empresa_id,whatsapp,ativo)
                    VALUES (%s,%s,%s,'PROMOTOR_VENDEDOR',%s,%s,1)""",
                    (n_nome.strip(), n_email.strip().lower(), _hash(n_senha), eid, n_wa or None))
                if n_wa:
                    link = _link_wa(n_wa, _msg_acesso(n_nome, n_email.strip().lower(), n_senha))
                    st.markdown(f'<a href="{link}" target="_blank"><button style="background:#25D366;color:white;border:none;padding:8px 16px;border-radius:6px;cursor:pointer;width:100%">💬 Enviar via WhatsApp</button></a>', unsafe_allow_html=True)
                st.session_state["eq_pv_msg"] = f"✅ {n_nome} criado!"
                st.rerun()


# ═══════════════════════════════════════════════════════════════
# SUPERVISORES
# ═══════════════════════════════════════════════════════════════

def _tela_supervisores():
    eid = empresa_id_atual()
    st.subheader("🎯 Supervisores")
    st.caption("🔑 Com login | ⚪ Sem login")

    if st.session_state.get("eq_sup_msg"):
        st.success(st.session_state.pop("eq_sup_msg"))

    sups = query("""
        SELECT s.supervisor_id, s.nome, s.fone, s.cidade, s.ativo, s.usuario_id,
               u.email, u.whatsapp
        FROM supervisor s
        LEFT JOIN usuario u ON u.usuario_id=s.usuario_id
        WHERE s.empresa_id=%s
        ORDER BY s.nome
    """, (eid,)) or []

    for s in sups:
        sid, nome, fone, cidade, ativo, uid, email, wa = s
        icon = "✅" if ativo else "❌"
        login_icon = "🔑" if uid else "⚪"
        with st.expander(f"{icon} {login_icon} {nome} | {cidade or '—'}"):
            if uid: st.caption(f"Login: {email}")

            with st.form(f"es_{sid}"):
                col1, col2 = st.columns(2)
                with col1:
                    e_nome  = st.text_input("Nome", value=nome, key=f"esn_{sid}")
                    e_fone  = st.text_input("Fone/WhatsApp", value=fone or "", key=f"esf_{sid}")
                with col2:
                    e_cid   = st.text_input("Cidade", value=cidade or "", key=f"esc_{sid}")
                    e_ativo = st.checkbox("Ativo", value=bool(ativo), key=f"esa_{sid}")
                salvar = st.form_submit_button("💾 Salvar", type="primary")
            if salvar:
                execute_write("UPDATE supervisor SET nome=%s,fone=%s,cidade=%s,ativo=%s WHERE supervisor_id=%s",
                              (e_nome.strip(), e_fone or None, e_cid or None, int(e_ativo), sid))
                if uid:
                    execute_write("UPDATE usuario SET nome=%s WHERE usuario_id=%s", (e_nome.strip(), uid))
                st.session_state["eq_sup_msg"] = "✅ Supervisor atualizado."
                st.rerun()

            if not uid:
                if st.button("🔑 Criar login", key=f"es_login_{sid}"):
                    st.session_state[f"es_criar_login_{sid}"] = True
                if st.session_state.get(f"es_criar_login_{sid}"):
                    with st.form(f"es_login_form_{sid}"):
                        l_email = st.text_input("Email/login *", key=f"esl_e_{sid}")
                        l_wa    = st.text_input("WhatsApp", key=f"esl_w_{sid}")
                        l_senha = st.text_input("Senha", value=_gerar_senha(), key=f"esl_s_{sid}")
                        criar   = st.form_submit_button("✅ Criar login")
                    if criar:
                        existe = query("SELECT 1 FROM usuario WHERE email=%s", (l_email.strip().lower(),))
                        if existe:
                            st.error("Email já cadastrado.")
                        else:
                            execute_write("""INSERT INTO usuario (nome,email,senha_hash,tipo,empresa_id,whatsapp,ativo)
                                VALUES (%s,%s,%s,'SUPERVISOR',%s,%s,1)""",
                                (nome, l_email.strip().lower(), _hash(l_senha), eid, l_wa or None))
                            novo_uid = (query("SELECT usuario_id FROM usuario WHERE email=%s",
                                             (l_email.strip().lower(),)) or [[None]])[0][0]
                            if novo_uid:
                                execute_write("UPDATE supervisor SET usuario_id=%s WHERE supervisor_id=%s",
                                              (novo_uid, sid))
                            wa_env = l_wa or fone or ""
                            if wa_env:
                                link = _link_wa(wa_env, _msg_acesso(nome, l_email.strip().lower(), l_senha))
                                st.markdown(f'<a href="{link}" target="_blank"><button style="background:#25D366;color:white;border:none;padding:8px 16px;border-radius:6px;cursor:pointer;width:100%">💬 Enviar via WhatsApp</button></a>', unsafe_allow_html=True)
                            st.session_state[f"es_criar_login_{sid}"] = False
                            st.session_state["eq_sup_msg"] = f"✅ Login criado para {nome}."
                            st.rerun()

    st.divider()
    st.subheader("➕ Novo supervisor")
    with st.form("novo_sup_eq", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            ns_nome  = st.text_input("Nome completo *")
            ns_fone  = st.text_input("Fone / WhatsApp")
            ns_email = st.text_input("E-mail")
        with col2:
            ns_cid  = st.text_input("Cidade")
            ns_uf   = st.selectbox("UF", _ufs())
            ns_bair = st.text_input("Bairro / região")
        ns_obs = st.text_input("Observação")
        salvar = st.form_submit_button("Salvar supervisor", type="primary")
    if salvar:
        if not ns_nome.strip(): st.error("Nome obrigatório."); return
        execute_write("""INSERT INTO supervisor (nome,fone,email,cidade,estado,bairro,observacao,empresa_id,ativo)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,1)""",
            (ns_nome.strip(), ns_fone or None, ns_email or None,
             ns_cid or None, ns_uf, ns_bair or None, ns_obs or None, eid))
        st.session_state["eq_sup_msg"] = f"✅ Supervisor '{ns_nome}' cadastrado!"
        st.rerun()
