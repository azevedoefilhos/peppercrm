# configuracao.py — PepperCRM
# Configuração do sistema e cadastro do representante

import streamlit as st
from database import conectar, query


def _ir(p):
    st.session_state["pagina"] = p
    st.session_state["_scroll_topo"] = True
    st.rerun()


def _sucesso(msg):
    st.success(msg)


def _erro(msg):
    st.error(msg)


def _ufs():
    return ["AC","AL","AM","AP","BA","CE","DF","ES","GO","MA",
            "MG","MS","MT","PA","PB","PE","PI","PR","RJ","RN",
            "RO","RR","RS","SC","SE","SP","TO"]


# ═══════════════════════════════════════════════════════
# ENTRADA PRINCIPAL
# ═══════════════════════════════════════════════════════

def tela_configuracao():
    st.header("⚙️ Configuração")
    if st.button("⬅ Voltar"):
        _ir("home")

    from permissoes import e_master
    ABAS_CFG = {
        "empresa": "🏢 Minha Empresa",
        "sistema": "⚙️ Sistema",
        "usuarios": "👤 Usuários",
    }
    if e_master():
        ABAS_CFG["empresas"] = "🏢 Empresas"

    if "cfg_aba" not in st.session_state: st.session_state["cfg_aba"] = "empresa"
    cols = st.columns(len(ABAS_CFG))
    for col,(k,v) in zip(cols, ABAS_CFG.items()):
        ativa = st.session_state["cfg_aba"] == k
        if col.button(v, key=f"cfgnav_{k}", width="stretch",
                      type="primary" if ativa else "secondary"):
            st.session_state["cfg_aba"] = k; st.rerun()
    st.divider()
    a = st.session_state["cfg_aba"]
    if a == "empresa":  _tela_minha_empresa()
    elif a == "sistema": _tela_sistema()
    elif a == "usuarios":
        from usuarios import tela_usuarios
        tela_usuarios(embutido=True)
    elif a == "empresas":
        from usuarios import tela_empresas
        tela_empresas(embutido=True)


# ═══════════════════════════════════════════════════════
# DADOS DO SISTEMA
# ═══════════════════════════════════════════════════════

def _tela_minha_empresa():
    """Une Dados do sistema + Representante em uma unica tela."""
    st.subheader("🏢 Minha Empresa")
    st.caption("Dados da empresa/representação — usados em documentos, relatórios e cabeçalhos.")
    _criar_tabela_configuracao()

    conn = conectar()
    cfg = conn.execute("SELECT * FROM configuracao ORDER BY config_id DESC LIMIT 1").fetchone()
    rep = conn.execute("SELECT * FROM representante ORDER BY representante_id LIMIT 1").fetchone()
    conn.close()

    with st.form("form_empresa"):
        st.markdown("**Identificação**")
        col1, col2 = st.columns(2)
        with col1:
            empresa  = st.text_input("Nome fantasia / Representação *",
                                     value=(rep["nome_fantasia"] if rep else "") or (cfg["empresa_nome"] if cfg else ""))
            razao    = st.text_input("Razão social",
                                     value=rep["razao_social"] if rep else "")
            cnpj     = st.text_input("CNPJ", value=rep["cnpj"] if rep else "")
        with col2:
            fone     = st.text_input("Telefone", value=rep["fone"] if rep else "")
            email_r  = st.text_input("E-mail", value=rep["email"] if rep else "")
            site     = st.text_input("Site", value=rep["site"] if rep else "")

        st.markdown("**Endereço**")
        col3, col4 = st.columns(2)
        with col3:
            endereco = st.text_input("Endereço", value=rep["endereco"] if rep else "")
            bairro   = st.text_input("Bairro", value=rep["bairro"] if rep else "")
        with col4:
            cidade   = st.text_input("Cidade", value=rep["cidade"] if rep else "")
            ufs_list = _ufs()
            idx_uf   = ufs_list.index(rep["estado"]) if rep and rep["estado"] in ufs_list else 25
            estado   = st.selectbox("UF", ufs_list, index=idx_uf)

        obs = st.text_area("Observação", value=rep["observacao"] if rep else "")
        salvar = st.form_submit_button("💾 Salvar dados da empresa", type="primary")

    if salvar:
        if not empresa.strip():
            _erro("Nome fantasia é obrigatório."); return
        conn = conectar()
        # Atualiza configuracao
        if cfg:
            conn.execute("UPDATE configuracao SET empresa_nome=? WHERE config_id=?",
                         (empresa.strip(), cfg["config_id"]))
        else:
            from datetime import date
            conn.execute("""INSERT INTO configuracao (empresa_nome, modo_operacao, data_instalacao, versao_sistema)
                VALUES (?,?,?,?)""", (empresa.strip(), 'REPRESENTACAO', str(date.today()), '1.0'))
        # Atualiza representante
        if rep:
            conn.execute("""UPDATE representante SET razao_social=?, nome_fantasia=?, cnpj=?,
                fone=?, email=?, endereco=?, bairro=?, cidade=?, estado=?, site=?, observacao=?
                WHERE representante_id=?""",
                (razao, empresa.strip(), cnpj, fone, email_r, endereco, bairro,
                 cidade, estado, site, obs, rep["representante_id"]))
        else:
            conn.execute("""INSERT INTO representante (razao_social,nome_fantasia,cnpj,fone,email,
                endereco,bairro,cidade,estado,site,observacao,ativo)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,1)""",
                (razao, empresa.strip(), cnpj, fone, email_r, endereco, bairro,
                 cidade, estado, site, obs))
        conn.commit(); conn.close()
        _sucesso("Dados da empresa salvos!")
        st.rerun()


