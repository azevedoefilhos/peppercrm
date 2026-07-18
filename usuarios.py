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

def tela_usuarios(embutido=False):
    exigir_admin()
    if not embutido:
        st.header("👤 Gestão de Usuários")
        if st.button("⬅ Voltar"): _ir("home")

    ABAS = {"usuarios": "👤 Usuários", "carteira": "🗂️ Carteira de Clientes"}
    if "usr_aba" not in st.session_state:
        st.session_state["usr_aba"] = "usuarios"
    cols = st.columns(len(ABAS))
    for col, (k, v) in zip(cols, ABAS.items()):
        ativa = st.session_state["usr_aba"] == k
        if col.button(v, key=f"usr_nav_{k}", width="stretch",
                      type="primary" if ativa else "secondary"):
            st.session_state["usr_aba"] = k
            st.rerun()
    st.divider()

    if st.session_state["usr_aba"] == "carteira":
        _tela_carteira()
        return

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

            # Editar dados basicos
            with st.expander("✏️ Editar dados"):
                e_nome_edit = st.text_input("Nome", value=nome, key=f"en_{uid}")
                e_wa_edit   = st.text_input("WhatsApp", value=wa or "",
                                            key=f"ewa_{uid}", placeholder="11 9 9999-9999")
                e_email_edit = st.text_input("Email/login", value=email, key=f"eem_{uid}")
                if st.button("💾 Salvar dados", key=f"sv_dados_{uid}", type="primary"):
                    # Verifica se novo email ja existe em outro usuario
                    if e_email_edit.strip().lower() != email:
                        existe = query("SELECT 1 FROM usuario WHERE email=%s AND usuario_id!=%s",
                                       (e_email_edit.strip().lower(), uid))
                        if existe:
                            st.error("Este email já está em uso por outro usuário.")
                        else:
                            execute_write("""UPDATE usuario SET nome=%s, whatsapp=%s, email=%s
                                WHERE usuario_id=%s""",
                                (e_nome_edit.strip(), e_wa_edit.strip() or None,
                                 e_email_edit.strip().lower(), uid))
                            st.success("Dados atualizados.")
                            st.rerun()
                    else:
                        execute_write("""UPDATE usuario SET nome=%s, whatsapp=%s
                            WHERE usuario_id=%s""",
                            (e_nome_edit.strip(), e_wa_edit.strip() or None, uid))
                        st.success("Dados atualizados.")
                        st.rerun()

            colA, colB, colC = st.columns(3)

            # Ativar/Desativar com redistribuicao de carteira
            if ativo:
                if colA.button("❌ Desativar", key=f"des_{uid}"):
                    # Verifica se tem clientes na carteira
                    n_clientes = query(
                        "SELECT COUNT(*) FROM cliente WHERE vendedor_id=%s", (uid,))
                    n_cli = n_clientes[0][0] if n_clientes else 0
                    if n_cli > 0:
                        st.session_state[f"desat_pendente_{uid}"] = n_cli
                    else:
                        execute_write("UPDATE usuario SET ativo=0 WHERE usuario_id=%s", (uid,))
                        execute_write("UPDATE sessao_token SET ativo=0 WHERE usuario_id=%s", (uid,))
                        st.success(f"{nome} desativado.")
                        st.rerun()

                # Fluxo de redistribuicao antes de desativar
                if st.session_state.get(f"desat_pendente_{uid}"):
                    n_cli = st.session_state[f"desat_pendente_{uid}"]
                    st.warning(f"⚠️ {nome} tem **{n_cli} cliente(s)** na carteira. O que fazer?")
                    outros_vend = query("""
                        SELECT usuario_id, nome FROM usuario
                        WHERE empresa_id=%s AND tipo IN
                        ('REPRESENTANTE_ADM','REPRESENTANTE','VENDEDOR','PROMOTOR_VENDEDOR')
                        AND ativo=1 AND usuario_id != %s ORDER BY nome
                    """, (empresa_id_atual(), uid)) or []
                    opts_dest = [(None, "— Deixar sem responsável")] + \
                                [(v[0], v[1]) for v in outros_vend]
                    dest = st.selectbox("Transferir carteira para",
                                        opts_dest, format_func=lambda x: x[1],
                                        key=f"dest_cart_{uid}")
                    col_conf, col_canc = st.columns(2)
                    if col_conf.button("✅ Confirmar desativação", key=f"conf_des_{uid}",
                                       type="primary"):
                        if dest[0]:
                            execute_write(
                                "UPDATE cliente SET vendedor_id=%s WHERE vendedor_id=%s",
                                (dest[0], uid))
                        else:
                            execute_write(
                                "UPDATE cliente SET vendedor_id=NULL WHERE vendedor_id=%s",
                                (uid,))
                        execute_write("UPDATE usuario SET ativo=0 WHERE usuario_id=%s", (uid,))
                        execute_write("UPDATE sessao_token SET ativo=0 WHERE usuario_id=%s", (uid,))
                        st.session_state.pop(f"desat_pendente_{uid}", None)
                        st.success(f"{nome} desativado. Carteira redistribuída.")
                        st.rerun()
                    if col_canc.button("Cancelar", key=f"canc_des_{uid}"):
                        st.session_state.pop(f"desat_pendente_{uid}", None)
                        st.rerun()
            else:
                if colA.button("✅ Reativar", key=f"rea_{uid}"):
                    execute_write("UPDATE usuario SET ativo=1 WHERE usuario_id=%s", (uid,))
                    st.success(f"{nome} reativado.")
                    st.rerun()

                # Verificar se pode excluir
                if colC.button("🗑️ Verificar exclusão", key=f"del_chk_{uid}"):
                    n_cli  = (query("SELECT COUNT(*) FROM cliente WHERE vendedor_id=%s", (uid,)) or [[0]])[0][0]
                    n_ped  = (query("SELECT COUNT(*) FROM pedido WHERE empresa_id=%s AND EXISTS (SELECT 1 FROM cliente c WHERE c.cliente_id=pedido.cliente_id AND c.vendedor_id=%s)", (empresa_id_atual(), uid)) or [[0]])[0][0]
                    n_cont = (query("SELECT COUNT(*) FROM contato_registro WHERE empresa_id=%s AND EXISTS (SELECT 1 FROM cliente c WHERE c.cliente_id=contato_registro.cliente_id AND c.vendedor_id=%s)", (empresa_id_atual(), uid)) or [[0]])[0][0]
                    if n_ped > 0 or n_cont > 0:
                        st.error(f"❌ Exclusão não permitida — {nome} tem {n_ped} pedido(s) e {n_cont} contato(s) registrados. Mantenha desativado.")
                    elif n_cli > 0:
                        st.error(f"❌ Exclusão não permitida — {nome} tem {n_cli} cliente(s) na carteira. Redistribua antes.")
                    else:
                        st.session_state[f"del_confirm_{uid}"] = True

                if st.session_state.get(f"del_confirm_{uid}"):
                    st.warning(f"⚠️ Confirma exclusão definitiva de **{nome}**?")
                    col_sim, col_nao = st.columns(2)
                    if col_sim.button("✅ Sim, excluir", key=f"del_sim_{uid}", type="primary"):
                        execute_write("DELETE FROM sessao_token WHERE usuario_id=%s", (uid,))
                        execute_write("DELETE FROM usuario WHERE usuario_id=%s", (uid,))
                        st.session_state.pop(f"del_confirm_{uid}", None)
                        st.success(f"Usuário {nome} excluído.")
                        st.rerun()
                    if col_nao.button("Cancelar", key=f"del_nao_{uid}"):
                        st.session_state.pop(f"del_confirm_{uid}", None)
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
            PERFIS = ['REPRESENTANTE_ADM','REPRESENTANTE','VENDEDOR',
                      'PROMOTOR_VENDEDOR','SUPERVISOR','PROMOTOR']
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
    st.subheader("➕ Criar novo usuário")

    # Perfil fora do expander para nao recolher
    PERFIS_NEW = ['REPRESENTANTE_ADM','REPRESENTANTE','VENDEDOR',
                  'PROMOTOR_VENDEDOR','SUPERVISOR','PROMOTOR']
    n_tipo = st.selectbox("Perfil do novo usuário", PERFIS_NEW, key="nu_tipo")

    if e_master():
        empresas_list = query(
            "SELECT empresa_id, nome FROM empresa WHERE ativo=1 ORDER BY nome") or []
        emp_opts = [(e[0], e[1]) for e in empresas_list]
        emp_sel  = st.selectbox("Empresa *", emp_opts,
                                format_func=lambda x: x[1], key="nu_empresa")
        eid_novo = emp_sel[0] if emp_sel else 1
    else:
        eid_novo = empresa_id_atual()

    # Vinculacao com colaborador existente — pré-popula campos
    # Reset da selecao de vinculo quando tipo muda
    if st.session_state.get("_nu_tipo_anterior") != n_tipo:
        for k in ["nu_vinc_prom","nu_vinc_sup","nu_vinc_vend"]:
            st.session_state.pop(k, None)
        st.session_state["_nu_tipo_anterior"] = n_tipo

    vinculo_id   = None
    vinculo_tipo = None
    _pre_nome  = st.session_state.get("nu_nome", "")
    _pre_email = st.session_state.get("nu_email", "")
    _pre_wa    = st.session_state.get("nu_wa", "")

    if n_tipo in ('REPRESENTANTE', 'VENDEDOR', 'REPRESENTANTE_ADM'):
        # Vendedores da tabela vendedor sem usuario vinculado
        sem_login_v = query("""
            SELECT vendedor_id, nome, fone, email, whatsapp FROM vendedor
            WHERE empresa_id=%s AND usuario_id IS NULL AND ativo!=0
            ORDER BY nome
        """, (eid_novo,)) or []
        if sem_login_v:
            opts_v = [(None, "— Criar novo vendedor")] + \
                     [(v[0], v[1]) for v in sem_login_v]
            sel_v = st.selectbox("Vincular a vendedor já cadastrado (opcional)",
                                 opts_v, format_func=lambda x: x[1],
                                 key="nu_vinc_vend")
            vinculo_id   = sel_v[0] if sel_v else None
            vinculo_tipo = 'vendedor'
            if vinculo_id:
                v = next(v for v in sem_login_v if v[0] == vinculo_id)
                st.info(f"✅ Vinculando a **{v[1]}** — dados pré-preenchidos abaixo.")
                _pre_nome  = v[1] or ""
                _pre_email = v[3] or ""
                _pre_wa    = v[4] or v[2] or ""

    elif n_tipo == 'PROMOTOR' or n_tipo == 'PROMOTOR_VENDEDOR':
        sem_login = query("""
            SELECT promotor_id, nome, fone, email FROM promotor
            WHERE empresa_id=%s AND ativo!=0
            AND usuario_id IS NULL AND nome != 'Sem promotor'
            ORDER BY nome
        """, (eid_novo,)) or []
        if sem_login:
            opts = [(None, "— Criar novo promotor")] + \
                   [(p[0], p[1]) for p in sem_login]
            sel = st.selectbox("Vincular a promotor já cadastrado (opcional)",
                               opts, format_func=lambda x: x[1],
                               key="nu_vinc_prom")
            vinculo_id   = sel[0] if sel else None
            vinculo_tipo = 'promotor'
            if vinculo_id:
                p = next(p for p in sem_login if p[0] == vinculo_id)
                st.info(f"✅ Vinculando a **{p[1]}** — dados pré-preenchidos abaixo.")
                _pre_nome  = p[1] or ""
                _pre_email = p[3] or ""
                _pre_wa    = p[2] or ""

    elif n_tipo == 'SUPERVISOR':
        sem_login_s = query("""
            SELECT supervisor_id, nome, fone, email FROM supervisor
            WHERE empresa_id=%s AND ativo!=0
            AND usuario_id IS NULL
            ORDER BY nome
        """, (eid_novo,)) or []
        if sem_login_s:
            opts_s = [(None, "— Criar novo supervisor")] + \
                     [(s[0], s[1]) for s in sem_login_s]
            sel_s = st.selectbox("Vincular a supervisor já cadastrado (opcional)",
                                 opts_s, format_func=lambda x: x[1],
                                 key="nu_vinc_sup")
            vinculo_id   = sel_s[0] if sel_s else None
            vinculo_tipo = 'supervisor'
            if vinculo_id:
                s = next(s for s in sem_login_s if s[0] == vinculo_id)
                st.info(f"✅ Vinculando a **{s[1]}** — dados pré-preenchidos abaixo.")
                _pre_nome  = s[1] or ""
                _pre_email = s[3] or ""
                _pre_wa    = s[2] or ""

    # Mostra credenciais do usuario recem-criado
    if st.session_state.get("nu_criado"):
        info = st.session_state["nu_criado"]
        st.success(f"✅ Usuário **{info['nome']}** criado!")
        _botoes_envio(info["nome"], info["email"], info["senha"], info["wa"])
        if st.button("➕ Criar outro usuário", key="nu_limpar"):
            for k in ["nu_criado","nu_nome","nu_email","nu_wa",
                      "nu_senha","nu_tipo","nu_vinc_prom","nu_vinc_sup"]:
                st.session_state.pop(k, None)
            st.rerun()
        return

    # Campos do formulário — pré-populados se vinculado
    n_nome  = st.text_input("Nome completo *", value=_pre_nome, key="nu_nome")
    n_email = st.text_input("Email/login *", value=_pre_email, key="nu_email",
                            placeholder="email@dominio.com.br")
    n_wa    = st.text_input("WhatsApp (opcional)", value=_pre_wa, key="nu_wa",
                            placeholder="11 9 9999-9999")
    n_senha = st.text_input("Senha inicial", key="nu_senha",
                            value=st.session_state.get("nu_senha", _gerar_senha()),
                            help="Gerada automaticamente. Pode alterar.")

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

                novo_uid = query("SELECT usuario_id FROM usuario WHERE email=%s",
                                 (n_email.strip().lower(),))
                novo_uid = novo_uid[0][0] if novo_uid else None
                if novo_uid and vinculo_id:
                    if vinculo_tipo == 'promotor':
                        execute_write(
                            "UPDATE promotor SET usuario_id=%s WHERE promotor_id=%s",
                            (novo_uid, vinculo_id))
                    elif vinculo_tipo == 'supervisor':
                        execute_write(
                            "UPDATE supervisor SET usuario_id=%s WHERE supervisor_id=%s",
                            (novo_uid, vinculo_id))
                    elif vinculo_tipo == 'vendedor':
                        execute_write(
                            "UPDATE vendedor SET usuario_id=%s WHERE vendedor_id=%s",
                            (novo_uid, vinculo_id))

                st.session_state["nu_criado"] = {
                    "nome":  n_nome.strip(),
                    "email": n_email.strip().lower(),
                    "senha": n_senha,
                    "wa":    n_wa.strip(),
                }
                st.rerun()


