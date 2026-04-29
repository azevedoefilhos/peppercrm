# análise_competitiva.py — PepperCRM
# Inteligencia competitiva: marcas, categorias, produtos, presença em PDVs

import streamlit as st
import pandas as pd
import io
from database import query


def _ir(p):
    st.session_state["pagina"] = p
    st.rerun()


def _pct(v, total):
    if not total: return "-%"
    return f"{v/total*100:.1f}%"


def tela_analise_competitiva():
    st.header("Inteligência Competitiva")
    st.caption("Análise de concorrentes, presença em PDVs e oportunidades estratégicas.")
    if st.button("⬅ Voltar"):
        _ir("home")

    # Verifica se ha dados suficientes
    n_pesq = query("SELECT COUNT(*) FROM pesquisa_preco WHERE status='finalizado'")[0][0]
    n_conc = query("SELECT COUNT(*) FROM produto_concorrente WHERE ativo=1")[0][0]

    if n_pesq == 0 and n_conc == 0:
        st.warning("Nenhuma pesquisa finalizada e nenhum produto concorrente cadastrado ainda.")
        return

    col1, col2, col3 = st.columns(3)
    col1.metric("Pesquisas finalizadas", n_pesq)
    col2.metric("Produtos concorrentes cadastrados", n_conc)
    pdvs_pesq = query("""SELECT COUNT(DISTINCT COALESCE(pdv_id::TEXT, cliente_id::TEXT||'c'))
        FROM pesquisa_preco WHERE status='finalizado'""")[0][0]
    col3.metric("PDVs/locais pesquisados", pdvs_pesq)

    st.divider()

    ABAS_ANA = {"mc":"Marcas/categorias","pdv":"Presença PDV",
                "vs":"Meu produto vs","op":"Oportunidades"}
    if "ana_aba" not in st.session_state: st.session_state["ana_aba"] = "mc"
    cols = st.columns(4)
    for col,(k,v) in zip(cols, ABAS_ANA.items()):
        ativa = st.session_state["ana_aba"] == k
        if col.button(v, key=f"ananav_{k}", use_container_width=True,
                      type="primary" if ativa else "secondary"):
            st.session_state["ana_aba"] = k; st.rerun()
    st.divider()
    a = st.session_state["ana_aba"]
    if a=="mc":  _marcas_categorias()
    elif a=="pdv":_presenca_pdv()
    elif a=="vs": _meu_produto_vs()
    elif a=="op": _oportunidades()


# ==============================================================
# ABA 1 — MARCAS E CATEGORIAS
# ==============================================================