def _tela_sistema():
    """Configuracoes do sistema: modo de operacao, API, seguranca."""
    st.subheader("⚙️ Configurações do sistema")
    _criar_tabela_configuracao()

    conn = conectar()
    cfg = conn.execute("SELECT * FROM configuracao ORDER BY config_id DESC LIMIT 1").fetchone()
    conn.close()

    modo_atual = cfg["modo_operacao"] if cfg else "REPRESENTACAO"
    api_atual  = cfg["anthropic_api_key"] if cfg and "anthropic_api_key" in cfg.keys() else ""
    senha_atual = cfg["senha_exclusao"] if cfg and "senha_exclusao" in cfg.keys() else "EXCLUIR123"

    with st.form("form_sistema"):
        st.markdown("**Modo de operação**")
        MODOS = {
            "REPRESENTACAO":  "Representação Comercial (autônomo, multilinhas)",
            "DISTRIBUIDOR":   "Distribuidor (compra e revende, foco em vendas)",
            "FORNECEDOR":     "Fornecedor / Indústria (fabrica e vende diretamente)",
        }
        idx_modo = list(MODOS.keys()).index(modo_atual) if modo_atual in MODOS else 0
        modo = st.selectbox("Modo", list(MODOS.keys()),
                            index=idx_modo,
                            format_func=lambda x: MODOS[x])
        st.caption("Define a terminologia e módulos disponíveis no sistema.")

        st.divider()
        st.markdown("**Inteligência Artificial (opcional)**")
        api_key = st.text_input("Chave de API Anthropic", value=api_atual or "",
                                type="password", placeholder="sk-ant-...")
        if api_atual:
            vis = api_atual[:12] + "..." + api_atual[-4:]
            st.caption(f"✅ Chave configurada: `{vis}`")

        st.divider()
        st.markdown("**Segurança**")
        senha_exc = st.text_input("Senha de exclusão", value=senha_atual,
                                  type="password", help="Exigida para excluir registros.")

        salvar = st.form_submit_button("💾 Salvar configurações", type="primary")

    if salvar:
        conn = conectar()
        if cfg:
            conn.execute("""UPDATE configuracao SET modo_operacao=?,
                anthropic_api_key=?, senha_exclusao=? WHERE config_id=?""",
                (modo, api_key.strip() or None, senha_exc.strip() or "EXCLUIR123",
                 cfg["config_id"]))
        else:
            from datetime import date
            conn.execute("""INSERT INTO configuracao (modo_operacao,anthropic_api_key,
                senha_exclusao,data_instalacao,versao_sistema)
                VALUES (?,?,?,?,?)""",
                (modo, api_key.strip() or None, senha_exc.strip() or "EXCLUIR123",
                 str(date.today()), "1.0"))
        conn.commit(); conn.close()
        _sucesso("Configurações salvas!")
        st.rerun()
    st.subheader("Dados do sistema")
    st.caption("Informações gerais sobre esta instalação do PepperCRM.")

    _criar_tabela_configuracao()

    conn = conectar()
    cfg = conn.execute(
        "SELECT * FROM configuracao ORDER BY config_id DESC LIMIT 1"
    ).fetchone()
    conn.close()

    # Valores atuais
    modo_atual    = cfg["modo_operacao"]  if cfg else "REPRESENTANTE"
    empresa_atual = cfg["empresa_nome"]   if cfg else ""
    versao_atual  = cfg["versao_sistema"] if cfg else "1.0"
    data_inst     = cfg["data_instalacao"] if cfg else ""

    api_key_atual = cfg["anthropic_api_key"] if cfg and "anthropic_api_key" in cfg.keys() else ""

    with st.form("form_config_sistema"):
        col1, col2 = st.columns(2)
        with col1:
            modo = st.selectbox(
                "Modo de operação",
                ["REPRESENTANTE", "FORNECEDOR"],
                index=0 if modo_atual == "REPRESENTANTE" else 1
            )
            empresa = st.text_input("Nome da empresa / representação",
                                    value=empresa_atual or "")
        with col2:
            versao = st.text_input("Versão do sistema", value=versao_atual or "1.0",
                                   disabled=True)
            if data_inst:
                st.caption(f"Instalado em: {data_inst}")

        st.divider()
        st.markdown("**Inteligência Artificial (opcional)**")
        st.caption(
            "Necessário para usar a sugestão de setores por IA. "
            "Obtenha sua chave em: console.anthropic.com → API Keys"
        )
        api_key_nova = st.text_input(
            "Chave de API Anthropic",
            value=api_key_atual or "",
            type="password",
            placeholder="sk-ant-...",
            help="A chave é armazenada localmente no banco de dados do app."
        )
        if api_key_atual:
            st.caption("✅ Chave de API configurada.")

        st.divider()
        st.markdown("**Segurança**")
        st.caption("Senha exigida para excluir produtos individualmente ou em lote.")
        senha_exc_atual = cfg["senha_exclusao"] if cfg and "senha_exclusao" in cfg.keys() and cfg["senha_exclusao"] else "EXCLUIR123"
        senha_exc_nova  = st.text_input(
            "Senha de exclusão",
            value=senha_exc_atual,
            type="password",
            help="Padrão inicial: EXCLUIR123"
        )

        salvar = st.form_submit_button("Salvar configuração")

    if salvar:
        if not empresa.strip():
            _erro("Nome da empresa é obrigatório.")
            return
        conn = conectar()
        if cfg:
            conn.execute("""
                UPDATE configuracao SET modo_operacao=?, empresa_nome=?,
                anthropic_api_key=?, senha_exclusao=?
                WHERE config_id=?
            """, (modo, empresa, api_key_nova.strip() or None,
                  senha_exc_nova.strip() or "EXCLUIR123", cfg["config_id"]))
        else:
            from datetime import date
            conn.execute("""
                INSERT INTO configuracao
                (modo_operacao, empresa_nome, data_instalacao, versao_sistema,
                 anthropic_api_key, senha_exclusao)
                VALUES (?,?,?,?,?,?)
            """, (modo, empresa, str(date.today()), "1.0",
                  api_key_nova.strip() or None,
                  senha_exc_nova.strip() or "EXCLUIR123"))
        conn.commit()
        conn.close()
        _sucesso("Configuração salva!")
        st.rerun()

    # Diagnóstico da chave de API — ajuda a confirmar se foi salva
    st.divider()
    st.caption("**Diagnóstico da chave de API:**")
    _chave_db = query("SELECT anthropic_api_key FROM configuracao ORDER BY config_id DESC LIMIT 1")
    _chave_val = _chave_db[0][0] if _chave_db and _chave_db[0][0] else None
    if _chave_val:
        # Mostra apenas os primeiros e últimos caracteres por segurança
        _vis = _chave_val[:12] + "..." + _chave_val[-4:]
        st.success(f"✅ Chave salva no banco: `{_vis}`")
    else:
        st.warning("⚠️ Nenhuma chave de API encontrada no banco. "
                   "Preencha o campo acima e clique em Salvar.")


