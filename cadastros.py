from cache_helpers import cache_clientes, cache_fornecedores, cache_categorias, cache_produtos_fornecedor
# cadastros.py — PepperCRM
# Módulos: Fornecedor · Produto · Tabela de Preços · Cliente · PDVs · Mix

import streamlit as st
import io
import pandas as pd
from database import conectar, query
# api key buscada diretamente no banco (evita importacao circular)

# ─────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────

def _ir(p):
    st.session_state["pagina"] = p
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
# 1. FORNECEDORES
# ═══════════════════════════════════════════════════════

def tela_fornecedores():
    st.header("Fornecedores")
    if st.button("⬅ Voltar"):
        _ir("home")

    ABAS_FORN = {"lista":"Lista","novo":"Novo Fornecedor","ct":"Contatos"}
    if "forn_aba" not in st.session_state: st.session_state["forn_aba"] = "lista"
    cols = st.columns(3)
    for col,(k,v) in zip(cols, ABAS_FORN.items()):
        ativa = st.session_state["forn_aba"] == k
        if col.button(v, key=f"fnav_{k}", use_container_width=True,
                      type="primary" if ativa else "secondary"):
            st.session_state["forn_aba"] = k; st.rerun()
    st.divider()
    a = st.session_state["forn_aba"]
    if a == "lista":
        dados = query("SELECT fornecedor_id, nome_fantasia, cidade, estado, cnpj, ativo FROM fornecedor ORDER BY nome_fantasia")
        if dados:
            df = pd.DataFrame(dados, columns=["ID", "Fantasia", "Cidade", "UF", "CNPJ", "Ativo"])
            df["Ativo"] = df["Ativo"].map({1: "✅", 0: "❌"})
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.divider()
            st.subheader("Editar fornecedor")
            ids = [(r[0], r[1]) for r in dados]
            sel = st.selectbox("Selecione", ids, format_func=lambda x: x[1])
            if sel:
                _form_editar_fornecedor(sel[0])
        else:
            st.info("Nenhum fornecedor cadastrado.")
    elif a == "novo": _form_novo_fornecedor()
    elif a == "ct":   _tela_contatos_fornecedor()