def _marcas_categorias():
    st.subheader("Marcas concorrentes por categoria")
    st.caption("Quantos produtos diretos e indiretos cada marca tem por categoria.")

    forns = query("SELECT fornecedor_id, nome_fantasia FROM fornecedor WHERE ativo=1 ORDER BY nome_fantasia")
    if not forns:
        st.info("Nenhum fornecedor cadastrado."); return

    forn_sel = st.selectbox("Fornecedor de referência", forns,
                            format_func=lambda x: x[1], key="ac_forn")
    forn_id = forn_sel[0]

    # — Tabela principal: marca x categoria x tipo de relação --
    dados = query("""
        SELECT
            conc.marca_concorrente,
            COALESCE(cat.nome_categoria, 'Sem categoria') AS categoria,
            SUM(CASE WHEN rel.tipo_relacao='direto'   THEN 1 ELSE 0 END) AS diretos,
            SUM(CASE WHEN rel.tipo_relacao='indireto' THEN 1 ELSE 0 END) AS indiretos,
            COUNT(DISTINCT rel.produto_concorrente_id) AS total_produtos
        FROM produto_concorrente_relacao rel
        JOIN produto_concorrente pc  ON rel.produto_concorrente_id=pc.produto_concorrente_id
        JOIN concorrente conc        ON pc.concorrente_id=conc.concorrente_id
        JOIN produto p               ON rel.produto_id=p.produto_id
        LEFT JOIN categoria cat      ON pc.categoria_id=cat.categoria_id
        WHERE p.fornecedor_id=? AND conc.ativo=1 AND pc.ativo=1
        GROUP BY conc.marca_concorrente, cat.nome_categoria
        ORDER BY total_produtos DESC, conc.marca_concorrente
    """, (forn_id,))

    if not dados:
        st.info("Nenhuma relação entre produtos seus e concorrentes cadastrada ainda.")
        st.caption("Acesse Concorrentes > Produtos e relações para vincular.")
        return

    df = pd.DataFrame(dados, columns=["Marca","Categoria","Diretos","Indiretos","Total"])

    # — Resumo por marca (total geral) --
    st.markdown("**Ranking de marcas concorrentes**")
    resumo_marca = df.groupby("Marca").agg(
        Diretos=("Diretos","sum"),
        Indiretos=("Indiretos","sum"),
        Total=("Total","sum")
    ).reset_index().sort_values("Total", ascending=False)
    resumo_marca["% Diretos"] = resumo_marca.apply(
        lambda r: _pct(r["Diretos"], r["Total"]), axis=1)
    st.dataframe(resumo_marca, use_container_width=True, hide_index=True)

    st.divider()

    # — Detalhamento por categoria --
    st.markdown("**Detalhamento marca x categoria**")
    cats_disp = ["Todas"] + sorted(df["Categoria"].unique().tolist())
    cat_fil = st.selectbox("Filtrar por categoria", cats_disp, key="ac_cat_fil")
    df_fil = df if cat_fil == "Todas" else df[df["Categoria"] == cat_fil]
    st.dataframe(df_fil, use_container_width=True, hide_index=True)

    st.divider()

    # — Heatmap: marcas x categorias (contagem de produtos) --
    st.markdown("**Presença de marcas por categoria (total de produtos)**")
    pivot = df.pivot_table(index="Marca", columns="Categoria",
                           values="Total", aggfunc="sum", fill_value=0)
    st.dataframe(pivot, use_container_width=True)

    # — Exportar --
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w:
        resumo_marca.to_excel(w, sheet_name="Ranking marcas", index=False)
        df.to_excel(w, sheet_name="Marca x Categoria", index=False)
        pivot.to_excel(w, sheet_name="Heatmap")
    buf.seek(0)
    st.download_button("⬇️ Exportar Excel", data=buf,
                       file_name="marcas_categorias.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


# ==============================================================
# ABA 2 — PRESENÇA POR PDV
# (cada PDV contado apenas uma vez, mesmo com multiplas pesquisas)
# ==============================================================

def _presenca_pdv():
    st.subheader("Presença de concorrentes nos PDVs")
    st.caption("Cada PDV contado uma unica vez, mesmo com multiplas pesquisas realizadas.")

    forns = query("SELECT fornecedor_id, nome_fantasia FROM fornecedor WHERE ativo=1 ORDER BY nome_fantasia")
    if not forns:
        st.info("Nenhum fornecedor cadastrado."); return

    forn_sel = st.selectbox("Fornecedor de referência", forns,
                            format_func=lambda x: x[1], key="pdv_forn")
    forn_id = forn_sel[0]

    # Total de PDVs unicos pesquisados para este fornecedor
    total_pdvs = query("""
        SELECT COUNT(DISTINCT COALESCE(pp.pdv_id::TEXT, pp.cliente_id::TEXT||'c'))
        FROM pesquisa_preco pp
        WHERE pp.fornecedor_id=? AND pp.status='finalizado'
    """, (forn_id,))[0][0]

    if total_pdvs == 0:
        st.info("Nenhuma pesquisa finalizada para este fornecedor.")
        return

    st.metric("Total de PDVs/locais pesquisados (unicos)", total_pdvs)
    st.divider()

    # -- Presença de cada produto concorrente (PDVs unicos) --
    st.markdown("**Presença por produto concorrente**")
    st.caption("Em quantos PDVs distintos cada produto concorrente foi encontrado.")

    dados_pdv = query("""
        SELECT
            conc.marca_concorrente,
            COALESCE(pc.descricao_curta, pc.descricao) AS produto,
            COALESCE(cat.nome_categoria, 'Sem categoria') AS categoria,
            COALESCE(rel_tipo.tipo_relacao, 'nao_vinculado') AS tipo,
            COUNT(DISTINCT COALESCE(pp.pdv_id::TEXT, pp.cliente_id::TEXT||'c')) AS pdvs_presentes
        FROM pesquisa_preco_item ppi
        JOIN pesquisa_preco pp       ON ppi.pesquisa_id=pp.pesquisa_id
        JOIN produto_concorrente pc  ON ppi.produto_concorrente_id=pc.produto_concorrente_id
        JOIN concorrente conc        ON pc.concorrente_id=conc.concorrente_id
        LEFT JOIN categoria cat      ON pc.categoria_id=cat.categoria_id
        LEFT JOIN (
            SELECT DISTINCT produto_concorrente_id, tipo_relacao
            FROM produto_concorrente_relacao rel
            JOIN produto p ON rel.produto_id=p.produto_id
            WHERE p.fornecedor_id=?
        ) rel_tipo ON rel_tipo.produto_concorrente_id=pc.produto_concorrente_id
        WHERE pp.fornecedor_id=? AND pp.status='finalizado'
          AND ppi.produto_concorrente_id IS NOT NULL
          AND ppi.ruptura=0
        GROUP BY pc.produto_concorrente_id, conc.marca_concorrente, pc.descricao_curta, pc.descricao, cat.nome_categoria, rel_tipo.tipo_relacao
        ORDER BY pdvs_presentes DESC, conc.marca_concorrente
    """, (forn_id, forn_id))

    if not dados_pdv:
        st.info("Nenhum dado de concorrentes nas pesquisas finalizadas.")
        return

    df_pdv = pd.DataFrame(dados_pdv,
                          columns=["Marca","Produto","Categoria","Tipo","PDVs presentes"])
    df_pdv["Presença %"] = df_pdv["PDVs presentes"].apply(
        lambda v: _pct(v, total_pdvs))
    df_pdv["Tipo"] = df_pdv["Tipo"].apply(
        lambda t: "Direto" if t=="direto" else ("Indireto" if t=="indireto" else "Nao vinculado"))

    # Filtros
    col1, col2 = st.columns(2)
    with col1:
        marcas_disp = ["Todas"] + sorted(df_pdv["Marca"].unique().tolist())
        marc_fil = st.selectbox("Filtrar por marca", marcas_disp, key="pdv_marc_fil")
    with col2:
        tipo_disp = ["Todos","Direto","Indireto","Nao vinculado"]
        tipo_fil = st.selectbox("Filtrar por tipo", tipo_disp, key="pdv_tipo_fil")

    df_show = df_pdv.copy()
    if marc_fil != "Todas":
        df_show = df_show[df_show["Marca"] == marc_fil]
    if tipo_fil != "Todos":
        df_show = df_show[df_show["Tipo"] == tipo_fil]

    st.dataframe(df_show, use_container_width=True, hide_index=True)
    st.caption(f"{len(df_show)} produto(s) encontrado(s) nos filtros")

    st.divider()

    # -- Presença por MARCA (consolidado) --
    st.markdown("**Presença consolidada por marca**")
    resumo_marc = query("""
        SELECT
            conc.marca_concorrente,
            COUNT(DISTINCT COALESCE(pp.pdv_id::TEXT, pp.cliente_id::TEXT||'c')) AS pdvs_presentes,
            COUNT(DISTINCT pc.produto_concorrente_id) AS produtos_encontrados
        FROM pesquisa_preco_item ppi
        JOIN pesquisa_preco pp       ON ppi.pesquisa_id=pp.pesquisa_id
        JOIN produto_concorrente pc  ON ppi.produto_concorrente_id=pc.produto_concorrente_id
        JOIN concorrente conc        ON pc.concorrente_id=conc.concorrente_id
        WHERE pp.fornecedor_id=? AND pp.status='finalizado'
          AND ppi.produto_concorrente_id IS NOT NULL
          AND ppi.ruptura=0
        GROUP BY conc.concorrente_id, conc.marca_concorrente
        ORDER BY pdvs_presentes DESC
    """, (forn_id,))

    if resumo_marc:
        df_marc = pd.DataFrame(resumo_marc,
                               columns=["Marca","PDVs com presença","Produtos encontrados"])
        df_marc["Presença %"] = df_marc["PDVs com presença"].apply(
            lambda v: _pct(v, total_pdvs))
        st.dataframe(df_marc, use_container_width=True, hide_index=True)

    st.divider()

    # — PDVs onde NOSSO produto NAO estava (ruptura) --
    st.markdown("**Rupturas do nosso produto por PDV**")
    st.caption("PDVs onde o produto nosso estava ausente mas o concorrente estava presente.")

    rupturas = query("""
        SELECT
            COALESCE(pdv.nome_loja, cli.nome_fantasia, 'Direto') AS local,
            COALESCE(pdv.cidade, cli.cidade, '-') AS cidade,
            p.descricao_curta AS nosso_produto,
            conc.marca_concorrente AS concorrente_presente,
            COUNT(DISTINCT ppi_conc.pesquisa_item_id) AS ocorrências
        FROM pesquisa_preco_item ppi_nosso
        JOIN pesquisa_preco pp       ON ppi_nosso.pesquisa_id=pp.pesquisa_id
        JOIN produto p               ON ppi_nosso.produto_id=p.produto_id
        JOIN pesquisa_preco_item ppi_conc ON ppi_conc.pesquisa_id=pp.pesquisa_id
            AND ppi_conc.produto_id=ppi_nosso.produto_id
            AND ppi_conc.produto_concorrente_id IS NOT NULL
        JOIN produto_concorrente pc  ON ppi_conc.produto_concorrente_id=pc.produto_concorrente_id
        JOIN concorrente conc        ON pc.concorrente_id=conc.concorrente_id
        LEFT JOIN pdv                ON pp.pdv_id=pdv.pdv_id
        LEFT JOIN cliente cli        ON pp.cliente_id=cli.cliente_id
        WHERE pp.fornecedor_id=? AND pp.status='finalizado'
          AND ppi_nosso.produto_concorrente_id IS NULL
          AND ppi_nosso.ruptura=1
        GROUP BY pp.pdv_id, p.produto_id, conc.concorrente_id
        ORDER BY ocorrências DESC
    """, (forn_id,))

    if rupturas:
        df_rupt = pd.DataFrame(rupturas,
                               columns=["PDV","Cidade","Nosso produto","Concorrente presente","Ocorrências"])
        st.dataframe(df_rupt, use_container_width=True, hide_index=True)
        st.caption(f"{len(rupturas)} situacoes de ruptura detectadas.")
    else:
        st.success("Nenhuma ruptura registrada nas pesquisas.")

    # Exportar
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w:
        df_pdv.to_excel(w, sheet_name="Presença por produto", index=False)
        if resumo_marc:
            df_marc.to_excel(w, sheet_name="Presença por marca", index=False)
        if rupturas:
            df_rupt.to_excel(w, sheet_name="Rupturas", index=False)
    buf.seek(0)
    st.download_button("⬇️ Exportar Excel", data=buf,
                       file_name="presença_pdv.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


# ==============================================================
# ABA 3 — MEU PRODUTO vs CONCORRENTES
# ==============================================================

def _meu_produto_vs():
    st.subheader("Meu produto vs concorrentes diretos e indiretos")

    forns = query("SELECT fornecedor_id, nome_fantasia FROM fornecedor WHERE ativo=1 ORDER BY nome_fantasia")
    if not forns:
        st.info("Nenhum fornecedor cadastrado."); return

    forn_sel = st.selectbox("Fornecedor", forns, format_func=lambda x: x[1], key="vs_forn")
    forn_id = forn_sel[0]

    meus = query("""SELECT p.produto_id, p.codigo_produto, p.descricao_curta,
        COUNT(rel.relacao_id) AS n_conc
        FROM produto p
        LEFT JOIN produto_concorrente_relacao rel ON rel.produto_id=p.produto_id
        WHERE p.fornecedor_id=? AND p.ativo=1
        GROUP BY p.produto_id ORDER BY p.descricao_curta""", (forn_id,))

    if not meus:
        st.info("Nenhum produto cadastrado para este fornecedor."); return

    prod_sel = st.selectbox("Meu produto", meus,
                            format_func=lambda x: f"{x[1]} - {x[2]} ({x[3]} concorrente(s))",
                            key="vs_prod")
    prod_id = prod_sel[0]

    # Total de PDVs pesquisados
    total_pdvs = query("""
        SELECT COUNT(DISTINCT COALESCE(pp.pdv_id::TEXT, pp.cliente_id::TEXT||'c'))
        FROM pesquisa_preco pp
        WHERE pp.fornecedor_id=? AND pp.status='finalizado'
    """, (forn_id,))[0][0]

    # Meu produto nos PDVs
    meu_nos_pdvs = query("""
        SELECT COUNT(DISTINCT COALESCE(pp.pdv_id::TEXT, pp.cliente_id::TEXT||'c'))
        FROM pesquisa_preco_item ppi
        JOIN pesquisa_preco pp ON ppi.pesquisa_id=pp.pesquisa_id
        WHERE pp.fornecedor_id=? AND pp.status='finalizado'
          AND ppi.produto_id=? AND ppi.produto_concorrente_id IS NULL
          AND ppi.ruptura=0
    """, (forn_id, prod_id))[0][0]

    meu_rupturas = query("""
        SELECT COUNT(DISTINCT COALESCE(pp.pdv_id::TEXT, pp.cliente_id::TEXT||'c'))
        FROM pesquisa_preco_item ppi
        JOIN pesquisa_preco pp ON ppi.pesquisa_id=pp.pesquisa_id
        WHERE pp.fornecedor_id=? AND pp.status='finalizado'
          AND ppi.produto_id=? AND ppi.produto_concorrente_id IS NULL
          AND ppi.ruptura=1
    """, (forn_id, prod_id))[0][0]

    col1, col2, col3 = st.columns(3)
    col1.metric("PDVs pesquisados", total_pdvs)
    col2.metric("PDVs com meu produto", f"{meu_nos_pdvs} ({_pct(meu_nos_pdvs, total_pdvs)})")
    col3.metric("PDVs com ruptura do meu produto", meu_rupturas,
                delta=f"-{_pct(meu_rupturas, total_pdvs)}" if meu_rupturas else None,
                delta_color="inverse")

    st.divider()

    # Concorrentes x presença nos PDVs
    concs = query("""
        SELECT
            conc.marca_concorrente,
            COALESCE(pc.descricao_curta, pc.descricao) AS produto_conc,
            rel.tipo_relacao,
            COUNT(DISTINCT COALESCE(pp.pdv_id::TEXT, pp.cliente_id::TEXT||'c')) AS pdvs_conc,
            -- PDVs onde concorrente esta mas MEU nao esta (ruptura)
            COUNT(DISTINCT CASE WHEN ppi_nosso.ruptura=1 OR ppi_nosso.pesquisa_item_id IS NULL
                THEN COALESCE(pp.pdv_id::TEXT, pp.cliente_id::TEXT||'c') END) AS pdvs_so_conc
        FROM produto_concorrente_relacao rel
        JOIN produto_concorrente pc   ON rel.produto_concorrente_id=pc.produto_concorrente_id
        JOIN concorrente conc         ON pc.concorrente_id=conc.concorrente_id
        LEFT JOIN pesquisa_preco_item ppi ON ppi.produto_concorrente_id=pc.produto_concorrente_id
        LEFT JOIN pesquisa_preco pp       ON ppi.pesquisa_id=pp.pesquisa_id
            AND pp.fornecedor_id=? AND pp.status='finalizado' AND ppi.ruptura=0
        LEFT JOIN pesquisa_preco_item ppi_nosso ON ppi_nosso.pesquisa_id=pp.pesquisa_id
            AND ppi_nosso.produto_id=? AND ppi_nosso.produto_concorrente_id IS NULL
        WHERE rel.produto_id=?
        GROUP BY rel.produto_concorrente_id, rel.tipo_relacao, conc.marca_concorrente, pc.descricao_curta, pc.descricao
        ORDER BY rel.tipo_relacao, pdvs_conc DESC
    """, (forn_id, prod_id, prod_id))

    if not concs:
        st.info("Nenhum concorrente vinculado a este produto.")
        st.caption("Acesse Concorrentes > Produtos e relações para vincular.")
        return

    df_concs = pd.DataFrame(concs,
        columns=["Marca","Produto concorrente","Tipo","PDVs com concorrente","PDVs so com concorrente"])
    df_concs["Presença concorrente %"] = df_concs["PDVs com concorrente"].apply(
        lambda v: _pct(v, total_pdvs))
    df_concs["Tipo"] = df_concs["Tipo"].apply(
        lambda t: "Direto" if t=="direto" else "Indireto")

    st.markdown("**Comparativo de presença nos PDVs**")
    st.dataframe(df_concs, use_container_width=True, hide_index=True)

    # Frentes de gôndola (facing) -- comparativo
    st.divider()
    st.markdown("**Frentes de gôndola (facing) -- media por produto**")
    facing = query("""
        SELECT 'Meu produto' AS nome,
               ROUND(AVG(ppi.frentes),1) AS media_frentes,
               MIN(ppi.frentes) AS min_frentes,
               MAX(ppi.frentes) AS max_frentes,
               COUNT(*) AS registros
        FROM pesquisa_preco_item ppi
        JOIN pesquisa_preco pp ON ppi.pesquisa_id=pp.pesquisa_id
        WHERE pp.fornecedor_id=? AND pp.status='finalizado'
          AND ppi.produto_id=? AND ppi.produto_concorrente_id IS NULL
          AND ppi.frentes IS NOT NULL AND ppi.ruptura=0

        UNION ALL

        SELECT conc.marca_concorrente||' - '||COALESCE(pc.descricao_curta,'') AS nome,
               ROUND(AVG(ppi.frentes),1),
               MIN(ppi.frentes), MAX(ppi.frentes), COUNT(*)
        FROM pesquisa_preco_item ppi
        JOIN pesquisa_preco pp ON ppi.pesquisa_id=pp.pesquisa_id
        JOIN produto_concorrente_relacao rel ON rel.produto_id=? AND rel.produto_concorrente_id=ppi.produto_concorrente_id
        JOIN produto_concorrente pc ON ppi.produto_concorrente_id=pc.produto_concorrente_id
        JOIN concorrente conc       ON pc.concorrente_id=conc.concorrente_id
        WHERE pp.fornecedor_id=? AND pp.status='finalizado'
          AND ppi.frentes IS NOT NULL
        GROUP BY ppi.produto_concorrente_id, conc.marca_concorrente, pc.descricao_curta
        ORDER BY media_frentes DESC
    """, (forn_id, prod_id, prod_id, forn_id))

    if facing and any(r[1] for r in facing):
        df_f = pd.DataFrame(facing, columns=["Produto","Media frentes","Min","Max","Registros"])
        st.dataframe(df_f, use_container_width=True, hide_index=True)
    else:
        st.caption("Nenhum dado de frentes registrado ainda.")

    # Ponto extra
    st.divider()
    st.markdown("**Ponto extra -- frequencia**")
    ponto = query("""
        SELECT 'Meu produto' AS nome,
               SUM(ppi.ponto_extra) AS com_ponto_extra,
               COUNT(*) AS total,
               ROUND(100.0*SUM(ppi.ponto_extra)/COUNT(*),1) AS pct
        FROM pesquisa_preco_item ppi
        JOIN pesquisa_preco pp ON ppi.pesquisa_id=pp.pesquisa_id
        WHERE pp.fornecedor_id=? AND pp.status='finalizado'
          AND ppi.produto_id=? AND ppi.produto_concorrente_id IS NULL

        UNION ALL

        SELECT conc.marca_concorrente||' - '||COALESCE(pc.descricao_curta,'') AS nome,
               SUM(ppi.ponto_extra), COUNT(*),
               ROUND(100.0*SUM(ppi.ponto_extra)/COUNT(*),1)
        FROM pesquisa_preco_item ppi
        JOIN pesquisa_preco pp ON ppi.pesquisa_id=pp.pesquisa_id
        JOIN produto_concorrente_relacao rel ON rel.produto_id=? AND rel.produto_concorrente_id=ppi.produto_concorrente_id
        JOIN produto_concorrente pc ON ppi.produto_concorrente_id=pc.produto_concorrente_id
        JOIN concorrente conc       ON pc.concorrente_id=conc.concorrente_id
        WHERE pp.fornecedor_id=? AND pp.status='finalizado'
        GROUP BY ppi.produto_concorrente_id, conc.marca_concorrente, pc.descricao_curta
        ORDER BY pct DESC
    """, (forn_id, prod_id, prod_id, forn_id))

    if ponto:
        df_p = pd.DataFrame(ponto, columns=["Produto","Com ponto extra","Total registros","% com ponto extra"])
        st.dataframe(df_p, use_container_width=True, hide_index=True)


# ==============================================================
# ABA 4 — OPORTUNIDADES ESTRATEGICAS
# ==============================================================

def _oportunidades():
    st.subheader("Oportunidades estratégicas")

    forns = query("SELECT fornecedor_id, nome_fantasia FROM fornecedor WHERE ativo=1 ORDER BY nome_fantasia")
    if not forns:
        st.info("Nenhum fornecedor cadastrado."); return

    forn_sel = st.selectbox("Fornecedor", forns, format_func=lambda x: x[1], key="op_forn")
    forn_id = forn_sel[0]

    total_pdvs = query("""
        SELECT COUNT(DISTINCT COALESCE(pp.pdv_id::TEXT, pp.cliente_id::TEXT||'c'))
        FROM pesquisa_preco pp WHERE pp.fornecedor_id=? AND pp.status='finalizado'
    """, (forn_id,))[0][0]

    if total_pdvs == 0:
        st.info("Nenhuma pesquisa finalizada para este fornecedor."); return

    # ----------------------------------------------------------
    # OPORTUNIDADE 1: PDVs onde concorrente direto esta mas
    # nosso produto não está (ruptura ou ausencia)
    # ----------------------------------------------------------
    st.markdown("### PDVs com concorrente direto sem nosso produto")
    st.caption("Prioridade maxima: o concorrente esta no PDV, mas nosso produto não foi encontrado.")

    op1 = query("""
        SELECT
            COALESCE(pdv.nome_loja, cli.nome_fantasia, 'Direto') AS local,
            COALESCE(pdv.cidade, cli.cidade, '-') AS cidade,
            p.descricao_curta AS nosso_produto,
            conc.marca_concorrente AS concorrente,
            COALESCE(pc.descricao_curta, pc.descricao) AS prod_conc,
            COUNT(DISTINCT pp.pesquisa_id) AS vezes_detectado
        FROM pesquisa_preco_item ppi_conc
        JOIN pesquisa_preco pp       ON ppi_conc.pesquisa_id=pp.pesquisa_id
        JOIN produto_concorrente pc  ON ppi_conc.produto_concorrente_id=pc.produto_concorrente_id
        JOIN concorrente conc        ON pc.concorrente_id=conc.concorrente_id
        JOIN produto_concorrente_relacao rel ON rel.produto_concorrente_id=pc.produto_concorrente_id
            AND rel.tipo_relacao='direto'
        JOIN produto p               ON rel.produto_id=p.produto_id
        LEFT JOIN pdv                ON pp.pdv_id=pdv.pdv_id
        LEFT JOIN cliente cli        ON pp.cliente_id=cli.cliente_id
        -- Garante que nosso produto NAO estava presente (ruptura ou nao pesquisado)
        LEFT JOIN pesquisa_preco_item ppi_nosso ON ppi_nosso.pesquisa_id=pp.pesquisa_id
            AND ppi_nosso.produto_id=p.produto_id
            AND ppi_nosso.produto_concorrente_id IS NULL
            AND ppi_nosso.ruptura=0
        WHERE pp.fornecedor_id=? AND pp.status='finalizado'
          AND p.fornecedor_id=?
          AND ppi_conc.ruptura=0
          AND (ppi_nosso.pesquisa_item_id IS NULL OR ppi_nosso.ruptura=1)
        GROUP BY COALESCE(pp.pdv_id::TEXT, pp.cliente_id::TEXT), p.produto_id, pc.produto_concorrente_id, p.descricao_curta, conc.marca_concorrente, pc.descricao_curta, pdv.nome_loja, cli.nome_fantasia, pdv.cidade, cli.cidade
        ORDER BY vezes_detectado DESC, local
    """, (forn_id, forn_id))

    if op1:
        df1 = pd.DataFrame(op1, columns=["PDV","Cidade","Nosso produto","Concorrente","Prod. concorrente","Detectado N vezes"])
        st.dataframe(df1, use_container_width=True, hide_index=True)
        st.caption(f"{len(op1)} oportunidade(s) de entrada imediata identificada(s).")
    else:
        st.success("Nosso produto esta presente em todos os PDVs onde ha concorrente direto.")

    st.divider()

    # ----------------------------------------------------------
    # OPORTUNIDADE 2: Concentração de concorrentes por PDV
    # PDVs com muitos concorrentes = mais disputado = priorizar defesa
    # ----------------------------------------------------------
    st.markdown("### PDVs mais disputados (maior concentração de concorrentes)")
    st.caption("PDVs com mais marcas concorrentes diferentes encontradas.")

    op2 = query("""
        SELECT
            COALESCE(pdv.nome_loja, cli.nome_fantasia, 'Direto') AS local,
            COALESCE(pdv.cidade, cli.cidade, '-') AS cidade,
            COUNT(DISTINCT conc.concorrente_id) AS marcas_concorrentes,
            COUNT(DISTINCT ppi.produto_concorrente_id) AS produtos_concorrentes,
            COUNT(DISTINCT pp.pesquisa_id) AS pesquisas_realizadas
        FROM pesquisa_preco_item ppi
        JOIN pesquisa_preco pp      ON ppi.pesquisa_id=pp.pesquisa_id
        JOIN produto_concorrente pc ON ppi.produto_concorrente_id=pc.produto_concorrente_id
        JOIN concorrente conc       ON pc.concorrente_id=conc.concorrente_id
        LEFT JOIN pdv               ON pp.pdv_id=pdv.pdv_id
        LEFT JOIN cliente cli       ON pp.cliente_id=cli.cliente_id
        WHERE pp.fornecedor_id=? AND pp.status='finalizado'
          AND ppi.produto_concorrente_id IS NOT NULL
        GROUP BY COALESCE(pp.pdv_id::TEXT, pp.cliente_id::TEXT||'c'), pdv.nome_loja, cli.nome_fantasia, pdv.cidade, cli.cidade
        ORDER BY marcas_concorrentes DESC, produtos_concorrentes DESC
    """, (forn_id,))

    if op2:
        df2 = pd.DataFrame(op2, columns=["PDV","Cidade","Marcas concorrentes","Produtos concorrentes","Pesquisas"])
        st.dataframe(df2, use_container_width=True, hide_index=True)
    else:
        st.info("Sem dados de concorrentes nas pesquisas.")

    st.divider()

    # ----------------------------------------------------------
    # OPORTUNIDADE 3: Produtos nossos sem nenhum concorrente vinculado
    # Risco: concorrentes desconhecidos podem existir
    # ----------------------------------------------------------
    st.markdown("### Nossos produtos sem concorrentes mapeados")
    st.caption("Produtos que ainda nao tem concorrentes vinculados -- risco de ponto cego.")

    op3 = query("""
        SELECT p.codigo_produto, p.descricao_curta,
               COALESCE(cat.nome_categoria, 'Sem categoria') AS categoria
        FROM produto p
        LEFT JOIN categoria cat ON p.categoria_id=cat.categoria_id
        WHERE p.fornecedor_id=? AND p.ativo=1
          AND NOT EXISTS (
              SELECT 1 FROM produto_concorrente_relacao rel WHERE rel.produto_id=p.produto_id)
        ORDER BY p.descricao_curta
    """, (forn_id,))

    if op3:
        df3 = pd.DataFrame(op3, columns=["Codigo","Produto","Categoria"])
        st.dataframe(df3, use_container_width=True, hide_index=True)
        st.caption(f"{len(op3)} produto(s) sem concorrente mapeado. Considere pesquisar esses itens no campo.")
    else:
        st.success("Todos os nossos produtos tem ao menos um concorrente mapeado.")

    st.divider()

    # ----------------------------------------------------------
    # OPORTUNIDADE 4: Marcas com alta presença mas sem ponto extra
    # Concorrentes dominando gôndola sem investimento extra = vulneravel
    # ----------------------------------------------------------
    st.markdown("### Concorrentes com alta presença sem ponto extra")
    st.caption("Marcas presentes em muitos PDVs sem ponto extra -- podem ser desalojadas com acao de trade.")

    op4 = query("""
        SELECT
            conc.marca_concorrente,
            COUNT(DISTINCT COALESCE(pp.pdv_id::TEXT, pp.cliente_id::TEXT||'c')) AS pdvs_presentes,
            SUM(CASE WHEN ppi.ponto_extra=1 THEN 1 ELSE 0 END) AS com_ponto_extra,
            SUM(CASE WHEN ppi.ponto_extra=0 THEN 1 ELSE 0 END) AS sem_ponto_extra,
            ROUND(100.0*SUM(CASE WHEN ppi.ponto_extra=0 THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_sem_ponto
        FROM pesquisa_preco_item ppi
        JOIN pesquisa_preco pp      ON ppi.pesquisa_id=pp.pesquisa_id
        JOIN produto_concorrente pc ON ppi.produto_concorrente_id=pc.produto_concorrente_id
        JOIN concorrente conc       ON pc.concorrente_id=conc.concorrente_id
        WHERE pp.fornecedor_id=? AND pp.status='finalizado'
          AND ppi.produto_concorrente_id IS NOT NULL AND ppi.ruptura=0
        GROUP BY conc.concorrente_id, conc.marca_concorrente
        HAVING COUNT(DISTINCT COALESCE(pp.pdv_id::TEXT, pp.cliente_id::TEXT||'c')) > 0
        ORDER BY pct_sem_ponto DESC, pdvs_presentes DESC
    """, (forn_id,))

    if op4:
        df4 = pd.DataFrame(op4,
            columns=["Marca","PDVs presentes","Com ponto extra","Sem ponto extra","% sem ponto extra"])
        st.dataframe(df4, use_container_width=True, hide_index=True)
    else:
        st.info("Sem dados suficientes.")

    st.divider()

    # — Exportar oportunidades --
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w:
        if op1: pd.DataFrame(op1, columns=["PDV","Cidade","Nosso produto","Concorrente","Prod. concorrente","N vezes"]).to_excel(w, sheet_name="Entrada imediata", index=False)
        if op2: pd.DataFrame(op2, columns=["PDV","Cidade","Marcas","Produtos","Pesquisas"]).to_excel(w, sheet_name="PDVs disputados", index=False)
        if op3: pd.DataFrame(op3, columns=["Codigo","Produto","Categoria"]).to_excel(w, sheet_name="Pontos cegos", index=False)
        if op4: pd.DataFrame(op4, columns=["Marca","PDVs","Com PE","Sem PE","% sem PE"]).to_excel(w, sheet_name="Trade oportunidade", index=False)
    buf.seek(0)
    st.download_button("⬇️ Exportar oportunidades Excel", data=buf,
                       file_name="oportunidades.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")