# ═══════════════════════════════════════════════════════
# REPRESENTANTE
# ═══════════════════════════════════════════════════════

def _tela_representante():
    st.subheader("Dados da representação")
    st.caption("Informações do representante comercial — usadas em documentos e relatórios.")

    conn = conectar()
    rep = conn.execute(
        "SELECT * FROM representante ORDER BY representante_id LIMIT 1"
    ).fetchone()
    conn.close()

    with st.form("form_representante"):
        col1, col2 = st.columns(2)
        with col1:
            razao    = st.text_input("Razão social",   value=rep["razao_social"]  if rep else "")
            fantasia = st.text_input("Nome fantasia",  value=rep["nome_fantasia"] if rep else "")
            cnpj     = st.text_input("CNPJ",           value=rep["cnpj"]          if rep else "")
            fone     = st.text_input("Telefone",       value=rep["fone"]          if rep else "")
            email    = st.text_input("E-mail",         value=rep["email"]         if rep else "")
        with col2:
            endereco = st.text_input("Endereço",       value=rep["endereco"]      if rep else "")
            bairro   = st.text_input("Bairro",         value=rep["bairro"]        if rep else "")
            cidade   = st.text_input("Cidade",         value=rep["cidade"]        if rep else "")
            ufs = _ufs()
            idx = ufs.index(rep["estado"]) if rep and rep["estado"] in ufs else 0
            estado   = st.selectbox("UF", ufs, index=idx)
            site     = st.text_input("Site",           value=rep["site"]          if rep else "")
        obs = st.text_area("Observação", value=rep["observacao"] if rep else "")
        salvar = st.form_submit_button("Salvar dados do representante")

    if salvar:
        if not fantasia.strip():
            _erro("Nome fantasia é obrigatório.")
            return
        conn = conectar()
        if rep:
            conn.execute("""
                UPDATE representante SET
                razao_social=?, nome_fantasia=?, cnpj=?, fone=?, email=?,
                endereco=?, bairro=?, cidade=?, estado=?, site=?, observacao=?, ativo=1
                WHERE representante_id=?
            """, (razao, fantasia, cnpj, fone, email,
                  endereco, bairro, cidade, estado, site, obs,
                  rep["representante_id"]))
        else:
            conn.execute("""
                INSERT INTO representante
                (razao_social, nome_fantasia, cnpj, fone, email,
                 endereco, bairro, cidade, estado, site, observacao, ativo)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,1)
            """, (razao, fantasia, cnpj, fone, email,
                  endereco, bairro, cidade, estado, site, obs))
        conn.commit()
        conn.close()
        _sucesso("Dados do representante salvos!")
        st.rerun()


