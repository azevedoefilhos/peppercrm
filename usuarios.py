# usuarios.py — PepperCRM
# Gestao de usuarios e empresas

import streamlit as st
import hashlib, secrets, string, urllib.parse
from database import query, execute_write, conectar
from permissoes import e_admin, e_master, exigir_admin, empresa_id_atual, perfil_atual

def _ir(p):
    st.session_state["pagina"] = p
    st.rerun()

def _hash(s):
    return hashlib.sha256(s.encode()).hexdigest()

def _gerar_senha(tamanho=10):
    chars = string.ascii_letters + string.digits + "!@#"
    return "".join(secrets.choice(chars) for _ in range(tamanho))

def _limpar_fone(fone: str) -> str:
    """Remove caracteres nao numericos e garante codigo do pais."""
    if not fone:
        return ""
    num = "".join(filter(str.isdigit, fone))
    if not num.startswith("55"):
        num = "55" + num
    return num

def _link_whatsapp(fone: str, msg: str) -> str:
    num = _limpar_fone(fone)
    return f"https://wa.me/{num}?text={urllib.parse.quote(msg)}"

def _msg_credenciais(nome: str, login: str, senha: str) -> str:
    return (
        f"Ola {nome.split()[0]}! 🌶️\n\n"
        f"Seu acesso ao *PepperCRM* esta pronto.\n\n"
        f"🌐 *Link de acesso:*\n"
        f"https://peppercrm-production.up.railway.app\n\n"
        f"👤 *Usuario:* {login}\n"
        f"🔑 *Senha:* {senha}\n\n"
        f"*Como acessar pelo celular:*\n"
        f"1. Abra o link acima\n"
        f"2. Faca login com seus dados\n"
        f"3. Salve o link como favorito\n\n"
        f"Qualquer duvida, me chame! 😊"
    )

def _botoes_envio(nome: str, login: str, senha: str, whatsapp: str):
    """Exibe botoes de envio via WhatsApp e copia de mensagem."""
    msg = _msg_credenciais(nome, login, senha)

    if whatsapp:
        wa_link = _link_whatsapp(whatsapp, msg)
        st.markdown(
            f'<a href="{wa_link}" target="_blank">'
            f'<button style="background:#25D366;color:white;border:none;'
            f'padding:8px 16px;border-radius:6px;font-size:14px;'
            f'cursor:pointer;width:100%">💬 Enviar credenciais via WhatsApp</button></a>',
            unsafe_allow_html=True
        )
    else:
        st.info("WhatsApp nao cadastrado. Copie a mensagem abaixo e envie manualmente:")

    with st.expander("📋 Ver mensagem completa"):
        st.code(msg, language=None)


# ═══════════════════════════════════════════════════════════════
# TELA DE USUARIOS
# ═══════════════════════════════════════════════════════════════

