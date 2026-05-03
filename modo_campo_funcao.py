#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
original = src

NOVA_FUNCAO = '''

# ══════════════════════════════════════════════════════════════════════════
# MODO CAMPO — EAN + busca por nome/categoria unificados
# ══════════════════════════════════════════════════════════════════════════

def _coleta_modo_campo(pq_id, forn_id):
    """
    Modo Campo: scanner EAN + busca por nome + navegação por categoria.
    Tudo numa única tela sem troca de abas.
    """
    st.subheader("⚡ Modo Campo")

    # ── Scanner + Campo de busca unificado ────────────────────────────────
    _scan_key = f"scan_ean_{pq_id}"
    _redirect_ean = st.session_state.pop(f"ean_vinc_ok_redirect_{pq_id}", None)

    # Se scanner retornou EAN, injeta no campo
    if _scan_key in st.session_state and st.session_state[_scan_key]:
        st.session_state[f"campo_busca_{pq_id}"] = st.session_state.pop(_scan_key)

    # Se veio de vinculacao, usa o EAN
    if _redirect_ean:
        st.session_state[f"campo_busca_{pq_id}"] = _redirect_ean

    # Scanner de camera — so aparece quando campo vazio
    _busca_atual = st.session_state.get(f"campo_busca_{pq_id}", "").strip()
    if not _busca_atual:
        st.session_state["pq_modo"] = "coleta"
        st.session_state["pq_id_ativo"] = pq_id
        ean_cam = scanner_ean(key_suffix=f"campo_{pq_id}")
        if ean_cam:
            st.session_state[_scan_key] = str(ean_cam)
            st.rerun()

    # Campo de busca unificado (EAN ou nome)
    col_busca, col_btn = st.columns([4, 1])
    with col_busca:
        busca_input = st.text_input(
            "Busca",
            placeholder="EAN (7891...) ou nome do produto",
            key=f"campo_busca_{pq_id}",
            label_visibility="collapsed",
            max_chars=60
        )
    with col_btn:
        buscar = st.button("🔍", key=f"campo_btn_{pq_id}",
                           use_container_width=True)

    busca = busca_input.strip() if busca_input else ""

    if not busca:
        # Sem busca: mostra navegacao por categoria
        _campo_navegacao(pq_id, forn_id)
        return

    # Determina se é EAN (so numeros, 8-14 digitos) ou nome
    _is_ean = busca.replace(" ","").replace("-","").replace(".","").isdigit()
    _ean_limpo = busca.replace(" ","").replace("-","").replace(".","")

    if _is_ean and len(_ean_limpo) in (8, 12, 13, 14):
        # Busca por EAN
        resultado = _lookup_ean_local(_ean_limpo)
        if resultado:
            _coleta_ean_produto_encontrado(pq_id, forn_id, resultado, _ean_limpo)
            return

        st.warning(f"EAN **{_ean_limpo}** não encontrado na base local.")

        # Opcao 1: vincular a concorrente sem EAN
        sem_ean = _lookup_ean_concorrentes_sem_ean(_ean_limpo, forn_id)
        if sem_ean:
            with st.expander(
                f"🔗 É um produto já cadastrado sem EAN? ({len(sem_ean)} disponíveis)",
                expanded=True
            ):
                st.caption("Selecione o produto se este EAN pertence a um concorrente já cadastrado:")
                opts = [(None,"— Não é nenhum destes —")] + \
                       [(s[0], f"{s[2]} — {s[1]}") for s in sem_ean]
                sel_vinc = st.selectbox("Produto cadastrado", opts,
                                        format_func=lambda x: x[1],
                                        key=f"campo_vinc_{pq_id}_{_ean_limpo}")
                if sel_vinc and sel_vinc[0]:
                    if st.button("✅ Vincular EAN e registrar preço",
                                 key=f"campo_vinc_ok_{pq_id}",
                                 type="primary", use_container_width=True):
                        from database import conectar as _con
                        conn = _con()
                        conn.execute(
                            "UPDATE produto_concorrente SET ean_concorrente=? "
                            "WHERE produto_concorrente_id=?",
                            (_ean_limpo, sel_vinc[0]))
                        conn.commit(); conn.close()
                        st.session_state[f"ean_vinc_ok_redirect_{pq_id}"] = _ean_limpo
                        st.success("✅ EAN vinculado!")
                        st.rerun()

        # Opcao 2: Open Food Facts
        st.divider()
        st.markdown("**Ou buscar na base pública:**")
        if st.button("🌐 Buscar na Open Food Facts",
                     key=f"campo_off_{pq_id}", use_container_width=True):
            st.session_state[f"campo_buscar_off_{pq_id}"] = True

        if st.session_state.get(f"campo_buscar_off_{pq_id}"):
            with st.spinner("Consultando Open Food Facts..."):
                off = _lookup_ean_openfoodfacts(_ean_limpo)
            if off:
                st.success(f"Produto encontrado! — {off.get('descricao','')} {off.get('peso','')} {off.get('um','')}")
                _form_cadastro_rapido_ean(pq_id, forn_id, _ean_limpo, off)
            else:
                st.info("Não encontrado no Open Food Facts.")
                _form_cadastro_rapido_ean(pq_id, forn_id, _ean_limpo, None)

        # Opcao 3: cadastro manual
        if not st.session_state.get(f"campo_buscar_off_{pq_id}"):
            with st.expander("✍️ Cadastrar manualmente (sem busca online)"):
                _form_cadastro_rapido_ean(pq_id, forn_id, _ean_limpo, None)

    else:
        # Busca por nome/descricao
        _campo_busca_nome(pq_id, forn_id, busca)


def _campo_busca_nome(pq_id, forn_id, busca):
    """Busca produtos nossos e concorrentes por nome/descricao."""
    from database import query

    termo = f"%{busca}%"

    # Produtos nossos
    nossos = query("""
        SELECT p.produto_id, p.descricao_curta, p.codigo_produto,
               m.nome_marca, p.ean
        FROM produto p
        JOIN marca m ON p.marca_id=m.marca_id
        WHERE p.fornecedor_id=? AND p.ativo=1
          AND (p.descricao LIKE ? OR p.descricao_curta LIKE ?
               OR m.nome_marca LIKE ? OR p.codigo_produto LIKE ?)
        ORDER BY p.descricao_curta
        LIMIT 10
    """, (forn_id, termo, termo, termo, termo))

    # Concorrentes
    concs = query("""
        SELECT pc.produto_concorrente_id, pc.descricao_curta,
               conc.marca_concorrente, pc.ean_concorrente
        FROM produto_concorrente pc
        JOIN concorrente conc ON pc.concorrente_id=conc.concorrente_id
        WHERE conc.fornecedor_id=? AND pc.ativo=1
          AND (pc.descricao LIKE ? OR pc.descricao_curta LIKE ?
               OR conc.marca_concorrente LIKE ?)
        ORDER BY pc.descricao_curta
        LIMIT 10
    """, (forn_id, termo, termo, termo))

    if not nossos and not concs:
        st.info(f"Nenhum produto encontrado para '{busca}'. Verifique o cadastro.")
        return

    if nossos:
        st.markdown("**🟢 Nossos produtos:**")
        for pid, desc, cod, marca, ean in nossos:
            label = f"{marca} — {desc}" + (f" ({cod})" if cod else "")
            if st.button(label, key=f"campo_n_{pq_id}_{pid}",
                        use_container_width=True):
                resultado = {"tipo":"nosso", "produto_id":pid,
                            "descricao":desc, "marca":marca, "ean":ean,
                            "pc_id":None}
                _coleta_ean_produto_encontrado(pq_id, forn_id, resultado,
                                               ean or "")

    if concs:
        st.markdown("**🔴 Concorrentes:**")
        for pc_id, desc, marca, ean in concs:
            label = f"{marca} — {desc}" + (f" | EAN:{ean}" if ean else "")
            if st.button(label, key=f"campo_c_{pq_id}_{pc_id}",
                        use_container_width=True):
                resultado = {"tipo":"conc", "pc_id":pc_id,
                            "descricao":desc, "marca":marca, "ean":ean,
                            "auditavel":1}
                _coleta_ean_produto_encontrado(pq_id, forn_id, resultado,
                                               ean or "")


def _campo_navegacao(pq_id, forn_id):
    """Navegacao por categoria quando campo de busca esta vazio."""
    st.caption("📂 Ou navegue por categoria:")

    cats = query("""
        SELECT DISTINCT cat.categoria_id, cat.nome_categoria
        FROM categoria cat WHERE cat.ativo=1 AND (
            EXISTS (SELECT 1 FROM produto p
                    WHERE p.categoria_id=cat.categoria_id
                    AND p.fornecedor_id=? AND p.ativo=1)
            OR
            EXISTS (SELECT 1 FROM produto_concorrente pc
                    JOIN concorrente c ON pc.concorrente_id=c.concorrente_id
                    WHERE pc.categoria_id=cat.categoria_id
                    AND c.fornecedor_id=? AND pc.ativo=1)
        )
        ORDER BY cat.nome_categoria
    """, (forn_id, forn_id))

    if not cats:
        return

    cat_opts = [(None, "— Selecione uma categoria —")] + list(cats)
    cat_sel = st.selectbox("Categoria", cat_opts,
                           format_func=lambda x: x[1],
                           key=f"campo_cat_{pq_id}")
    if not cat_sel or not cat_sel[0]:
        return

    cat_id = cat_sel[0]

    # Produtos da categoria
    nossos = query("""
        SELECT p.produto_id, p.descricao_curta, m.nome_marca
        FROM produto p JOIN marca m ON p.marca_id=m.marca_id
        WHERE p.fornecedor_id=? AND p.categoria_id=? AND p.ativo=1
        ORDER BY m.nome_marca, p.descricao_curta
    """, (forn_id, cat_id))

    concs = query("""
        SELECT pc.produto_concorrente_id, pc.descricao_curta,
               conc.marca_concorrente, pc.ean_concorrente
        FROM produto_concorrente pc
        JOIN concorrente conc ON pc.concorrente_id=conc.concorrente_id
        WHERE conc.fornecedor_id=? AND pc.categoria_id=? AND pc.ativo=1
        ORDER BY conc.marca_concorrente, pc.descricao_curta
    """, (forn_id, cat_id))

    if nossos:
        st.markdown("**🟢 Nossos:**")
        for pid, desc, marca in nossos:
            if st.button(f"{marca} — {desc}",
                        key=f"campo_nav_n_{pq_id}_{pid}",
                        use_container_width=True):
                resultado = {"tipo":"nosso","produto_id":pid,
                            "descricao":desc,"marca":marca,"ean":None,"pc_id":None}
                _coleta_ean_produto_encontrado(pq_id, forn_id, resultado, "")

    if concs:
        st.markdown("**🔴 Concorrentes:**")
        for pc_id, desc, marca, ean in concs:
            if st.button(f"{marca} — {desc}",
                        key=f"campo_nav_c_{pq_id}_{pc_id}",
                        use_container_width=True):
                resultado = {"tipo":"conc","pc_id":pc_id,
                            "descricao":desc,"marca":marca,
                            "ean":ean,"auditavel":1}
                _coleta_ean_produto_encontrado(pq_id, forn_id, resultado,
                                               ean or "")

'''

# Insere antes da funcao _coleta_modo_ean existente
if 'def _coleta_modo_ean' in src:
    src = src.replace('def _coleta_modo_ean', NOVA_FUNCAO + 'def _coleta_modo_ean', 1)
    print("✅ Função _coleta_modo_campo inserida")
else:
    print("⚠️  Ponto de inserção não encontrado")

if src != original:
    pathlib.Path("pesquisa.py").write_text(src, encoding="utf-8")
    print("Salvo")