# ═══════════════════════════════════════════════════════
# VENDEDORES
# ═══════════════════════════════════════════════════════

def _tela_vendedores():
    st.subheader("Vendedores / equipe")
    st.caption("Cadastre os vendedores vinculados a esta representação.")

    conn = conectar()
    rep = conn.execute(
        "SELECT representante_id FROM representante LIMIT 1"
    ).fetchone()
    conn.close()

    if not rep:
        st.warning("Cadastre os dados do representante primeiro.")
        return

    rep_id = rep["representante_id"]

    # Lista atual
    vendedores = query("""
        SELECT vendedor_id, nome, fone, email, cpf, ativo
        FROM vendedor WHERE representante_id=?
        ORDER BY nome
    """, (rep_id,))

    if vendedores:
        import pandas as pd
        df = pd.DataFrame(vendedores,
                          columns=["ID", "Nome", "Fone", "E-mail", "CPF", "Ativo"])
        df["Ativo"] = df["Ativo"].map({1: "✅", 0: "❌"})
        st.dataframe(df, width="stretch", hide_index=True)

        # Editar vendedor
        st.divider()
        st.subheader("Editar vendedor")
        ids = [(r[0], r[1]) for r in vendedores]
        sel = st.selectbox("Selecione", ids, format_func=lambda x: x[1],
                           key="sel_vend_edit")
        if sel:
            _form_editar_vendedor(sel[0])
    else:
        st.info("Nenhum vendedor cadastrado.")

    st.divider()
    st.subheader("Novo vendedor")
    _form_novo_vendedor(rep_id)