def tela_usuarios():
    exigir_admin()
    st.header("👤 Gestão de Usuários")
    if st.button("⬅ Voltar"): _ir("home")

    eid = empresa_id_atual() if not e_master() else None

    if eid:
        usuarios = query("""
            SELECT usuario_id, nome, email, tipo, ativo, whatsapp
            FROM usuario WHERE empresa_id=%s ORDER BY nome
        """, (eid,)) or []
    else:
        usuarios = query("""
            SELECT u.usuario_id, u.nome, u.email, u.tipo, u.ativo,
                   u.whatsapp, e.nome as emp_nome
            FROM usuario u
            LEFT JOIN empresa e ON u.empresa_id=e.empresa_id
            ORDER BY u.empresa_id, u.nome
        """) or []

    st.subheader(f"Usuários cadastrados ({len(usuarios)})")

    for u in usuarios:
        uid   = u[0]; nome = u[1]; email = u[2]
        tipo  = u[3]; ativo = u[4]; wa = u[5]
        emp_nome = u[6] if e_master() and len(u) > 6 else ""
        icon  = "✅" if ativo else "❌"
        titulo = f"{icon} {nome} — {tipo}"
        if emp_nome:
            titulo += f" | {emp_nome}"

        with st.expander(titulo):
            col1, col2, col3 = st.columns(3)
            col1.write(f"**Login:** {email}")
            col2.write(f"**Perfil:** {tipo}")
            col3.write(f"**WhatsApp:** {wa or '—'}")

            # Editar WhatsApp
            novo_wa = st.text_input("Editar WhatsApp", value=wa or "",
                                    key=f"wa_{uid}", placeholder="11 9 9999-9999")
            if novo_wa != (wa or ""):
                if st.button("💾 Salvar WhatsApp", key=f"sv_wa_{uid}"):
                    execute_write("UPDATE usuario SET whatsapp=%s WHERE usuario_id=%s",
                                  (novo_wa.strip() or None, uid))
                    st.success("WhatsApp atualizado.")
                    st.rerun()

            colA, colB, colC = st.columns(3)

            # Ativar/Desativar
            if ativo:
                if colA.button("❌ Desativar", key=f"des_{uid}"):
                    execute_write("UPDATE usuario SET ativo=0 WHERE usuario_id=%s", (uid,))
                    execute_write("UPDATE sessao_token SET ativo=0 WHERE usuario_id=%s", (uid,))
                    st.success(f"{nome} desativado. Acesso revogado imediatamente.")
                    st.rerun()
            else:
                if colA.button("✅ Reativar", key=f"rea_{uid}"):
                    execute_write("UPDATE usuario SET ativo=1 WHERE usuario_id=%s", (uid,))
                    st.success(f"{nome} reativado.")
                    st.rerun()

            # Redefinir senha
            if colB.button("🔑 Nova senha", key=f"pwd_{uid}"):
                nova = _gerar_senha()
                execute_write("UPDATE usuario SET senha_hash=%s WHERE usuario_id=%s",
                              (_hash(nova), uid))
                execute_write("UPDATE sessao_token SET ativo=0 WHERE usuario_id=%s", (uid,))
                st.success(f"Nova senha gerada: **{nova}**")
                st.session_state[f"nova_senha_{uid}"] = nova

            if st.session_state.get(f"nova_senha_{uid}"):
                _botoes_envio(nome, email, st.session_state[f"nova_senha_{uid}"], wa or "")

            # Alterar perfil
            PERFIS = ['REPRESENTANTE_ADM','REPRESENTANTE','VENDEDOR','SUPERVISOR','PROMOTOR']
            if e_master(): PERFIS = ['MASTER'] + PERFIS
            idx = PERFIS.index(tipo) if tipo in PERFIS else 0
            novo_tipo = colC.selectbox("Perfil", PERFIS, index=idx, key=f"tipo_{uid}")
            if novo_tipo != tipo:
                if st.button("💾 Salvar perfil", key=f"sv_tipo_{uid}"):
                    execute_write("UPDATE usuario SET tipo=%s WHERE usuario_id=%s",
                                  (novo_tipo, uid))
                    st.success("Perfil atualizado.")
                    st.rerun()

    st.divider()

    # Criar novo usuario
    with st.expander("➕ Criar novo usuário"):
        n_nome  = st.text_input("Nome completo *", key="nu_nome")
        n_email = st.text_input("Email/login *", key="nu_email",
                                placeholder="email@dominio.com.br")
        n_wa    = st.text_input("WhatsApp (opcional)", key="nu_wa",
                                placeholder="11 9 9999-9999")
        PERFIS_NEW = ['REPRESENTANTE_ADM','REPRESENTANTE','VENDEDOR','SUPERVISOR','PROMOTOR']
        n_tipo  = st.selectbox("Perfil", PERFIS_NEW, key="nu_tipo")
        n_senha = st.text_input("Senha inicial", key="nu_senha",
                                value=_gerar_senha(),
                                help="Gerada automaticamente. Pode alterar.")

        if e_master():
            empresas_list = query(
                "SELECT empresa_id, nome FROM empresa WHERE ativo=1 ORDER BY nome") or []
            emp_opts = [(e[0], e[1]) for e in empresas_list]
            emp_sel  = st.selectbox("Empresa *", emp_opts,
                                    format_func=lambda x: x[1], key="nu_empresa")
            eid_novo = emp_sel[0] if emp_sel else 1
        else:
            eid_novo = empresa_id_atual()
            st.caption(f"Usuário será criado na sua empresa.")

        if st.button("💾 Criar usuário", key="nu_criar", type="primary"):
            if not n_nome.strip() or not n_email.strip():
                st.error("Nome e email são obrigatórios.")
            else:
                existe = query("SELECT 1 FROM usuario WHERE email=%s",
                               (n_email.strip().lower(),))
                if existe:
                    st.error("Este email já está cadastrado.")
                else:
                    execute_write("""
                        INSERT INTO usuario
                            (nome, email, senha_hash, tipo, empresa_id, whatsapp, ativo)
                        VALUES (%s, %s, %s, %s, %s, %s, 1)
                    """, (n_nome.strip(), n_email.strip().lower(),
                          _hash(n_senha), n_tipo, eid_novo,
                          n_wa.strip() or None))
                    st.success(f"✅ Usuário **{n_nome}** criado!")
                    _botoes_envio(n_nome, n_email.strip().lower(), n_senha, n_wa)
                    st.rerun()


# ═══════════════════════════════════════════════════════════════
# TELA DE EMPRESAS (so MASTER)
# ═══════════════════════════════════════════════════════════════