def _form_novo_fornecedor():
    st.subheader("Novo fornecedor")
    with st.form("form_novo_forn", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            razao    = st.text_input("Razão social")
            fantasia = st.text_input("Nome fantasia")
            cnpj     = st.text_input("CNPJ")
            ie       = st.text_input("IE")
        with col2:
            endereco = st.text_input("Endereço")
            bairro   = st.text_input("Bairro")
            cidade   = st.text_input("Cidade")
            estado   = st.selectbox("UF", _ufs())
        pedido_minimo = st.number_input(
            "💰 Pedido mínimo (R$)",
            min_value=0.0, value=0.0, step=50.0, format="%.2f",
            help="Valor mínimo por pedido. Deixe 0 para sem restrição.")
        obs    = st.text_area("Observação")
        salvar = st.form_submit_button("Salvar fornecedor")

    if salvar:
        if not fantasia.strip():
            _erro("Nome fantasia é obrigatório.")
            return
        conn = conectar()
        conn.execute("""
            INSERT INTO fornecedor
            (razao_social, nome_fantasia, cnpj, ie, endereco, bairro, cidade, estado, observacao, ativo, pedido_minimo)
            VALUES (?,?,?,?,?,?,?,?,?,1,?)
        """, (razao, fantasia, cnpj, ie, endereco, bairro, cidade, estado, obs,
              pedido_minimo if pedido_minimo > 0 else None))
        conn.commit(); conn.close()
        _sucesso(f"Fornecedor '{fantasia}' cadastrado!")


def _form_editar_fornecedor(forn_id):
    conn = conectar()
    f = conn.execute("SELECT * FROM fornecedor WHERE fornecedor_id=?", (forn_id,)).fetchone()
    conn.close()
    if not f:
        return
    with st.form(f"edit_forn_{forn_id}"):
        col1, col2 = st.columns(2)
        with col1:
            razao    = st.text_input("Razão social",  f["razao_social"] or "")
            fantasia = st.text_input("Nome fantasia", f["nome_fantasia"] or "")
            cnpj     = st.text_input("CNPJ",          f["cnpj"] or "")
            ie       = st.text_input("IE",            f["ie"] or "")
        with col2:
            endereco = st.text_input("Endereço", f["endereco"] or "")
            bairro   = st.text_input("Bairro",   f["bairro"] or "")
            cidade   = st.text_input("Cidade",   f["cidade"] or "")
            ufs = _ufs()
            idx = ufs.index(f["estado"]) if f["estado"] in ufs else 0
            estado = st.selectbox("UF", ufs, index=idx)
        _pm_atual = float(f["pedido_minimo"]) if f["pedido_minimo"] else 0.0
        pedido_minimo = st.number_input(
            "💰 Pedido mínimo (R$)",
            min_value=0.0, value=_pm_atual, step=50.0, format="%.2f",
            help="Valor mínimo por pedido. Deixe 0 para sem restrição.")
        obs   = st.text_area("Observação", f["observacao"] or "")
        ativo = st.checkbox("Ativo", value=bool(f["ativo"]))
        salvar = st.form_submit_button("Salvar alterações")

    if salvar:
        conn = conectar()
        conn.execute("""
            UPDATE fornecedor SET razao_social=?, nome_fantasia=?, cnpj=?, ie=?,
            endereco=?, bairro=?, cidade=?, estado=?, observacao=?, ativo=?,
            pedido_minimo=?
            WHERE fornecedor_id=?
        """, (razao, fantasia, cnpj, ie, endereco, bairro, cidade, estado, obs, int(ativo),
              pedido_minimo if pedido_minimo > 0 else None, forn_id))
        conn.commit(); conn.close()
        _sucesso("Fornecedor atualizado!")


def _tela_contatos_fornecedor():
    st.subheader("Contatos por fornecedor")
    forns = cache_fornecedores()
    if not forns:
        st.info("Cadastre um fornecedor primeiro.")
        return
    forn_sel = st.selectbox("Fornecedor", forns, format_func=lambda x: x[1])
    forn_id  = forn_sel[0]
    contatos = query("""
        SELECT contato_fornecedor_id, nome_contato, departamento, fone, email
        FROM contato_fornecedor WHERE fornecedor_id=? AND ativo=1
    """, (forn_id,))
    if contatos:
        st.dataframe(pd.DataFrame(contatos, columns=["ID","Nome","Departamento","Fone","E-mail"]),
                     use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum contato cadastrado para este fornecedor.")
    st.subheader("Adicionar contato")
    with st.form(f"novo_contato_forn_{forn_id}", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nome  = st.text_input("Nome")
            depto = st.text_input("Departamento")
        with col2:
            fone  = st.text_input("Fone")
            email = st.text_input("E-mail")
        obs    = st.text_input("Observação")
        salvar = st.form_submit_button("Adicionar contato")
    if salvar:
        if not nome.strip():
            _erro("Nome é obrigatório.")
            return
        conn = conectar()
        conn.execute("""
            INSERT INTO contato_fornecedor
            (fornecedor_id, nome_contato, departamento, fone, email, observacao, ativo)
            VALUES (?,?,?,?,?,?,1)
        """, (forn_id, nome, depto, fone, email, obs))
        conn.commit(); conn.close()
        _sucesso(f"Contato '{nome}' adicionado!")
        st.rerun()


# ═══════════════════════════════════════════════════════
# 2. PRODUTOS
# ═══════════════════════════════════════════════════════



@st.cache_data(ttl=60, show_spinner=False)
def _load_produtos():
    """Cache de produtos - nivel de modulo para persistir entre navegacoes."""
    return query("""
        SELECT p.produto_id, f.nome_fantasia, m.nome_marca,
               COALESCE(cat.nome_categoria,''), COALESCE(l.nome_linha,''),
               p.codigo_produto, p.descricao, p.descricao_curta,
               p.unidade_medida, p.unidades_caixa,
               COALESCE(p.peso,0), COALESCE(p.peso_caixa,0),
               COALESCE(p.sub_categoria,''), COALESCE(p.grupo,''),
               COALESCE(p.validade_dias,0),
               COALESCE(p.ean,''), COALESCE(p.dun,''),
               COALESCE(p.ncm,''), COALESCE(p.cest,''),
               COALESCE(p.observacao,''),
               p.ativo
        FROM produto p
        LEFT JOIN fornecedor f   ON p.fornecedor_id = f.fornecedor_id
        LEFT JOIN marca m        ON p.marca_id = m.marca_id
        LEFT JOIN categoria cat  ON p.categoria_id = cat.categoria_id
        LEFT JOIN linha l        ON p.linha_id = l.linha_id
        ORDER BY f.nome_fantasia, p.descricao
    """)

def tela_produtos():
    st.header("Produtos")
    if st.button("⬅ Voltar"): _ir("home")
    ABAS_PROD = {"lista":"Lista","novo":"Novo Produto",
                 "import":"Importar Excel","catalogo":"📄 Catálogo PDF",
                 "excluir":"⚠️ Excluir em lote"}
    if "prod_aba" not in st.session_state:
        st.session_state["prod_aba"] = "lista"
    cols = st.columns(len(ABAS_PROD))
    for col,(k,v) in zip(cols, ABAS_PROD.items()):
        ativa = st.session_state["prod_aba"] == k
        if col.button(v, key=f"pnav_{k}", use_container_width=True,
                      type="primary" if ativa else "secondary"):
            st.session_state["prod_aba"] = k; st.rerun()
    st.divider()
    a = st.session_state["prod_aba"]
    if a=="lista":    _lista_produtos()
    elif a=="novo":   _form_novo_produto()
    elif a=="import": _importar_produtos_excel()
    elif a=="catalogo":
        from catalogo import _tela_catalogo
        _tela_catalogo()
    elif a=="excluir":_excluir_produtos_lote()


def _lista_produtos():
    # Scroll para o topo ao entrar na lista
    st.markdown('<div id="topo_produtos"></div>', unsafe_allow_html=True)

    # Banners de feedback
    msg_del  = st.session_state.pop("prod_excluir_ok", None)
    msg_edit = st.session_state.pop("prod_edit_ok", None)
    msg_novo = st.session_state.pop("prod_sucesso_msg", None)
    if msg_del:  st.success(msg_del)
    if msg_edit: st.success(msg_edit)
    if msg_novo: st.success(msg_novo)

    dados = _load_produtos()
    if not dados:
        st.info("Nenhum produto cadastrado.")
        return

    colunas_exp = ["ID","Fornecedor","Marca","Categoria","Linha","Codigo",
                   "Descricao","Descricao curta","UM","Un/Cx",
                   "Peso un.","Peso cx.","Sub-categoria","Grupo",
                   "Validade (d)","EAN","DUN","NCM","CEST","Observacao","Ativo"]
    df_full = pd.DataFrame(dados, columns=colunas_exp)

    # ── BLOCO DE FILTROS ─────────────────────────────────────────────────
    # Linha 1: Fornecedor + Categoria + Busca texto
    col_f, col_cat, col_b = st.columns([1.8, 1.8, 2.4])
    with col_f:
        forns = ["Todos"] + sorted(df_full["Fornecedor"].dropna().unique().tolist())
        sel_forn = st.selectbox("Fornecedor", forns, key="lp_forn_filtro")

    # Aplica filtro de fornecedor antes de popular os demais filtros
    df_forn = df_full if sel_forn == "Todos" else df_full[df_full["Fornecedor"] == sel_forn]

    with col_cat:
        cats_disp = ["Todos"] + sorted(
            v for v in df_forn["Categoria"].dropna().unique() if v and v != "—")
        sel_cat = st.selectbox("Categoria", cats_disp, key="lp_cat_filtro")

    # Aplica filtro de categoria
    df_forn_cat = df_forn if sel_cat == "Todos" else df_forn[df_forn["Categoria"] == sel_cat]

    with col_b:
        busca = st.text_input("🔍 Buscar por descrição ou código",
                              placeholder="Digite parte do nome ou código...",
                              key="lp_busca")

    # Linha 2: Filtro coringa sincronizado com fornecedor+categoria
    col_tipo, col_val, col_exp_x, col_exp_p = st.columns([1.5, 2.5, 0.7, 0.7])
    with col_tipo:
        tipo_coringa = st.selectbox("Filtrar por",
                                    ["— nenhum —","Linha","Sub-categoria","Grupo"],
                                    key="lp_coringa_tipo")
    with col_val:
        def _opts(coluna):
            return ["Todos"] + sorted(
                v for v in df_forn_cat[coluna].dropna().unique() if v and v != "—")

        if tipo_coringa == "Linha":
            val_coringa = st.selectbox("Linha", _opts("Linha"), key="lp_cv_linha")
        elif tipo_coringa == "Sub-categoria":
            val_coringa = st.selectbox("Sub-categoria", _opts("Sub-categoria"), key="lp_cv_sub")
        elif tipo_coringa == "Grupo":
            val_coringa = st.selectbox("Grupo", _opts("Grupo"), key="lp_cv_grp")
        else:
            val_coringa = "Todos"
            st.empty()

    with col_exp_x:
        if st.button("⬇️ Excel", key="exp_prod_xlsx", use_container_width=True):
            st.session_state["exp_prod_trigger"] = "excel"
    with col_exp_p:
        if st.button("⬇️ PDF", key="exp_prod_pdf", use_container_width=True):
            st.session_state["exp_prod_trigger"] = "pdf"

    # ── APLICA TODOS OS FILTROS em cascata ────────────────────────────────
    df = df_forn_cat.copy()

    # Filtro coringa
    if tipo_coringa != "— nenhum —" and val_coringa != "Todos":
        df = df[df[tipo_coringa] == val_coringa]

    # Busca texto
    if busca.strip():
        b = busca.strip()
        mask = (df["Descricao"].str.contains(b, case=False, na=False) |
                df["Descricao curta"].str.contains(b, case=False, na=False) |
                df["Codigo"].str.contains(b, case=False, na=False))
        df = df[mask]

    # ── CONTADOR CONTEXTUAL ───────────────────────────────────────────────
    filtros_ativos = []
    if sel_forn != "Todos":    filtros_ativos.append(sel_forn)
    if sel_cat  != "Todos":    filtros_ativos.append(sel_cat)
    if tipo_coringa != "— nenhum —" and val_coringa != "Todos":
        filtros_ativos.append(f"{tipo_coringa}: {val_coringa}")
    if busca.strip():          filtros_ativos.append(f'"{busca.strip()}"')
    contexto = f" — {' | '.join(filtros_ativos)}" if filtros_ativos else ""
    st.caption(f"**{len(df)}** produto(s){contexto}  |  Total no banco: {len(df_full)}")

    # ── EXPORTAÇÃO — gera antes do botão para 1 clique ───────────────────
    # Renomeia para nomes do template de importação
    # Reordena e renomeia para espelhar template de importação
    _cols_ordem = ["fornecedor_nome","marca_nome","categoria_nome","linha_nome",
                   "sub_categoria","grupo","codigo_produto","descricao","descricao_curta",
                   "unidade_medida","peso_unidade","peso_caixa","unidades_caixa",
                   "validade_dias","ean","dun","ncm","cest","observacao","ativo"]
    _mapa_cols = {
        "Fornecedor":"fornecedor_nome","Marca":"marca_nome","Categoria":"categoria_nome",
        "Linha":"linha_nome","Sub-categoria":"sub_categoria","Grupo":"grupo",
        "Codigo":"codigo_produto","Descricao":"descricao","Descricao curta":"descricao_curta",
        "UM":"unidade_medida","Peso un.":"peso_unidade","Peso cx.":"peso_caixa",
        "Un/Cx":"unidades_caixa","Validade (d)":"validade_dias",
        "EAN":"ean","DUN":"dun","NCM":"ncm","CEST":"cest","Observacao":"observacao","Ativo":"ativo"
    }
    df_exp_prod = df.copy().replace("—","").rename(columns=_mapa_cols)
    # Mantém só as colunas do template na ordem correta (sem ID)
    _cols_disp = [c for c in _cols_ordem if c in df_exp_prod.columns]
    df_exp_prod = df_exp_prod[_cols_disp]
    _buf_prod_xl = io.BytesIO()
    with pd.ExcelWriter(_buf_prod_xl, engine='openpyxl') as _w:
        df_exp_prod.to_excel(_w, index=False, sheet_name="Produtos")
    _nome_prod = f"produtos_{sel_forn.replace(' ','_') if sel_forn!='Todos' else 'todos'}"

    trigger = st.session_state.pop("exp_prod_trigger", None)
    if trigger == "excel":
        st.download_button(
            "📥 Baixar Excel",
            data=_buf_prod_xl.getvalue(), file_name=f"{_nome_prod}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True, key="dl_xlsx_prod_now")
    elif trigger == "pdf":
        with st.spinner("Gerando PDF..."):
            pdf_bytes = _exportar_produtos_pdf(df, sel_forn)
        st.download_button(
            "📥 Baixar PDF",
            data=pdf_bytes, file_name=f"{_nome_prod}.pdf",
            mime="application/pdf",
            use_container_width=True, key="dl_pdf_prod_now")

    st.divider()

    # ── LISTA LEVE — dataframe com seleção para editar ────────────────────
    df_view = df[["ID","Fornecedor","Marca","Codigo","Descricao curta",
                  "Un/Cx","UM","Ativo"]].copy()
    df_view.columns = ["ID","Fornecedor","Marca","Código","Descrição","Un/Cx","UM","Ativo"]

    st.dataframe(df_view, use_container_width=True, hide_index=True,
                 column_config={
                     "ID":        st.column_config.NumberColumn(width="small"),
                     "Fornecedor":st.column_config.TextColumn(width="medium"),
                     "Marca":     st.column_config.TextColumn(width="small"),
                     "Código":    st.column_config.TextColumn(width="small"),
                     "Descrição": st.column_config.TextColumn(width="large"),
                     "Un/Cx":     st.column_config.TextColumn(width="small"),
                     "UM":        st.column_config.TextColumn(width="small"),
                     "Ativo":     st.column_config.TextColumn(width="small"),
                 })

    # ── EDITAR / EXCLUIR — seleção por ID ────────────────────────────────
    st.divider()
    ids_disp = df["ID"].tolist()
    col_sel, col_ed, col_del = st.columns([3, 1, 1])
    with col_sel:
        pid_sel = st.selectbox("Selecionar produto pelo ID",
                               [None] + ids_disp,
                               format_func=lambda x: "— selecione —" if x is None else
                                   f"#{x} — {df[df['ID']==x]['Descricao curta'].values[0]}",
                               key="prod_sel_id")
    with col_ed:
        st.write("")
        if st.button("✏️ Editar", key="btn_ed_prod",
                     use_container_width=True, disabled=pid_sel is None):
            st.session_state["prod_editar_id"] = pid_sel
            st.session_state.pop("prod_excluir_id", None)
            st.rerun()
    with col_del:
        st.write("")
        if st.button("🗑️ Excluir", key="btn_del_prod",
                     use_container_width=True, disabled=pid_sel is None):
            st.session_state["prod_excluir_id"] = pid_sel
            st.session_state.pop("prod_editar_id", None)
            st.rerun()

    # Form editar/excluir renderizado abaixo da lista
    _eid = st.session_state.get("prod_editar_id")
    _did = st.session_state.get("prod_excluir_id")
    if _eid and _eid in ids_disp:
        row = df[df["ID"] == _eid].iloc[0]
        st.info(f"Editando: **{row['Descricao curta']}** (#{_eid})")
        _form_editar_produto(_eid)
    if _did and _did in ids_disp:
        row = df[df["ID"] == _did].iloc[0]
        _confirmacao_excluir_produto(_did,
            str(row["Descricao curta"]), str(row["Codigo"]))



def _confirmacao_excluir_produto(pid, desc_c, codigo):
    """Confirmação com senha antes de excluir produto individualmente."""
    st.warning(f"Excluir produto **{desc_c}** (código: {codigo}, ID: {pid})?")

    # Verifica vínculos
    n_tab = query("""SELECT COUNT(*) FROM tabela_preco_item WHERE produto_id=?""",
                  (pid,))[0][0]
    n_mix = query("""SELECT COUNT(*) FROM mix_cliente WHERE produto_id=?""",
                  (pid,))[0][0]
    n_ped = query("""SELECT COUNT(*) FROM pedido_item
                     WHERE produto_id=? AND quantidade > 0""", (pid,))[0][0]

    if n_ped:
        st.error(
            f"Este produto está em **{n_ped} pedido(s)**. "
            f"Não é possível excluí-lo. Use a opção Editar para desativá-lo."
        )
        if st.button("Fechar", key=f"fechar_del_prod_{pid}"):
            st.session_state.pop("prod_excluir_id", None)
            st.rerun()
        return

    if n_tab or n_mix:
        st.info(
            f"Este produto está em **{n_tab} item(ns) de tabela de preços** "
            f"e **{n_mix} mix de PDV(s)**. "
            f"Esses vínculos também serão removidos."
        )

    col_s, col_c = st.columns(2)
    with col_s:
        senha = st.text_input("Senha de administrador", type="password",
                              key=f"del_prod_senha_{pid}",
                              help="Senha padrão: EXCLUIR123")
    with col_c:
        st.write("")
        st.write("")
        confirmar = st.button("✅ Confirmar exclusão", key=f"conf_del_prod_{pid}",
                              type="primary", use_container_width=True)
        cancelar  = st.button("Cancelar", key=f"canc_del_prod_{pid}",
                              use_container_width=True)

    if confirmar:
        if senha != "EXCLUIR123":
            st.error("Senha incorreta.")
            return
        conn = conectar()
        conn.execute("DELETE FROM tabela_preco_item WHERE produto_id=?", (pid,))
        conn.execute("DELETE FROM mix_cliente WHERE produto_id=?", (pid,))
        conn.execute("UPDATE pedido_item SET produto_id=NULL WHERE produto_id=?", (pid,))
        conn.execute("DELETE FROM produto WHERE produto_id=?", (pid,))
        conn.commit(); conn.close()
        st.session_state.pop("prod_excluir_id", None)
        st.session_state["prod_excluir_ok"] = f"✅ Produto '{desc_c}' excluído."
        st.rerun()

    if cancelar:
        st.session_state.pop("prod_excluir_id", None)
        st.rerun()

def _form_editar_produto(prod_id):
    """Formulário de edição inline com todos os campos do produto."""
    prod = query("""
        SELECT p.fornecedor_id, p.marca_id, p.categoria_id, p.linha_id,
               p.codigo_produto, p.descricao, p.descricao_curta,
               p.unidade_medida, p.unidades_caixa, p.peso,
               p.peso_caixa, p.ean, p.dun, p.validade_dias,
               p.ncm, p.cest, p.sub_categoria, p.grupo,
               p.observacao, p.ativo
        FROM produto p WHERE p.produto_id=?
    """, (prod_id,))
    if not prod:
        return

    (forn_id_at, marca_id_at, cat_id_at, linha_id_at,
     codigo_at, desc_at, desc_c_at, um_at, un_cx_at,
     peso_at, peso_cx_at, ean_at, dun_at, val_at,
     ncm_at, cest_at, subcat_at, grupo_at,
     obs_at, ativo_at) = prod[0]

    forns  = cache_fornecedores()
    marcas = query("SELECT marca_id, nome_marca FROM marca WHERE fornecedor_id=? AND ativo=1 ORDER BY nome_marca", (forn_id_at,))
    cats   = cache_categorias()
    linhas = query("""SELECT MIN(linha_id), nome_linha FROM linha WHERE ativo=1
                      GROUP BY nome_linha ORDER BY nome_linha""")

    forn_ids  = [f[0] for f in forns]
    idx_forn  = forn_ids.index(forn_id_at) if forn_id_at in forn_ids else 0
    marca_ids = [m[0] for m in marcas]
    idx_marca = marca_ids.index(marca_id_at) if marca_id_at in marca_ids else 0
    cat_ids   = [c[0] for c in cats]
    idx_cat   = cat_ids.index(cat_id_at) if cat_id_at in cat_ids else 0
    linha_opts    = [(None, "— nenhuma —")] + list(linhas)
    linha_opt_ids = [l[0] for l in linha_opts]
    idx_linha = linha_opt_ids.index(linha_id_at) if linha_id_at in linha_opt_ids else 0
    UMS = ["UN","PCT","kg","g","L","ml","cx","fardo","balde","pote"]
    idx_um = UMS.index(um_at) if um_at in UMS else 0

    st.markdown("**✏️ Editar produto**")
    with st.form(f"edit_prod_{prod_id}"):
        col1, col2 = st.columns(2)
        with col1:
            forn_e    = st.selectbox("Fornecedor", forns, index=idx_forn,
                                     format_func=lambda x: x[1], key=f"ep_forn_{prod_id}")
            marca_e   = st.selectbox("Marca", marcas if marcas else [("","— sem marca —")],
                                     index=idx_marca,
                                     format_func=lambda x: x[1], key=f"ep_marca_{prod_id}")
            cat_e     = st.selectbox("Categoria", cats, index=idx_cat,
                                     format_func=lambda x: x[1], key=f"ep_cat_{prod_id}")
            linha_e   = st.selectbox("Linha", linha_opts, index=idx_linha,
                                     format_func=lambda x: x[1], key=f"ep_linha_{prod_id}")
            subcat_e  = st.text_input("Sub-categoria", value=subcat_at or "",
                                      key=f"ep_sc_{prod_id}")
            grupo_e   = st.text_input("Grupo", value=grupo_at or "",
                                      key=f"ep_gr_{prod_id}")
            codigo_e  = st.text_input("Código do produto", value=codigo_at or "",
                                      key=f"ep_cod_{prod_id}")
            desc_e    = st.text_input("Descrição completa", value=desc_at or "",
                                      key=f"ep_desc_{prod_id}")
            desc_ce   = st.text_input("Descrição curta", value=desc_c_at or "",
                                      max_chars=60, key=f"ep_dc_{prod_id}")
        with col2:
            um_e      = st.selectbox("Unidade de medida", UMS, index=idx_um,
                                     key=f"ep_um_{prod_id}")
            peso_e    = st.number_input("Peso unitário (kg)", min_value=0.0,
                                        value=float(peso_at or 0), format="%.3f",
                                        key=f"ep_peso_{prod_id}")
            peso_cx_e = st.number_input("Peso da caixa (kg)", min_value=0.0,
                                        value=float(peso_cx_at or 0), format="%.3f",
                                        key=f"ep_pcx_{prod_id}")
            un_cx_e   = st.number_input("Unidades por caixa", min_value=1,
                                        value=int(un_cx_at or 1), key=f"ep_uncx_{prod_id}")
            ean_e     = st.text_input("EAN-13", value=ean_at or "",
                                      key=f"ep_ean_{prod_id}")
            dun_e     = st.text_input("DUN-14", value=dun_at or "",
                                      key=f"ep_dun_{prod_id}")
            val_e     = st.number_input("Validade (dias)", min_value=0,
                                        value=int(val_at or 0), key=f"ep_val_{prod_id}")
            ncm_e     = st.text_input("NCM", value=ncm_at or "",
                                      placeholder="8 dígitos", key=f"ep_ncm_{prod_id}")
            cest_e    = st.text_input("CEST", value=cest_at or "",
                                      placeholder="7 dígitos", key=f"ep_cest_{prod_id}")
            obs_e     = st.text_input("Observação", value=obs_at or "",
                                      key=f"ep_obs_{prod_id}")
            ativo_e   = st.checkbox("Ativo", value=bool(ativo_at), key=f"ep_ativo_{prod_id}")

        col_s, col_c = st.columns(2)
        with col_s: salvar   = st.form_submit_button("💾 Salvar alterações", type="primary")
        with col_c: cancelar = st.form_submit_button("Cancelar")

    if salvar:
        if not codigo_e.strip() or not desc_e.strip() or not desc_ce.strip():
            st.error("Código, descrição e descrição curta são obrigatórios.")
        else:
            linha_id_novo = linha_e[0] if linha_e and linha_e[0] else None
            conn = conectar()
            conn.execute("""
                UPDATE produto SET
                fornecedor_id=?, marca_id=?, categoria_id=?, linha_id=?,
                sub_categoria=?, grupo=?,
                codigo_produto=?, descricao=?, descricao_curta=?,
                unidade_medida=?, unidades_caixa=?, peso=?, peso_caixa=?,
                ean=?, dun=?, validade_dias=?,
                ncm=?, cest=?, observacao=?, ativo=?
                WHERE produto_id=?
            """, (forn_e[0], marca_e[0] if marca_e and marca_e[0] else None,
                  cat_e[0], linha_id_novo,
                  subcat_e.strip() or None, grupo_e.strip() or None,
                  codigo_e.strip(), desc_e.strip(), desc_ce.strip(),
                  um_e, un_cx_e, peso_e or None, peso_cx_e or None,
                  ean_e.strip() or None, dun_e.strip() or None,
                  val_e or None,
                  ncm_e.strip() or None, cest_e.strip() or None,
                  obs_e.strip() or None, 1 if ativo_e else 0,
                  prod_id))
            conn.commit(); conn.close()
            st.session_state.pop("prod_editar_id", None)
            st.session_state["prod_edit_ok"] = f"✅ Produto '{desc_ce.strip()}' atualizado!"
            st.rerun()

    if cancelar:
        st.session_state.pop("prod_editar_id", None)
        st.rerun()


def _form_novo_produto():
    st.subheader("Novo produto")
    forns  = cache_fornecedores()

    # Fornecedor selecionado FORA do form — filtra marca/categoria/linha reativamente
    forn_pre = st.selectbox("Fornecedor", forns,
                            format_func=lambda x: x[1],
                            key="np_forn_pre") if forns else None
    forn_pre_id = forn_pre[0] if forn_pre else None

    # Filtra marcas e linhas pelo fornecedor selecionado
    if forn_pre_id:
        marcas = query("""SELECT marca_id, nome_marca FROM marca
                          WHERE fornecedor_id=? AND ativo=1 ORDER BY nome_marca""",
                       (forn_pre_id,))
        # Linhas do fornecedor: busca via produtos, agrupando por nome para evitar duplicatas
        linhas = query("""SELECT MIN(l.linha_id), l.nome_linha
                          FROM linha l
                          JOIN produto p ON p.linha_id = l.linha_id
                          WHERE p.fornecedor_id=? AND l.ativo=1
                          GROUP BY l.nome_linha
                          ORDER BY l.nome_linha""", (forn_pre_id,))
    else:
        marcas = query("SELECT marca_id, nome_marca FROM marca WHERE ativo=1 ORDER BY nome_marca")
        # Sem fornecedor: todas as linhas sem duplicatas de nome
        linhas = query("""SELECT MIN(linha_id), nome_linha FROM linha
                          WHERE ativo=1 GROUP BY nome_linha ORDER BY nome_linha""")

    cats = cache_categorias()

    with st.expander("+ Cadastrar nova Marca / Categoria / Linha"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.caption("Nova marca")
            with st.form("nova_marca", clear_on_submit=True):
                forn_m = st.selectbox("Fornecedor", forns,
                                      format_func=lambda x: x[1], key="fm") if forns else None
                nm     = st.text_input("Nome da marca")
                if st.form_submit_button("Adicionar marca"):
                    if nm and forn_m:
                        conn = conectar()
                        conn.execute("INSERT INTO marca (fornecedor_id, nome_marca, ativo) VALUES (?,?,1)",
                                     (forn_m[0], nm))
                        conn.commit(); conn.close()
                        _sucesso(f"Marca '{nm}' criada!"); st.rerun()
        with col2:
            st.caption("Nova categoria")
            with st.form("nova_cat", clear_on_submit=True):
                nc = st.text_input("Nome da categoria")
                if st.form_submit_button("Adicionar categoria"):
                    if nc:
                        conn = conectar()
                        conn.execute("INSERT INTO categoria (nome_categoria, ativo) VALUES (?,1)", (nc,))
                        conn.commit(); conn.close()
                        _sucesso(f"Categoria '{nc}' criada!"); st.rerun()
        with col3:
            st.caption("Nova linha")
            with st.form("nova_linha", clear_on_submit=True):
                cat_l = st.selectbox("Categoria", cats,
                                     format_func=lambda x: x[1], key="cl") if cats else None
                nl    = st.text_input("Nome da linha")
                if st.form_submit_button("Adicionar linha"):
                    if nl and cat_l:
                        conn = conectar()
                        conn.execute("INSERT INTO linha (categoria_id, nome_linha, ativo) VALUES (?,?,1)",
                                     (cat_l[0], nl))
                        conn.commit(); conn.close()
                        _sucesso(f"Linha '{nl}' criada!"); st.rerun()

    # Campos SEM st.form — preserva dados ao pressionar Enter acidentalmente
    # Mensagem de erro persistente
    suc_msg = st.session_state.pop("np_sucesso_msg", None)
    if suc_msg:
        st.success(suc_msg)
    err_msg = st.session_state.pop("np_erro_msg", None)
    if err_msg:
        st.error(err_msg)

    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Fornecedor selecionado",
                      value=forn_pre[1] if forn_pre else "—",
                      disabled=True)
        marca_sel = st.selectbox("Marca", marcas,
                                 format_func=lambda x: x[1],
                                 key="np_marca") if marcas else None
        cat_sel   = st.selectbox("Categoria", cats,
                                 format_func=lambda x: x[1],
                                 key="np_cat") if cats else None
        linha_sel = st.selectbox("Linha",
                                 [(None, "— nenhuma —")] + list(linhas),
                                 format_func=lambda x: x[1],
                                 key="np_linha")
        sub_cat   = st.text_input("Sub-categoria",
                                  placeholder="Ex: Extra, Especial, 1ª, Fatiado",
                                  key="np_subcat")
        grupo     = st.text_input("Grupo",
                                  placeholder="Ex: Suino, Frango, Bovino, Embutido",
                                  key="np_grupo")
        codigo    = st.text_input("Codigo do produto (fornecedor)", key="np_codigo")
        descricao = st.text_input("Descricao completa", key="np_desc")
        descricao_curta = st.text_input("Descricao curta (tela de pedido)",
                                        max_chars=60,
                                        help="Ate 60 caracteres",
                                        key="np_desc_c")
    with col2:
        unidade    = st.selectbox("Unidade de medida",
                                  ["UN","PCT","kg","g","L","ml","cx","fardo","balde","pote"],
                                  key="np_unidade")
        peso       = st.number_input("Peso / volume unitario (un)", min_value=0.0, value=0.0,
                                     format="%.3f", help="Peso da unidade individual",
                                     key="np_peso")
        peso_caixa = st.number_input("Peso da caixa (kg)", min_value=0.0, value=0.0,
                                     format="%.3f", help="Peso bruto da caixa fechada",
                                     key="np_peso_cx")
        un_caixa   = st.number_input("Unidades por caixa", min_value=1, value=12,
                                     key="np_uncx")
        ean      = st.text_input("EAN-13 (código de barras unidade)",
                                 placeholder="13 dígitos", key="np_ean")
        dun      = st.text_input("DUN-14 (código de barras caixa)",
                                 placeholder="14 dígitos", key="np_dun")
        validade = st.number_input("Validade (dias)", min_value=0, value=0,
                                   key="np_validade")
        ncm      = st.text_input("NCM", placeholder="8 dígitos — ex: 16010010",
                                 help="Nomenclatura Comum do Mercosul", key="np_ncm")
        cest     = st.text_input("CEST", placeholder="7 dígitos — ex: 1700100",
                                 help="Código Especificador da Substituição Tributária",
                                 key="np_cest")
        obs_prod = st.text_input("Observacao", key="np_obs")

    col_btn1, col_btn2, _ = st.columns([1, 1, 3])
    salvar  = col_btn1.button("💾 Salvar produto", type="primary",
                              use_container_width=True, key="np_salvar")
    limpar  = col_btn2.button("🗑️ Limpar campos", use_container_width=True,
                              key="np_limpar")

    if limpar:
        for k in ["np_marca","np_cat","np_linha","np_subcat","np_grupo",
                  "np_codigo","np_desc","np_desc_c","np_unidade",
                  "np_ean","np_dun","np_validade","np_ncm","np_cest","np_obs"]:
            st.session_state.pop(k, None)
        st.rerun()

    if salvar:
        erros = []
        if not forn_pre_id:             erros.append("Fornecedor")
        if not marca_sel:               erros.append("Marca")
        if not cat_sel:                 erros.append("Categoria")
        if not codigo.strip():          erros.append("Codigo")
        if not descricao.strip():       erros.append("Descricao")
        if not descricao_curta.strip(): erros.append("Descricao curta")
        if erros:
            st.session_state["np_erro_msg"] = f"Campos obrigatorios: {', '.join(erros)}"
            st.rerun()
            return

        # Verifica duplicata — mesmo codigo E mesmo fornecedor
        cod_limpo = codigo.strip()
        existe_cod = query("""SELECT produto_id, descricao FROM produto
                              WHERE LOWER(codigo_produto)=LOWER(?) AND fornecedor_id=?
                              AND ativo=1""",
                           (cod_limpo, forn_pre_id))
        if existe_cod:
            st.session_state["np_erro_msg"] = (
                f"Produto com código **{cod_limpo}** já existe para este fornecedor: "
                f"*{existe_cod[0][1]}* (ID {existe_cod[0][0]}). "
                f"Edite o produto existente na aba Lista."
            )
            st.rerun()
            return

        # Verifica duplicata — mesma descricao E mesmo fornecedor
        existe_desc = query("""SELECT produto_id, codigo_produto FROM produto
                               WHERE LOWER(descricao)=LOWER(?) AND fornecedor_id=?
                               AND ativo=1""",
                            (descricao.strip(), forn_pre_id))
        if existe_desc:
            st.session_state["np_erro_msg"] = (
                f"Produto com esta descrição já existe: "
                f"código **{existe_desc[0][1]}** (ID {existe_desc[0][0]}). "
                f"Edite o produto existente na aba Lista."
            )
            st.rerun()
            return

        linha_id = linha_sel[0] if linha_sel and linha_sel[0] else None
        conn = conectar()
        conn.execute("""
            INSERT INTO produto
            (fornecedor_id, marca_id, categoria_id, linha_id, codigo_produto,
             descricao, descricao_curta, unidade_medida, unidades_caixa,
             peso, peso_caixa, ean, dun, validade_dias,
             ncm, cest, sub_categoria, grupo, observacao, ativo)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,1)
        """, (forn_pre_id, marca_sel[0], cat_sel[0], linha_id, cod_limpo,
              descricao.strip(), descricao_curta.strip(), unidade, un_caixa,
              peso or None, peso_caixa or None,
              ean.strip() or None, dun.strip() or None,
              validade or None,
              ncm.strip() or None, cest.strip() or None,
              sub_cat or None, grupo or None, obs_prod or None))
        conn.commit(); conn.close()

        # Limpa campos e volta para aba lista
        for k in ["np_codigo","np_desc","np_desc_c","np_subcat","np_grupo",
                  "np_ean","np_dun","np_ncm","np_cest","np_obs",
                  "np_marca","np_cat","np_linha","np_unidade",
                  "np_peso","np_peso_cx","np_uncx","np_validade",
                  "prod_aba"]:
            st.session_state.pop(k, None)
        st.session_state["prod_sucesso_msg"] = f"✅ Produto '{descricao_curta.strip()}' cadastrado!"
        st.session_state["prod_aba"] = "lista"  # volta para a aba lista
        st.rerun()


def _importar_produtos_excel():
    st.subheader("Importar produtos via Excel")

    # Exibe resultado de importacao anterior
    resultado_prod = st.session_state.pop("imp_prod_resultado", None)
    if resultado_prod:
        st.success(
            f"✅ **{resultado_prod['importados']} produto(s) importado(s)** e "
            f"**{resultado_prod['atualizados']} atualizado(s)** com sucesso!"
        )
        if resultado_prod["erros"]:
            st.warning(f"⚠️ {len(resultado_prod['erros'])} linha(s) com erro:")
            for err in resultado_prod["erros"][:20]:
                st.caption(err)
        st.caption("Selecione outro arquivo para nova importacao ou va para a aba Lista.")
        if st.button("Importar outro arquivo", key="btn_nova_imp_prod"):
            st.rerun()
        return

    # Template para download
    df_tpl = pd.DataFrame([{
        "fornecedor_nome":  "Specialli",
        "marca_nome":       "Specialli",
        "categoria_nome":   "Charcutaria",
        "linha_nome":       "Presunto",
        "sub_categoria":    "Extra",
        "grupo":            "Suino",
        "codigo_produto":   "SPE001",
        "descricao":        "Presunto Cozido Extra Specialli 3kg",
        "descricao_curta":  "Presunto Extra 3kg",
        "unidade_medida":   "kg",
        "peso_unidade":     3.0,
        "peso_caixa":       6.0,
        "unidades_caixa":   2,
        "validade_dias":    30,
        "ean":              "",
        "dun":              "",
        "ncm":              "",
        "cest":             "",
        "observacao":       "",
        "ativo":            1,
    }])
    buf_tpl = io.BytesIO()
    with pd.ExcelWriter(buf_tpl, engine="openpyxl") as _w:
        df_tpl.to_excel(_w, index=False, sheet_name="Produtos")
    st.download_button("⬇️ Baixar template de Produtos", data=buf_tpl.getvalue(),
                       file_name="template_produtos.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    st.caption(
        "Colunas obrigatorias: fornecedor_nome, marca_nome, categoria_nome, "
        "codigo_produto, descricao, descricao_curta.  "
        "sub_categoria = Calibre  |  grupo = Materia-prima  |  "
        "ean = código de barras unidade  |  dun = código de barras caixa  |  "
        "ncm = 8 dígitos  |  cest = 7 dígitos"
    )
    st.divider()

    arquivo = st.file_uploader("Selecione o arquivo Excel de produtos",
                               type=["xlsx","xls"], key="up_prod_imp")
    if not arquivo:
        return
    try:
        df = pd.read_excel(arquivo, dtype=str)
        df.columns = df.columns.str.strip().str.lower().str.replace(" ","_").str.replace("*","")
        # Normaliza separador decimal em colunas numericas (virgula → ponto)
        cols_num = ["peso_unidade","peso_caixa","unidades_caixa","validade_dias"]
        for _cn in cols_num:
            if _cn in df.columns:
                df[_cn] = df[_cn].astype(str).str.replace(",",".").str.strip()
                df[_cn] = df[_cn].replace({"nan":"","None":"","":" "})
        # Codigo_produto e opcional — filtra apenas linhas sem descricao
        df = df.dropna(subset=["descricao"])
        df = df.where(pd.notnull(df), None)
        # Preenche codigo vazio com slug da descricao para uso como chave unica
        def _slug(v):
            import re, unicodedata
            s = str(v).lower().strip()
            s = unicodedata.normalize('NFKD', s).encode('ascii','ignore').decode()
            s = re.sub(r"[^a-z0-9]", "_", s)
            s = re.sub(r"_+", "_", s).strip("_")
            return s[:60]
        mask_sem_cod = df["codigo_produto"].isna() | (df["codigo_produto"].astype(str).str.strip() == "")
        df.loc[mask_sem_cod, "codigo_produto"] = df.loc[mask_sem_cod, "descricao"].apply(_slug)
        st.caption(f"Preview — {len(df)} produto(s):")
        st.dataframe(df.head(10), use_container_width=True)
    except Exception as e:
        _erro(f"Erro ao ler o arquivo: {e}"); return

    def _pf(v, default=None):
        """Parse float seguro."""
        try:
            if v is None or str(v).strip() in ("","nan","None"): return default
            return float(str(v).replace(",","."))
        except: return default

    def _pi(v, default=None):
        """Parse int seguro."""
        try:
            if v is None or str(v).strip() in ("","nan","None"): return default
            return int(float(str(v)))
        except: return default

    if st.button("Confirmar importacao de produtos", type="primary", key="btn_imp_prod"):
        conn = conectar()
        importados = 0; atualizados = 0; erros_imp = []
        for idx, row in df.iterrows():
            try:
                forn_nome = str(row.get("fornecedor_nome","")).strip()
                marca_nm  = str(row.get("marca_nome","")).strip()
                cat_nm    = str(row.get("categoria_nome","")).strip()
                linha_nm  = str(row.get("linha_nome") or "").strip()
                sub_cat   = str(row.get("sub_categoria") or "").strip() or None
                grupo     = str(row.get("grupo") or "").strip() or None
                codigo    = str(row.get("codigo_produto","")).strip()
                desc      = str(row.get("descricao","")).strip()
                desc_c    = str(row.get("descricao_curta") or desc[:56]).strip()
                unidade   = str(row.get("unidade_medida") or "UN").strip()
                un_cx     = _pi(row.get("unidades_caixa"), 1)
                peso_un   = _pf(row.get("peso_unidade"))
                peso_cx   = _pf(row.get("peso_caixa"))
                ean       = str(row.get("ean")  or "").strip() or None
                dun_i     = str(row.get("dun")  or "").strip() or None
                val_dias  = _pi(row.get("validade_dias"))
                ncm_i     = str(row.get("ncm")  or "").strip() or None
                cest_i    = str(row.get("cest") or "").strip() or None
                obs_p     = str(row.get("observacao") or "").strip() or None

                if not forn_nome or not codigo or not desc:
                    erros_imp.append(f"Linha {idx+2}: campos obrigatorios ausentes."); continue

                forn = conn.execute("SELECT fornecedor_id FROM fornecedor WHERE LOWER(nome_fantasia)=LOWER(?)", (forn_nome,)).fetchone()
                if not forn:
                    conn.execute("INSERT INTO fornecedor (nome_fantasia, ativo) VALUES (?,1)", (forn_nome,))
                    forn_id = conn.execute("SELECT fornecedor_id FROM fornecedor WHERE LOWER(nome_fantasia)=LOWER(?)", (forn_nome,)).fetchone()[0]
                else: forn_id = forn[0]

                marca = conn.execute("SELECT marca_id FROM marca WHERE LOWER(nome_marca)=LOWER(?) AND fornecedor_id=?", (marca_nm, forn_id)).fetchone()
                if not marca:
                    conn.execute("INSERT INTO marca (fornecedor_id, nome_marca, ativo) VALUES (?,?,1)", (forn_id, marca_nm))
                    marca_id = conn.execute("SELECT marca_id FROM marca WHERE LOWER(nome_marca)=LOWER(?) AND fornecedor_id=?", (marca_nm, forn_id)).fetchone()[0]
                else: marca_id = marca[0]

                cat = conn.execute("SELECT categoria_id FROM categoria WHERE LOWER(nome_categoria)=LOWER(?)", (cat_nm,)).fetchone()
                if not cat:
                    conn.execute("INSERT INTO categoria (nome_categoria, ativo) VALUES (?,1)", (cat_nm,))
                    cat_id = conn.execute("SELECT categoria_id FROM categoria WHERE LOWER(nome_categoria)=LOWER(?)", (cat_nm,)).fetchone()[0]
                else: cat_id = cat[0]

                linha_id = None
                if linha_nm and linha_nm.lower() not in ("nan","none",""):
                    # Busca pelo nome em qualquer categoria para evitar duplicatas
                    linha = conn.execute(
                        "SELECT linha_id FROM linha WHERE LOWER(nome_linha)=LOWER(?) AND ativo=1 ORDER BY linha_id LIMIT 1",
                        (linha_nm,)).fetchone()
                    if not linha:
                        conn.execute("INSERT INTO linha (categoria_id, nome_linha, ativo) VALUES (?,?,1)",
                                     (cat_id, linha_nm))
                        linha_id = conn.execute(
                            "SELECT linha_id FROM linha WHERE LOWER(nome_linha)=LOWER(?) AND ativo=1 ORDER BY linha_id LIMIT 1",
                            (linha_nm,)).fetchone()[0]
                    else:
                        linha_id = linha[0]

                existe = conn.execute("SELECT produto_id FROM produto WHERE codigo_produto=? AND fornecedor_id=?", (codigo, forn_id)).fetchone()
                if existe:
                    conn.execute("""UPDATE produto SET marca_id=?, categoria_id=?, linha_id=?,
                        descricao=?, descricao_curta=?, unidade_medida=?, unidades_caixa=?,
                        peso=COALESCE(?,peso), peso_caixa=COALESCE(?,peso_caixa),
                        ean=COALESCE(?,ean), dun=COALESCE(?,dun),
                        validade_dias=COALESCE(?,validade_dias),
                        ncm=COALESCE(?,ncm), cest=COALESCE(?,cest),
                        sub_categoria=COALESCE(?,sub_categoria), grupo=COALESCE(?,grupo),
                        observacao=COALESCE(?,observacao), ativo=1
                        WHERE produto_id=?""",
                        (marca_id, cat_id, linha_id, desc, desc_c, unidade, un_cx,
                         peso_un, peso_cx, ean, dun_i, val_dias,
                         ncm_i, cest_i, sub_cat, grupo, obs_p, existe[0]))
                    atualizados += 1
                else:
                    conn.execute("""INSERT INTO produto
                        (fornecedor_id, marca_id, categoria_id, linha_id, codigo_produto,
                         descricao, descricao_curta, unidade_medida, unidades_caixa,
                         peso, peso_caixa, ean, dun, validade_dias,
                         ncm, cest, sub_categoria, grupo, observacao, ativo)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,1)""",
                        (forn_id, marca_id, cat_id, linha_id, codigo,
                         desc, desc_c, unidade, un_cx,
                         peso_un, peso_cx, ean, dun_i, val_dias,
                         ncm_i, cest_i, sub_cat, grupo, obs_p))
                    importados += 1
            except Exception as e:
                erros_imp.append(f"Linha {idx+2}: {e}")

        conn.commit(); conn.close()
        st.session_state["imp_prod_resultado"] = {
            "importados":  importados,
            "atualizados": atualizados,
            "erros":       erros_imp,
        }
        st.rerun()


# ═══════════════════════════════════════════════════════
# 3. TABELAS DE PREÇO
# ═══════════════════════════════════════════════════════

def tela_tabelas_preco():
    st.header("Tabelas de Preço")
    if st.button("⬅ Voltar"):
        _ir("home")
    ABAS_TAB = {"lista":"Lista","nova":"Nova Tabela",
                "import":"Importar Excel","historico":"📈 Histórico de Preços",
                "catalogo":"📄 Catálogo PDF"}
    if "tab_preco_aba" not in st.session_state:
        st.session_state["tab_preco_aba"] = "lista"
    cols = st.columns(5)
    for col,(k,v) in zip(cols, ABAS_TAB.items()):
        ativa = st.session_state["tab_preco_aba"] == k
        if col.button(v, key=f"tpnav_{k}", use_container_width=True,
                      type="primary" if ativa else "secondary"):
            st.session_state["tab_preco_aba"] = k; st.rerun()
    st.divider()
    a = st.session_state["tab_preco_aba"]
    if a=="lista":      _lista_tabelas()
    elif a=="nova":     _form_nova_tabela()
    elif a=="import":   _importar_tabela_excel()
    elif a=="historico":_historico_precos()
    elif a=="catalogo":
        from catalogo import _tela_catalogo
        _tela_catalogo()


def _lista_tabelas():
    dados = query("""
        SELECT tp.tabela_preco_id, f.fornecedor_id, f.nome_fantasia, tp.nome_tabela,
               tp.tipo_tabela, tp.prazo_pagamento, tp.frete,
               tp.data_inicio, tp.data_fim, tp.ativo,
               COUNT(tpi.tabela_preco_item_id) AS qtd_itens
        FROM tabela_preco tp
        LEFT JOIN fornecedor f ON tp.fornecedor_id = f.fornecedor_id
        LEFT JOIN tabela_preco_item tpi ON tp.tabela_preco_id = tpi.tabela_preco_id
        GROUP BY tp.tabela_preco_id, f.fornecedor_id, f.nome_fantasia, tp.nome_tabela, tp.tipo_tabela, tp.prazo_pagamento, tp.frete, tp.data_inicio, tp.data_fim, tp.ativo
        ORDER BY f.nome_fantasia, tp.data_inicio DESC
    """)
    if not dados:
        st.info("Nenhuma tabela de preço cadastrada.")
        return

    df = pd.DataFrame(dados, columns=["ID","Forn.ID","Fornecedor","Tabela","Tipo","Prazo",
                                       "Frete","Inicio","Fim","Ativo","Itens"])
    df["Fim"] = df["Fim"].fillna("— sem prazo")

    # ── FILTROS ──────────────────────────────────────────────────────────
    col_f1, col_f2, col_f3 = st.columns([2, 2, 1.5])
    with col_f1:
        forns_t = ["Todos"] + sorted(df["Fornecedor"].dropna().unique().tolist())
        sel_t   = st.selectbox("Fornecedor", forns_t, key="lt_forn_filtro")
    with col_f2:
        df_forn = df if sel_t == "Todos" else df[df["Fornecedor"] == sel_t]
        tipos_t = ["Todos"] + sorted(df_forn["Tipo"].dropna().unique().tolist())
        sel_tipo = st.selectbox("Tipo de tabela", tipos_t, key="lt_tipo_filtro")
    with col_f3:
        sel_status = st.selectbox("Status", ["Ativas", "Inativas", "Todas"],
                                  key="lt_status_filtro",
                                  help="Padrão: só tabelas ativas")

    # Aplica filtros
    df_vis = df_forn if sel_tipo == "Todos" else df_forn[df_forn["Tipo"] == sel_tipo]
    if sel_status == "Ativas":
        df_vis = df_vis[df_vis["Ativo"] == 1]
    elif sel_status == "Inativas":
        df_vis = df_vis[df_vis["Ativo"] == 0]
    # "Todas" — sem filtro adicional

    df_vis = df_vis.copy()
    df_vis["Ativo"] = df_vis["Ativo"].map({1: "✅ Ativa", 0: "❌ Inativa"})

    col_exp_tx, col_exp_tp = st.columns(2)
    with col_exp_tx:
        if st.button("⬇️ Excel", key="exp_tab_xlsx", use_container_width=True):
            st.session_state["exp_tab_trigger"] = "excel"
    with col_exp_tp:
        if st.button("⬇️ PDF", key="exp_tab_pdf", use_container_width=True):
            st.session_state["exp_tab_trigger"] = "pdf"



    trigger_t = st.session_state.pop("exp_tab_trigger", None)
    if trigger_t:
        # Busca itens das tabelas filtradas com dados completos do produto
        tab_ids = tuple(df_vis["ID"].tolist())
        if tab_ids:
            ph = ",".join("?" * len(tab_ids))
            itens = query(f"""
                SELECT tp.nome_tabela, f.nome_fantasia,
                       p.codigo_produto, p.descricao_curta,
                       COALESCE(p.sub_categoria,'—'), COALESCE(p.grupo,'—'),
                       p.unidade_medida, p.unidades_caixa,
                       COALESCE(p.peso,0),
                       tpi.preco_caixa,
                       ROUND(tpi.preco_caixa / NULLIF(p.unidades_caixa,0), 4) AS preco_un,
                       COALESCE(tpi.preco_kg,0),
                       COALESCE(tpi.desconto_maximo,0),
                       COALESCE(tpi.observacao,'—')
                FROM tabela_preco_item tpi
                JOIN tabela_preco tp  ON tpi.tabela_preco_id=tp.tabela_preco_id
                JOIN produto p        ON tpi.produto_id=p.produto_id
                JOIN fornecedor f     ON tp.fornecedor_id=f.fornecedor_id
                WHERE tpi.tabela_preco_id IN ({ph})
                ORDER BY tp.nome_tabela, p.descricao_curta
            """, tuple(tab_ids))

            df_itens = pd.DataFrame(itens or [], columns=[
                "Tabela","Fornecedor","Codigo","Produto",
                "Sub-cat.","Grupo","UM","Un/Cx","Peso un.(kg)",
                "Preco cx.(R$)","Preco un.(R$)","Preco/kg(R$)",
                "Desc.max(%)","Observacao"])

            if trigger_t == "excel":
                buf_t = io.BytesIO()
                with pd.ExcelWriter(buf_t, engine="openpyxl") as w:
                    df_vis[["Fornecedor","Tabela","Tipo","Prazo","Frete","Inicio","Fim","Ativo","Itens"]].to_excel(
                        w, index=False, sheet_name="Tabelas")
                    df_itens.to_excel(w, index=False, sheet_name="Itens")
                buf_t.seek(0)
                nome_t = f"tabela_precos_{sel_t.replace(' ','_') if sel_t!='Todos' else 'todas'}.xlsx"
                st.download_button("📥 Baixar Excel da tabela", data=buf_t,
                                   file_name=nome_t,
                                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                   use_container_width=True)
            elif trigger_t == "pdf":
                buf_tp = _exportar_tabela_pdf(df_itens, sel_t)
                nome_tp = f"tabela_precos_{sel_t.replace(' ','_') if sel_t!='Todos' else 'todas'}.pdf"
                st.download_button("📥 Baixar PDF da tabela", data=buf_tp,
                                   file_name=nome_tp, mime="application/pdf",
                                   use_container_width=True)

    # ── Auto-inativação de tabelas com data_fim expirada ─────────────────
    from datetime import date as _date
    _hoje = _date.today().isoformat()
    _expiradas = query("""
        SELECT tabela_preco_id FROM tabela_preco
        WHERE ativo=1 AND data_fim IS NOT NULL AND data_fim < ?
    """, (_hoje,))
    if _expiradas:
        conn = conectar()
        for _exp in _expiradas:
            conn.execute("UPDATE tabela_preco SET ativo=0 WHERE tabela_preco_id=?",
                         (_exp[0],))
        conn.commit(); conn.close()
        # Recarrega dados após auto-inativação
        dados = query("""
            SELECT tp.tabela_preco_id, f.fornecedor_id, f.nome_fantasia, tp.nome_tabela,
                   tp.tipo_tabela, tp.prazo_pagamento, tp.frete,
                   tp.data_inicio, tp.data_fim, tp.ativo,
                   COUNT(tpi.tabela_preco_item_id) AS qtd_itens
            FROM tabela_preco tp
            LEFT JOIN fornecedor f ON tp.fornecedor_id = f.fornecedor_id
            LEFT JOIN tabela_preco_item tpi ON tp.tabela_preco_id = tpi.tabela_preco_id
            GROUP BY tp.tabela_preco_id, f.fornecedor_id, f.nome_fantasia, tp.nome_tabela,
                     tp.tipo_tabela, tp.prazo_pagamento, tp.frete, tp.data_inicio, tp.data_fim, tp.ativo
            ORDER BY f.nome_fantasia, tp.data_inicio DESC
        """)
        df = pd.DataFrame(dados, columns=["ID","Forn.ID","Fornecedor","Tabela","Tipo","Prazo",
                                           "Frete","Inicio","Fim","Ativo","Itens"])
        df["Fim"] = df["Fim"].fillna("— sem prazo")
        df_forn = df if sel_t == "Todos" else df[df["Fornecedor"] == sel_t]
        df_vis = df_forn if sel_tipo == "Todos" else df_forn[df_forn["Tipo"] == sel_tipo]
        if sel_status == "Ativas":
            df_vis = df_vis[df_vis["Ativo"] == 1]
        elif sel_status == "Inativas":
            df_vis = df_vis[df_vis["Ativo"] == 0]
        df_vis = df_vis.copy()

    df_vis["Ativo"] = df_vis["Ativo"].map({1: "✅ Ativa", 0: "❌ Inativa"})

    st.dataframe(df_vis[["ID","Fornecedor","Tabela","Tipo","Prazo","Frete","Inicio","Fim","Ativo","Itens"]],
                 use_container_width=True, hide_index=True)

    st.divider()

    # ── Seleção da tabela para editar — apenas ativas ─────────────────────
    dados_ativas = [r for r in dados if r[9] == 1]  # ativo=1
    if not dados_ativas:
        st.info("Nenhuma tabela ativa para editar. Use o filtro 'Inativas' para reativar tabelas.")
        return

    ids     = [(r[0], f"{r[2]} · {r[3]}") for r in dados_ativas]
    ids_map = {r[0]: i for i, r in enumerate(ids)}

    tab_id_fixo = st.session_state.get("tab_editando_id")
    idx_sel = ids_map.get(tab_id_fixo, 0) if tab_id_fixo and tab_id_fixo in ids_map else 0

    sel = st.selectbox("Selecione a tabela para editar", ids,
                       index=idx_sel,
                       format_func=lambda x: x[1],
                       key="tab_sel_edit")
    if not sel:
        return

    tab_id = sel[0]
    st.session_state["tab_editando_id"] = tab_id

    tab_row = next(r for r in dados_ativas if r[0] == tab_id)
    (_, forn_id_at, forn_nome_at, nome_at, tipo_at, prazo_at,
     frete_at, ini_at, fim_at, ativo_at, _) = tab_row

    # ── 1. Editar cabeçalho da tabela ─────────────────
    # Chave de feedback: "cab_salvo_{tab_id}" indica que acabou de ser salvo
    cab_salvo = st.session_state.pop(f"cab_salvo_{tab_id}", False)

    # Botão/label que abre o expander — verde se acabou de salvar, normal caso contrário
    if cab_salvo:
        lbl_expander = "✅ Cabeçalho salvo"
        expandido    = False   # fecha após salvar
    else:
        lbl_expander = "✏️ Editar cabeçalho da tabela"
        expandido    = False

    # Exibe o banner de sucesso FORA do expander para ficar sempre visível
    if cab_salvo:
        st.success(f"✅ Cabeçalho de **{nome_at}** salvo com sucesso!")

    with st.expander(lbl_expander, expanded=expandido):
        import datetime
        def _parse_date(s):
            if not s: return None
            return datetime.date.fromisoformat(str(s).strip()[:10])

        forns_e     = cache_fornecedores()
        forn_ids_e  = [f[0] for f in forns_e]
        idx_forn_e  = forn_ids_e.index(forn_id_at) if forn_id_at in forn_ids_e else 0
        tipos_e     = ["rede","varejo","atacado"]
        idx_tipo_e  = tipos_e.index(tipo_at) if tipo_at in tipos_e else 0
        fretes_e    = ["FOB","CIF","—"]
        idx_frete_e = fretes_e.index(frete_at) if frete_at in fretes_e else 2

        with st.form(f"edit_cab_tab_{tab_id}"):
            col1, col2 = st.columns(2)
            with col1:
                forn_e2 = st.selectbox("Fornecedor", forns_e, index=idx_forn_e,
                                       format_func=lambda x: x[1])
                nome_e2 = st.text_input("Nome da tabela", value=nome_at or "")
                tipo_e2 = st.selectbox("Tipo", tipos_e, index=idx_tipo_e)
            with col2:
                prazo_e2 = st.text_input("Prazo de pagamento", value=prazo_at or "")
                frete_e2 = st.selectbox("Frete", fretes_e, index=idx_frete_e)
                ini_e2   = st.date_input("Vigência — início",
                                         value=_parse_date(ini_at) or datetime.date.today())
                fim_e2   = st.date_input("Vigência — fim (opcional)",
                                         value=_parse_date(fim_at))
                ativo_e2 = st.checkbox("Ativa", value=bool(ativo_at))
            salvar_cab = st.form_submit_button("💾 Salvar cabeçalho", type="primary")

        if salvar_cab:
            if not nome_e2.strip() or not prazo_e2.strip():
                _erro("Nome e prazo são obrigatórios.")
            else:
                conn = conectar()
                conn.execute("""UPDATE tabela_preco SET
                    fornecedor_id=?, nome_tabela=?, tipo_tabela=?, prazo_pagamento=?,
                    frete=?, data_inicio=?, data_fim=?, ativo=?
                    WHERE tabela_preco_id=?""",
                    (forn_e2[0], nome_e2.strip(), tipo_e2, prazo_e2.strip(),
                     frete_e2 if frete_e2 != "—" else None,
                     str(ini_e2), str(fim_e2) if fim_e2 else None,
                     1 if ativo_e2 else 0, tab_id))
                conn.commit(); conn.close()
                st.session_state["tab_editando_id"] = tab_id
                st.session_state[f"cab_salvo_{tab_id}"] = True
                st.rerun()

    # ── 2. Itens da tabela com filtros e busca ───────────────────────────
    st.subheader("Produtos desta tabela")

    # Busca todos os itens com dados completos para filtrar
    itens_todos = query("""
        SELECT tpi.tabela_preco_item_id, p.produto_id,
               p.codigo_produto, p.descricao_curta,
               tpi.preco_caixa, tpi.desconto_maximo,
               COALESCE(cat.nome_categoria,'—') AS categoria,
               COALESCE(l.nome_linha,'—') AS linha,
               COALESCE(p.ean,'') AS ean
        FROM tabela_preco_item tpi
        JOIN produto p ON tpi.produto_id = p.produto_id
        LEFT JOIN categoria cat ON p.categoria_id = cat.categoria_id
        LEFT JOIN linha l       ON p.linha_id     = l.linha_id
        WHERE tpi.tabela_preco_id = ?
        ORDER BY p.descricao_curta
    """, (tab_id,))

    if not itens_todos:
        st.info("Nenhum produto nesta tabela ainda.")
    else:
        # Filtros dentro da tabela
        col_b1, col_b2, col_b3 = st.columns([3, 2, 2])
        with col_b1:
            busca_item = st.text_input("🔍 Buscar produto",
                                       placeholder="Nome, código ou EAN...",
                                       key=f"lt_busca_item_{tab_id}")
        with col_b2:
            cats_tab = ["Todas"] + sorted(set(r[6] for r in itens_todos if r[6] != "—"))
            fil_cat  = st.selectbox("Categoria", cats_tab, key=f"lt_fil_cat_{tab_id}")

        # Linhas disponíveis apenas para a categoria selecionada
        itens_pos_cat = itens_todos if fil_cat == "Todas" else                         [r for r in itens_todos if r[6] == fil_cat]
        with col_b3:
            linhas_tab = ["Todas"] + sorted(set(r[7] for r in itens_pos_cat if r[7] != "—"))
            # Reset da linha se não pertence à categoria atual
            if st.session_state.get(f"lt_fil_lin_{tab_id}") not in linhas_tab:
                st.session_state[f"lt_fil_lin_{tab_id}"] = "Todas"
            fil_lin = st.selectbox("Linha", linhas_tab, key=f"lt_fil_lin_{tab_id}")

        # Aplica filtros em cascata: categoria → linha → busca texto
        itens = itens_pos_cat
        if fil_lin != "Todas":
            itens = [r for r in itens if r[7] == fil_lin]
        if busca_item.strip():
            b = busca_item.strip().lower()
            itens = [r for r in itens if
                     b in (r[3] or "").lower() or
                     b in (r[2] or "").lower() or
                     b in (r[8] or "").lower()]

        total_tab = len(itens_todos)
        filtrados = len(itens)
        contexto  = ""
        if busca_item.strip() or fil_cat != "Todas" or fil_lin != "Todas":
            contexto = f" (filtrado: {filtrados} de {total_tab})"
        st.caption(f"{total_tab} produto(s){contexto} — ✏️ editar preço  |  🗑️ remover")

        # Cabeçalho
        hc = st.columns([1.0, 1.5, 3.0, 1.8, 1.8, 1.0])
        for col, txt in zip(hc, ["Código","Categoria","Descrição","Preço/Cx (R$)","Desc. Máx (%)","Ações"]):
            col.markdown(f"<small><b>{txt}</b></small>", unsafe_allow_html=True)

        for item in itens:
            iid, pid, cod, desc, preco_cx, desc_max, cat_i, lin_i, ean_i = item
            c1, c2, c3, c4, c5, c6 = st.columns([1.0, 1.5, 3.0, 1.8, 1.8, 1.0])
            c1.caption(cod or "—")
            c2.caption(cat_i if cat_i != "—" else lin_i if lin_i != "—" else "—")
            c3.write(desc or "—")
            c4.caption(f"R$ {preco_cx:,.2f}".replace(",","X").replace(".",",").replace("X",".") if preco_cx else "—")
            c5.caption(f"{desc_max:.1f}%" if desc_max else "—")
            with c6:
                b1, b2 = st.columns(2)
                with b1:
                    if st.button("✏️", key=f"ed_tpi_{iid}", help="Editar",
                                 use_container_width=True):
                        st.session_state["tpi_editar_id"] = iid
                        st.session_state.pop("tpi_excluir_id", None)
                        st.rerun()
                with b2:
                    if st.button("🗑️", key=f"ex_tpi_{iid}", help="Remover da tabela",
                                 use_container_width=True):
                        st.session_state["tpi_excluir_id"] = iid
                        st.session_state.pop("tpi_editar_id", None)
                        st.rerun()

            # Form edição inline
            if st.session_state.get("tpi_editar_id") == iid:
                with st.form(f"edit_tpi_{iid}"):
                    col_a, col_b, col_c = st.columns([2, 2, 1])
                    with col_a:
                        novo_preco = st.number_input("Preço/Cx (R$)", min_value=0.0,
                                                     value=float(preco_cx or 0),
                                                     step=0.01, format="%.2f")
                    with col_b:
                        novo_desc = st.number_input("Desc. Máx (%)", min_value=0.0,
                                                    max_value=100.0,
                                                    value=float(desc_max or 0),
                                                    step=0.1, format="%.1f")
                    with col_c:
                        st.write("")
                        salvar_item = st.form_submit_button("💾 Salvar", type="primary")
                        cancelar_item = st.form_submit_button("Cancelar")
                if salvar_item:
                    if novo_preco <= 0:
                        _erro("Preço deve ser maior que zero.")
                    else:
                        conn = conectar()
                        conn.execute("""UPDATE tabela_preco_item
                            SET preco_caixa=?, desconto_maximo=?
                            WHERE tabela_preco_item_id=?""",
                            (novo_preco, novo_desc, iid))
                        conn.commit(); conn.close()
                        st.session_state.pop("tpi_editar_id", None)
                        st.session_state["tab_editando_id"] = tab_id
                        _sucesso(f"Preço de '{desc}' atualizado!")
                        st.rerun()
                if cancelar_item:
                    st.session_state.pop("tpi_editar_id", None)
                    st.rerun()

            # Confirmação exclusão inline
            if st.session_state.get("tpi_excluir_id") == iid:
                st.warning(f"Remover **{desc}** desta tabela?")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🗑️ Confirmar remoção", key=f"conf_ex_tpi_{iid}",
                                 type="primary", use_container_width=True):
                        conn = conectar()
                        conn.execute("DELETE FROM tabela_preco_item WHERE tabela_preco_item_id=?", (iid,))
                        conn.commit(); conn.close()
                        st.session_state.pop("tpi_excluir_id", None)
                        st.session_state["tab_editando_id"] = tab_id
                        _sucesso(f"'{desc}' removido da tabela.")
                        st.rerun()
                with col2:
                    if st.button("Cancelar", key=f"canc_ex_tpi_{iid}",
                                 use_container_width=True):
                        st.session_state.pop("tpi_excluir_id", None)
                        st.rerun()

    # ── 3. Adicionar produto à tabela ──────────────────
    st.divider()
    with st.expander("➕ Adicionar produto à tabela"):
        ids_ja = {r[1] for r in itens} if itens else set()
        prods_disp = query("""SELECT produto_id, codigo_produto, descricao_curta
            FROM produto WHERE fornecedor_id=? AND ativo=1
            ORDER BY descricao_curta""", (forn_id_at,))
        prods_disp = [p for p in prods_disp if p[0] not in ids_ja]

        if not prods_disp:
            st.caption("Todos os produtos deste fornecedor já estão na tabela.")
        else:
            with st.form(f"add_item_tab_{tab_id}", clear_on_submit=True):
                prod_add = st.selectbox("Produto", prods_disp,
                                        format_func=lambda x: f"{x[1]} — {x[2]}")
                col1, col2 = st.columns(2)
                with col1:
                    preco_add = st.number_input("Preço/Cx (R$)", min_value=0.0,
                                                step=0.01, format="%.2f")
                with col2:
                    desc_add  = st.number_input("Desc. Máx (%)", min_value=0.0,
                                                max_value=100.0, step=0.1, format="%.1f")
                if st.form_submit_button("Adicionar", type="primary"):
                    if preco_add <= 0:
                        _erro("Informe o preço.")
                    else:
                        conn = conectar()
                        conn.execute("""INSERT OR REPLACE INTO tabela_preco_item
                            (tabela_preco_id, produto_id, preco_caixa, desconto_maximo)
                            VALUES (?,?,?,?)""",
                            (tab_id, prod_add[0], preco_add, desc_add))
                        conn.commit(); conn.close()
                        st.session_state["tab_editando_id"] = tab_id
                        _sucesso(f"'{prod_add[2]}' adicionado à tabela!")
                        st.rerun()


def _form_nova_tabela():
    st.subheader("Nova tabela de preço")
    forns = query("SELECT fornecedor_id, nome_fantasia FROM fornecedor WHERE ativo=1")
    if not forns:
        st.warning("Cadastre um fornecedor primeiro.")
        return
    with st.form("nova_tabela"):
        col1, col2 = st.columns(2)
        with col1:
            forn_sel    = st.selectbox("Fornecedor", forns, format_func=lambda x: x[1])
            nome_tabela = st.text_input("Nome da tabela", placeholder="Ex: Rede 28d")
            tipo        = st.selectbox("Tipo", ["rede","varejo","atacado"])
        with col2:
            prazo    = st.text_input("Prazo de pagamento", placeholder="Ex: 28 dias")
            frete    = st.selectbox("Frete", ["FOB","CIF","—"])
            data_ini = st.date_input("Vigência — início")
            data_fim = st.date_input("Vigência — fim (opcional)", value=None)
        salvar = st.form_submit_button("Criar tabela")
    if salvar:
        if not nome_tabela.strip() or not prazo.strip():
            _erro("Nome e prazo são obrigatórios."); return
        conn = conectar()
        conn.execute("""
            INSERT INTO tabela_preco
            (fornecedor_id, nome_tabela, tipo_tabela, prazo_pagamento, frete, data_inicio, data_fim, ativo)
            VALUES (?,?,?,?,?,?,?,1)
        """, (forn_sel[0], nome_tabela, tipo, prazo,
              frete if frete != "—" else None,
              str(data_ini), str(data_fim) if data_fim else None))
        conn.commit(); conn.close()
        _sucesso(f"Tabela '{nome_tabela}' criada!")



def _brl_fmt(v):
    try: return f"R$ {float(v):,.2f}".replace(",","X").replace(".",",").replace("X",".")
    except: return "—"


def _historico_precos():
    """Histórico de evolução de preços por produto — comparação dentro do mesmo tipo de tabela."""
    import pandas as pd

    st.subheader("📈 Histórico de preços")
    st.caption(
        "Compara a evolução de preços dentro do mesmo tipo de tabela "
        "(varejo com varejo, rede com rede). "
        "Use como argumento em negociações."
    )

    forns = cache_fornecedores()
    if not forns:
        st.info("Nenhum fornecedor cadastrado."); return

    # ── Filtros ──────────────────────────────────────────────────────────
    col1, col2, col3 = st.columns(3)
    with col1:
        forn_sel = st.selectbox("Fornecedor", forns,
                                format_func=lambda x: x[1], key="hp_forn")

    fid = forn_sel[0]

    # Tipos disponíveis para este fornecedor
    tipos_disp = query("""SELECT DISTINCT tipo_tabela
        FROM tabela_preco
        WHERE fornecedor_id=? AND tipo_tabela IS NOT NULL
        ORDER BY tipo_tabela""", (fid,))
    tipo_opts = [(t[0], t[0].capitalize()) for t in tipos_disp]
    if not tipo_opts:
        st.info("Nenhuma tabela cadastrada para este fornecedor.")
        return

    with col2:
        tipo_sel = st.selectbox("Tipo de tabela", tipo_opts,
                                format_func=lambda x: x[1], key="hp_tipo")

    ttipo = tipo_sel[0]

    # Prazos disponíveis para este fornecedor + tipo
    prazos_disp = query("""SELECT DISTINCT prazo_pagamento
        FROM tabela_preco
        WHERE fornecedor_id=? AND tipo_tabela=?
          AND prazo_pagamento IS NOT NULL
        ORDER BY prazo_pagamento""", (fid, ttipo))
    prazo_opts = [(None,"Todos os prazos")] + [(p[0], p[0]) for p in prazos_disp]

    with col3:
        prazo_sel = st.selectbox("Prazo de pagamento",
                                 prazo_opts,
                                 format_func=lambda x: x[1],
                                 key="hp_prazo",
                                 help="Compare apenas tabelas do mesmo prazo")

    col4, col5 = st.columns(2)
    with col4:
        cats = query("""SELECT DISTINCT cat.categoria_id, cat.nome_categoria
            FROM produto p JOIN categoria cat ON p.categoria_id=cat.categoria_id
            WHERE p.fornecedor_id=? ORDER BY cat.nome_categoria""", (fid,))
        cat_opts = [(None,"Todas as categorias")] + list(cats)
        cat_sel  = st.selectbox("Categoria", cat_opts,
                                format_func=lambda x: x[1], key="hp_cat")
    with col5:
        busca_p = st.text_input("Buscar produto",
                                placeholder="Nome ou código...", key="hp_busca")

    # Tabelas filtradas por tipo + prazo
    where_tab = ["fornecedor_id=?", "tipo_tabela=?", "ativo=1"]
    params_tab = [fid, ttipo]
    if prazo_sel[0]:
        where_tab.append("prazo_pagamento=?")
        params_tab.append(prazo_sel[0])

    tabelas_tipo = query(f"""
        SELECT tabela_preco_id, nome_tabela, data_inicio, prazo_pagamento
        FROM tabela_preco
        WHERE {' AND '.join(where_tab)}
        ORDER BY COALESCE(data_inicio,'') ASC
    """, tuple(params_tab))

    if not tabelas_tipo:
        st.info("Nenhuma tabela encontrada para esta combinação.")
        return

    if len(tabelas_tipo) == 1:
        st.info(
            f"Apenas 1 tabela encontrada: **{tabelas_tipo[0][1]}**. "
            "Importe uma nova tabela do mesmo tipo e prazo para ver a evolução de preços."
        )

    # Banner das tabelas sendo comparadas
    prazo_label = f" · {prazo_sel[0]}" if prazo_sel[0] else ""
    st.caption(
        f"Comparando **{len(tabelas_tipo)} tabela(s)** — "
        f"**{ttipo.capitalize()}{prazo_label}**: "
        + "  ›  ".join(
            f"{t[1]} ({(t[2] or '')[:10]})"
            for t in tabelas_tipo)
    )
    st.divider()

    # ── Busca produtos com histórico neste tipo de tabela ────────────────
    tab_ids = tuple(t[0] for t in tabelas_tipo)
    ph = ",".join("?"*len(tab_ids))

    where_p = ["p.fornecedor_id=?",
               f"h.tabela_id IN ({ph})"]
    params_p = [fid] + list(tab_ids)
    if cat_sel[0]:
        where_p.append("p.categoria_id=?"); params_p.append(cat_sel[0])
    if busca_p.strip():
        b = f"%{busca_p.strip()}%"
        where_p.append("(p.descricao LIKE ? OR p.descricao_curta LIKE ? OR p.codigo_produto LIKE ?)")
        params_p.extend([b, b, b])

    prods_com_hist = query(f"""
        SELECT p.produto_id, p.descricao_curta, p.codigo_produto,
               COALESCE(cat.nome_categoria,'—'), COALESCE(l.nome_linha,'—')
        FROM produto p
        JOIN historico_preco h ON h.produto_id = p.produto_id
        LEFT JOIN categoria cat ON p.categoria_id=cat.categoria_id
        LEFT JOIN linha l       ON p.linha_id=l.linha_id
        WHERE {' AND '.join(where_p)}
        GROUP BY p.produto_id, p.descricao_curta, p.codigo_produto, cat.nome_categoria, l.nome_linha
        ORDER BY cat.nome_categoria, p.descricao_curta
    """, tuple(params_p))

    if not prods_com_hist:
        st.info("Nenhum histórico encontrado para os filtros selecionados.")
        return

    st.caption(f"**{len(prods_com_hist)}** produto(s) com histórico neste tipo de tabela")

    # ── Exibe por produto ─────────────────────────────────────────────────
    cat_atual = None
    for pid, desc, cod, cat_nome, linha_nome in prods_com_hist:

        # Cabeçalho de categoria
        if cat_nome != cat_atual:
            cat_atual = cat_nome
            st.markdown(f"#### {cat_nome}")

        # Busca histórico apenas das tabelas deste tipo
        hist = query(f"""
            SELECT h.data_vigencia, h.preco_caixa, h.preco_kg,
                   h.nome_tabela, tp.tipo_tabela,
                   p.unidades_caixa, p.unidade_medida
            FROM historico_preco h
            JOIN produto p ON p.produto_id = h.produto_id
            JOIN tabela_preco tp ON h.tabela_id = tp.tabela_preco_id
            WHERE h.produto_id=? AND h.fornecedor_id=?
              AND h.tabela_id IN ({ph})
            ORDER BY COALESCE(h.data_vigencia,'') ASC, h.hist_id ASC
        """, (pid, fid) + tab_ids)

        if not hist: continue

        n_reg    = len(hist)
        lbl_cat  = f" · {linha_nome}" if linha_nome and linha_nome != "—" else ""
        lbl_head = f"{desc or cod}  ({cod}){lbl_cat}  —  {n_reg} entrada(s)"

        with st.expander(lbl_head, expanded=False):

            if n_reg >= 2:
                preco_ini  = hist[0][1]
                preco_fim  = hist[-1][1]
                var_pct    = (preco_fim-preco_ini)/preco_ini*100 if preco_ini else 0
                var_abs    = preco_fim - preco_ini
                cor_var    = "🔴" if var_pct > 0 else "🟢" if var_pct < 0 else "⚪"
                data_ini_h = str(hist[0][0])[:10]
                data_fim_h = str(hist[-1][0])[:10]

                c1, c2, c3, c4, c5 = st.columns(5)
                c1.metric("Preço mais antigo", _brl_fmt(preco_ini),
                          help=f"Tabela: {hist[0][3]} ({data_ini_h})")
                c2.metric("Preço mais recente", _brl_fmt(preco_fim),
                          help=f"Tabela: {hist[-1][3]} ({data_fim_h})")
                c3.metric("Variação %",
                          f"{cor_var} {abs(var_pct):.1f}%",
                          delta=f"R$ {var_abs:+.2f}".replace(".",","),
                          delta_color="inverse")
                c4.metric("Entradas comparadas", str(n_reg))
                c5.metric("Período",
                          f"{data_ini_h[:7]} → {data_fim_h[:7]}")

                # Gráfico — uma linha por tipo de tabela (aqui já é único tipo)
                df_g = pd.DataFrame(hist,
                    columns=["Data","R$ Cx","R$ Kg","Tabela","Tipo","Un/Cx","UM"])
                df_g["Data"] = pd.to_datetime(df_g["Data"], format="mixed")
                df_g = df_g.set_index("Data")[["R$ Cx"]]
                st.line_chart(df_g, height=160,
                              color="#2d6a4f")

            elif n_reg == 1:
                st.caption(f"Apenas 1 entrada — aguardando próxima tabela para comparar.")

            # Tabela detalhada
            df_det = pd.DataFrame(hist,
                columns=["Data vigência","R$ Cx","R$ Kg","Tabela","Tipo","Un/Cx","UM"])
            df_det["Data vigência"] = df_det["Data vigência"].apply(
                lambda v: str(v)[:10] if v else "—")
            df_det["R$ Cx"] = df_det["R$ Cx"].apply(_brl_fmt)
            df_det["R$ Kg"] = df_det["R$ Kg"].apply(
                lambda v: _brl_fmt(v) if v else "—")
            st.dataframe(
                df_det[["Data vigência","Tabela","R$ Cx","R$ Kg"]],
                use_container_width=True, hide_index=True)


def _importar_tabela_excel():
    st.subheader("Importar tabela de precos via Excel")

    # Template para download
    df_tpl_tab = pd.DataFrame([{
        "fornecedor_nome":  "Specialli",
        "nome_tabela":      "Tabela Distribuidor Jan/2026",
        "tipo_tabela":      "distribuidor",
        "prazo_pagamento":  "28 DDL",
        "frete":            "CIF",
        "data_inicio":      "2026-01-01",
        "data_fim":         "",
        "codigo_produto":   "SPE001",
        "preco_caixa":      89.90,
        "preco_kg":         14.98,
        "desconto_maximo":  5.0,
        "observacao":       "",
    }])
    buf_tpl_tab = io.BytesIO()
    with pd.ExcelWriter(buf_tpl_tab, engine="openpyxl") as _w:
        df_tpl_tab.to_excel(_w, index=False, sheet_name="Tabela")
    st.download_button("⬇️ Baixar template de Tabela de Preços", data=buf_tpl_tab.getvalue(),
                       file_name="template_tabela_precos.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    st.caption(
        "Colunas obrigatorias: fornecedor_nome, nome_tabela, codigo_produto, preco_caixa.  "
        "Opcionais: tipo_tabela, prazo_pagamento, frete, data_inicio, data_fim, preco_kg, desconto_maximo, observacao.  "
        "preco_kg = Valor por kg/PCT (R$)  |  desconto_maximo = % maximo de desconto"
    )
    st.divider()

    # ── Resultado da importacao anterior (exibido ANTES do uploader) ──
    resultado = st.session_state.pop("imp_tab_resultado", None)
    if resultado:
        n_ok    = resultado["importados"]
        erros   = resultado["erros"]
        tabelas = resultado["tabelas"]

        if n_ok > 0:
            st.success(
                f"✅ **{n_ok} item(ns) importado(s) com sucesso!**  "
                f"Tabela(s): {', '.join(sorted(tabelas)) or '—'}"
            )
        else:
            st.error("❌ Nenhum item foi importado.")

        if erros:
            st.warning(f"⚠️ {len(erros)} linha(s) com erro:")
            for err in erros[:20]:
                st.caption(err)
            if len(erros) > 20:
                st.caption(f"... e mais {len(erros)-20} erro(s) não exibido(s).")

        # Sempre oferece tentar novamente — com ou sem erros
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔄 Importar outro arquivo", key="btn_nova_imp_tab",
                         use_container_width=True):
                st.rerun()
        with col_b:
            if n_ok == 0:
                st.info("💡 Verifique o nome do fornecedor na coluna **fornecedor_nome** "
                        "— deve ser idêntico ao cadastrado no app.")
        return

    # ── Uploader ──────────────────────────────────────
    arquivo = st.file_uploader("Selecione o arquivo Excel", type=["xlsx","xls"],
                               key="upload_tabela")
    if not arquivo:
        return

    try:
        df = pd.read_excel(arquivo, dtype=str)
        df.columns = df.columns.str.strip().str.lower().str.replace(" ","_").str.replace("*","")
        df = df.dropna(subset=["codigo_produto","preco_caixa"])
        df["preco_caixa"] = pd.to_numeric(df["preco_caixa"], errors="coerce")
        df = df[df["preco_caixa"] > 0]
        st.caption(f"Preview — {len(df)} item(ns) encontrado(s) no arquivo:")
        st.dataframe(df.head(10), use_container_width=True)
        if len(df) > 10:
            st.caption(f"... e mais {len(df)-10} linha(s) não exibida(s).")
    except Exception as e:
        _erro(f"Erro ao ler o arquivo: {e}"); return

    # Desabilita o botão se já está processando (evita duplo clique)
    if st.session_state.get("imp_tab_processando"):
        st.info("⏳ Processando importação...")
        return

    if st.button("✅ Confirmar importação", type="primary", key="btn_conf_imp_tab"):
        st.session_state["imp_tab_processando"] = True

        conn = conectar()
        importados = 0
        erros_imp  = []
        tabelas_criadas = set()

        for idx, row in df.iterrows():
            try:
                forn_nome  = str(row.get("fornecedor_nome","")).strip()
                nome_tab   = str(row.get("nome_tabela","")).strip()
                tipo_tab   = str(row.get("tipo_tabela","varejo")).strip()
                prazo      = str(row.get("prazo_pagamento","")).strip()
                frete      = str(row.get("frete","")).strip() or None
                data_ini   = str(row.get("data_inicio","")).strip()[:10]
                data_fim_v = str(row.get("data_fim","")).strip()
                data_fim_v = data_fim_v[:10] if data_fim_v and data_fim_v.lower() not in ("nan","none","") else None
                codigo     = str(row.get("codigo_produto","")).strip()
                preco      = float(row["preco_caixa"])
                desc_max   = float(row["desconto_maximo"]) if pd.notna(row.get("desconto_maximo")) else 0.0
                preco_kg_t = None
                try:
                    v = row.get("preco_kg")
                    if v and str(v).strip() not in ("","nan","None"):
                        preco_kg_t = float(str(v).replace(",","."))
                except: pass
                obs_tab_t  = str(row.get("observacao") or "").strip() or None

                forn = conn.execute(
                    "SELECT fornecedor_id FROM fornecedor WHERE nome_fantasia=?",
                    (forn_nome,)).fetchone()
                if not forn:
                    erros_imp.append(f"Linha {idx+2}: Fornecedor '{forn_nome}' não encontrado."); continue
                forn_id = forn[0]

                tab = conn.execute("""
                    SELECT tabela_preco_id FROM tabela_preco
                    WHERE fornecedor_id=? AND nome_tabela=? AND data_inicio LIKE ?
                """, (forn_id, nome_tab, data_ini + "%")).fetchone()
                if not tab:
                    conn.execute("""
                        INSERT INTO tabela_preco
                        (fornecedor_id, nome_tabela, tipo_tabela, prazo_pagamento,
                         frete, data_inicio, data_fim, ativo)
                        VALUES (?,?,?,?,?,?,?,1)
                    """, (forn_id, nome_tab, tipo_tab, prazo, frete, data_ini, data_fim_v))
                    tab_id = conn.execute("""
                        SELECT tabela_preco_id FROM tabela_preco
                        WHERE fornecedor_id=? AND nome_tabela=? AND data_inicio LIKE ?
                    """, (forn_id, nome_tab, data_ini + "%")).fetchone()[0]
                else:
                    tab_id = tab[0]
                tabelas_criadas.add(nome_tab)

                prod = conn.execute("""
                    SELECT produto_id FROM produto
                    WHERE codigo_produto=? AND fornecedor_id=?
                """, (codigo, forn_id)).fetchone()
                if not prod:
                    erros_imp.append(f"Linha {idx+2}: Produto '{codigo}' não encontrado."); continue

                # Upsert compatível SQLite + PostgreSQL
                existe = conn.execute("""
                    SELECT 1 FROM tabela_preco_item
                    WHERE tabela_preco_id=? AND produto_id=?
                """, (tab_id, prod[0])).fetchone()

                if existe:
                    conn.execute("""
                        UPDATE tabela_preco_item
                        SET preco_caixa=?,
                            desconto_maximo=?,
                            preco_kg=COALESCE(?, preco_kg),
                            observacao=COALESCE(?, observacao)
                        WHERE tabela_preco_id=? AND produto_id=?
                    """, (preco, desc_max, preco_kg_t, obs_tab_t, tab_id, prod[0]))
                else:
                    conn.execute("""
                        INSERT INTO tabela_preco_item
                            (tabela_preco_id, produto_id, preco_caixa, desconto_maximo,
                             preco_kg, observacao)
                        VALUES (?,?,?,?,?,?)
                    """, (tab_id, prod[0], preco, desc_max, preco_kg_t, obs_tab_t))

                # Registra no histórico de preços
                from datetime import date as _date
                _hoje_str = _date.today().isoformat()
                preco_ant = conn.execute("""
                    SELECT preco_caixa FROM historico_preco
                    WHERE produto_id=? AND fornecedor_id=?
                    ORDER BY data_vigencia DESC, hist_id DESC LIMIT 1
                """, (prod[0], forn_id)).fetchone()
                # Só registra se o preço mudou ou não tem histórico
                if not preco_ant or abs(float(preco_ant[0]) - preco) > 0.001:
                    conn.execute("""
                        INSERT INTO historico_preco
                        (produto_id, fornecedor_id, tabela_id, nome_tabela,
                         data_vigencia, preco_caixa, preco_kg, data_registro)
                        VALUES (?,?,?,?,?,?,?,?)
                    """, (prod[0], forn_id, tab_id, nome_tab,
                          data_ini or _hoje_str, preco, preco_kg_t, _hoje_str))
                importados += 1

            except Exception as e:
                erros_imp.append(f"Linha {idx+2}: {e}")

        conn.commit(); conn.close()

        # Salva resultado no session_state e limpa flag de processamento
        st.session_state["imp_tab_resultado"]   = {
            "importados": importados,
            "erros":      erros_imp,
            "tabelas":    tabelas_criadas,
        }
        st.session_state.pop("imp_tab_processando", None)
        st.rerun()


# ═══════════════════════════════════════════════════════
# 4. CLIENTES
# ═══════════════════════════════════════════════════════

def tela_clientes():
    st.header("Clientes")
    _msg_cli = st.session_state.pop("_cli_msg_ok", None)
    if _msg_cli: st.success(_msg_cli)
    if st.button("⬅ Voltar"):
        _ir("home")
    ABAS_CLI = {
        "lista":"Lista","novo":"Novo Cliente","assoc":"Associações",
        "central":"Central Compras","import":"Importar","vinculos":"Vínculos",
        "pdvs":"PDVs","setores":"PDVs por Setor","mix":"Mix por PDV","contatos":"Contatos"
    }
    if "cli_aba" not in st.session_state:
        st.session_state["cli_aba"] = "lista"
    # Linha 1: primeiras 5 abas
    row1 = list(ABAS_CLI.items())[:5]
    row2 = list(ABAS_CLI.items())[5:]
    for row in [row1, row2]:
        cols = st.columns(len(row))
        for col,(k,v) in zip(cols, row):
            ativa = st.session_state["cli_aba"] == k
            if col.button(v, key=f"cnav_{k}", use_container_width=True,
                          type="primary" if ativa else "secondary"):
                st.session_state["cli_aba"] = k; st.rerun()
    st.divider()
    a = st.session_state["cli_aba"]
    if a=="lista":    _lista_clientes()
    elif a=="novo":   _form_novo_cliente()
    elif a=="assoc":  _tela_associacoes()
    elif a=="central":_tela_central_compras()
    elif a=="import": _tela_importar_clientes_pdvs()
    elif a=="vinculos":_tela_vinculos_cliente()
    elif a=="pdvs":   _tela_pdvs()
    elif a=="setores":_tela_pdvs_por_setor()
    elif a=="mix":    _tela_mix_pdv()
    elif a=="contatos":_tela_contatos_cliente()


def _executar_massa_cli(novo_status, filtro_status):
    """Executa alteracao em massa de status de clientes."""
    ativo_novo = 1 if novo_status == "Ativo" else 0
    conn = conectar()
    if filtro_status == "Todos":
        # Atualiza absolutamente todos
        conn.execute("UPDATE cliente SET status=?, ativo=?",
                     [novo_status, ativo_novo])
    elif filtro_status == "Ativo":
        # Inclui: status='Ativo', status='ativo', status NULL, ativo=1
        conn.execute("""UPDATE cliente SET status=?, ativo=?
            WHERE LOWER(COALESCE(status,'ativo'))='ativo' OR ativo=1""",
            [novo_status, ativo_novo])
    else:
        # Busca case-insensitive para outros status
        conn.execute("""UPDATE cliente SET status=?, ativo=?
            WHERE LOWER(COALESCE(status,''))=LOWER(?)""",
            [novo_status, ativo_novo, filtro_status])
    n = conn.execute("SELECT changes()").fetchone()[0]
    conn.commit()
    conn.close()
    st.session_state["_massa_cli_msg"] = f"✅ {n} cliente(s) atualizados para **{novo_status}**!"
    st.rerun()


def _executar_massa_pdv(novo_status, filtro_status, cliente_id=None):
    """Executa alteracao em massa de status de PDVs."""
    ativo_novo = 1 if novo_status == "Ativo" else 0
    cli_where  = " AND cliente_id=?" if cliente_id else ""
    cli_params = [cliente_id] if cliente_id else []
    conn = conectar()
    if filtro_status == "Todos":
        conn.execute(f"UPDATE pdv SET status=?, ativo=? WHERE 1=1{cli_where}",
                     [novo_status, ativo_novo] + cli_params)
    elif filtro_status == "Ativo":
        conn.execute(f"""UPDATE pdv SET status=?, ativo=?
            WHERE (LOWER(COALESCE(status,'ativo'))='ativo' OR ativo=1){cli_where}""",
            [novo_status, ativo_novo] + cli_params)
    else:
        conn.execute(f"""UPDATE pdv SET status=?, ativo=?
            WHERE LOWER(COALESCE(status,''))=LOWER(?){cli_where}""",
            [novo_status, ativo_novo, filtro_status] + cli_params)
    n = conn.execute("SELECT changes()").fetchone()[0]
    conn.commit()
    conn.close()
    st.session_state["_massa_pdv_msg"] = f"✅ {n} PDV(s) atualizados para **{novo_status}**!"
    st.rerun()


def COALESCE_STATUS(v, opts=None):
    """Normaliza status para o enum correto. Retorna o valor se valido, senao None."""
    if not v: return None
    # Aceita qualquer lista de opcoes validas
    validos = opts or (STATUS_CLI_OPTS + STATUS_PDV_OPTS)
    if v in validos: return v
    # Tenta case-insensitive
    for s in validos:
        if s.lower() == v.lower(): return s
    return None


STATUS_CLI_OPTS  = ['Prospecto', 'Visitado', 'Ativo', 'Inativo', 'Suspenso', 'Encerrado']
STATUS_PDV_OPTS  = ['Prospecto', 'Visitado', 'Ativo', 'Inativo', 'Suspenso', 'Encerrado']
STATUS_ICONE_MAP = {'Prospecto': '🔵', 'Visitado': '🟣', 'Ativo': '🟢', 'Inativo': '⚫', 'Suspenso': '🟡', 'Encerrado': '🔴', None: '⚪'}


def _status_icone(s):
    return STATUS_ICONE_MAP.get(s, "⚪") + " " + (s or "—")


def _lista_clientes():
    msg_massa = st.session_state.pop("_massa_cli_msg", None)
    if msg_massa:
        st.success(msg_massa)

    PERFIS_CLI = ["Todos","Empório","Supermercado","Hipermercado","Atacadista","Mini Mercado","Mercearia","Sacolão","Hortifruti","Açougue","Casa de Carnes","Peixaria","Padaria","Confeitaria","Delicatessen","Hamburgueria","Restaurante","Lanchonete","Bar / Boteco","Clube / Associação","Outro"]

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        fil_status = st.selectbox("Filtrar por status",
                                  ["Todos"] + STATUS_CLI_OPTS, key="fil_cli_status")
    with col_f2:
        fil_busca  = st.text_input("Buscar por nome", key="fil_cli_nome",
                                   placeholder="Digite parte do nome...")
    with col_f3:
        fil_perfil = st.selectbox("Tipo de estabelecimento",
                                  PERFIS_CLI, key="fil_cli_perfil")

    # Alteracao em massa — session_state para capturar apos rerun
    with st.expander("🔄 Alterar status em massa"):
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.selectbox("Novo status", STATUS_CLI_OPTS, key="massa_cli_status")
        with col_m2:
            st.selectbox("Aplicar em clientes com status",
                         ["Todos"] + STATUS_CLI_OPTS, key="massa_cli_filtro")
        st.button("✅ Aplicar agora", key="btn_massa_cli",
                  type="primary", use_container_width=True)

    # Processa FORA do expander, no nivel principal da funcao
    if st.session_state.get("btn_massa_cli"):
        _executar_massa_cli(
            st.session_state.get("massa_cli_status", STATUS_CLI_OPTS[0]),
            st.session_state.get("massa_cli_filtro", "Todos"),
        )

    where_q  = []
    params_q = []
    if fil_status != "Todos":
        where_q.append("c.status=?"); params_q.append(fil_status)
    if fil_busca.strip():
        where_q.append("c.nome_fantasia LIKE ?"); params_q.append(f"%{fil_busca.strip()}%")
    if fil_perfil != "Todos":
        where_q.append("c.perfil=?"); params_q.append(fil_perfil)
    where_sql = ("WHERE " + " AND ".join(where_q)) if where_q else ""

    dados = query(f"""
        SELECT c.cliente_id, c.nome_fantasia, c.cidade, c.estado,
               c.ativo, COALESCE(c.status,'Ativo') AS status,
               COUNT(DISTINCT cf.cliente_fornecedor_id) AS fornecedores,
               COUNT(DISTINCT p.pdv_id) AS pdvs
        FROM cliente c
        LEFT JOIN cliente_fornecedor cf ON c.cliente_id=cf.cliente_id AND cf.ativo!=0
        LEFT JOIN pdv p ON c.cliente_id=p.cliente_id AND p.ativo!=0
        {where_sql}
        GROUP BY c.cliente_id, c.nome_fantasia, c.cidade, c.estado, c.ativo, c.status
        ORDER BY c.nome_fantasia
    """, tuple(params_q))

    if not dados:
        st.info("Nenhum cliente encontrado.")
        return

    col_ct, col_exp = st.columns([3,1])
    col_ct.caption(f"{len(dados)} cliente(s)")
    with col_exp:
        if st.button("⬇️ Exportar Excel", key="btn_exp_cli", use_container_width=True):
            try:
                extras = query(f"""
                    SELECT c.cliente_id, COALESCE(c.razao_social,''),
                           COALESCE(c.perfil,''), COALESCE(c.fone,''),
                           COALESCE(c.email,''),
                           COALESCE(c.cnpj,''), COALESCE(c.endereco,''),
                           COALESCE(c.bairro,''), COALESCE(c.site,''),
                           COALESCE(c.instagram,''), COALESCE(c.observacao,''),
                           COALESCE(a.nome,'')
                    FROM cliente c
                    LEFT JOIN associacao a ON a.associacao_id = c.associacao_id
                    {where_sql}
                    ORDER BY c.nome_fantasia
                """, tuple(params_q))
                extras_map = {r[0]: r for r in extras}
                cols_exp = ["ID","nome_fantasia","razao_social","perfil","status",
                            "fone","email","cnpj","endereco","bairro","cidade",
                            "estado","site","instagram","associacao_nome","observacao"]
                linhas = []
                for r in dados:
                    ex = extras_map.get(r[0],[r[0],'','','','','','','','','','',''])
                    linhas.append([r[0],r[1],ex[1],ex[2],r[5],ex[3],ex[4],ex[5],
                                   ex[6],ex[7],r[2],r[3],ex[8],ex[9],ex[11],ex[10]])
                df_exp = pd.DataFrame(linhas, columns=cols_exp)
                buf_exp = io.BytesIO()
                with pd.ExcelWriter(buf_exp, engine='openpyxl') as writer:
                    df_exp.to_excel(writer, index=False, sheet_name="Clientes")
                st.session_state["_cli_xlsx"] = buf_exp.getvalue()
            except Exception as _ex:
                st.error(f"Erro: {_ex}")

    if "_cli_xlsx" in st.session_state:
        st.download_button("📥 Baixar Excel",
                           data=st.session_state.pop("_cli_xlsx"),
                           file_name="clientes_peppercrm.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           key="dl_cli_xlsx")

    h1,h2,h3,h4,h5,h6 = st.columns([0.4,2.8,1.2,0.6,1.5,1.2])
    for col, txt in zip([h1,h2,h3,h4,h5,h6],
                        ["ID","Cliente","Cidade","UF","Status",""]):
        col.markdown(f"<small><b>{txt}</b></small>", unsafe_allow_html=True)

    for row in dados:
        cid, nome, cidade, uf, ativo, status, fornec, pdvs = row

        c1,c2,c3,c4,c5,c6 = st.columns([0.4,2.8,1.2,0.6,1.5,1.2])
        c1.caption(str(cid))
        c2.write(nome)
        c3.caption(cidade or "—")
        c4.caption(uf or "—")
        c5.caption(_status_icone(status))
        with c6:
            b1, b2 = st.columns(2)
            with b1:
                if st.button("✏️", key=f"ed_cli_{cid}", help="Editar",
                             use_container_width=True):
                    st.session_state["cli_editar_id"] = cid
                    st.session_state.pop("cli_excluir_id", None)
                    st.rerun()
            with b2:
                if st.button("🗑️", key=f"ex_cli_{cid}", help="Excluir",
                             use_container_width=True):
                    st.session_state["cli_excluir_id"] = cid
                    st.session_state.pop("cli_editar_id", None)
                    st.rerun()

        if st.session_state.get("cli_editar_id") == cid:
            _form_editar_cliente(cid)
        if st.session_state.get("cli_excluir_id") == cid:
            _confirmacao_excluir_cliente(cid, nome)



def _confirmacao_excluir_cliente(cid, nome):
    n_ped = query('SELECT COUNT(*) FROM pedido WHERE cliente_id=?', (cid,))[0][0]
    n_pdv = query('SELECT COUNT(*) FROM pdv WHERE cliente_id=?', (cid,))[0][0]
    n_vis = query('SELECT COUNT(*) FROM visita_cliente WHERE cliente_id=?', (cid,))[0][0]
    n_pq  = query('SELECT COUNT(*) FROM pesquisa_preco WHERE cliente_id=?', (cid,))[0][0]

    if n_ped > 0:
        st.error(
            f"Não é possível excluir **{nome}** pois possui {n_ped} pedido(s) vinculado(s). "
            f"Use a opção Editar para desativar o cliente."
        )
        if st.button("Fechar", key=f"fechar_ex_cli_{cid}"):
            st.session_state.pop("cli_excluir_id", None); st.rerun()
        return

    msg = f"Excluir permanentemente **{nome}**?"
    detalhes = []
    if n_pdv: detalhes.append(f"{n_pdv} PDV(s)")
    if n_vis: detalhes.append(f"{n_vis} visita(s)")
    if n_pq:  detalhes.append(f"{n_pq} pesquisa(s) de preço")
    if detalhes:
        msg += f" Isso removerá também: {', '.join(detalhes)}."
    st.warning(msg)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Confirmar exclusão", key=f"conf_ex_cli_{cid}",
                     type="primary", use_container_width=True):
            conn = conectar()
            # Remove dependências sem pedido
            conn.execute("DELETE FROM mix_cliente WHERE cliente_id=?", (cid,))
            conn.execute("DELETE FROM pesquisa_preco_item WHERE pesquisa_id IN (SELECT pesquisa_id FROM pesquisa_preco WHERE cliente_id=?)", (cid,))
            conn.execute("DELETE FROM pesquisa_preco WHERE cliente_id=?", (cid,))
            conn.execute("DELETE FROM visita_cliente WHERE cliente_id=?", (cid,))
            conn.execute("DELETE FROM contato_cliente WHERE cliente_id=?", (cid,))
            conn.execute("DELETE FROM cliente_fornecedor WHERE cliente_id=?", (cid,))
            conn.execute("DELETE FROM pdv WHERE cliente_id=?", (cid,))
            conn.execute("DELETE FROM cliente WHERE cliente_id=?", (cid,))
            conn.commit(); conn.close()
            st.session_state.pop("cli_excluir_id", None)
            st.success(f"Cliente excluido!"); st.rerun()
    with col2:
        if st.button("Cancelar", key=f"canc_ex_cli_{cid}", use_container_width=True):
            st.session_state.pop("cli_excluir_id", None); st.rerun()


def _form_novo_cliente():
    st.subheader("Novo cliente")
    assocs = query("SELECT associacao_id, nome FROM associacao WHERE ativo=1 ORDER BY nome")
    assoc_opts = [(None, "— Nenhuma (cliente independente)")] + [(a[0], a[1]) for a in assocs]
    with st.form("novo_cliente", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            fantasia = st.text_input("Nome fantasia *")
            razao    = st.text_input("Razao social")
            perfil   = st.selectbox("Perfil / tipo *", ["— Selecione —","Empório","Supermercado","Hipermercado","Atacadista","Mini Mercado","Mercearia","Sacolão","Hortifruti","Açougue","Casa de Carnes","Peixaria","Padaria","Confeitaria","Delicatessen","Hamburgueria","Restaurante","Lanchonete","Bar / Boteco","Clube / Associação","Outro"])
            fone     = st.text_input("Fone / WhatsApp", placeholder="Ex: 13988776655")
            email    = st.text_input("E-mail", placeholder="Ex: compras@cliente.com.br")
            cnpj     = st.text_input("CNPJ")
            site     = st.text_input("Site")
            insta    = st.text_input("Instagram", placeholder="@perfil")
            assoc_sel= st.selectbox("Associacao de compras", assoc_opts,
                                    format_func=lambda x: x[1])
        with col2:
            endereco = st.text_input("Endereco")
            bairro   = st.text_input("Bairro")
            cidade   = st.text_input("Cidade")
            estado   = st.selectbox("UF", _ufs())
        obs      = st.text_area("Observacao")
        status_n = st.selectbox("Status inicial", STATUS_CLI_OPTS,
                                index=0,
                                help="Prospecto = ainda nao e cliente ativo")
        salvar = st.form_submit_button("Salvar cliente", type="primary")
    if salvar:
        if not fantasia.strip():
            _erro("Nome fantasia e obrigatorio."); return
        if perfil == "— Selecione —":
            _erro("Selecione o tipo de estabelecimento."); return
        existe = query("SELECT cliente_id FROM cliente WHERE LOWER(nome_fantasia)=LOWER(?)",
                       (fantasia.strip(),))
        if existe:
            _erro(f"Ja existe um cliente com o nome '{fantasia}'."); return
        ativo_n = 1 if status_n == "Ativo" else 0
        conn = conectar()
        conn.execute("""
            INSERT INTO cliente
            (razao_social, nome_fantasia, perfil, fone, email, cnpj, ie, endereco, bairro,
             cidade, estado, site, instagram, associacao_id, observacao, status, ativo)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (razao, fantasia.strip(), perfil, fone or None, email or None,
              cnpj or None, None,
              endereco or None, bairro or None, cidade, estado,
              site or None, insta or None, assoc_sel[0], obs or None,
              status_n, ativo_n))
        conn.commit(); conn.close()
        st.session_state["_cli_msg_ok"] = f"✅ Cliente '{fantasia}' cadastrado como {status_n}!"
        st.rerun()


def _form_editar_cliente(cli_id):
    conn = conectar()
    c = conn.execute("SELECT * FROM cliente WHERE cliente_id=?", (cli_id,)).fetchone()
    conn.close()
    if not c: return
    assocs   = query("SELECT associacao_id, nome FROM associacao WHERE ativo=1 ORDER BY nome")
    assoc_opts = [(None, "— Nenhuma")] + [(a[0], a[1]) for a in assocs]
    assoc_ids  = [a[0] for a in assoc_opts]
    idx_assoc  = assoc_ids.index(c["associacao_id"]) if c["associacao_id"] in assoc_ids else 0
    perfis_e   = ["— Selecione —","Empório","Supermercado","Hipermercado","Atacadista","Mini Mercado","Mercearia","Sacolão","Hortifruti","Açougue","Casa de Carnes","Peixaria","Padaria","Confeitaria","Delicatessen","Hamburgueria","Restaurante","Lanchonete","Bar / Boteco","Clube / Associação","Outro"]
    perfil_at  = c["perfil"] if c["perfil"] and c["perfil"] in perfis_e else perfis_e[0]

    with st.form(f"edit_cli_{cli_id}"):
        col1, col2 = st.columns(2)
        with col1:
            fantasia = st.text_input("Nome fantasia", c["nome_fantasia"] or "")
            razao    = st.text_input("Razao social",  c["razao_social"]  or "")
            perfil   = st.selectbox("Perfil / tipo", perfis_e,
                                    index=perfis_e.index(perfil_at))
            fone     = st.text_input("Fone / WhatsApp", c["fone"] or "")
            email    = st.text_input("E-mail",          c["email"] or "" if "email" in (c.keys() if hasattr(c,'keys') else []) else "")
            cnpj     = st.text_input("CNPJ",           c["cnpj"]     or "")
            site     = st.text_input("Site",            c["site"]     or "")
            insta    = st.text_input("Instagram",       c["instagram"] or "")
            assoc_e  = st.selectbox("Associacao de compras", assoc_opts,
                                    index=idx_assoc, format_func=lambda x: x[1])
        with col2:
            endereco = st.text_input("Endereco", c["endereco"] or "")
            bairro   = st.text_input("Bairro",   c["bairro"]   or "")
            cidade   = st.text_input("Cidade",   c["cidade"]   or "")
            ufs = _ufs()
            idx = ufs.index(c["estado"]) if c["estado"] in ufs else 0
            estado = st.selectbox("UF", ufs, index=idx)
        obs    = st.text_area("Observacao", c["observacao"] or "")
        st_at  = COALESCE_STATUS(c["status"])
        idx_st = STATUS_CLI_OPTS.index(st_at) if st_at in STATUS_CLI_OPTS else 0
        status_e = st.selectbox("Status", STATUS_CLI_OPTS, index=idx_st)
        salvar = st.form_submit_button("Salvar alteracoes", type="primary")

    if salvar:
        if not fantasia.strip():
            _erro("Nome fantasia e obrigatorio."); return
        existe = query("SELECT cliente_id FROM cliente WHERE LOWER(nome_fantasia)=LOWER(?) AND cliente_id!=?",
                       (fantasia.strip(), cli_id))
        if existe:
            _erro(f"Ja existe outro cliente com o nome '{fantasia}'."); return
        ativo_novo = 1 if status_e == "Ativo" else 0
        # Verifica se coluna email existe antes de incluir no UPDATE
        _tem_email = True
        try:
            query("SELECT email FROM cliente LIMIT 1")
        except Exception:
            _tem_email = False

        conn = conectar()
        if _tem_email:
            conn.execute("""
                UPDATE cliente SET razao_social=?, nome_fantasia=?, perfil=?, fone=?,
                email=?, cnpj=?, endereco=?, bairro=?, cidade=?, estado=?,
                site=?, instagram=?, associacao_id=?, observacao=?, status=?, ativo=?
                WHERE cliente_id=?
            """, (razao, fantasia.strip(), perfil, fone or None,
                  email or None, cnpj or None, endereco or None, bairro or None, cidade, estado,
                  site or None, insta or None, assoc_e[0], obs or None,
                  status_e, ativo_novo, cli_id))
        else:
            conn.execute("""
                UPDATE cliente SET razao_social=?, nome_fantasia=?, perfil=?, fone=?,
                cnpj=?, endereco=?, bairro=?, cidade=?, estado=?,
                site=?, instagram=?, associacao_id=?, observacao=?, status=?, ativo=?
                WHERE cliente_id=?
            """, (razao, fantasia.strip(), perfil, fone or None,
                  cnpj or None, endereco or None, bairro or None, cidade, estado,
                  site or None, insta or None, assoc_e[0], obs or None,
                  status_e, ativo_novo, cli_id))
            st.warning("⚠️ E-mail não foi salvo — coluna ainda não existe no banco. Aguarde migration.")
        conn.commit(); conn.close()
        st.session_state["_cli_msg_ok"] = "✅ Cliente atualizado com sucesso!"
        st.rerun()


def _tela_vinculos_cliente():
    st.subheader("Vínculos cliente ↔ fornecedor")
    st.caption("Defina qual tabela de preço e prazo valem para cada par cliente/fornecedor.")
    # Inclui todos os status — prospectos e visitados precisam de contatos cadastrados
    clientes = query("""SELECT cliente_id,
        nome_fantasia || ' (' || COALESCE(status,'Ativo') || ')'
        FROM cliente ORDER BY nome_fantasia""")
    if not clientes:
        st.warning("Cadastre clientes e fornecedores primeiro."); return

    cli_sel = st.selectbox("Cliente", clientes, format_func=lambda x: x[1], key="vinc_cli")
    cli_id  = cli_sel[0]

    forns   = cache_fornecedores()
    tabelas = query("SELECT tabela_preco_id, fornecedor_id, nome_tabela, prazo_pagamento FROM tabela_preco WHERE ativo=1 ORDER BY nome_tabela")

    vinculos = query("""
        SELECT cf.cliente_fornecedor_id, f.fornecedor_id, f.nome_fantasia,
               cf.tabela_preco_id, tp.nome_tabela,
               cf.prazo_pagamento, cf.codigo_cliente, cf.observacao, cf.ativo
        FROM cliente_fornecedor cf
        JOIN fornecedor f ON cf.fornecedor_id = f.fornecedor_id
        LEFT JOIN tabela_preco tp ON cf.tabela_preco_id = tp.tabela_preco_id
        WHERE cf.cliente_id = ?
        ORDER BY f.nome_fantasia
    """, (cli_id,))

    # ── Vínculos existentes com botão Editar por linha ─
    if vinculos:
        st.caption(f"{len(vinculos)} vínculo(s) cadastrado(s)")

        h1, h2, h3, h4, h5 = st.columns([2, 2.5, 1.5, 0.5, 1])
        for col, txt in zip([h1,h2,h3,h4,h5], ["Fornecedor","Tabela de preço","Prazo","St.",""]):
            col.markdown(f"<small><b>{txt}</b></small>", unsafe_allow_html=True)

        for v in vinculos:
            cf_id, forn_id_v, forn_n, tab_id_v, tab_n, prazo_v, cod_cli_v, obs_v, ativo_v = v
            c1, c2, c3, c4, c5 = st.columns([2, 2.5, 1.5, 0.5, 1])
            c1.write(forn_n)
            c2.caption(tab_n or "— sem tabela")
            c3.caption(prazo_v or "—")
            c4.caption("✅" if ativo_v else "❌")
            with c5:
                if st.button("✏️ Editar", key=f"ed_vinc_{cf_id}", use_container_width=True):
                    st.session_state["vinc_editar_id"] = cf_id
                    st.rerun()

            # Form de edição inline
            if st.session_state.get("vinc_editar_id") == cf_id:
                with st.container():
                    st.markdown(f"**Editando vínculo com {forn_n}**")
                    tabs_forn_e = [(t[0], f"{t[2]} ({t[3]})") for t in tabelas if t[1] == forn_id_v]
                    tab_ids_e   = [t[0] for t in tabs_forn_e]
                    idx_tab_e   = tab_ids_e.index(tab_id_v) if tab_id_v in tab_ids_e else 0

                    with st.form(f"edit_vinc_{cf_id}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            if tabs_forn_e:
                                tab_e = st.selectbox("Tabela de preço", tabs_forn_e,
                                                     index=idx_tab_e,
                                                     format_func=lambda x: x[1],
                                                     key=f"tab_e_{cf_id}")
                            else:
                                st.caption("Nenhuma tabela disponível para este fornecedor.")
                                tab_e = None
                            prazo_e = st.text_input("Prazo específico",
                                                    value=prazo_v or "",
                                                    help="Deixe vazio para usar o prazo da tabela")
                        with col2:
                            cod_e   = st.text_input("Código do cliente no fornecedor",
                                                    value=cod_cli_v or "")
                            obs_e   = st.text_input("Observação", value=obs_v or "")
                            ativo_e = st.checkbox("Ativo", value=bool(ativo_v))

                        col_s, col_c = st.columns(2)
                        with col_s: salvar_e   = st.form_submit_button("💾 Salvar alterações", type="primary")
                        with col_c: cancelar_e = st.form_submit_button("Cancelar")

                    if salvar_e:
                        novo_tab_id = tab_e[0] if tab_e else None
                        conn = conectar()
                        conn.execute("""UPDATE cliente_fornecedor SET
                            tabela_preco_id=?, prazo_pagamento=?,
                            codigo_cliente=?, observacao=?, ativo=?
                            WHERE cliente_fornecedor_id=?""",
                            (novo_tab_id, prazo_e or None,
                             cod_e or None, obs_e or None,
                             1 if ativo_e else 0, cf_id))
                        conn.commit(); conn.close()
                        st.session_state.pop("vinc_editar_id", None)
                        _sucesso(f"Vínculo com {forn_n} atualizado!")
                        st.rerun()

                    if cancelar_e:
                        st.session_state.pop("vinc_editar_id", None)
                        st.rerun()
    else:
        st.info("Nenhum vínculo cadastrado para este cliente.")

    # ── Adicionar novo vínculo ─────────────────────────
    st.divider()
    st.subheader("Adicionar vínculo")

    # Fornecedores que ainda NÃO têm vínculo com este cliente
    forn_ids_ja = {v[1] for v in vinculos} if vinculos else set()
    forns_disp  = [f for f in forns if f[0] not in forn_ids_ja]

    if not forns_disp:
        st.caption("Este cliente já está vinculado a todos os fornecedores cadastrados.")
        return

    with st.form(f"novo_vinculo_{cli_id}", clear_on_submit=True):
        forn_sel  = st.selectbox("Fornecedor", forns_disp, format_func=lambda x: x[1])
        tabs_forn = [(t[0], f"{t[2]} ({t[3]})") for t in tabelas if forn_sel and t[1] == forn_sel[0]]
        tab_sel   = st.selectbox("Tabela de preço",
                                 tabs_forn if tabs_forn else [(None, "— nenhuma tabela disponível")],
                                 format_func=lambda x: x[1])
        prazo_esp = st.text_input("Prazo específico (deixe vazio para usar o da tabela)")
        cod_cli   = st.text_input("Código deste cliente no fornecedor (opcional)")
        obs_v2    = st.text_input("Observação")
        salvar    = st.form_submit_button("➕ Adicionar vínculo", type="primary")

    if salvar:
        if not forn_sel:
            _erro("Selecione o fornecedor."); return
        conn = conectar()
        tab_id = tab_sel[0] if tab_sel and tab_sel[0] else None
        try:
            conn.execute("""INSERT INTO cliente_fornecedor
                (cliente_id, fornecedor_id, tabela_preco_id, prazo_pagamento, codigo_cliente, observacao, ativo)
                VALUES (?,?,?,?,?,?,1)""",
                (cli_id, forn_sel[0], tab_id, prazo_esp or None, cod_cli or None, obs_v2 or None))
            conn.commit()
            _sucesso(f"Vínculo com {forn_sel[1]} adicionado!")
            st.rerun()
        except Exception as e:
            _erro("Este cliente já está vinculado a este fornecedor." if "UNIQUE" in str(e) else str(e))
        finally:
            conn.close()


# ─────────────────────────────────────────────────────
# PDVs
# ─────────────────────────────────────────────────────

def _tela_pdvs():
    msg_pdv = st.session_state.pop("_massa_pdv_msg", None)
    if msg_pdv: st.success(msg_pdv)
    msg_pdv_ok = st.session_state.pop("_pdv_msg_ok", None)
    if msg_pdv_ok: st.success(msg_pdv_ok)

    st.subheader("PDVs (lojas)")
    st.caption("Cadastre as lojas de cada cliente. Clientes sem PDV recebem os pedidos diretamente.")

    clientes_all = query("SELECT cliente_id, nome_fantasia FROM cliente ORDER BY nome_fantasia")

    # ── CORREÇÃO DE TIPO PDV ────────────────────────────────────────────
    with st.expander("🔧 Padronizar tipo de PDV — corrigir duplicatas"):
        st.caption(
            "Use para corrigir variações do mesmo tipo — ex: 'emporio' e 'Empório' "
            "são o mesmo tipo mas grafias diferentes. Selecione o valor errado e "
            "informe o correto."
        )
        tipos_existentes = query("""SELECT DISTINCT tipo_pdv, COUNT(*) as qtd
            FROM pdv WHERE tipo_pdv IS NOT NULL
            GROUP BY tipo_pdv ORDER BY tipo_pdv""")
        if tipos_existentes:
            col_de, col_para, col_btn_pad = st.columns([2, 2, 1])
            with col_de:
                tipo_errado = st.selectbox(
                    "Valor a corrigir",
                    [(t[0], f"{t[0]}  ({t[1]} PDV(s))") for t in tipos_existentes],
                    format_func=lambda x: x[1],
                    key="pad_tipo_de")
            with col_para:
                tipo_certo = st.text_input(
                    "Substituir por",
                    placeholder="Ex: Empório",
                    key="pad_tipo_para")
            with col_btn_pad:
                st.write("")
                if st.button("✅ Aplicar", key="btn_pad_tipo",
                             use_container_width=True, type="primary"):
                    if tipo_certo.strip() and tipo_errado:
                        conn = conectar()
                        conn.execute(
                            "UPDATE pdv SET tipo_pdv=? WHERE tipo_pdv=?",
                            (tipo_certo.strip(), tipo_errado[0]))
                        qtd = conn.execute(
                            "SELECT changes()").fetchone()[0]
                        conn.commit(); conn.close()
                        st.session_state["_massa_pdv_msg"] = (
                            f"✅ {qtd} PDV(s) atualizados: "
                            f"'{tipo_errado[0]}' → '{tipo_certo.strip()}'")
                        st.rerun()
                    else:
                        st.error("Preencha o valor correto.")
            st.divider()
            # Exibe tabela atual de tipos para referência
            df_tipos = pd.DataFrame(tipos_existentes, columns=["Tipo","Qtd PDVs"])
            st.dataframe(df_tipos, use_container_width=True, hide_index=True)

    # ── FILTROS ──────────────────────────────────────────────────────────
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    with col_f1:
        cli_opts = [(None,"Todos os clientes")] + [(c[0],c[1]) for c in clientes_all]
        cli_fil  = st.selectbox("Cliente", cli_opts,
                                format_func=lambda x: x[1], key="pdv_cli_fil")
    with col_f2:
        fil_pdv_st = st.selectbox("Status", ["Todos"] + STATUS_PDV_OPTS,
                                  key="fil_pdv_st2")
    with col_f3:
        tipos_pdv_fil = query("""SELECT DISTINCT tipo_pdv FROM pdv
            WHERE tipo_pdv IS NOT NULL ORDER BY tipo_pdv""")
        tipo_opts = ["Todos"] + [t[0] for t in tipos_pdv_fil if t[0]]
        fil_tipo  = st.selectbox("Tipo de PDV", tipo_opts, key="fil_pdv_tipo")
    with col_f4:
        cidades_pdv = query("""SELECT DISTINCT cidade FROM pdv
            WHERE cidade IS NOT NULL ORDER BY cidade""")
        cid_opts  = ["Todas"] + [c[0] for c in cidades_pdv if c[0]]
        fil_cid   = st.selectbox("Cidade", cid_opts, key="fil_pdv_cid")

    # ── ALTERAÇÃO EM MASSA ───────────────────────────────────────────────
    with st.expander("🔄 Alterar status em massa — PDVs"):
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.selectbox("Novo status", STATUS_PDV_OPTS, key="massa_pdv2")
        with col_m2:
            st.selectbox("Aplicar em PDVs com status",
                         ["Todos"] + STATUS_PDV_OPTS, key="massa_pdv_f2")
        st.caption("Os filtros acima serão respeitados.")
        st.button("✅ Aplicar agora", key="btn_massa_pdv2",
                  type="primary", use_container_width=True)

    if st.session_state.get("btn_massa_pdv2"):
        _executar_massa_pdv(
            st.session_state.get("massa_pdv2", STATUS_PDV_OPTS[0]),
            st.session_state.get("massa_pdv_f2", "Todos"),
            cli_fil[0] if cli_fil[0] else None)

    # ── QUERY com todos os filtros ────────────────────────────────────────
    where_p = ["1=1"]; params_p = []
    if cli_fil[0]:
        where_p.append("p.cliente_id=?");            params_p.append(cli_fil[0])
    if fil_pdv_st != "Todos":
        where_p.append("COALESCE(p.status,'Ativo')=?"); params_p.append(fil_pdv_st)
    if fil_tipo != "Todos":
        where_p.append("p.tipo_pdv=?");              params_p.append(fil_tipo)
    if fil_cid != "Todas":
        where_p.append("p.cidade=?");                params_p.append(fil_cid)

    pdvs = query(f"""
        SELECT p.pdv_id, c.nome_fantasia, p.numero_loja, p.nome_loja,
               COALESCE(p.tipo_pdv,'—') AS tipo,
               COALESCE(p.setor,'—')    AS setor,
               COALESCE(p.cidade,'—')   AS cidade,
               COALESCE(p.status,'Ativo') AS status,
               p.cliente_id
        FROM pdv p
        JOIN cliente c ON p.cliente_id=c.cliente_id
        WHERE {' AND '.join(where_p)}
        ORDER BY c.nome_fantasia, p.nome_loja
    """, tuple(params_p))

    if pdvs:
        df = pd.DataFrame(pdvs, columns=["ID","Cliente","Nr.","Nome","Tipo","Setor",
                                          "Cidade","Status","cli_id"])
        col_ct2, col_exp2 = st.columns([3,1])
        col_ct2.caption(f"{len(pdvs)} PDV(s) encontrado(s)")
        with col_exp2:
            if st.button("⬇️ Exportar Excel", key="exp_pdv_xlsx",
                         use_container_width=True):
                st.session_state["exp_pdv_trigger"] = True

        if st.session_state.pop("exp_pdv_trigger", False):
            # Exportação respeita os filtros ativos
            dados_pdv_exp = query(f"""
                SELECT p.pdv_id, c.nome_fantasia AS cliente,
                       COALESCE(p.numero_loja,''), p.nome_loja,
                       COALESCE(p.tipo_pdv,''), COALESCE(p.setor,''),
                       COALESCE(p.endereco,''), COALESCE(p.bairro,''),
                       COALESCE(p.cidade,''), COALESCE(p.estado,''),
                       COALESCE(p.cnpj,''), COALESCE(p.gerente,''),
                       COALESCE(p.fone_gerente,''),
                       COALESCE(p.horario_recebimento,''),
                       COALESCE(p.status,'Ativo'),
                       COALESCE(p.latitude,''), COALESCE(p.longitude,''),
                       COALESCE(p.observacao,'')
                FROM pdv p
                JOIN cliente c ON p.cliente_id=c.cliente_id
                WHERE {' AND '.join(where_p)}
                ORDER BY c.nome_fantasia, p.nome_loja
            """, tuple(params_p))
            df_pdv_exp = pd.DataFrame(dados_pdv_exp, columns=[
                "ID","cliente_nome","numero_loja","nome_loja","tipo_pdv","setor",
                "endereco","bairro","cidade","estado","cnpj","gerente","fone_gerente",
                "horario_recebimento","status","latitude","longitude","observacao"])
            buf_pdv = io.BytesIO()
            df_pdv_exp.to_excel(buf_pdv, index=False, sheet_name="PDVs")
            buf_pdv.seek(0)
            # Nome do arquivo reflete os filtros
            sufixo = "_".join(filter(None, [
                fil_tipo if fil_tipo!="Todos" else "",
                fil_cid if fil_cid!="Todas" else "",
                fil_pdv_st if fil_pdv_st!="Todos" else ""
            ])) or "todos"
            st.download_button(
                "📥 Baixar PDVs filtrados",
                data=buf_pdv,
                file_name=f"pdvs_{sufixo[:30]}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True)

        df["Status"] = df["Status"].apply(_status_icone)
        st.dataframe(df[["Cliente","Nr.","Nome","Tipo","Setor","Cidade","Status"]],
                     use_container_width=True, hide_index=True)

        st.divider()
        st.subheader("Editar PDV")
        ids = [(r[0], f"{r[1]} — {r[3]}") for r in pdvs]
        col_sel, col_del = st.columns([4, 1])
        with col_sel:
            sel = st.selectbox("Selecione o PDV", ids,
                               format_func=lambda x: x[1], key="pdv_edit_sel")
        with col_del:
            st.write(""); st.write("")
            if st.button("🗑️ Excluir", key="btn_excluir_pdv",
                         use_container_width=True,
                         help="Excluir o PDV selecionado"):
                st.session_state["pdv_excluir_id"] = sel[0]
                st.rerun()

        if st.session_state.get("pdv_excluir_id") == sel[0]:
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
                    st.rerun()
    else:
        st.info("Nenhum PDV encontrado para os filtros selecionados.")

    st.divider()
    # Novo PDV - cliente deve ser selecionado explicitamente
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
        _form_novo_pdv(cli_novo[0])


def _form_novo_pdv(cli_id):
    TIPOS_PDV = [
            "Supermercado",
            "Hipermercado",
            "Atacadista",
            "Mini Mercado",
            "Mercearia",
            "Emporio",
            "Sacolao",
            "Hortifruti",
            "Acougue",
            "Casa de Carnes",
            "Peixaria",
            "Padaria",
            "Confeitaria",
            "Delicatessen",
            "Hamburgueria",
            "Restaurante",
            "Lanchonete",
            "Bar / Boteco",
            "Clube / Associacao",
            "Outro"
        ]
    with st.form(f"novo_pdv_{cli_id}", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nome_loja = st.text_input("Nome da loja *")
            tipo_pdv  = st.selectbox("Tipo de PDV", TIPOS_PDV, key=f"pdv_tipo_{cli_id}")
            numero    = st.text_input("Numero da loja (opcional)",
                                      placeholder="Ex: Loja 05, Filial Centro")
            endereco  = st.text_input("Endereco")
            bairro    = st.text_input("Bairro")
            cidade    = st.text_input("Cidade")
            estado    = st.selectbox("UF", _ufs(), key=f"pdv_uf_{cli_id}")
            cnpj      = st.text_input("CNPJ (opcional)")
        with col2:
            gerente          = st.text_input("Gerente")
            fone_gerente     = st.text_input("Fone gerente")
            encarregado      = st.text_input("Encarregado / Responsavel compras")
            fone_encarregado = st.text_input("Fone encarregado")
            horario          = st.text_input("Horario de recebimento",
                                             placeholder="Ex: Seg-Sex 08h-17h")
            setor            = st.text_input("Setor",
                                            placeholder="Ex: Setor Centro, Setor Leste, Setor Baixada 1",
                                            help="Setor geografico — facilita planejamento de roteiro e alocacao de promotores")
            cluster          = st.selectbox("Cluster (poder aquisitivo)",
                                            ["A/B","B/C","C/D","A","B","C","D","—"],
                                            key=f"pdv_cluster_{cli_id}",
                                            help="A/B = premium, B/C = medio, C/D = popular")
            tamanho_pdv      = st.selectbox("Tamanho do PDV",
                                            ["GG","G","M","P","PP","—"],
                                            key=f"pdv_tamanho_{cli_id}",
                                            help="GG=hipermercado, G=grande, M=medio, P=pequeno, PP=micro")
        status_pdv = st.selectbox("Status do PDV *",
                                   ["Prospecto", "Ativo", "Inativo", "Bloqueado"],
                                   index=0,
                                   key=f"pdv_status_novo_{cli_id}",
                                   help="Prospecto = cliente em prospecção, ainda não compra")
        obs    = st.text_area("Observacao")
        salvar = st.form_submit_button("💾 Salvar PDV", type="primary")

    if salvar:
        if not nome_loja.strip():
            _erro("Nome da loja e obrigatorio."); return
        existe = query("SELECT pdv_id FROM pdv WHERE cliente_id=? AND LOWER(nome_loja)=LOWER(?)",
                       (cli_id, nome_loja.strip()))
        if existe:
            _erro(f"Este cliente ja possui um PDV com o nome '{nome_loja}'."); return
        conn = conectar()
        conn.execute("""
            INSERT INTO pdv
            (cliente_id, numero_loja, nome_loja, tipo_pdv, cnpj, ie,
             endereco, bairro, cidade, estado,
             gerente, fone_gerente, encarregado, fone_encarregado,
             horario_recebimento, setor, cluster, tamanho_pdv, observacao, status, ativo)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,1)
        """, (cli_id, numero or None, nome_loja.strip(), tipo_pdv,
              cnpj or None, None,
              endereco or None, bairro or None, cidade or None, estado,
              gerente or None, fone_gerente or None,
              encarregado or None, fone_encarregado or None,
              horario or None, setor or None,
              cluster if cluster != "—" else None,
              tamanho_pdv if tamanho_pdv != "—" else None,
              obs or None,
              status_pdv))
        conn.commit(); conn.close()
        st.session_state["_pdv_msg_ok"] = f"✅ PDV '{nome_loja}' cadastrado com sucesso!"
        st.rerun()



def _confirmacao_excluir_pdv(pdv_id, pdv_label):
    """Confirmacao antes de excluir um PDV."""
    n_ped  = query("SELECT COUNT(*) FROM pedido    WHERE pdv_id=?", (pdv_id,))[0][0]
    n_vis  = query("SELECT COUNT(*) FROM visita_cliente WHERE pdv_id=?", (pdv_id,))[0][0]
    n_pq   = query("SELECT COUNT(*) FROM pesquisa_preco WHERE pdv_id=?", (pdv_id,))[0][0]
    n_mix  = query("SELECT COUNT(*) FROM mix_cliente WHERE pdv_id=?", (pdv_id,))[0][0]
    n_atp  = query("SELECT COUNT(*) FROM att_promotor WHERE pdv_id=?", (pdv_id,))[0][0]
    n_atv  = query("SELECT COUNT(*) FROM att_vendedor WHERE pdv_id=?", (pdv_id,))[0][0]

    st.warning(f"Excluir PDV **{pdv_label}** (ID {pdv_id})?")

    vinculos = []
    if n_ped:  vinculos.append(f"{n_ped} pedido(s)")
    if n_vis:  vinculos.append(f"{n_vis} visita(s)")
    if n_pq:   vinculos.append(f"{n_pq} pesquisa(s)")
    if n_mix:  vinculos.append(f"{n_mix} item(ns) de mix")
    if n_atp:  vinculos.append(f"{n_atp} atendimento(s) de promotor")
    if n_atv:  vinculos.append(f"{n_atv} atendimento(s) de vendedor")

    if vinculos:
        st.error(
            f"Este PDV possui dados vinculados: {', '.join(vinculos)}. "
            "A exclusao removerá apenas o PDV — os registros historicos "
            "serao mantidos mas ficarao sem PDV associado."
        )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Confirmar exclusao", key=f"conf_del_pdv_{pdv_id}",
                     type="primary", use_container_width=True):
            conn = conectar()
            # Remove vinculos de atendimento
            conn.execute("DELETE FROM att_promotor WHERE pdv_id=?", (pdv_id,))
            conn.execute("DELETE FROM att_vendedor  WHERE pdv_id=?", (pdv_id,))
            conn.execute("DELETE FROM mix_cliente   WHERE pdv_id=?", (pdv_id,))
            # Desvincula (nao exclui) pedidos, visitas e pesquisas
            conn.execute("UPDATE pedido           SET pdv_id=NULL WHERE pdv_id=?", (pdv_id,))
            conn.execute("UPDATE visita_cliente   SET pdv_id=NULL WHERE pdv_id=?", (pdv_id,))
            conn.execute("UPDATE pesquisa_preco   SET pdv_id=NULL WHERE pdv_id=?", (pdv_id,))
            # Exclui o PDV
            conn.execute("DELETE FROM pdv WHERE pdv_id=?", (pdv_id,))
            conn.commit(); conn.close()
            st.session_state.pop("pdv_excluir_id", None)
            st.success(f"PDV '{pdv_label}' excluido com sucesso.")
            st.rerun()
    with col2:
        if st.button("Cancelar", key=f"canc_del_pdv_{pdv_id}",
                     use_container_width=True):
            st.session_state.pop("pdv_excluir_id", None)
            st.rerun()


def _form_editar_pdv(pdv_id):
    TIPOS_PDV = [
            "Supermercado",
            "Hipermercado",
            "Atacadista",
            "Mini Mercado",
            "Mercearia",
            "Emporio",
            "Sacolao",
            "Hortifruti",
            "Acougue",
            "Casa de Carnes",
            "Peixaria",
            "Padaria",
            "Confeitaria",
            "Delicatessen",
            "Hamburgueria",
            "Restaurante",
            "Lanchonete",
            "Bar / Boteco",
            "Clube / Associacao",
            "Outro"
        ]
    conn = conectar()
    p = conn.execute("SELECT * FROM pdv WHERE pdv_id=?", (pdv_id,)).fetchone()
    conn.close()
    if not p: return

    # Indice do tipo atual no selectbox
    tipo_at  = p["tipo_pdv"] if "tipo_pdv" in p.keys() and p["tipo_pdv"] else "Supermercado"
    idx_tipo = TIPOS_PDV.index(tipo_at) if tipo_at in TIPOS_PDV else 0

    with st.form(f"edit_pdv_{pdv_id}"):
        col1, col2 = st.columns(2)
        with col1:
            nome_loja = st.text_input("Nome da loja",    p["nome_loja"]    or "")
            tipo_pdv  = st.selectbox("Tipo de PDV", TIPOS_PDV, index=idx_tipo,
                                     key=f"pdv_tipo_edit_{pdv_id}")
            numero    = st.text_input("Numero da loja",  p["numero_loja"]  or "")
            endereco  = st.text_input("Endereco",        p["endereco"]     or "")
            bairro    = st.text_input("Bairro",          p["bairro"]       or "")
            cidade    = st.text_input("Cidade",          p["cidade"]       or "")
            ufs = _ufs()
            idx = ufs.index(p["estado"]) if p["estado"] in ufs else 0
            estado    = st.selectbox("UF", ufs, index=idx,
                                     key=f"pdv_uf_edit_{pdv_id}")
            cnpj      = st.text_input("CNPJ",            p["cnpj"]         or "")
        with col2:
            gerente          = st.text_input("Gerente",              p["gerente"]           or "")
            fone_gerente     = st.text_input("Fone gerente",         p["fone_gerente"]      or "")
            encarregado      = st.text_input("Encarregado / Resp.",  p["encarregado"]       or "")
            fone_encarregado = st.text_input("Fone encarregado",     p["fone_encarregado"]  or "")
            horario          = st.text_input("Horario recebimento",  p["horario_recebimento"] or "")
            setor_at = p["setor"] if "setor" in p.keys() and p["setor"] else ""
            setor       = st.text_input("Setor", value=setor_at,
                                        placeholder="Ex: Setor Centro, Setor Leste",
                                        key=f"pdv_setor_{pdv_id}",
                                        help="Setor geografico para planejamento de roteiro")
            _cl_opts = ["A/B","B/C","C/D","A","B","C","D","—"]
            _tm_opts = ["GG","G","M","P","PP","—"]
            _cl_at   = p["cluster"]     if "cluster"     in p.keys() and p["cluster"]     else "—"
            _tm_at   = p["tamanho_pdv"] if "tamanho_pdv" in p.keys() and p["tamanho_pdv"] else "—"
            cluster     = st.selectbox("Cluster", _cl_opts,
                                       index=_cl_opts.index(_cl_at) if _cl_at in _cl_opts else 0,
                                       key=f"pdv_cluster_{pdv_id}")
            tamanho_pdv = st.selectbox("Tamanho", _tm_opts,
                                       index=_tm_opts.index(_tm_at) if _tm_at in _tm_opts else 0,
                                       key=f"pdv_tamanho_{pdv_id}")
        lat_e  = st.number_input("Latitude GPS", value=float(p["latitude"]  or 0) if p["latitude"]  else 0.0,
                                format="%.6f", key=f"pdv_lat_{pdv_id}",
                                help="Obtenha no Google Maps: pressione o ponto -> copie as coordenadas")
        lng_e  = st.number_input("Longitude GPS", value=float(p["longitude"] or 0) if p["longitude"] else 0.0,
                                 format="%.6f", key=f"pdv_lng_{pdv_id}")
        obs    = st.text_area("Observacao",  p["observacao"] or "")
        status_raw   = p["status"] if "status" in p.keys() else None
        st_pdv       = COALESCE_STATUS(status_raw, STATUS_PDV_OPTS)
        # Se nulo ou invalido, infere pelo campo ativo
        if not st_pdv:
            st_pdv = "Ativo" if p["ativo"] else "Inativo"
        idx_pdv_st   = STATUS_PDV_OPTS.index(st_pdv) if st_pdv in STATUS_PDV_OPTS else 0
        status_pdv_e = st.selectbox("Status", STATUS_PDV_OPTS, index=idx_pdv_st,
                                    key=f"pdv_status_{pdv_id}")
        salvar = st.form_submit_button("Salvar alteracoes", type="primary")

    if salvar:
        conn = conectar()
        conn.execute("""
            UPDATE pdv SET nome_loja=?, tipo_pdv=?, numero_loja=?,
            endereco=?, bairro=?, cidade=?, estado=?, cnpj=?,
            gerente=?, fone_gerente=?, encarregado=?, fone_encarregado=?,
            horario_recebimento=?, setor=?, cluster=?, tamanho_pdv=?,
            latitude=?, longitude=?, observacao=?, status=?, ativo=?
            WHERE pdv_id=?
        """, (nome_loja, tipo_pdv, numero or None,
              endereco or None, bairro or None, cidade or None, estado, cnpj or None,
              gerente or None, fone_gerente or None,
              encarregado or None, fone_encarregado or None,
              horario or None, setor or None,
              cluster if cluster != "—" else None,
              tamanho_pdv if tamanho_pdv != "—" else None,
              lat_e or None, lng_e or None,
              obs or None, status_pdv_e,
              1 if status_pdv_e=="Ativo" else 0, pdv_id))
        conn.commit(); conn.close()
        st.session_state[f"pdv_salvo_{pdv_id}"] = True
        st.rerun()

    if st.session_state.pop(f"pdv_salvo_{pdv_id}", False):
        st.success(f"PDV atualizado com sucesso!")


# ─────────────────────────────────────────────────────
# MIX POR PDV  ← CORREÇÃO DO BUG
# ─────────────────────────────────────────────────────

def _tela_mix_pdv():
    st.subheader("Mix de produtos por PDV")
    st.caption("Define quais produtos cada loja trabalha. Na tela de pedido só aparecem esses produtos.")

    clientes = query("SELECT cliente_id, nome_fantasia FROM cliente WHERE ativo=1 ORDER BY nome_fantasia")
    if not clientes:
        st.info("Cadastre um cliente primeiro."); return

    # Key inclui índice para garantir reset ao trocar de cliente
    cli_sel = st.selectbox("Cliente", clientes, format_func=lambda x: x[1], key="mix_cli")
    cli_id  = cli_sel[0]

    # PDVs buscados do banco com base no cli_id selecionado agora
    pdvs = query("""
        SELECT pdv_id, numero_loja, nome_loja
        FROM pdv WHERE cliente_id=? AND ativo=1
        ORDER BY numero_loja, nome_loja
    """, (cli_id,))

    forns = query("""
        SELECT f.fornecedor_id, f.nome_fantasia FROM cliente_fornecedor cf
        JOIN fornecedor f ON cf.fornecedor_id = f.fornecedor_id
        WHERE cf.cliente_id=? AND cf.ativo=1
    """, (cli_id,))

    if not forns:
        st.warning("Vincule este cliente a pelo menos um fornecedor primeiro."); return

    col1, col2 = st.columns(2)
    with col1:
        pdv_opts = [(None, "— sem PDV (cliente direto)")] + [
            (p[0], f"{p[1]} — {p[2]}") for p in pdvs
        ]
        # KEY INCLUI cli_id: força novo widget quando o cliente muda
        pdv_sel = st.selectbox(
            "PDV / Loja",
            pdv_opts,
            format_func=lambda x: x[1],
            key=f"mix_pdv_{cli_id}"
        )
    with col2:
        # KEY INCLUI cli_id: força novo widget quando o cliente muda
        forn_sel = st.selectbox(
            "Fornecedor",
            forns,
            format_func=lambda x: x[1],
            key=f"mix_forn_{cli_id}"
        )

    pdv_id  = pdv_sel[0]
    forn_id = forn_sel[0]

    # Mix atual
    if pdv_id:
        mix_atual = query("""
            SELECT mc.mix_id, p.codigo_produto, p.descricao_curta, mc.ativo
            FROM mix_cliente mc
            JOIN produto p ON mc.produto_id = p.produto_id
            WHERE mc.cliente_id=? AND mc.fornecedor_id=? AND mc.pdv_id=?
            ORDER BY p.descricao_curta
        """, (cli_id, forn_id, pdv_id))
    else:
        mix_atual = query("""
            SELECT mc.mix_id, p.codigo_produto, p.descricao_curta, mc.ativo
            FROM mix_cliente mc
            JOIN produto p ON mc.produto_id = p.produto_id
            WHERE mc.cliente_id=? AND mc.fornecedor_id=? AND mc.pdv_id IS NULL
            ORDER BY p.descricao_curta
        """, (cli_id, forn_id))

    if mix_atual:
        df_mix = pd.DataFrame(mix_atual, columns=["ID","Código","Descrição","Ativo"])
        df_mix["Ativo"] = df_mix["Ativo"].map({1: "✅", 0: "❌"})
        st.dataframe(df_mix, use_container_width=True, hide_index=True)
        st.caption(f"{len(mix_atual)} produto(s) no mix")
    else:
        st.info("Nenhum produto no mix. Adicione abaixo.")

    st.divider()
    st.subheader("Adicionar produto ao mix")

    produtos = query("""
        SELECT produto_id, codigo_produto, descricao_curta
        FROM produto WHERE fornecedor_id=? AND ativo=1
        ORDER BY descricao_curta
    """, (forn_id,))

    if not produtos:
        st.warning("Nenhum produto cadastrado para este fornecedor."); return

    # KEY DO FORM inclui cli_id + pdv_id + forn_id para evitar conflitos
    with st.form(f"add_mix_{cli_id}_{forn_id}_{pdv_id}", clear_on_submit=True):
        prod_sel = st.selectbox("Produto", produtos, format_func=lambda x: f"{x[1]} — {x[2]}")
        obs_mix  = st.text_input("Observação")
        salvar   = st.form_submit_button("Adicionar ao mix")

    if salvar and prod_sel:
        conn = conectar()
        try:
            conn.execute("""
                INSERT INTO mix_cliente (cliente_id, fornecedor_id, pdv_id, produto_id, observacao, ativo)
                VALUES (?,?,?,?,?,1)
            """, (cli_id, forn_id, pdv_id, prod_sel[0], obs_mix or None))
            conn.commit()
            _sucesso(f"'{prod_sel[2]}' adicionado ao mix!")
            st.rerun()
        except Exception as e:
            _erro("Produto já está no mix." if "UNIQUE" in str(e) else str(e))
        finally:
            conn.close()


# ─────────────────────────────────────────────────────
# CONTATOS DO CLIENTE
# ─────────────────────────────────────────────────────

def _tela_contatos_cliente():
    st.subheader("Contatos por cliente")
    st.caption("Lista todos os clientes — ativos, visitados e prospectos.")

    # Todos os clientes independente de status
    clientes = query("""
        SELECT cliente_id,
               nome_fantasia || ' — ' || COALESCE(status,'Ativo') AS label
        FROM cliente
        ORDER BY nome_fantasia
    """)
    if not clientes:
        st.info("Cadastre um cliente primeiro."); return

    # Filtro por status para facilitar busca
    col_f1, col_f2 = st.columns([2,2])
    with col_f1:
        fil_st_cont = st.selectbox("Filtrar por status",
                                   ["Todos"] + STATUS_CLI_OPTS, key="fil_cont_status")
    with col_f2:
        busca_cont = st.text_input("Buscar por nome", key="fil_cont_nome",
                                   placeholder="Digite parte do nome...")

    # Aplica filtro
    where_c = []
    params_c = []
    if fil_st_cont != "Todos":
        where_c.append("COALESCE(status,'Ativo')=?"); params_c.append(fil_st_cont)
    if busca_cont.strip():
        where_c.append("nome_fantasia LIKE ?"); params_c.append(f"%{busca_cont.strip()}%")
    where_sql_c = ("WHERE " + " AND ".join(where_c)) if where_c else ""

    clientes_fil = query(f"""
        SELECT cliente_id,
               nome_fantasia || ' — ' || COALESCE(status,'Ativo') AS label
        FROM cliente {where_sql_c}
        ORDER BY nome_fantasia
    """, tuple(params_c))

    if not clientes_fil:
        st.info("Nenhum cliente encontrado."); return

    cli_sel = st.selectbox("Cliente", clientes_fil,
                           format_func=lambda x: x[1], key="cc_cli")
    cli_id  = cli_sel[0]

    # Lista contatos existentes
    contatos = query("""
        SELECT contato_cliente_id, nome_contato, departamento,
               COALESCE(fone,'—'), COALESCE(whatsapp,'—'), COALESCE(email,'—'),
               observacao, ativo
        FROM contato_cliente WHERE cliente_id=? AND ativo=1
        ORDER BY nome_contato
    """, (cli_id,))

    if contatos:
        df_cont = pd.DataFrame(contatos,
                               columns=["ID","Nome","Departamento","Fone",
                                        "WhatsApp","E-mail","Obs","Ativo"])

        # Linha por contato com botoes de acao
        st.caption(f"{len(contatos)} contato(s) cadastrado(s)")
        hc = st.columns([2.0, 1.5, 1.5, 1.8, 1.8, 1.8, 0.8])
        for col, txt in zip(hc, ["Nome","Cargo/Depto","Fone","WhatsApp","E-mail","Obs",""]):
            col.markdown(f"<small><b>{txt}</b></small>", unsafe_allow_html=True)

        for ct in contatos:
            cid_ct, nome_ct, depto_ct, fone_ct, wa_ct, email_ct, obs_ct, ativo_ct = ct
            c = st.columns([2.0, 1.5, 1.5, 1.8, 1.8, 1.8, 0.8])
            c[0].write(nome_ct or "—")
            c[1].caption(depto_ct or "—")
            c[2].caption(fone_ct)

            # WhatsApp com link direto
            if wa_ct and wa_ct != "—":
                wa_num = "".join(filter(str.isdigit, wa_ct))
                if not wa_num.startswith("55"): wa_num = "55" + wa_num
                c[3].markdown(f"[📱 {wa_ct}](https://wa.me/{wa_num})")
            else:
                c[3].caption("—")

            # E-mail com link
            if email_ct and email_ct != "—":
                c[4].markdown(f"[✉️ {email_ct}](mailto:{email_ct})")
            else:
                c[4].caption("—")

            c[5].caption(obs_ct or "—")
            with c[6]:
                if st.button("🗑️", key=f"del_ct_{cid_ct}",
                             use_container_width=True, help="Remover contato"):
                    conn = conectar()
                    conn.execute("UPDATE contato_cliente SET ativo=0 WHERE contato_cliente_id=?",
                                 (cid_ct,))
                    conn.commit(); conn.close(); st.rerun()
    else:
        st.info("Nenhum contato cadastrado para este cliente.")

    st.divider()
    st.subheader("Adicionar contato")
    with st.form(f"novo_contato_cli_{cli_id}", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nome  = st.text_input("Nome *")
            depto = st.text_input("Cargo / Departamento",
                                  placeholder="Ex: Comprador, Gerente, Dono")
            fone  = st.text_input("Fone", placeholder="Ex: 1399887766")
        with col2:
            whatsapp = st.text_input("WhatsApp",
                                     placeholder="Ex: 13988776655",
                                     help="Numero com DDD — sera usado para envio direto")
            email = st.text_input("E-mail")
            obs   = st.text_input("Observacao")
        salvar = st.form_submit_button("Adicionar contato", type="primary")

    if salvar:
        if not nome.strip():
            _erro("Nome e obrigatorio."); return
        conn = conectar()
        conn.execute("""
            INSERT INTO contato_cliente
            (cliente_id, nome_contato, departamento, fone, whatsapp, email, observacao, ativo)
            VALUES (?,?,?,?,?,?,?,1)
        """, (cli_id, nome.strip(), depto or None,
              fone or None, whatsapp or None, email or None, obs or None))
        conn.commit(); conn.close()
        _sucesso(f"Contato '{nome}' adicionado!")
        st.rerun()


# ═══════════════════════════════════════════════════════
# ASSOCIACOES DE COMPRAS
# ═══════════════════════════════════════════════════════

def _tela_associacoes():
    st.subheader("Associacoes de compras")
    st.caption("Redes e centrais de compras — agrupa clientes que negociam em conjunto (ex: Rede Litoral).")

    assocs = query("""
        SELECT a.associacao_id, a.nome, a.tipo, a.cidade, a.estado,
               a.fone, a.contato, a.ativo,
               COUNT(c.cliente_id) AS membros
        FROM associacao a
        LEFT JOIN cliente c ON c.associacao_id=a.associacao_id AND c.ativo=1
        GROUP BY a.associacao_id ORDER BY a.nome
    """)

    if assocs:
        df = pd.DataFrame(assocs, columns=["ID","Nome","Tipo","Cidade","UF",
                                            "Fone","Contato","Ativo","Membros"])
        df["Ativo"] = df["Ativo"].map({1:"Sim",0:"Nao"})
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Seleciona para ver membros
        opts = [(a[0], f"{a[1]} ({a[8]} membro(s))") for a in assocs]
        sel  = st.selectbox("Ver membros de", opts, format_func=lambda x: x[1],
                            key="assoc_sel")
        if sel:
            membros = query("""SELECT c.cliente_id, c.nome_fantasia, c.cidade, c.status
                FROM cliente c WHERE c.associacao_id=? AND c.ativo=1
                ORDER BY c.nome_fantasia""", (sel[0],))
            if membros:
                st.dataframe(pd.DataFrame(membros,
                    columns=["ID","Cliente","Cidade","Status"]),
                    use_container_width=True, hide_index=True)
            else:
                st.info("Nenhum membro cadastrado ainda.")
    else:
        st.info("Nenhuma associacao cadastrada ainda.")

    st.divider()
    st.subheader("Nova associacao")
    with st.form("nova_assoc", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nome_a  = st.text_input("Nome da associacao *",
                                    placeholder="Ex: Rede Litoral")
            tipo_a  = st.selectbox("Tipo", ["Associacao de compras","Rede voluntaria",
                                            "Cooperativa","Franquia","Outro"])
            contato = st.text_input("Nome do contato")
            fone_a  = st.text_input("Fone")
        with col2:
            cidade_a = st.text_input("Cidade sede")
            estado_a = st.selectbox("UF", _ufs(), key="assoc_uf")
            email_a  = st.text_input("E-mail")
        obs_a  = st.text_input("Observacao")
        salvar = st.form_submit_button("Salvar associacao", type="primary")

    if salvar:
        if not nome_a.strip():
            _erro("Nome e obrigatorio."); return
        conn = conectar()
        conn.execute("""INSERT INTO associacao
            (nome, tipo, cidade, estado, fone, email, contato, observacao, ativo)
            VALUES (?,?,?,?,?,?,?,?,1)""",
            (nome_a.strip(), tipo_a, cidade_a or None, estado_a,
             fone_a or None, email_a or None, contato or None, obs_a or None))
        conn.commit(); conn.close()
        _sucesso(f"Associacao '{nome_a}' cadastrada!")
        st.rerun()


# ═══════════════════════════════════════════════════════
# IMPORTACAO DE CLIENTES E PDVs VIA EXCEL
# ═══════════════════════════════════════════════════════

def _tela_importar_clientes_pdvs():
    st.subheader("Importacao em massa — Clientes e PDVs")

    ABAS_IMP = {"cli":"Importar Clientes","pdv":"Importar PDVs",
                "gps":"Atualizar GPS","ia":"Setores (IA)"}
    if "imp_aba" not in st.session_state: st.session_state["imp_aba"] = "cli"
    cols = st.columns(4)
    for col,(k,v) in zip(cols, ABAS_IMP.items()):
        ativa = st.session_state["imp_aba"] == k
        if col.button(v, key=f"impnav_{k}", use_container_width=True,
                      type="primary" if ativa else "secondary"):
            st.session_state["imp_aba"] = k; st.rerun()
    st.divider()
    a = st.session_state["imp_aba"]
    if a=="cli":  _importar_clientes_excel()
    elif a=="pdv":_importar_pdvs_excel()
    elif a=="gps":_atualizar_gps_massa()
    elif a=="ia": _tela_sugestao_setores_ia()


def _baixar_templates():
    st.markdown("### Templates Excel para importacao")
    st.caption("Baixe, preencha e importe. Campos com * sao obrigatorios.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Template de Clientes**")
        st.caption("Colunas: nome_fantasia*, razao_social, perfil, status, fone, email, cnpj, "
                   "endereco, bairro, cidade, estado, site, instagram, associacao_nome, observacao")
        df_cli = pd.DataFrame([{
            "nome_fantasia":   "Empório Exemplo",
            "razao_social":    "",
            "perfil":          "Empório",
            "status":          "Ativo",
            "fone":            "13988776655",
            "email":           "compras@emporio.com.br",
            "cnpj":            "",
            "endereco":        "Av. Ana Costa 123",
            "bairro":          "Gonzaga",
            "cidade":          "Santos",
            "estado":          "SP",
            "site":            "",
            "instagram":       "@emporio_exemplo",
            "associacao_nome": "",
            "observacao":      "",
        }])
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as w:
            df_cli.to_excel(w, index=False, sheet_name="Clientes")
        st.download_button("⬇️ Baixar template Clientes", data=buf.getvalue(),
                           file_name="template_importacao_clientes.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           use_container_width=True, key="tpl_cli_dl_old")

    with col2:
        st.markdown("**Template de PDVs**")
        st.caption("Colunas: cliente_nome*, numero_loja, nome_loja*, tipo_pdv, setor, endereco, bairro, "
                   "cidade, estado, gerente, fone_gerente, horario_recebimento, "
                   "latitude, longitude, observacao")
        df_pdv = pd.DataFrame([{
            "cliente_nome":        "Supermercado Exemplo",
            "numero_loja":         "01",
            "nome_loja":           "Loja Centro",
            "tipo_pdv":            "Supermercado",
            "setor":               "Setor Centro",
            "endereco":            "Rua XV de Novembro 100",
            "bairro":              "Centro",
            "cidade":              "Santos",
            "estado":              "SP",
            "cnpj":                "",
            "gerente":             "Joao Silva",
            "fone_gerente":        "13977665544",
            "horario_recebimento": "Seg-Sex 08h-17h",
            "status":              "Ativo",
            "latitude":            "",
            "longitude":           "",
            "observacao":          "",
        }])
        _buf_pdv_old = io.BytesIO()
        with pd.ExcelWriter(_buf_pdv_old, engine="openpyxl") as _w:
            df_pdv.to_excel(_w, index=False, sheet_name="PDVs")
        st.download_button("⬇️ Baixar template PDVs", data=_buf_pdv_old.getvalue(),
                           file_name="template_importacao_pdvs.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           use_container_width=True, key="tpl_pdv_dl_old")


def _importar_clientes_excel():
    st.subheader("Importar clientes via Excel")

    # Template direto — sem expander para 1 clique
    _df_tpl_cli = pd.DataFrame([{
        "nome_fantasia": "Empório Exemplo", "razao_social": "",
        "perfil": "Empório", "status": "Ativo",
        "fone": "13988776655", "email": "compras@emporio.com.br",
        "cnpj": "", "endereco": "Av. Ana Costa 123", "bairro": "Gonzaga",
        "cidade": "Santos", "estado": "SP", "site": "",
        "instagram": "@emporio_exemplo", "associacao_nome": "", "observacao": "",
    }])
    _buf_tpl_cli = io.BytesIO()
    with pd.ExcelWriter(_buf_tpl_cli, engine='openpyxl') as _w:
        _df_tpl_cli.to_excel(_w, index=False, sheet_name="Clientes")
    st.download_button("📥 Baixar template de Clientes", data=_buf_tpl_cli.getvalue(),
                       file_name="template_importacao_clientes.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                       key="tpl_cli_dl_imp")
    st.caption("Campos obrigatórios: nome_fantasia. Perfil: Empório, Supermercado, Padaria, etc.")

    resultado = st.session_state.pop("imp_cli_resultado", None)
    if resultado:
        st.success(f"Importacao concluida: **{resultado['ok']} cliente(s)** cadastrado(s).")
        if resultado['atualizados']:
            st.info(f"{resultado['atualizados']} cliente(s) ja existiam e foram atualizados.")
        if resultado['erros']:
            st.warning(f"{len(resultado['erros'])} erro(s):")
            for e in resultado['erros'][:20]: st.caption(e)
        return

    arquivo = st.file_uploader("Selecione o arquivo Excel de clientes",
                               type=["xlsx","xls"], key="up_cli")
    if not arquivo: return

    try:
        df = pd.read_excel(arquivo, dtype=str)
        df.columns = (df.columns.str.strip().str.lower()
                      .str.replace(" ","_").str.replace("*",""))
        df = df.where(pd.notnull(df), None)
        st.caption(f"Preview — {len(df)} linha(s):")
        st.dataframe(df.head(10), use_container_width=True)
    except Exception as e:
        _erro(f"Erro ao ler arquivo: {e}"); return

    opcao = st.radio("Se o cliente ja existir:", ["Pular","Atualizar"], key="imp_cli_op")
    if st.button("Confirmar importacao", type="primary", key="btn_imp_cli"):
        conn = conectar()
        ok = 0; atualizados = 0; erros = []
        assocs_cache = {a[1].lower(): a[0] for a in
                        (conn.execute("SELECT associacao_id, nome FROM associacao").fetchall() or [])}

        for idx, row in df.iterrows():
            try:
                fantasia = (row.get("nome_fantasia") or "").strip()
                if not fantasia:
                    erros.append(f"Linha {idx+2}: nome_fantasia vazio."); continue

                assoc_id = None
                assoc_nome = (row.get("associacao_nome") or "").strip().lower()
                if assoc_nome:
                    assoc_id = assocs_cache.get(assoc_nome)
                    if not assoc_id:
                        erros.append(f"Linha {idx+2}: associacao '{assoc_nome}' nao encontrada.")

                existe = conn.execute(
                    "SELECT cliente_id FROM cliente WHERE LOWER(nome_fantasia)=LOWER(?)",
                    (fantasia,)).fetchone()

                if existe:
                    if opcao == "Atualizar":
                        conn.execute("""UPDATE cliente SET
                            perfil=COALESCE(?,perfil), fone=COALESCE(?,fone),
                            cidade=COALESCE(?,cidade), estado=COALESCE(?,estado),
                            bairro=COALESCE(?,bairro), endereco=COALESCE(?,endereco),
                            cnpj=COALESCE(?,cnpj), site=COALESCE(?,site),
                            instagram=COALESCE(?,instagram),
                            associacao_id=COALESCE(?,associacao_id),
                            observacao=COALESCE(?,observacao)
                            WHERE cliente_id=?""",
                            (row.get("perfil"), row.get("fone"),
                             row.get("cidade"), row.get("estado") or "SP",
                             row.get("bairro"), row.get("endereco"),
                             row.get("cnpj"), row.get("site"),
                             row.get("instagram"), assoc_id,
                             row.get("observacao"), existe[0]))
                        atualizados += 1
                else:
                    # Status da importacao: usa coluna "status" do Excel
                    # se nao informado, padrao e Prospecto
                    status_imp = (row.get("status") or "Prospecto").strip()
                    if status_imp not in STATUS_CLI_OPTS:
                        status_imp = "Prospecto"
                    ativo_imp  = 1 if status_imp == "Ativo" else 0
                    conn.execute("""INSERT INTO cliente
                        (nome_fantasia, perfil, fone, cidade, estado, bairro,
                         endereco, cnpj, site, instagram, associacao_id,
                         observacao, status, ativo)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                        (fantasia,
                         row.get("perfil"), row.get("fone"),
                         row.get("cidade"), row.get("estado") or "SP",
                         row.get("bairro"), row.get("endereco"),
                         row.get("cnpj"), row.get("site"),
                         row.get("instagram"), assoc_id, row.get("observacao"),
                         status_imp, ativo_imp))
                    ok += 1
            except Exception as e:
                erros.append(f"Linha {idx+2}: {e}")

        conn.commit(); conn.close()
        st.session_state["imp_cli_resultado"] = {
            "ok": ok, "atualizados": atualizados, "erros": erros}
        st.rerun()


def _importar_pdvs_excel():
    st.subheader("Importar PDVs via Excel")
    st.info("O cliente ja deve estar cadastrado. Use o nome_fantasia exatamente como cadastrado.")

    # Template direto — sem expander para 1 clique
    _df_tpl_pdv = pd.DataFrame([{
        "cliente_nome": "Supermercado Exemplo", "numero_loja": "01",
        "nome_loja": "Loja Centro", "tipo_pdv": "Supermercado",
        "setor": "Setor Centro", "endereco": "Rua XV de Novembro 100",
        "bairro": "Centro", "cidade": "Santos", "estado": "SP",
        "cnpj": "", "gerente": "Joao Silva", "fone_gerente": "13977665544",
        "horario_recebimento": "Seg-Sex 08h-17h", "status": "Ativo",
        "latitude": "", "longitude": "", "observacao": "",
    }])
    _buf_tpl_pdv = io.BytesIO()
    with pd.ExcelWriter(_buf_tpl_pdv, engine='openpyxl') as _w:
        _df_tpl_pdv.to_excel(_w, index=False, sheet_name="PDVs")
    st.download_button("📥 Baixar template de PDVs", data=_buf_tpl_pdv.getvalue(),
                       file_name="template_importacao_pdvs.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                       key="tpl_pdv_dl_imp")
    st.caption("Campos obrigatórios: cliente_nome, nome_loja.")

    resultado = st.session_state.pop("imp_pdv_resultado", None)
    if resultado:
        st.success(f"Importacao concluida: **{resultado['ok']} PDV(s)** cadastrado(s).")
        if resultado['atualizados']:
            st.info(f"{resultado['atualizados']} PDV(s) ja existiam e foram atualizados.")
        if resultado['erros']:
            st.warning(f"{len(resultado['erros'])} erro(s):")
            for e in resultado['erros'][:20]: st.caption(e)
        return

    arquivo = st.file_uploader("Selecione o arquivo Excel de PDVs",
                               type=["xlsx","xls"], key="up_pdv")
    if not arquivo: return

    try:
        df = pd.read_excel(arquivo, dtype=str)
        df.columns = (df.columns.str.strip().str.lower()
                      .str.replace(" ","_").str.replace("*",""))
        df = df.where(pd.notnull(df), None)
        st.caption(f"Preview — {len(df)} linha(s):")
        st.dataframe(df.head(10), use_container_width=True)
    except Exception as e:
        _erro(f"Erro ao ler arquivo: {e}"); return

    opcao = st.radio("Se o PDV ja existir (mesmo cliente + mesmo nome):",
                     ["Pular","Atualizar"], key="imp_pdv_op")
    if st.button("Confirmar importacao", type="primary", key="btn_imp_pdv"):
        conn = conectar()
        ok = 0; atualizados = 0; erros = []

        for idx, row in df.iterrows():
            try:
                cli_nome  = (row.get("cliente_nome") or "").strip()
                nome_loja = (row.get("nome_loja") or "").strip()
                if not cli_nome or not nome_loja:
                    erros.append(f"Linha {idx+2}: cliente_nome e nome_loja sao obrigatorios."); continue

                cli = conn.execute(
                    "SELECT cliente_id FROM cliente WHERE LOWER(nome_fantasia)=LOWER(?)",
                    (cli_nome,)).fetchone()
                if not cli:
                    erros.append(f"Linha {idx+2}: cliente '{cli_nome}' nao encontrado."); continue
                cli_id = cli[0]

                existe = conn.execute(
                    "SELECT pdv_id FROM pdv WHERE cliente_id=? AND LOWER(nome_loja)=LOWER(?)",
                    (cli_id, nome_loja)).fetchone()

                # Converte lat/lng
                def _parse_float(v):
                    try:
                        if not v or str(v).strip() == "": return None
                        s = str(v).strip().replace(",",".")
                        return float(s)
                    except: return None

                campos = {
                    "numero_loja":        row.get("numero_loja"),
                    "tipo_pdv":           row.get("tipo_pdv"),
                    "setor":              row.get("setor"),
                    "endereco":           row.get("endereco"),
                    "bairro":             row.get("bairro"),
                    "cidade":             row.get("cidade"),
                    "estado":             row.get("estado") or "SP",
                    "gerente":            row.get("gerente"),
                    "fone_gerente":       row.get("fone_gerente"),
                    "horario_recebimento":row.get("horario_recebimento"),
                    "latitude":           _parse_float(row.get("latitude")),
                    "longitude":          _parse_float(row.get("longitude")),
                    "observacao":         row.get("observacao"),
                }

                if existe:
                    if opcao == "Atualizar":
                        status_pdv_upd = (row.get("status") or "").strip()
                        if status_pdv_upd not in STATUS_PDV_OPTS:
                            status_pdv_upd = None  # mantem o existente
                        conn.execute("""UPDATE pdv SET
                            numero_loja=COALESCE(?,numero_loja),
                            tipo_pdv=COALESCE(?,tipo_pdv),
                            setor=COALESCE(?,setor),
                            endereco=COALESCE(?,endereco),
                            bairro=COALESCE(?,bairro), cidade=COALESCE(?,cidade),
                            estado=COALESCE(?,estado), gerente=COALESCE(?,gerente),
                            fone_gerente=COALESCE(?,fone_gerente),
                            horario_recebimento=COALESCE(?,horario_recebimento),
                            latitude=COALESCE(?,latitude), longitude=COALESCE(?,longitude),
                            observacao=COALESCE(?,observacao),
                            status=COALESCE(?,status),
                            ativo=CASE WHEN ?='Ativo' THEN 1 ELSE ativo END
                            WHERE pdv_id=?""",
                            (*campos.values(), status_pdv_upd, status_pdv_upd, existe[0]))
                        atualizados += 1
                else:
                    # Status do PDV importado
                    status_pdv_imp = (row.get("status") or "Prospecto").strip()
                    if status_pdv_imp not in STATUS_PDV_OPTS:
                        status_pdv_imp = "Prospecto"
                    ativo_pdv_imp  = 1 if status_pdv_imp == "Ativo" else 0
                    conn.execute("""INSERT INTO pdv
                        (cliente_id, numero_loja, nome_loja, tipo_pdv, setor,
                         endereco, bairro, cidade, estado,
                         gerente, fone_gerente, horario_recebimento,
                         latitude, longitude, observacao, status, ativo)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                        (cli_id, campos["numero_loja"] or None, nome_loja,
                         campos["tipo_pdv"], campos["setor"],
                         campos["endereco"], campos["bairro"],
                         campos["cidade"], campos["estado"],
                         campos["gerente"], campos["fone_gerente"],
                         campos["horario_recebimento"],
                         campos["latitude"], campos["longitude"],
                         campos["observacao"],
                         status_pdv_imp, ativo_pdv_imp))
                    ok += 1
            except Exception as e:
                erros.append(f"Linha {idx+2}: {e}")

        conn.commit(); conn.close()
        st.session_state["imp_pdv_resultado"] = {
            "ok": ok, "atualizados": atualizados, "erros": erros}
        st.rerun()


# ═══════════════════════════════════════════════════════
# SUGESTAO DE SETORES POR IA
# ═══════════════════════════════════════════════════════

def _tela_sugestao_setores_ia():
    st.subheader("Sugestao de Setores por Inteligencia Artificial")

    # Passo a passo visual
    st.info(
        "**Como usar — passo a passo:**\n\n"
        "1️⃣  Baixe o template abaixo e preencha seus PDVs (cliente_nome, nome_loja, "
        "bairro, cidade — a coluna *setor* pode ficar em branco)\n\n"
        "2️⃣  Suba o arquivo preenchido no campo de upload abaixo\n\n"
        "3️⃣  Escolha quantos setores deseja e clique em **Analisar com IA**\n\n"
        "4️⃣  Revise e ajuste os setores sugeridos na tabela editavel\n\n"
        "5️⃣  Baixe o Excel com setor preenchido e importe na aba **Importar PDVs**"
    )

    # Template para download — direto nesta tela
    st.markdown("**Passo 1 — Baixe e preencha o template:**")
    df_tpl_ia = pd.DataFrame([
        {
            "cliente_nome":        "Supermercado Exemplo",
            "numero_loja":         "01",
            "nome_loja":           "Loja Centro",
            "tipo_pdv":            "Supermercado",
            "setor":               "",
            "endereco":            "Rua XV de Novembro 100",
            "bairro":              "Centro",
            "cidade":              "Santos",
            "estado":              "SP",
            "gerente":             "",
            "fone_gerente":        "",
            "horario_recebimento": "",
            "latitude":            "",
            "longitude":           "",
            "observacao":          "",
        },
        {
            "cliente_nome":        "Emporio Exemplo",
            "numero_loja":         "",
            "nome_loja":           "Loja Gonzaga",
            "tipo_pdv":            "Emporio",
            "setor":               "",
            "endereco":            "Av. Ana Costa 500",
            "bairro":              "Gonzaga",
            "cidade":              "Santos",
            "estado":              "SP",
            "gerente":             "",
            "fone_gerente":        "",
            "horario_recebimento": "",
            "latitude":            "",
            "longitude":           "",
            "observacao":          "",
        },
    ])
    buf_tpl = io.BytesIO()
    df_tpl_ia.to_excel(buf_tpl, index=False, sheet_name="PDVs")
    buf_tpl.seek(0)
    st.download_button(
        "⬇️ Baixar template de PDVs para sugestao de setores",
        data=buf_tpl,
        file_name="template_pdvs_para_setores.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=False,
    )
    st.caption(
        "Colunas obrigatorias: **cliente_nome** e **nome_loja**. "
        "Quanto mais informacoes de bairro e cidade, melhor a sugestao da IA. "
        "Deixe a coluna **setor** em branco — a IA vai preencher."
    )

    st.divider()
    st.markdown("**Passo 2 — Suba o arquivo preenchido:**")
    arquivo = st.file_uploader(
        "Selecione sua planilha de PDVs preenchida",
        type=["xlsx","xls"],
        key="up_ia_setor",
        help="Use o template acima ou qualquer Excel com as colunas: "
             "cliente_nome, nome_loja, bairro, cidade"
    )
    if not arquivo:
        return

    try:
        df_orig = pd.read_excel(arquivo, dtype=str)
        df_orig.columns = (df_orig.columns.str.strip().str.lower()
                           .str.replace(" ","_").str.replace("*",""))
        df_orig = df_orig.where(pd.notnull(df_orig), "")
    except Exception as e:
        st.error(f"Erro ao ler arquivo: {e}"); return

    # Valida colunas minimas
    colunas_ok = [c for c in ["nome_loja","bairro","cidade","endereco"] if c in df_orig.columns]
    if not colunas_ok:
        st.error("Planilha precisa ter ao menos: nome_loja, bairro ou cidade.")
        return

    st.caption(f"{len(df_orig)} PDV(s) carregado(s). Preview:")
    st.dataframe(df_orig.head(10), use_container_width=True, hide_index=True)

    # Parametros
    col1, col2 = st.columns(2)
    with col1:
        n_setores = st.slider(
            "Quantidade de setores desejada",
            min_value=2, max_value=15, value=5,
            help="A IA tentara agrupar os PDVs nesta quantidade de setores"
        )
    with col2:
        prefixo = st.text_input(
            "Prefixo dos setores",
            value="Setor",
            help="Ex: 'Setor' gera Setor 1, Setor 2... ou use 'Zona' para Zona Norte etc."
        )

    # Monta lista para enviar a IA
    linhas_pdv = []
    for i, row in df_orig.iterrows():
        partes = []
        for campo in ["nome_loja","cliente_nome","endereco","bairro","cidade","estado"]:
            v = str(row.get(campo,"")).strip()
            if v: partes.append(v)
        linhas_pdv.append(f"{i+1}. {' | '.join(partes)}")

    lista_txt = "\n".join(linhas_pdv)

    if st.button("Analisar e sugerir setores com IA", type="primary",
                 use_container_width=True, key="btn_ia_setor"):

        # Verifica se a chave de API esta configurada
        # Busca chave direto no banco — sem dependencia de importacao
        _cfg_key = query("SELECT anthropic_api_key FROM configuracao ORDER BY config_id DESC LIMIT 1")
        api_key  = _cfg_key[0][0] if _cfg_key and _cfg_key[0][0] else None
        if not api_key:
            st.error(
                "Chave de API Anthropic nao configurada.\n\n"
                "Va em **⚙️ Configurações** (botao no topo direito do menu principal) → "
                "preencha o campo **Chave de API Anthropic** → Salvar.\n\n"
                "Obtenha sua chave gratuita em: https://console.anthropic.com/settings/keys"
            )
            st.stop()

        with st.spinner("A IA esta analisando os PDVs e sugerindo setores..."):
            import json, requests

            prompt = f"""Voce e um especialista em logistica e rotas de vendas no Brasil.

Analise a lista de {len(df_orig)} pontos de venda (PDVs) abaixo e agrupe-os em exatamente {n_setores} setores geograficos.

Criterios de agrupamento:
- Proximidade geografica (bairros e cidades proximos devem ficar no mesmo setor)
- Equilibrio de PDVs por setor (tente distribuir de forma homogenea)
- Logica de roteiro (setores devem fazer sentido como rota de visitas)
- Use o prefixo "{prefixo}" nos nomes dos setores

Lista de PDVs:
{lista_txt}

Responda SOMENTE com um JSON valido, sem explicacoes, sem markdown, sem ```json.
Formato exato:
{{
  "setores": [
    {{
      "nome": "{prefixo} Centro",
      "criterio": "Bairros centrais de Santos",
      "pdvs": [1, 3, 7, 12]
    }}
  ]
}}

Onde "pdvs" sao os numeros de linha (1 a {len(df_orig)}) de cada PDV naquele setor.
Certifique-se de que todo PDV apareca em exatamente um setor.
"""

            try:
                resp = requests.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "Content-Type":    "application/json",
                        "x-api-key":       api_key,
                        "anthropic-version": "2023-06-01",
                    },
                    json={
                        "model":      "claude-sonnet-4-20250514",
                        "max_tokens": 2000,
                        "messages":   [{"role": "user", "content": prompt}]
                    },
                    timeout=60
                )
                resp.raise_for_status()
                data = resp.json()
                txt  = "".join(b["text"] for b in data.get("content",[]) if b.get("type")=="text")

                # Remove possiveis backticks
                txt = txt.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
                resultado = json.loads(txt)
                st.session_state["ia_setores_resultado"] = resultado
                st.session_state["ia_setores_df_orig"]   = df_orig
                st.rerun()

            except json.JSONDecodeError as e:
                st.error(f"IA retornou resposta invalida. Tente novamente. Detalhe: {e}")
                st.code(txt[:500])
            except Exception as e:
                st.error(f"Erro ao chamar a IA: {e}")

    # Exibe resultado
    resultado = st.session_state.get("ia_setores_resultado")
    df_base   = st.session_state.get("ia_setores_df_orig")

    if not resultado or df_base is None:
        return

    st.divider()
    st.subheader("Resultado da IA — revise e ajuste")

    setores_ia = resultado.get("setores", [])
    nomes_setores = [s["nome"] for s in setores_ia]

    # Monta df com setor sugerido
    setor_por_linha = {}
    for setor in setores_ia:
        for idx in setor.get("pdvs", []):
            setor_por_linha[idx] = setor["nome"]

    # Verifica PDVs nao alocados
    nao_alocados = [i+1 for i in range(len(df_base)) if (i+1) not in setor_por_linha]
    if nao_alocados:
        st.warning(f"PDVs nao alocados pela IA: linhas {nao_alocados}. Serao colocados em 'Sem setor'.")

    df_result = df_base.copy()
    df_result["setor_sugerido"] = [
        setor_por_linha.get(i+1, "Sem setor") for i in range(len(df_base))]

    # Resumo por setor
    st.markdown("**Resumo por setor:**")
    for setor in setores_ia:
        qtd   = len(setor.get("pdvs", []))
        crit  = setor.get("criterio","")
        col_a, col_b = st.columns([1,3])
        col_a.metric(setor["nome"], f"{qtd} PDV(s)")
        col_b.caption(crit)

    st.divider()
    st.markdown("**Edite o setor de cada PDV se necessario:**")
    st.caption("Clique na celula da coluna 'setor_sugerido' para alterar.")

    # Editor interativo
    opcoes_setor = nomes_setores + ["Sem setor"]
    df_edit = df_result.copy()

    # Seleciona colunas relevantes para exibir
    cols_exibir = [c for c in ["cliente_nome","nome_loja","bairro","cidade","setor_sugerido"]
                   if c in df_edit.columns]
    if "setor_sugerido" not in cols_exibir:
        cols_exibir.append("setor_sugerido")

    df_editado = st.data_editor(
        df_edit[cols_exibir],
        column_config={
            "setor_sugerido": st.column_config.SelectboxColumn(
                "Setor (editavel)",
                options=opcoes_setor,
                required=True,
            )
        },
        use_container_width=True,
        hide_index=False,
        key="editor_setores_ia"
    )

    st.divider()
    st.markdown("**Exportar Excel com setores para importar no app:**")
    st.caption("O arquivo exportado ja tera a coluna 'setor' preenchida e estara no formato correto para importacao.")

    if st.button("Gerar Excel com setores", type="primary",
                 use_container_width=True, key="btn_gerar_excel_setor"):
        # Aplica setor editado no df original completo
        df_final = df_base.copy()
        df_final["setor"] = df_editado["setor_sugerido"].values

        # Garante colunas na ordem do template
        colunas_template = [
            "cliente_nome","numero_loja","nome_loja","tipo_pdv","setor","endereco",
            "bairro","cidade","estado","gerente","fone_gerente",
            "horario_recebimento","latitude","longitude","observacao"
        ]
        for col in colunas_template:
            if col not in df_final.columns:
                df_final[col] = ""

        df_export = df_final[colunas_template]

        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as w:
            df_export.to_excel(w, index=False, sheet_name="PDVs")
        buf.seek(0)

        st.download_button(
            "Baixar Excel com setores preenchidos",
            data=buf,
            file_name="pdvs_com_setores.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
        st.success(
            "Excel gerado! Va ate a aba 'Importar PDVs', suba este arquivo "
            "e clique em 'Confirmar importacao'."
        )


# ═══════════════════════════════════════════════════════
# ATUALIZACAO DE GPS EM MASSA
# ═══════════════════════════════════════════════════════

def _atualizar_gps_massa():
    st.subheader("Atualizar coordenadas GPS em massa")
    st.caption(
        "Suba uma planilha com as colunas **cliente_nome**, **nome_loja**, "
        "**latitude** e **longitude**. "
        "O sistema busca o PDV pelo nome do cliente + nome da loja e atualiza as coordenadas. "
        "Valores negativos como -23.9632 e -46.3917 sao aceitos normalmente."
    )

    # Template GPS
    df_tpl = pd.DataFrame([{
        "cliente_nome": "Supermercado Exemplo",
        "nome_loja":    "Loja Centro",
        "latitude":     -23.9632,
        "longitude":    -46.3917,
    }])
    buf_t = io.BytesIO()
    df_tpl.to_excel(buf_t, index=False, sheet_name="GPS")
    buf_t.seek(0)
    st.download_button("Baixar template GPS", data=buf_t,
                       file_name="template_gps_pdvs.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    st.divider()
    arquivo = st.file_uploader("Selecione sua planilha com coordenadas GPS",
                               type=["xlsx","xls"], key="up_gps")
    if not arquivo:
        return

    try:
        df = pd.read_excel(arquivo)
        df.columns = (df.columns.str.strip().str.lower()
                      .str.replace(" ","_").str.replace("*",""))
    except Exception as e:
        st.error(f"Erro ao ler arquivo: {e}"); return

    # Valida colunas obrigatorias
    faltam = [c for c in ["cliente_nome","nome_loja","latitude","longitude"]
              if c not in df.columns]
    if faltam:
        st.error(f"Colunas ausentes: {', '.join(faltam)}"); return

    st.caption(f"{len(df)} linha(s) carregada(s). Preview:")
    st.dataframe(df.head(10), use_container_width=True)

    if st.button("Atualizar GPS", type="primary",
                 use_container_width=True, key="btn_gps_massa"):
        conn = conectar()
        ok = 0; nao_encontrado = []; erro_coord = []

        for idx, row in df.iterrows():
            cli_nome  = str(row.get("cliente_nome") or "").strip()
            loja_nome = str(row.get("nome_loja")    or "").strip()

            # Parse coordenadas — aceita float, int, string com virgula ou ponto
            def _pf(v):
                try:
                    if v is None or str(v).strip() in ("","nan","None"): return None
                    return float(str(v).strip().replace(",","."))
                except: return None

            lat = _pf(row.get("latitude"))
            lng = _pf(row.get("longitude"))

            if not cli_nome or not loja_nome:
                continue

            if lat is None or lng is None:
                erro_coord.append(f"Linha {idx+2}: coordenadas invalidas "
                                  f"({row.get('latitude')}, {row.get('longitude')})")
                continue

            # Busca PDV pelo cliente + nome da loja (case-insensitive)
            pdv = conn.execute("""
                SELECT pdv.pdv_id FROM pdv
                JOIN cliente c ON pdv.cliente_id=c.cliente_id
                WHERE LOWER(c.nome_fantasia)=LOWER(?)
                  AND LOWER(pdv.nome_loja)=LOWER(?)
                LIMIT 1
            """, (cli_nome, loja_nome)).fetchone()

            if not pdv:
                nao_encontrado.append(f"Linha {idx+2}: '{cli_nome}' / '{loja_nome}'")
                continue

            conn.execute("UPDATE pdv SET latitude=?, longitude=? WHERE pdv_id=?",
                         (lat, lng, pdv[0]))
            ok += 1

        conn.commit(); conn.close()

        # Resultado
        if ok:
            st.success(f"✅ {ok} PDV(s) atualizados com coordenadas GPS!")
        if nao_encontrado:
            st.warning(f"Nao encontrados ({len(nao_encontrado)}):")
            for msg in nao_encontrado[:20]:
                st.caption(msg)
            st.caption("Verifique se o nome do cliente e da loja estao iguais ao cadastro.")
        if erro_coord:
            st.error(f"Coordenadas invalidas ({len(erro_coord)}):")
            for msg in erro_coord[:10]:
                st.caption(msg)


# ═══════════════════════════════════════════════════════
# PDVs POR SETOR
# ═══════════════════════════════════════════════════════

def _tela_pdvs_por_setor():
    st.subheader("PDVs por Setor")
    st.caption("Visualizacao agrupada por setor geografico — ideal para planejamento de campo.")

    # ── Filtros no cabeçalho ─────────────────────────────
    col1, col2, col3 = st.columns([1.5, 1.5, 3])

    with col1:
        cidades_r = query("""
            SELECT DISTINCT cidade FROM pdv
            WHERE cidade IS NOT NULL AND cidade != ''
              AND COALESCE(status,'Ativo') NOT IN ('Inativo','Encerrado','Suspenso')
            ORDER BY cidade""")
        cid_opts = ["Todas"] + [c[0] for c in cidades_r]
        fil_cidade = st.selectbox("Cidade", cid_opts, key="setor_fil_cidade")

    with col2:
        setores_r = query("""
            SELECT DISTINCT setor FROM pdv
            WHERE setor IS NOT NULL AND setor != ''
              AND COALESCE(status,'Ativo') NOT IN ('Inativo','Encerrado','Suspenso')
            ORDER BY setor""")
        setor_opts = ["Todos os setores"] + [s[0] for s in setores_r]
        fil_setor_unico = st.selectbox("Setor", setor_opts, key="setor_fil_setor")

    with col3:
        tipos_r = query("""
            SELECT DISTINCT tipo_pdv FROM pdv
            WHERE tipo_pdv IS NOT NULL AND tipo_pdv != ''
              AND COALESCE(status,'Ativo') NOT IN ('Inativo','Encerrado','Suspenso')
            ORDER BY tipo_pdv""")
        tipos_disp = [t[0] for t in tipos_r if t[0]]
        fil_tipos = st.multiselect(
            "Tipos de PDV (vazio = todos)",
            options=tipos_disp,
            default=[],
            key="setor_fil_tipos_multi",
            help="Selecione um ou mais tipos. Lista, exportacao e rota do Maps refletem apenas os tipos selecionados."
        )

    # ── Monta WHERE ──────────────────────────────────────
    # Inativos, Suspensos e Encerrados NUNCA aparecem
    where_s  = ["COALESCE(p.status,'Ativo') NOT IN ('Inativo','Encerrado','Suspenso')"]
    params_s = []
    if fil_cidade != "Todas":
        where_s.append("p.cidade=?");  params_s.append(fil_cidade)
    if fil_setor_unico != "Todos os setores":
        where_s.append("p.setor=?");   params_s.append(fil_setor_unico)
    if fil_tipos:
        ph = ",".join("?" * len(fil_tipos))
        where_s.append(f"p.tipo_pdv IN ({ph})")
        params_s.extend(fil_tipos)

    pdvs_setor = query(f"""
        SELECT
            COALESCE(p.setor,'— Sem setor')     AS setor,
            c.nome_fantasia                       AS cliente,
            COALESCE(p.numero_loja,'')            AS nr,
            p.nome_loja,
            COALESCE(p.tipo_pdv,'—')             AS tipo,
            COALESCE(p.endereco,'—')             AS endereco,
            COALESCE(p.bairro,'—')               AS bairro,
            COALESCE(p.cidade,'—')               AS cidade,
            COALESCE(p.gerente,'—')              AS gerente,
            COALESCE(p.fone_gerente,'—')         AS fone,
            COALESCE(p.horario_recebimento,'—')  AS horario,
            COALESCE(p.status,'Ativo')           AS status,
            p.latitude,
            p.longitude,
            p.pdv_id,
            COALESCE(p.cluster,'—')              AS cluster,
            COALESCE(p.tamanho_pdv,'—')          AS tamanho
        FROM pdv p
        JOIN cliente c ON p.cliente_id = c.cliente_id
        WHERE {' AND '.join(where_s)}
        ORDER BY setor, c.nome_fantasia, p.nome_loja
    """, tuple(params_s))

    if not pdvs_setor:
        st.info("Nenhum PDV encontrado para os filtros selecionados.")
        return

    # ── Métricas ─────────────────────────────────────────
    setores_unicos = list(dict.fromkeys(r[0] for r in pdvs_setor))
    com_gps_total  = sum(1 for r in pdvs_setor
                         if r[12] and r[13]
                         and str(r[12]).strip() and str(r[13]).strip())

    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("PDVs",    len(pdvs_setor))
    col_m2.metric("Setores", len(setores_unicos))
    col_m3.metric("Com GPS", com_gps_total)
    col_m4.metric("Tipos",   len(set(r[4] for r in pdvs_setor if r[4] and r[4] != "—")))

    if fil_tipos:
        st.info(f"🔍 Filtro ativo: **{', '.join(fil_tipos)}** — lista, exportacao e rotas do mapa refletem apenas estes tipos.")

    # ── Exportação (respeita filtro de tipos) ────────────
    col_ex, col_ep, _ = st.columns([1, 1, 3])
    with col_ex:
        if st.button("⬇️ Excel", key="exp_setor_xlsx", use_container_width=True):
            st.session_state["exp_setor_trigger"] = "excel"
    with col_ep:
        if st.button("⬇️ PDF", key="exp_setor_pdf", use_container_width=True):
            st.session_state["exp_setor_trigger"] = "pdf"

    trigger_setor = st.session_state.pop("exp_setor_trigger", None)
    if trigger_setor:
        COLS_DF = ["Setor","Cliente","Nr.","Nome loja","Tipo","Endereco","Bairro",
                   "Cidade","Gerente","Fone","Horario","Status",
                   "Latitude","Longitude","ID","Cluster","Tamanho"]
        df_s     = pd.DataFrame(pdvs_setor, columns=COLS_DF)
        df_s_exp = df_s.drop(columns=["ID"])
        tipos_slug = "_".join(t[:6].replace(" ","") for t in fil_tipos) if fil_tipos else "todos"

        if trigger_setor == "excel":
            buf_s = io.BytesIO()
            with pd.ExcelWriter(buf_s, engine="openpyxl") as writer:
                df_s_exp.to_excel(writer, index=False, sheet_name="Todos")
                for st_nome in setores_unicos:
                    df_st = df_s_exp[df_s_exp["Setor"] == st_nome]
                    aba   = st_nome[:28].replace("/","_").replace("\\","_")
                    df_st.to_excel(writer, index=False, sheet_name=aba)
            buf_s.seek(0)
            st.download_button("📥 Baixar Excel",
                               data=buf_s,
                               file_name=f"pdvs_setor_{tipos_slug}.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                               use_container_width=True)

        elif trigger_setor == "pdf":
            try:
                from reportlab.lib.pagesizes import landscape, A4
                from reportlab.lib.units    import cm
                from reportlab.lib          import colors
                from reportlab.platypus     import (SimpleDocTemplate, Table,
                                                    TableStyle, Paragraph,
                                                    Spacer, HRFlowable)
                from reportlab.lib.styles   import getSampleStyleSheet, ParagraphStyle
                from reportlab.lib.enums    import TA_CENTER
                from datetime import datetime as _dt

                VERDE  = colors.HexColor("#2d6a4f")
                CINZA  = colors.HexColor("#555555")
                CINZAC = colors.HexColor("#f8f9fa")
                sty    = getSampleStyleSheet()
                s_t = ParagraphStyle("ps_t", parent=sty["Normal"], fontSize=13,
                                     fontName="Helvetica-Bold", textColor=VERDE)
                s_s = ParagraphStyle("ps_s", parent=sty["Normal"], fontSize=8, textColor=CINZA)
                s_h = ParagraphStyle("ps_h", parent=sty["Normal"], fontSize=7,
                                     fontName="Helvetica-Bold", textColor=colors.white)
                s_c = ParagraphStyle("ps_c", parent=sty["Normal"], fontSize=7, leading=9)
                s_r = ParagraphStyle("ps_r", parent=sty["Normal"], fontSize=6,
                                     textColor=CINZA, alignment=TA_CENTER)

                buf_pdf = io.BytesIO()
                # Margens menores para aproveitar a largura
                doc = SimpleDocTemplate(buf_pdf, pagesize=landscape(A4),
                                        leftMargin=0.8*cm, rightMargin=0.8*cm,
                                        topMargin=1*cm, bottomMargin=1*cm)
                el = []
                rep = query("SELECT nome_fantasia FROM representante WHERE ativo=1 LIMIT 1")
                rep_nome  = rep[0][0] if rep else "PepperCRM"
                tipos_txt = ", ".join(fil_tipos) if fil_tipos else "Todos os tipos"
                el.append(Paragraph(f"{rep_nome}  —  PDVs por Setor", s_t))
                el.append(Paragraph(
                    f"Tipos: {tipos_txt}  |  {len(pdvs_setor)} PDV(s)  |  "
                    f"Gerado em {_dt.now().strftime('%d/%m/%Y %H:%M')}", s_s))
                el.append(HRFlowable(width="100%", thickness=2, color=VERDE, spaceAfter=6))

                # Agrupado por setor — sem coluna Setor, com cabeçalho por grupo
                PDF_COLS = ["Cliente","PDV","Tipo","Endereço","Bairro",
                            "Cidade","Gerente","Fone","Clust.","Tam."]
                PDF_IDX  = [1, 3, 4, 5, 6, 7, 8, 9, 15, 16]
                PDF_CW   = [3.5*cm, 3.0*cm, 2.2*cm, 5.0*cm, 2.8*cm,
                            2.5*cm, 2.8*cm, 2.5*cm, 1.2*cm, 1.3*cm]

                s_setor = ParagraphStyle("ps_setor", parent=sty["Normal"], fontSize=9,
                                         fontName="Helvetica-Bold", textColor=colors.white)

                # Agrupa por setor
                from collections import OrderedDict
                grupos = OrderedDict()
                for r in pdvs_setor:
                    s = r[0] or "Sem setor"
                    grupos.setdefault(s, []).append(r)

                for setor_nome, rows_s in grupos.items():
                    # Cabeçalho do setor
                    cab_setor = Table(
                        [[Paragraph(f"📍  {setor_nome}  —  {len(rows_s)} PDV(s)", s_setor)]],
                        colWidths=[sum(PDF_CW)])
                    cab_setor.setStyle(TableStyle([
                        ("BACKGROUND", (0,0), (-1,-1), VERDE),
                        ("TOPPADDING", (0,0), (-1,-1), 5),
                        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
                        ("LEFTPADDING", (0,0), (-1,-1), 6),
                    ]))
                    el.append(cab_setor)

                    # Cabeçalho das colunas
                    rows_tbl = [[Paragraph(c, s_h) for c in PDF_COLS]]
                    for r in rows_s:
                        rows_tbl.append([Paragraph(str(r[i] or "—")[:55], s_c)
                                        for i in PDF_IDX])

                    t_s = Table(rows_tbl, colWidths=PDF_CW, repeatRows=1)
                    t_s.setStyle(TableStyle([
                        ("BACKGROUND",    (0,0), (-1,0),  colors.HexColor("#4a9e6e")),
                        ("TEXTCOLOR",     (0,0), (-1,0),  colors.white),
                        ("FONTSIZE",      (0,0), (-1,-1), 7),
                        ("TOPPADDING",    (0,0), (-1,-1), 3),
                        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
                        ("LEFTPADDING",   (0,0), (-1,-1), 3),
                        ("GRID",          (0,0), (-1,-1), 0.3, colors.HexColor("#cccccc")),
                        ("ROWBACKGROUNDS",(0,1), (-1,-1), [colors.white, CINZAC]),
                        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
                    ]))
                    el.append(t_s)
                    el.append(Spacer(1, 0.4*cm))
                el.append(Spacer(1, 0.3*cm))
                el.append(Paragraph("PepperCRM", s_r))
                doc.build(el)
                st.download_button("📥 Baixar PDF",
                                   data=buf_pdf.getvalue(),
                                   file_name=f"pdvs_setor_{tipos_slug}.pdf",
                                   mime="application/pdf",
                                   use_container_width=True)
            except ImportError:
                st.error("Instale reportlab: pip install reportlab")

    st.divider()

    # ── Lista agrupada por setor ─────────────────────────
    for st_nome in setores_unicos:
        pdvs_s  = [r for r in pdvs_setor if r[0] == st_nome]
        # GPS apenas dos PDVs filtrados por tipo
        com_gps = [(r[12], r[13]) for r in pdvs_s
                   if r[12] and r[13]
                   and str(r[12]).strip() and str(r[13]).strip()]

        label_tipos = f"  |  tipos: {', '.join(fil_tipos)}" if fil_tipos else ""
        with st.expander(
            f"📍 {st_nome}  —  {len(pdvs_s)} PDV(s){label_tipos}"
            + (f"  |  {len(com_gps)} com GPS" if com_gps else ""),
            expanded=True
        ):
            # Cabeçalho
            hc = st.columns([0.4, 1.8, 1.8, 1.1, 0.7, 0.7, 1.3, 1.3, 1.3, 0.5])
            for col, txt in zip(hc, ["Nr.","Cliente","PDV","Tipo",
                                     "Clust.","Tam.","Gerente","Fone","Horario","📍"]):
                col.markdown(f"<small><b>{txt}</b></small>", unsafe_allow_html=True)

            for r in pdvs_s:
                (setor_r, cliente, nr, loja, tipo, end, bairro, cidade,
                 gerente, fone, horario, status, lat, lng, pdv_id,
                 cluster_r, tamanho_r) = r
                c = st.columns([0.4, 1.8, 1.8, 1.1, 0.7, 0.7, 1.3, 1.3, 1.3, 0.5])
                c[0].caption(nr or "—")
                c[1].write(cliente)
                c[2].caption(f"{loja}  {_status_icone(status)}")
                c[3].caption(tipo)
                c[4].caption(cluster_r or "—")
                c[5].caption(tamanho_r or "—")
                c[6].caption(gerente)
                c[7].caption(fone)
                c[8].caption(horario)
                with c[9]:
                    if lat and lng and str(lat).strip() and str(lng).strip():
                        st.markdown(f"[📍](https://www.google.com/maps?q={lat},{lng})")
                    else:
                        st.caption("—")

            # Rota do setor — usa APENAS os PDVs filtrados com GPS
            if len(com_gps) >= 2:
                orig = f"{com_gps[0][0]},{com_gps[0][1]}"
                dest = f"{com_gps[-1][0]},{com_gps[-1][1]}"
                wps  = "/".join(f"{p[0]},{p[1]}" for p in com_gps[1:-1])
                url  = (f"https://www.google.com/maps/dir/{orig}/{wps}/{dest}"
                        if wps else
                        f"https://www.google.com/maps/dir/{orig}/{dest}")
                label_rota = f"🗺️ Rota {st_nome} — {len(com_gps)} pontos"
                if fil_tipos:
                    label_rota += f" ({', '.join(fil_tipos)})"
                st.link_button(label_rota, url)
            elif len(com_gps) == 1:
                st.link_button("📍 Ver no Maps",
                               f"https://www.google.com/maps?q={com_gps[0][0]},{com_gps[0][1]}")
            else:
                st.caption("Sem GPS cadastrado neste filtro.")


# ═══════════════════════════════════════════════════════
# CENTRAL DE COMPRAS
# ═══════════════════════════════════════════════════════

def _tela_central_compras():
    st.subheader("Central de Compras")
    st.caption(
        "Redes e clientes com central de compras propria — onde o pedido e negociado "
        "com um comprador central, mesmo que a entrega seja feita loja a loja ou em CD."
    )

    st.info(
        "**Como funciona:**  \n"
        "🏪 **Loja isolada** — compra e recebe na propria loja (padrao)  \n"
        "🏢 **Central propria** — a rede tem um comprador central; entrega pode ser no "
        "CD ou loja a loja  \n"
        "🤝 **Associacao** — central compartilhada entre varios clientes (ja cadastrada "
        "na aba Associacoes)"
    )

    # Lista centrais existentes
    centrais = query("""
        SELECT cc.central_id, c.nome_fantasia, cc.nome_central,
               cc.tipo_entrega, cc.contato, cc.fone, cc.email,
               cc.cidade_cd, cc.ativo
        FROM central_compras cc
        JOIN cliente c ON cc.cliente_id=c.cliente_id
        ORDER BY c.nome_fantasia
    """)

    if centrais:
        df_cc = pd.DataFrame(centrais,
                             columns=["ID","Cliente","Central","Tipo entrega",
                                      "Contato","Fone","Email","Cidade CD","Ativo"])
        df_cc["Ativo"] = df_cc["Ativo"].map({1:"✅",0:"❌"})
        st.dataframe(df_cc.drop(columns=["ID"]),
                     use_container_width=True, hide_index=True)
    else:
        st.info("Nenhuma central de compras cadastrada ainda.")

    st.divider()
    st.subheader("Cadastrar central de compras")

    clientes_cc = query("""SELECT cliente_id, nome_fantasia || ' (' || COALESCE(status,'Ativo') || ')'
        FROM cliente ORDER BY nome_fantasia""")
    if not clientes_cc:
        st.info("Nenhum cliente cadastrado."); return

    with st.form("nova_central", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            cli_cc   = st.selectbox("Cliente (rede)", clientes_cc,
                                    format_func=lambda x: x[1])
            nome_cc  = st.text_input("Nome da central / comprador",
                                     placeholder="Ex: Central Krill, Compras Rede Litoral")
            contato  = st.text_input("Nome do comprador / contato")
            fone_cc  = st.text_input("Fone / WhatsApp do comprador")
            email_cc = st.text_input("E-mail do comprador")
        with col2:
            tipo_ent = st.selectbox("Tipo de entrega", [
                "Loja a loja",
                "CD (Centro de Distribuicao)",
                "CD + Loja a loja (misto)",
            ], help="Como o fornecedor entrega os pedidos desta rede")
            end_cd   = st.text_input("Endereco do CD (se aplicavel)",
                                     placeholder="Apenas se entrega em CD")
            bairro_cd= st.text_input("Bairro do CD")
            cidade_cd= st.text_input("Cidade do CD")
            estado_cd= st.selectbox("UF do CD", _ufs(), key="cc_uf")
        obs_cc = st.text_input("Observacao")
        salvar = st.form_submit_button("Salvar central de compras", type="primary")

    if salvar:
        if not nome_cc.strip():
            st.error("Nome da central e obrigatorio."); return
        conn = conectar()
        conn.execute("""INSERT INTO central_compras
            (cliente_id, nome_central, tipo_entrega, contato, fone, email,
             endereco_cd, bairro_cd, cidade_cd, estado_cd, observacao, ativo)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,1)""",
            (cli_cc[0], nome_cc.strip(), tipo_ent,
             contato or None, fone_cc or None, email_cc or None,
             end_cd or None, bairro_cd or None, cidade_cd or None, estado_cd,
             obs_cc or None))
        conn.commit(); conn.close()
        st.success(f"Central '{nome_cc}' cadastrada para {cli_cc[1].split(' (')[0]}!")
        st.rerun()

    # Exibe detalhes e permite editar tipo de entrega
    if centrais:
        st.divider()
        st.subheader("Editar central existente")
        opts_cc = [(c[0], f"{c[1]} — {c[2]}") for c in centrais]
        sel_cc  = st.selectbox("Selecione", opts_cc,
                               format_func=lambda x: x[1], key="cc_edit_sel")
        if sel_cc:
            cc = query("SELECT * FROM central_compras WHERE central_id=?",
                       (sel_cc[0],))
            if cc:
                cc = cc[0]
                with st.form(f"edit_cc_{sel_cc[0]}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        nome_e   = st.text_input("Nome central", cc[2] or "")
                        cont_e   = st.text_input("Contato",      cc[10] or "")
                        fone_e   = st.text_input("Fone",         cc[8]  or "")
                        email_e  = st.text_input("Email",        cc[9]  or "")
                    with col2:
                        tipos = ["Loja a loja","CD (Centro de Distribuicao)",
                                 "CD + Loja a loja (misto)"]
                        idx_t = tipos.index(cc[3]) if cc[3] in tipos else 0
                        tipo_e   = st.selectbox("Tipo entrega", tipos, index=idx_t)
                        end_e    = st.text_input("Endereco CD",  cc[4]  or "")
                        cidade_e = st.text_input("Cidade CD",    cc[6]  or "")
                        ativo_e  = st.checkbox("Ativo", value=bool(cc[12]))
                    obs_e = st.text_input("Observacao", cc[11] or "")
                    if st.form_submit_button("Salvar alteracoes", type="primary"):
                        conn = conectar()
                        conn.execute("""UPDATE central_compras SET
                            nome_central=?, tipo_entrega=?, contato=?, fone=?,
                            email=?, endereco_cd=?, cidade_cd=?, observacao=?, ativo=?
                            WHERE central_id=?""",
                            (nome_e, tipo_e, cont_e or None, fone_e or None,
                             email_e or None, end_e or None, cidade_e or None,
                             obs_e or None, int(ativo_e), sel_cc[0]))
                        conn.commit(); conn.close()
                        st.success("Central atualizada!"); st.rerun()


# ═══════════════════════════════════════════════════════
# PDF — LISTA DE PRODUTOS E TABELA DE PRECOS
# ═══════════════════════════════════════════════════════

def _exportar_produtos_pdf(df, filtro_forn="Todos"):
    from reportlab.lib.pagesizes import landscape, A4
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle,
                                    Paragraph, Spacer, HRFlowable, KeepTogether)
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER
    from datetime import datetime as _dt
    import io as _io

    VERDE  = colors.HexColor("#2d6a4f")
    VERDE_L= colors.HexColor("#e8f5e9")
    CINZA  = colors.HexColor("#555555")
    CINZA_C= colors.HexColor("#f8f9fa")

    styles = getSampleStyleSheet()
    s_tit  = ParagraphStyle("t", parent=styles["Normal"], fontSize=14,
                            fontName="Helvetica-Bold", textColor=VERDE)
    s_sub  = ParagraphStyle("s", parent=styles["Normal"], fontSize=8, textColor=CINZA)
    s_cat  = ParagraphStyle("cat", parent=styles["Normal"], fontSize=9,
                            fontName="Helvetica-Bold", textColor=VERDE,
                            spaceBefore=8, spaceAfter=3)
    s_hdr  = ParagraphStyle("h", parent=styles["Normal"], fontSize=7,
                            fontName="Helvetica-Bold", textColor=colors.white)
    s_cel  = ParagraphStyle("c", parent=styles["Normal"], fontSize=7)
    s_rod  = ParagraphStyle("r", parent=styles["Normal"], fontSize=6,
                            textColor=CINZA, alignment=TA_CENTER)

    buf = _io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=landscape(A4),
                            leftMargin=1.2*cm, rightMargin=1.2*cm,
                            topMargin=1.2*cm, bottomMargin=1.2*cm)
    el = []

    rep = query("SELECT nome_fantasia FROM representante WHERE ativo=1 LIMIT 1")
    rep_nome = rep[0][0] if rep else "PepperCRM"

    el.append(Paragraph(f"{rep_nome}  —  Lista de Produtos", s_tit))
    forn_label = filtro_forn if filtro_forn != "Todos" else "Todos os fornecedores"
    el.append(Paragraph(f"Fornecedor: {forn_label}  |  {len(df)} produto(s)  |  "
                        f"Gerado em {_dt.now().strftime('%d/%m/%Y %H:%M')}", s_sub))
    el.append(HRFlowable(width="100%", thickness=2, color=VERDE, spaceAfter=6))

    # Colunas sem Shelf Life
    colunas = ["Fornecedor","Marca","Codigo","Descricao","UM","Un/Cx",
               "Peso un.","Peso cx.","Sub-cat.","Grupo","Validade (d)"]
    cw      = [2.8*cm, 2.5*cm, 1.8*cm, 5.5*cm, 1.0*cm, 1.0*cm,
               1.5*cm, 1.5*cm, 2.0*cm, 2.0*cm, 1.8*cm]
    col_map = {
        "Fornecedor":"Fornecedor","Marca":"Marca","Codigo":"Codigo",
        "Descricao":"Descricao curta","UM":"UM","Un/Cx":"Un/Cx",
        "Peso un.":"Peso un.","Peso cx.":"Peso cx.",
        "Sub-cat.":"Sub-categoria","Grupo":"Grupo","Validade (d)":"Validade (d)"
    }

    header = [Paragraph(c, s_hdr) for c in colunas]

    t_style = TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),  VERDE),
        ("TEXTCOLOR",     (0,0), (-1,0),  colors.white),
        ("FONTSIZE",      (0,0), (-1,-1), 7),
        ("TOPPADDING",    (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ("LEFTPADDING",   (0,0), (-1,-1), 3),
        ("GRID",          (0,0), (-1,-1), 0.3, colors.HexColor("#cccccc")),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [colors.white, CINZA_C]),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ])

    # Agrupa por Categoria
    df_sorted = df.sort_values(["Categoria","Fornecedor","Descricao curta"])
    categorias = df_sorted["Categoria"].fillna("—").unique()

    for cat in categorias:
        df_cat = df_sorted[df_sorted["Categoria"].fillna("—") == cat]
        rows = [header]
        for _, row in df_cat.iterrows():
            linha = [Paragraph(str(row.get(col_map[c], "—") or "—")[:60], s_cel)
                     for c in colunas]
            rows.append(linha)

        t = Table(rows, colWidths=cw, repeatRows=1)
        t.setStyle(t_style)

        bloco = [
            Paragraph(f"▸ {cat}  ({len(df_cat)} produto(s))", s_cat),
            t,
            Spacer(1, 0.3*cm)
        ]
        el.append(KeepTogether(bloco) if len(df_cat) <= 15 else bloco[0])
        if len(df_cat) > 15:
            el.append(t)
            el.append(Spacer(1, 0.3*cm))

    el.append(HRFlowable(width="100%", thickness=0.5,
                         color=colors.HexColor("#cccccc"), spaceAfter=3))
    el.append(Paragraph(f"PepperCRM — {rep_nome}  |  Gerado em "
                        f"{_dt.now().strftime('%d/%m/%Y %H:%M')}", s_rod))

    doc.build(el)
    buf.seek(0)
    return buf.read()  # retorna bytes, não BytesIO


def _exportar_tabela_pdf(df_itens, filtro_forn="Todos"):
    from reportlab.lib.pagesizes import landscape, A4
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle,
                                    Paragraph, Spacer, HRFlowable)
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT
    from datetime import datetime as _dt
    import io as _io

    VERDE  = colors.HexColor("#2d6a4f")
    CINZA  = colors.HexColor("#555555")
    CINZA_C= colors.HexColor("#f8f9fa")

    styles = getSampleStyleSheet()
    s_tit  = ParagraphStyle("t", parent=styles["Normal"], fontSize=14,
                            fontName="Helvetica-Bold", textColor=VERDE)
    s_sub  = ParagraphStyle("s", parent=styles["Normal"], fontSize=8, textColor=CINZA)
    s_hdr  = ParagraphStyle("h", parent=styles["Normal"], fontSize=7,
                            fontName="Helvetica-Bold", textColor=colors.white)
    s_cel  = ParagraphStyle("c", parent=styles["Normal"], fontSize=7)
    s_num  = ParagraphStyle("n", parent=styles["Normal"], fontSize=7,
                            alignment=TA_RIGHT)
    s_rod  = ParagraphStyle("r", parent=styles["Normal"], fontSize=6,
                            textColor=CINZA, alignment=TA_CENTER)

    def brl(v):
        try: return f"R$ {float(v):,.2f}".replace(",","X").replace(".",",").replace("X",".")
        except: return "—"

    buf = _io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=landscape(A4),
                            leftMargin=1.2*cm, rightMargin=1.2*cm,
                            topMargin=1.2*cm, bottomMargin=1.2*cm)
    el = []

    rep = query("SELECT nome_fantasia FROM representante WHERE ativo=1 LIMIT 1")
    rep_nome = rep[0][0] if rep else "PepperCRM"
    forn_label = filtro_forn if filtro_forn != "Todos" else "Todos os fornecedores"

    el.append(Paragraph(f"{rep_nome}  —  Tabela de Precos", s_tit))
    el.append(Paragraph(
        f"Fornecedor: {forn_label}  |  {len(df_itens)} item(ns)  |  "
        f"Gerado em {_dt.now().strftime('%d/%m/%Y %H:%M')}", s_sub))
    el.append(HRFlowable(width="100%", thickness=2, color=VERDE, spaceAfter=6))

    if df_itens.empty:
        el.append(Paragraph("Nenhum item encontrado.", s_sub))
    else:
        colunas = ["Tabela","Codigo","Produto","Sub-cat.","Grupo",
                   "UM","Un/Cx","Peso(kg)","Preco cx.","Preco un.","Preco/kg","Desc.max"]
        cw = [3.5*cm,1.8*cm,4.5*cm,1.8*cm,2.0*cm,
              1.0*cm,1.0*cm,1.5*cm,2.0*cm,2.0*cm,2.0*cm,1.5*cm]
        col_map_t = {
            "Tabela":"Tabela","Codigo":"Codigo","Produto":"Produto",
            "Sub-cat.":"Sub-cat.","Grupo":"Grupo",
            "UM":"UM","Un/Cx":"Un/Cx","Peso(kg)":"Peso un.(kg)",
            "Preco cx.":"Preco cx.(R$)","Preco un.":"Preco un.(R$)",
            "Preco/kg":"Preco/kg(R$)","Desc.max":"Desc.max(%)",
        }
        cols_brl = {"Preco cx.","Preco un.","Preco/kg"}
        header = [Paragraph(c, s_hdr) for c in colunas]
        rows   = [header]
        for _, row in df_itens.iterrows():
            linha = []
            for c in colunas:
                val = str(row.get(col_map_t[c],"") or "—")
                if c in cols_brl:
                    try: val = brl(float(val.replace("R$","").replace(".","").replace(",",".")))
                    except: pass
                    linha.append(Paragraph(val, s_num))
                else:
                    linha.append(Paragraph(val[:50], s_cel))
            rows.append(linha)

        t = Table(rows, colWidths=cw, repeatRows=1)
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,0),  VERDE),
            ("TEXTCOLOR",     (0,0), (-1,0),  colors.white),
            ("FONTSIZE",      (0,0), (-1,-1), 7),
            ("TOPPADDING",    (0,0), (-1,-1), 3),
            ("BOTTOMPADDING", (0,0), (-1,-1), 3),
            ("LEFTPADDING",   (0,0), (-1,-1), 3),
            ("GRID",          (0,0), (-1,-1), 0.3, colors.HexColor("#cccccc")),
            ("ROWBACKGROUNDS",(0,1), (-1,-1), [colors.white, CINZA_C]),
            ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ]))
        el.append(t)

    el.append(Spacer(1, 0.3*cm))
    el.append(Paragraph("PepperCRM", s_rod))
    doc.build(el)
    buf.seek(0)
    return buf


# ═══════════════════════════════════════════════════════
# EXCLUSÃO DE PRODUTOS EM LOTE
# ═══════════════════════════════════════════════════════

def _excluir_produtos_lote():
    st.subheader("⚠️ Exclusão de produtos em lote")

    st.error(
        "**Atenção — operação irreversível.**  \n"
        "Esta função exclui PERMANENTEMENTE todos os produtos de um fornecedor "
        "e em cascata: itens de tabela de preços, mix de PDVs e pesquisas de preço "
        "vinculados a esses produtos.  \n"
        "**Use apenas quando necessário reimportar toda a linha de um fornecedor.**"
    )

    forns = cache_fornecedores()
    if not forns:
        st.info("Nenhum fornecedor cadastrado.")
        return

    col1, col2 = st.columns(2)
    with col1:
        forn_sel = st.selectbox("Fornecedor", forns,
                                format_func=lambda x: x[1],
                                key="excl_lote_forn")
    with col2:
        # Mostra quantos produtos serão afetados
        if forn_sel:
            n_prod = query("SELECT COUNT(*) FROM produto WHERE fornecedor_id=?",
                           (forn_sel[0],))[0][0]
            n_tab  = query("""SELECT COUNT(*) FROM tabela_preco_item tpi
                              JOIN tabela_preco tp ON tpi.tabela_preco_id=tp.tabela_preco_id
                              JOIN produto p ON tpi.produto_id=p.produto_id
                              WHERE p.fornecedor_id=?""", (forn_sel[0],))[0][0]
            n_mix  = query("""SELECT COUNT(*) FROM mix_cliente mc
                              JOIN produto p ON mc.produto_id=p.produto_id
                              WHERE p.fornecedor_id=?""", (forn_sel[0],))[0][0]
            st.metric("Produtos", n_prod)
            st.caption(f"Tabela de preços: {n_tab} item(ns)  |  Mix de PDVs: {n_mix}")

    if not forn_sel or n_prod == 0:
        if forn_sel and n_prod == 0:
            st.info(f"{forn_sel[1]} não possui produtos cadastrados.")
        return

    st.divider()
    st.markdown("**Para confirmar a exclusão, preencha os campos abaixo:**")

    col_s, col_c = st.columns(2)
    with col_s:
        confirma_nome = st.text_input(
            "Digite o nome do fornecedor para confirmar",
            placeholder=forn_sel[1],
            key="excl_confirma_nome"
        )
    with col_c:
        senha_adm = st.text_input(
            "Senha de administrador",
            type="password",
            key="excl_senha",
            help="Senha padrão inicial: EXCLUIR123 — altere em Configurações"
        )

    # Senha fixa — implemente em Configurações futuramente se necessário
    SENHA_CORRETA = "EXCLUIR123"

    nome_ok  = confirma_nome.strip().lower() == forn_sel[1].strip().lower()
    senha_ok = senha_adm == SENHA_CORRETA

    if st.button("🗑️ EXCLUIR TODOS OS PRODUTOS DE " + forn_sel[1].upper(),
                 type="primary",
                 disabled=not (nome_ok and senha_ok),
                 key="btn_excluir_lote"):

        conn = conectar()
        try:
            # 1. Deleta itens de tabela de preços
            ids_prod = [r[0] for r in conn.execute(
                "SELECT produto_id FROM produto WHERE fornecedor_id=?",
                (forn_sel[0],)).fetchall()]

            if ids_prod:
                ph = ",".join("?" * len(ids_prod))
                conn.execute(f"DELETE FROM tabela_preco_item WHERE produto_id IN ({ph})",
                             ids_prod)
                # 2. Deleta mix de PDVs
                conn.execute(f"DELETE FROM mix_cliente WHERE produto_id IN ({ph})",
                             ids_prod)
                # 3. Deleta pesquisa de preço itens
                conn.execute(f"DELETE FROM pesquisa_preco_item WHERE produto_id IN ({ph})",
                             ids_prod)
                # 4. Deleta pedido itens (zera produto_id)
                conn.execute(f"UPDATE pedido_item SET produto_id=NULL WHERE produto_id IN ({ph})",
                             ids_prod)

            # 5. Deleta os produtos
            conn.execute("DELETE FROM produto WHERE fornecedor_id=?", (forn_sel[0],))
            conn.commit()

            st.session_state["excl_lote_resultado"] = {
                "forn": forn_sel[1],
                "n_prod": len(ids_prod),
                "n_tab": n_tab,
                "n_mix": n_mix,
            }
        except Exception as e:
            conn.rollback()
            st.error(f"Erro durante exclusão: {e}")
        finally:
            conn.close()
        st.rerun()

    # Exibe resultado
    res = st.session_state.pop("excl_lote_resultado", None)
    if res:
        st.success(
            f"✅ **{res['n_prod']} produto(s)** de **{res['forn']}** excluídos.  \n"
            f"Tabela de preços: {res['n_tab']} item(ns) removido(s).  \n"
            f"Mix de PDVs: {res['n_mix']} item(ns) removido(s).  \n"
            f"Agora você pode reimportar os produtos e a tabela de preços."
        )

    # Feedback visual para campos incompletos
    if forn_sel and n_prod > 0:
        if not nome_ok and confirma_nome:
            st.warning("O nome digitado não confere com o fornecedor selecionado.")
        if not senha_ok and senha_adm:
            st.warning("Senha incorreta.")
        if nome_ok and senha_ok:
            st.success("✅ Confirmação válida — clique no botão acima para excluir.")