# ═══════════════════════════════════════════════════════════════
# TELA DE EMPRESAS (so MASTER)
# ═══════════════════════════════════════════════════════════════

def tela_empresas(embutido=False):
    if not e_master():
        st.error("Acesso restrito ao administrador master.")
        st.stop()

    st.header("🏢 Gestão de Empresas")
    if not embutido:
        if st.button("⬅ Voltar", key="emp_voltar"): _ir("home")

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


# ═══════════════════════════════════════════════════════════════
# TELA DE CARTEIRA — Atribuicao de clientes a vendedores
# ═══════════════════════════════════════════════════════════════

def _tela_carteira():
    st.subheader("🗂️ Atribuição de Carteira de Clientes")
    st.caption("Filtre, selecione e atribua clientes aos vendedores da sua equipe.")

    eid = empresa_id_atual()

    vendedores = query("""
        SELECT usuario_id, nome, tipo FROM usuario
        WHERE empresa_id=%s
          AND tipo IN ('REPRESENTANTE_ADM','REPRESENTANTE','VENDEDOR','PROMOTOR_VENDEDOR')
          AND ativo=1 ORDER BY nome
    """, (eid,)) or []

    if not vendedores:
        st.info("Nenhum vendedor/representante cadastrado ainda.")
        return

    vend_opts      = [(None, "— Sem vendedor")] + [(v[0], v[1]) for v in vendedores]
    vend_opts_dest = [(v[0], v[1]) for v in vendedores]

    # ── Resumo ────────────────────────────────────────────────────────────
    with st.expander("📊 Resumo da carteira por vendedor"):
        resumo = query("""
            SELECT u.nome, u.tipo, COUNT(c.cliente_id) as total
            FROM usuario u
            LEFT JOIN cliente c ON c.vendedor_id=u.usuario_id
            WHERE u.empresa_id=%s
              AND u.tipo IN ('REPRESENTANTE_ADM','REPRESENTANTE','VENDEDOR','PROMOTOR_VENDEDOR')
              AND u.ativo=1
            GROUP BY u.nome, u.tipo ORDER BY total DESC
        """, (eid,)) or []
        sem_vend = query(
            "SELECT COUNT(*) FROM cliente WHERE empresa_id=%s AND vendedor_id IS NULL",
            (eid,))
        col1, col2 = st.columns(2)
        for i, r in enumerate(resumo):
            tipo_label = " (PV)" if r[1] == 'PROMOTOR_VENDEDOR' else ""
            (col1 if i % 2 == 0 else col2).metric(f"{r[0]}{tipo_label}", f"{r[2]} clientes")
        sv = sem_vend[0][0] if sem_vend else 0
        if sv:
            st.metric("Sem responsável", f"{sv} clientes")

    st.divider()

    # ── Filtros ───────────────────────────────────────────────────────────
    st.markdown("**Filtros**")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        fil_vend = st.selectbox("Vendedor atual", vend_opts,
                                format_func=lambda x: x[1], key="cart_fil_vend")
    with col2:
        # Busca perfis existentes
        perfis_db = query("SELECT DISTINCT perfil FROM cliente WHERE perfil IS NOT NULL ORDER BY perfil") or []
        perf_opts = ["Todos"] + [p[0] for p in perfis_db if p[0]]
        fil_perfil = st.selectbox("Perfil/Tipo", perf_opts, key="cart_fil_perfil")
    with col3:
        STATUS_OPTS = ["Todos", "Prospecto", "Ativo", "Visitado", "Inativo", "Suspenso"]
        fil_status = st.selectbox("Status", STATUS_OPTS, key="cart_fil_status")
    with col4:
        # Busca cidades existentes
        cidades_db = query("SELECT DISTINCT cidade FROM cliente WHERE cidade IS NOT NULL ORDER BY cidade") or []
        cid_opts = ["Todas"] + [c[0] for c in cidades_db if c[0]]
        fil_cidade = st.selectbox("Cidade", cid_opts, key="cart_fil_cidade")

    fil_busca = st.text_input("Buscar por nome", key="cart_busca",
                              placeholder="Digite parte do nome...")

    # Monta WHERE
    where, params = [], []
    if fil_vend[0] is not None:
        where.append("c.vendedor_id=%s"); params.append(fil_vend[0])
    else:
        where.append("c.vendedor_id IS NULL")
    if fil_perfil != "Todos":
        where.append("c.perfil=%s"); params.append(fil_perfil)
    if fil_status != "Todos":
        where.append("c.status=%s"); params.append(fil_status)
    if fil_cidade != "Todas":
        where.append("c.cidade=%s"); params.append(fil_cidade)
    if fil_busca.strip():
        where.append("c.nome_fantasia ILIKE %s"); params.append(f"%{fil_busca.strip()}%")

    where_sql = "WHERE " + " AND ".join(where) if where else ""
    clientes  = query(f"""
        SELECT c.cliente_id, c.nome_fantasia, c.status, c.perfil, c.cidade, c.vendedor_id
        FROM cliente c {where_sql} ORDER BY c.nome_fantasia
    """, tuple(params)) or []

    st.divider()
    st.write(f"**{len(clientes)} cliente(s) encontrado(s)**")

    if not clientes:
        st.info("Nenhum cliente com estes filtros.")
        return

    # ── Atribuicao em massa com selecao ───────────────────────────────────
    st.markdown("**Atribuição em lote**")
    st.caption("Selecione os clientes desejados e atribua a um vendedor.")

    destino = st.selectbox("Atribuir selecionados a",
                           vend_opts_dest, format_func=lambda x: x[1],
                           key="cart_destino")

    col_sel, col_btn = st.columns([3, 1])
    with col_sel:
        selecionar_todos = st.checkbox("Selecionar todos da lista", key="cart_sel_todos")
    with col_btn:
        aplicar = st.button("✅ Atribuir selecionados", key="cart_aplicar",
                            type="primary", width="stretch")

    # Checkboxes por cliente
    selecionados = []
    for c in clientes:
        cid, nome, status, perfil, cidade, vend_id_atual = c
        vend_nome_atual = next((v[1] for v in vendedores if v[0] == vend_id_atual), "Sem vendedor")
        label = f"**{nome}** | {perfil or '—'} | {cidade or '—'} | {status} | 👤 {vend_nome_atual}"
        marcado = st.checkbox(label, key=f"chk_{cid}",
                              value=selecionar_todos)
        if marcado:
            selecionados.append(cid)

    if aplicar:
        if not selecionados:
            st.warning("Selecione ao menos um cliente.")
        else:
            placeholders = ",".join(["%s"] * len(selecionados))
            execute_write(
                f"UPDATE cliente SET vendedor_id=%s WHERE cliente_id IN ({placeholders})",
                [destino[0]] + selecionados
            )
            st.success(f"✅ {len(selecionados)} cliente(s) atribuídos a **{destino[1]}**!")
            # Limpa selecao
            for c in clientes:
                st.session_state.pop(f"chk_{c[0]}", None)
            st.session_state.pop("cart_sel_todos", None)
            st.rerun()