def _form_novo_vendedor(rep_id):
    with st.form("novo_vendedor", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nome      = st.text_input("Nome")
            fone      = st.text_input("Fone / WhatsApp")
            email     = st.text_input("E-mail")
        with col2:
            cpf       = st.text_input("CPF")
            pix       = st.text_input("Chave PIX")
            aniver    = st.text_input("Data de aniversário", placeholder="DD/MM")
        obs    = st.text_input("Observação")
        salvar = st.form_submit_button("Cadastrar vendedor")

    if salvar:
        if not nome.strip():
            _erro("Nome é obrigatório.")
            return
        conn = conectar()
        conn.execute("""
            INSERT INTO vendedor
            (representante_id, nome, fone, email, cpf, chave_pix,
             data_aniversario, observacao, ativo)
            VALUES (?,?,?,?,?,?,?,?,1)
        """, (rep_id, nome, fone, email, cpf, pix, aniver or None, obs or None))
        conn.commit()
        conn.close()
        _sucesso(f"Vendedor '{nome}' cadastrado!")
        st.rerun()


def _form_editar_vendedor(vend_id):
    conn = conectar()
    v = conn.execute(
        "SELECT * FROM vendedor WHERE vendedor_id=?", (vend_id,)
    ).fetchone()
    conn.close()
    if not v:
        return

    with st.form(f"edit_vend_{vend_id}"):
        col1, col2 = st.columns(2)
        with col1:
            nome   = st.text_input("Nome",          value=v["nome"] or "")
            fone   = st.text_input("Fone",          value=v["fone"] or "")
            email  = st.text_input("E-mail",        value=v["email"] or "")
        with col2:
            cpf    = st.text_input("CPF",           value=v["cpf"] or "")
            pix    = st.text_input("Chave PIX",     value=v["chave_pix"] or "")
            aniver = st.text_input("Aniversário",   value=v["data_aniversario"] or "")
        obs   = st.text_input("Observação",         value=v["observacao"] or "")
        ativo = st.checkbox("Ativo", value=bool(v["ativo"]))
        salvar = st.form_submit_button("Salvar alterações")

    if salvar:
        conn = conectar()
        conn.execute("""
            UPDATE vendedor SET nome=?, fone=?, email=?, cpf=?,
            chave_pix=?, data_aniversario=?, observacao=?, ativo=?
            WHERE vendedor_id=?
        """, (nome, fone, email, cpf, pix, aniver or None,
              obs or None, int(ativo), vend_id))
        conn.commit()
        conn.close()
        _sucesso("Vendedor atualizado!")
        st.rerun()


# ═══════════════════════════════════════════════════════
# HELPERS PARA OUTROS MÓDULOS
# ═══════════════════════════════════════════════════════

def get_nome_empresa():
    """Retorna o nome da empresa configurada, ou 'PepperCRM' como padrão."""
    try:
        _criar_tabela_configuracao()
        rows = query("SELECT empresa_nome FROM configuracao ORDER BY config_id DESC LIMIT 1")
        return rows[0][0] if rows and rows[0][0] else "PepperCRM"
    except Exception:
        return "PepperCRM"


def _criar_tabela_configuracao():
    """Cria tabela configuracao se não existir — Railway e SQLite."""
    from database import _check_supabase, execute_write
    from datetime import date
    if _check_supabase():
        execute_write("""
            CREATE TABLE IF NOT EXISTS configuracao (
                config_id           SERIAL PRIMARY KEY,
                modo_operacao       TEXT DEFAULT 'REPRESENTANTE',
                empresa_nome        TEXT,
                versao_sistema      TEXT DEFAULT '1.0',
                data_instalacao     TEXT,
                anthropic_api_key   TEXT,
                senha_exclusao      TEXT DEFAULT 'EXCLUIR123'
            )
        """)
    else:
        execute_write("""
            CREATE TABLE IF NOT EXISTS configuracao (
                config_id           INTEGER PRIMARY KEY AUTOINCREMENT,
                modo_operacao       TEXT DEFAULT 'REPRESENTANTE',
                empresa_nome        TEXT,
                versao_sistema      TEXT DEFAULT '1.0',
                data_instalacao     TEXT,
                anthropic_api_key   TEXT,
                senha_exclusao      TEXT DEFAULT 'EXCLUIR123'
            )
        """)
    # Insere registro padrão se vazia
    rows = query("SELECT COUNT(*) FROM configuracao")
    if rows and rows[0][0] == 0:
        execute_write(
            "INSERT INTO configuracao (modo_operacao, empresa_nome, versao_sistema, data_instalacao, senha_exclusao) VALUES (?,?,?,?,?)",
            ('REPRESENTANTE', 'Azevedo e Filhos Representação Comercial',
             '1.0', str(date.today()), 'EXCLUIR123')
        )


def get_representante():
    """Retorna os dados do representante ou None."""
    conn = conectar()
    rep = conn.execute(
        "SELECT * FROM representante ORDER BY representante_id LIMIT 1"
    ).fetchone()
    conn.close()
    return rep


def get_anthropic_api_key():
    """Retorna a chave de API Anthropic configurada, ou None."""
    rows = query("SELECT anthropic_api_key FROM configuracao ORDER BY config_id DESC LIMIT 1")
    if rows and rows[0][0]:
        return rows[0][0]
    return None