def tela_empresas():
    if not e_master():
        st.error("Acesso restrito ao administrador master.")
        st.stop()

    st.header("🏢 Gestão de Empresas")
    if st.button("⬅ Voltar"): _ir("home")

    empresas = query("""
        SELECT empresa_id, nome, plano, status, max_usuarios,
               max_clientes, data_criacao, email_admin
        FROM empresa ORDER BY empresa_id
    """) or []

    st.subheader(f"Empresas cadastradas ({len(empresas)})")

    for e in empresas:
        eid, nome, plano, status, max_u, max_c, data_c, email = e
        icon = "✅" if status == 'ativo' else "⚠️" if status == 'trial' else "❌"
        with st.expander(f"{icon} [{eid}] {nome} — {plano}"):
            col1, col2, col3 = st.columns(3)
            col1.metric("Plano", plano)
            col2.metric("Status", status)
            col3.metric("Max usuários", max_u)

            col4, col5 = st.columns(2)
            col4.write(f"**Admin:** {email}")
            col5.write(f"**Criada em:** {str(data_c)[:10] if data_c else '—'}")

            u_count   = query("SELECT COUNT(*) FROM usuario WHERE empresa_id=%s AND ativo=1", (eid,))
            cli_count = query("SELECT COUNT(*) FROM cliente WHERE empresa_id=%s", (eid,))
            st.caption(
                f"Usuários ativos: {u_count[0][0] if u_count else 0}/{max_u} | "
                f"Clientes: {cli_count[0][0] if cli_count else 0}/{max_c}"
            )

            STATUS_OPTS = ['trial','ativo','suspenso','cancelado']
            idx_s = STATUS_OPTS.index(status) if status in STATUS_OPTS else 1
            novo_status = st.selectbox("Status", STATUS_OPTS, index=idx_s, key=f"est_{eid}")
            if st.button("💾 Salvar status", key=f"sv_est_{eid}"):
                execute_write("UPDATE empresa SET status=%s WHERE empresa_id=%s",
                              (novo_status, eid))
                if novo_status == 'suspenso':
                    execute_write("""
                        UPDATE sessao_token SET ativo=0
                        WHERE usuario_id IN (
                            SELECT usuario_id FROM usuario WHERE empresa_id=%s
                        )
                    """, (eid,))
                st.success(f"Status atualizado para '{novo_status}'.")
                st.rerun()

    st.divider()

    with st.expander("➕ Cadastrar nova empresa"):
        ne_nome       = st.text_input("Nome da empresa *", key="ne_nome")
        ne_email      = st.text_input("Email do admin *", key="ne_email")
        ne_wa         = st.text_input("WhatsApp do admin (opcional)", key="ne_wa",
                                      placeholder="11 9 9999-9999")
        ne_plano      = st.selectbox("Plano", ['solo','equipe','escritorio'], key="ne_plano")
        LIMITES       = {'solo':(1,150),'equipe':(5,500),'escritorio':(15,9999)}
        max_u, max_c  = LIMITES[ne_plano]
        st.caption(f"Plano {ne_plano}: até {max_u} usuários e {max_c} clientes")
        ne_admin_nome = st.text_input("Nome do administrador *", key="ne_admin_nome")
        ne_senha      = _gerar_senha()
        st.info(f"Senha inicial gerada: **{ne_senha}**")

        if st.button("💾 Criar empresa", key="ne_criar", type="primary"):
            if not ne_nome.strip() or not ne_email.strip() or not ne_admin_nome.strip():
                st.error("Nome da empresa, email e nome do admin são obrigatórios.")
            else:
                try:
                    execute_write("""
                        INSERT INTO empresa
                            (nome, email_admin, plano, status, max_usuarios, max_clientes, ativo)
                        VALUES (%s,%s,%s,'ativo',%s,%s,1)
                    """, (ne_nome.strip(), ne_email.strip().lower(),
                          ne_plano, max_u, max_c))

                    novo_eid = query("SELECT MAX(empresa_id) FROM empresa")[0][0]

                    execute_write("""
                        INSERT INTO usuario
                            (nome, email, senha_hash, tipo, empresa_id, whatsapp, ativo)
                        VALUES (%s,%s,%s,'REPRESENTANTE_ADM',%s,%s,1)
                    """, (ne_admin_nome.strip(), ne_email.strip().lower(),
                          _hash(ne_senha), novo_eid, ne_wa.strip() or None))

                    st.success(f"✅ Empresa **{ne_nome}** criada (empresa_id={novo_eid})!")
                    _botoes_envio(ne_admin_nome, ne_email.strip().lower(),
                                  ne_senha, ne_wa)
                    st.rerun()
                except Exception as ex:
                    st.error(f"Erro: {ex}")
