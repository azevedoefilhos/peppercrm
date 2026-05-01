from cache_helpers import cache_fornecedores
# metas.py — PepperCRM
# Módulo de metas mensais por fornecedor com acompanhamento % atingido

import streamlit as st
import pandas as pd
import io
from datetime import date, datetime
from database import conectar, query


def _ir(p):
    st.session_state["pagina"] = p
    st.session_state["_scroll_topo"] = True
    st.rerun()


def _brl(v):
    try:
        return f"R$ {float(v):,.2f}".replace(",","X").replace(".",",").replace("X",".")
    except:
        return "R$ 0,00"


def tela_metas():
    st.header("🎯 Metas")
    if st.button("⬅ Voltar"): _ir("home")

    # 3 abas com função bem definida e distinta
    ABAS_MT = {
        "painel": "📊 Painel do mês",
        "definir": "➕ Definir metas",
        "hist":   "📅 Histórico",
    }
    st.caption(
        "**📊 Painel do mês** — acompanhe todas as metas (faturamento + mix) do mês selecionado  |  "
        "**➕ Definir metas** — crie ou edite metas de faturamento e de mix  |  "
        "**📅 Histórico** — veja o desempenho de meses anteriores"
    )
    if "mt_nav_aba" not in st.session_state: st.session_state["mt_nav_aba"] = "painel"
    cols = st.columns(3)
    for col,(k,v) in zip(cols, ABAS_MT.items()):
        ativa = st.session_state["mt_nav_aba"] == k
        if col.button(v, key=f"mtnav_{k}", use_container_width=True,
                      type="primary" if ativa else "secondary"):
            st.session_state["mt_nav_aba"] = k; st.rerun()
    st.divider()
    a = st.session_state["mt_nav_aba"]
    if a=="painel":  _painel_unificado()
    elif a=="definir": _definir_metas()
    elif a=="hist":  _historico_metas()



# ══════════════════════════════════════════════════════
# PAINEL UNIFICADO — faturamento + mix no mesmo lugar
# ══════════════════════════════════════════════════════
def _painel_unificado():
    """Painel do mês: mostra TODAS as metas (faturamento e mix) juntas."""
    _garantir_tabela()
    _garantir_meta_mix()

    hoje   = date.today()
    meses  = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho",
               "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]

    col1, col2, col3 = st.columns(3)
    with col1:
        forns = cache_fornecedores()
        forn_opts = [(0,"Todos os fornecedores")] + [(f[0],f[1]) for f in forns]
        forn_sel  = st.selectbox("Fornecedor", forn_opts,
                                 format_func=lambda x: x[1], key="pu_forn")
    with col2:
        ano_sel = st.selectbox("Ano", list(range(hoje.year, hoje.year-3, -1)),
                               key="pu_ano")
    with col3:
        mes_sel = st.selectbox("Mês", range(1,13),
                               format_func=lambda x: meses[x-1],
                               index=hoje.month-1, key="pu_mes")

    fids = [f[0] for f in forns] if forn_sel[0]==0 else [forn_sel[0]]
    tem_algo = False

    for fid in fids:
        forn_nome = next((f[1] for f in forns if f[0]==fid), "—")

        # Metas de faturamento deste fornecedor/mês
        metas_fat = query("""
            SELECT m.meta_id, m.meta_valor, m.meta_pedidos,
                   COALESCE((
                       SELECT ROUND(SUM(pi.quantidade*pi.preco_final
                              *(1-COALESCE(p.desconto_geral,0)/100.0)),2)
                       FROM pedido p JOIN pedido_item pi ON pi.pedido_id=p.pedido_id
                       WHERE p.fornecedor_id=? AND p.status_pedido NOT IN ('CANCELADO','RECUSADO')
                         AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO')
                         AND strftime('%Y',p.data_pedido)=?
                         AND strftime('%m',p.data_pedido)=?
                   ),0) AS realizado,
                   COALESCE((
                       SELECT COUNT(*) FROM pedido p
                       WHERE p.fornecedor_id=? AND p.status_pedido NOT IN ('CANCELADO','RECUSADO')
                         AND strftime('%Y',p.data_pedido)=?
                         AND strftime('%m',p.data_pedido)=?
                   ),0) AS pedidos_feitos
            FROM meta_fornecedor m
            WHERE m.fornecedor_id=? AND m.ano=? AND m.mes=? AND m.ativo=1
        """, (fid, str(ano_sel), f"{mes_sel:02d}",
              fid, str(ano_sel), f"{mes_sel:02d}",
              fid, ano_sel, mes_sel))

        # Metas de mix deste fornecedor/mês
        metas_mix = query("""
            SELECT meta_mix_id, tipo, referencia_id, descricao,
                   meta_qtd, meta_clientes, observacao
            FROM meta_mix
            WHERE fornecedor_id=? AND ano=? AND mes=? AND ativo=1
            ORDER BY tipo, descricao
        """, (fid, ano_sel, mes_sel))

        if not metas_fat and not metas_mix:
            continue

        tem_algo = True
        st.markdown(f"### 🏭 {forn_nome}")

        # ── Metas de faturamento ──────────────────────────────────────────
        if metas_fat:
            st.caption("💰 **Faturamento**")
            for row in metas_fat:
                mid, meta_v, meta_p, realizado, pedidos = row
                pct = min(realizado/meta_v*100,100) if meta_v else 0
                cor = "🟢" if pct>=100 else "🟡" if pct>=70 else "🟠" if pct>=40 else "🔴"
                with st.container(border=True):
                    c1,c2,c3,c4 = st.columns(4)
                    c1.metric("Meta", _brl(meta_v))
                    c2.metric("Realizado", _brl(realizado),
                              delta=_brl(realizado-meta_v) if realizado!=meta_v else None)
                    c3.metric("Atingimento", f"{cor} {pct:.0f}%")
                    c4.metric("Pedidos", f"{pedidos}" + (f"/{meta_p}" if meta_p else ""))
                    st.progress(pct/100)

        # ── Metas de mix ──────────────────────────────────────────────────
        if metas_mix:
            st.caption("🎯 **Mix de produtos**")
            for row in metas_mix:
                mmid, tipo, ref_id, desc, meta_qtd, meta_cli, obs = row
                real_cli=0; real_qtd=0

                if tipo=="produto" and ref_id:
                    r = query("""SELECT COUNT(DISTINCT p.cliente_id),
                                    COALESCE(SUM(pi.quantidade),0)
                                 FROM pedido p JOIN pedido_item pi ON pi.pedido_id=p.pedido_id
                                 WHERE pi.produto_id=?
                                   AND strftime('%Y',p.data_pedido)=?
                                   AND strftime('%m',p.data_pedido)=?
                                   AND p.status_pedido NOT IN ('CANCELADO','RECUSADO')""",
                              (ref_id,str(ano_sel),f"{mes_sel:02d}"))
                    if r: real_cli,real_qtd=r[0][0],int(r[0][1] or 0)
                elif tipo=="categoria" and ref_id:
                    r = query("""SELECT COUNT(DISTINCT p.cliente_id),
                                    COALESCE(SUM(pi.quantidade),0)
                                 FROM pedido p JOIN pedido_item pi ON pi.pedido_id=p.pedido_id
                                 JOIN produto pr ON pi.produto_id=pr.produto_id
                                 WHERE pr.categoria_id=? AND p.fornecedor_id=?
                                   AND strftime('%Y',p.data_pedido)=?
                                   AND strftime('%m',p.data_pedido)=?
                                   AND p.status_pedido NOT IN ('CANCELADO','RECUSADO')""",
                              (ref_id,fid,str(ano_sel),f"{mes_sel:02d}"))
                    if r: real_cli,real_qtd=r[0][0],int(r[0][1] or 0)
                elif tipo=="linha" and ref_id:
                    r = query("""SELECT COUNT(DISTINCT p.cliente_id),
                                    COALESCE(SUM(pi.quantidade),0)
                                 FROM pedido p JOIN pedido_item pi ON pi.pedido_id=p.pedido_id
                                 JOIN produto pr ON pi.produto_id=pr.produto_id
                                 WHERE pr.linha_id=? AND p.fornecedor_id=?
                                   AND strftime('%Y',p.data_pedido)=?
                                   AND strftime('%m',p.data_pedido)=?
                                   AND p.status_pedido NOT IN ('CANCELADO','RECUSADO')""",
                              (ref_id,fid,str(ano_sel),f"{mes_sel:02d}"))
                    if r: real_cli,real_qtd=r[0][0],int(r[0][1] or 0)

                tipo_ico = {"produto":"📦","categoria":"🏷️","linha":"📋","livre":"🎯"}.get(tipo,"🎯")
                with st.container(border=True):
                    c1,c2,c3 = st.columns([3,1.5,1.5])
                    c1.markdown(f"**{tipo_ico} {desc}**")
                    if obs: c1.caption(obs)
                    if meta_cli:
                        pct_c = min(real_cli/meta_cli,1.0) if meta_cli else 0
                        cor_c = "🟢" if pct_c>=1 else "🟡" if pct_c>=0.5 else "🔴"
                        c2.metric("Clientes",f"{real_cli}/{meta_cli}",
                                  f"{cor_c} {pct_c*100:.0f}%")
                    if meta_qtd:
                        pct_q = min(real_qtd/meta_qtd,1.0) if meta_qtd else 0
                        cor_q = "🟢" if pct_q>=1 else "🟡" if pct_q>=0.5 else "🔴"
                        c3.metric("Qtd (Cx)",f"{real_qtd}/{meta_qtd}",
                                  f"{cor_q} {pct_q*100:.0f}%")
                    if meta_cli:
                        st.progress(min(real_cli/meta_cli,1.0))

        st.divider()

    if not tem_algo:
        st.info(
            f"Nenhuma meta definida para "
            f"{'todos os fornecedores' if forn_sel[0]==0 else forn_sel[1]} "
            f"em {meses[mes_sel-1]}/{ano_sel}. "
            "Use **➕ Definir metas** para criar."
        )


# ══════════════════════════════════════════════════════
# DEFINIR METAS — faturamento e mix na mesma tela
# ══════════════════════════════════════════════════════
def _definir_metas():
    """Tela única para criar/editar metas de faturamento e de mix."""
    _garantir_tabela()
    _garantir_meta_mix()

    st.caption(
        "Defina aqui as metas do período. "
        "**Meta de faturamento** = valor total em R$ que deseja faturar com o fornecedor. "
        "**Meta de mix** = quantidade de clientes ou caixas para um produto/categoria/linha específica."
    )

    ABAS_DEF = {"fat":"💰 Faturamento","mix":"🎯 Mix de produtos"}
    if "def_aba" not in st.session_state: st.session_state["def_aba"] = "fat"
    cols = st.columns(2)
    for col,(k,v) in zip(cols, ABAS_DEF.items()):
        ativa = st.session_state["def_aba"] == k
        if col.button(v, key=f"defnav_{k}", use_container_width=True,
                      type="primary" if ativa else "secondary"):
            st.session_state["def_aba"] = k; st.rerun()
    st.divider()

    if st.session_state["def_aba"] == "fat":
        _form_meta()
    else:
        _tela_meta_mix()


# ══════════════════════════════════════════════════════
# MIGRAÇÃO — cria tabela se não existir
# ══════════════════════════════════════════════════════
def _garantir_tabela():
    conn = conectar()
    conn.execute("""CREATE TABLE IF NOT EXISTS meta_fornecedor (
        meta_id        INTEGER PRIMARY KEY AUTOINCREMENT,
        fornecedor_id  INTEGER NOT NULL REFERENCES fornecedor(fornecedor_id),
        ano            INTEGER NOT NULL,
        mes            INTEGER NOT NULL,
        meta_valor     REAL NOT NULL,
        meta_pedidos   INTEGER,
        observacao     TEXT,
        ativo          INTEGER DEFAULT 1,
        UNIQUE(fornecedor_id, ano, mes))""")
    conn.commit(); conn.close()


# ══════════════════════════════════════════════════════
# 1. PAINEL DE METAS
# ══════════════════════════════════════════════════════
def _painel_metas():
    _garantir_tabela()

    hoje = date.today()
    col1, col2 = st.columns(2)
    with col1:
        ano_sel = st.selectbox("Ano", list(range(hoje.year, hoje.year-3, -1)),
                               key="mt_ano")
    with col2:
        meses = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho",
                 "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]
        mes_sel = st.selectbox("Mês", range(1,13),
                               format_func=lambda x: meses[x-1],
                               index=hoje.month-1, key="mt_mes")

    metas = query("""
        SELECT m.meta_id, f.nome_fantasia, f.fornecedor_id,
               m.meta_valor, COALESCE(m.meta_pedidos,0),
               COALESCE((
                   SELECT ROUND(SUM(pi.quantidade * pi.preco_final
                          * (1 - COALESCE(p.desconto_geral,0)/100.0)),2)
                   FROM pedido p
                   JOIN pedido_item pi ON pi.pedido_id=p.pedido_id
                   WHERE p.fornecedor_id=f.fornecedor_id
                     AND strftime('%Y',p.data_pedido)=?
                     AND strftime('%m',p.data_pedido)=?
                     AND p.status_pedido NOT IN ('CANCELADO','RECUSADO')
                     AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO')
               ),0) AS realizado,
               COALESCE((
                   SELECT COUNT(*)
                   FROM pedido p
                   WHERE p.fornecedor_id=f.fornecedor_id
                     AND strftime('%Y',p.data_pedido)=?
                     AND strftime('%m',p.data_pedido)=?
                     AND p.status_pedido NOT IN ('CANCELADO','RECUSADO')
               ),0) AS pedidos_feitos
        FROM meta_fornecedor m
        JOIN fornecedor f ON m.fornecedor_id=f.fornecedor_id
        WHERE m.ano=? AND m.mes=? AND m.ativo=1
        ORDER BY f.nome_fantasia
    """, (str(ano_sel), f"{mes_sel:02d}",
          str(ano_sel), f"{mes_sel:02d}",
          ano_sel, mes_sel))

    if not metas:
        st.info(f"Nenhuma meta definida para {meses[mes_sel-1]}/{ano_sel}. "
                f"Use a aba **➕ Definir meta** para cadastrar.")
        return

    st.subheader(f"Metas — {meses[mes_sel-1]}/{ano_sel}")

    total_meta = sum(r[3] for r in metas)
    total_real = sum(r[5] for r in metas)
    pct_geral  = min(total_real/total_meta*100, 100) if total_meta > 0 else 0

    # KPIs gerais
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Meta total",    _brl(total_meta))
    c2.metric("Realizado",     _brl(total_real))
    c3.metric("Atingimento",   f"{pct_geral:.1f}%")
    c4.metric("Saldo",         _brl(total_real - total_meta))

    st.progress(min(pct_geral/100, 1.0))
    st.divider()

    # Cards por fornecedor
    for row in metas:
        (mid, forn_n, forn_id, meta_v, meta_p,
         realizado, pedidos_feitos) = row

        pct    = min(realizado/meta_v*100, 100) if meta_v > 0 else 0
        saldo  = realizado - meta_v
        cor    = ("🟢" if pct >= 100 else
                  "🟡" if pct >= 70 else
                  "🟠" if pct >= 40 else "🔴")

        with st.container(border=True):
            col_n, col_m, col_r, col_p, col_pct = st.columns([2,1.5,1.5,1,1])
            col_n.markdown(f"**{forn_n}**")
            col_m.metric("Meta",      _brl(meta_v))
            col_r.metric("Realizado", _brl(realizado),
                         delta=_brl(saldo) if saldo != 0 else None)
            col_p.metric("Pedidos",   f"{pedidos_feitos}" +
                         (f"/{meta_p}" if meta_p else ""))
            col_pct.metric("Atingimento", f"{cor} {pct:.0f}%")
            st.progress(pct/100)


# ══════════════════════════════════════════════════════
# 2. DEFINIR / EDITAR META
# ══════════════════════════════════════════════════════
def _form_meta():
    _garantir_tabela()

    msg = st.session_state.pop("mt_msg", None)
    if msg: st.success(msg)

    forns = query("SELECT fornecedor_id, nome_fantasia FROM fornecedor WHERE ativo=1 ORDER BY nome_fantasia")
    if not forns:
        st.info("Nenhum fornecedor cadastrado.")
        return

    hoje = date.today()
    meses = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho",
             "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]

    col1, col2, col3 = st.columns(3)
    with col1:
        forn_sel = st.selectbox("Fornecedor", forns,
                                format_func=lambda x: x[1], key="mt_forn_form")
    with col2:
        ano_f = st.selectbox("Ano", list(range(hoje.year, hoje.year+2)),
                             key="mt_ano_form")
    with col3:
        mes_f = st.selectbox("Mês", range(1,13),
                             format_func=lambda x: meses[x-1],
                             index=hoje.month-1, key="mt_mes_form")

    # Verifica se já existe meta
    existe = query("""SELECT meta_id, meta_valor, meta_pedidos, observacao
                      FROM meta_fornecedor
                      WHERE fornecedor_id=? AND ano=? AND mes=? AND ativo=1""",
                   (forn_sel[0], ano_f, mes_f))

    if existe:
        st.info(f"Já existe meta para {forn_sel[1]} em {meses[mes_f-1]}/{ano_f}. "
                f"Editando...")
        meta_atual = existe[0][1]
        ped_atual  = existe[0][2] or 0
        obs_atual  = existe[0][3] or ""
        mid        = existe[0][0]
    else:
        meta_atual = 0.0
        ped_atual  = 0
        obs_atual  = ""
        mid        = None

    meta_v = st.number_input("Meta de faturamento (R$)", min_value=0.0,
                              value=float(meta_atual), format="%.2f",
                              key="mt_valor_form")
    meta_p = st.number_input("Meta de pedidos (quantidade, opcional)",
                              min_value=0, value=int(ped_atual), key="mt_ped_form")
    obs    = st.text_input("Observação", value=obs_atual, key="mt_obs_form")

    col_s, col_c = st.columns(2)
    salvar  = col_s.button("💾 Salvar meta", type="primary",
                            use_container_width=True, key="mt_salvar")
    if mid:
        excluir = col_c.button("🗑️ Remover meta", use_container_width=True,
                                key="mt_excluir")
    else:
        excluir = False

    if salvar:
        if meta_v <= 0:
            st.error("O valor da meta deve ser maior que zero.")
            return
        conn = conectar()
        if mid:
            conn.execute("""UPDATE meta_fornecedor SET
                meta_valor=?, meta_pedidos=?, observacao=?
                WHERE meta_id=?""",
                (meta_v, meta_p or None, obs.strip() or None, mid))
        else:
            conn.execute("""INSERT INTO meta_fornecedor
                (fornecedor_id, ano, mes, meta_valor, meta_pedidos, observacao, ativo)
                VALUES (?,?,?,?,?,?,1)""",
                (forn_sel[0], ano_f, mes_f, meta_v,
                 meta_p or None, obs.strip() or None))
        conn.commit(); conn.close()
        st.session_state["mt_msg"] = (
            f"✅ Meta de {_brl(meta_v)} para {forn_sel[1]} "
            f"em {meses[mes_f-1]}/{ano_f} salva!")
        st.rerun()

    if excluir:
        conn = conectar()
        conn.execute("UPDATE meta_fornecedor SET ativo=0 WHERE meta_id=?", (mid,))
        conn.commit(); conn.close()
        st.session_state["mt_msg"] = "Meta removida."
        st.rerun()


# ══════════════════════════════════════════════════════
# 3. HISTÓRICO DE METAS
# ══════════════════════════════════════════════════════
def _historico_metas():
    _garantir_tabela()

    forns = query("SELECT fornecedor_id, nome_fantasia FROM fornecedor WHERE ativo=1 ORDER BY nome_fantasia")
    forn_opts = [(0,"Todos os fornecedores")] + list(forns)
    forn_h = st.selectbox("Fornecedor", forn_opts,
                          format_func=lambda x: x[1], key="mt_hist_forn")

    hist = query("""
        SELECT f.nome_fantasia, m.ano, m.mes, m.meta_valor,
               COALESCE((
                   SELECT ROUND(SUM(pi.quantidade * pi.preco_final
                          * (1-COALESCE(p.desconto_geral,0)/100.0)),2)
                   FROM pedido p JOIN pedido_item pi ON pi.pedido_id=p.pedido_id
                   WHERE p.fornecedor_id=f.fornecedor_id
                     AND strftime('%Y',p.data_pedido)=CAST(m.ano AS TEXT)
                     AND strftime('%m',p.data_pedido)=printf('%02d',m.mes)
                     AND p.status_pedido NOT IN ('CANCELADO','RECUSADO')
                     AND pi.status_item NOT IN ('PENDENTE','DEVOLVIDO')
               ),0) AS realizado
        FROM meta_fornecedor m
        JOIN fornecedor f ON m.fornecedor_id=f.fornecedor_id
        WHERE m.ativo=1
          AND (? = 0 OR m.fornecedor_id=?)
        ORDER BY m.ano DESC, m.mes DESC, f.nome_fantasia
    """, (forn_h[0], forn_h[0]))

    if not hist:
        st.info("Nenhuma meta registrada.")
        return

    meses = ["Jan","Fev","Mar","Abr","Mai","Jun",
             "Jul","Ago","Set","Out","Nov","Dez"]

    rows = []
    for forn_n, ano, mes, meta_v, realizado in hist:
        pct = realizado/meta_v*100 if meta_v > 0 else 0
        rows.append({
            "Fornecedor": forn_n,
            "Período":    f"{meses[mes-1]}/{ano}",
            "Meta":       _brl(meta_v),
            "Realizado":  _brl(realizado),
            "Atingimento":f"{min(pct,100):.0f}%",
            "Status":     ("🟢 Atingida" if pct>=100 else
                           "🟡 Parcial"  if pct>=70  else
                           "🔴 Abaixo"),
        })

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

    buf = io.BytesIO()
    df.to_excel(buf, index=False, sheet_name="Histórico Metas")
    buf.seek(0)
    st.download_button("⬇️ Exportar Excel", data=buf,
                       file_name="historico_metas.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


# ══════════════════════════════════════════════════════
# META DE MIX — por produto, categoria ou linha
# ══════════════════════════════════════════════════════
def _garantir_meta_mix():
    """Cria tabela meta_mix com UNIQUE para evitar duplicatas."""
    conn = conectar()
    # Recria com UNIQUE se não existir corretamente
    conn.execute("""CREATE TABLE IF NOT EXISTS meta_mix (
        meta_mix_id   INTEGER PRIMARY KEY AUTOINCREMENT,
        fornecedor_id INTEGER NOT NULL,
        tipo          TEXT NOT NULL DEFAULT 'produto',
        referencia_id INTEGER,
        descricao     TEXT NOT NULL,
        ano           INTEGER NOT NULL,
        mes           INTEGER NOT NULL,
        meta_qtd      INTEGER,
        meta_clientes INTEGER,
        observacao    TEXT,
        ativo         INTEGER DEFAULT 1)""")
    conn.commit(); conn.close()


def _tela_meta_mix():
    _garantir_meta_mix()

    st.subheader("🎯 Metas de mix")
    st.caption(
        "Defina metas de penetração: quantos clientes devem comprar "
        "determinado produto, categoria ou linha em um período. "
        "Ex: colocar salsichas Specialli em 10 hamburguerias novas este mês."
    )

    msg = st.session_state.pop("mm_msg", None)
    if msg: st.success(msg)
    err = st.session_state.pop("mm_err", None)
    if err: st.error(err)

    forns = query("SELECT fornecedor_id, nome_fantasia FROM fornecedor WHERE ativo=1 ORDER BY nome_fantasia")
    hoje  = date.today()
    meses = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho",
             "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]

    # ── PAINEL — aparece sempre no topo ──────────────────────────────────
    st.markdown("#### Metas cadastradas")
    col_pf, col_pm, col_pa = st.columns(3)
    with col_pf:
        forn_v = st.selectbox("Fornecedor", forns,
                              format_func=lambda x: x[1], key="mm_v_forn")
    with col_pm:
        mes_v  = st.selectbox("Mês", range(1,13),
                              format_func=lambda x: meses[x-1],
                              index=hoje.month-1, key="mm_v_mes")
    with col_pa:
        ano_v  = st.selectbox("Ano", list(range(hoje.year, hoje.year-2, -1)),
                              key="mm_v_ano")

    metas_mix = query("""
        SELECT mm.meta_mix_id, mm.tipo, mm.referencia_id,
               mm.descricao, mm.meta_qtd, mm.meta_clientes, mm.observacao
        FROM meta_mix mm
        WHERE mm.fornecedor_id=? AND mm.ano=? AND mm.mes=? AND mm.ativo=1
        ORDER BY mm.tipo, mm.descricao
    """, (forn_v[0], ano_v, mes_v))

    if not metas_mix:
        st.info(f"Nenhuma meta de mix para {forn_v[1]} em {meses[mes_v-1]}/{ano_v}. "
                "Use o formulário abaixo para criar.")
    else:
        st.caption(f"{len(metas_mix)} meta(s) definida(s) para {forn_v[1]} — {meses[mes_v-1]}/{ano_v}")

        for row in metas_mix:
            (mmid, tipo, ref_id, desc, meta_qtd, meta_cli, obs) = row

            # Calcula realizado
            real_cli = 0; real_qtd = 0
            if tipo == "produto" and ref_id:
                r = query("""SELECT COUNT(DISTINCT p.cliente_id),
                                COALESCE(SUM(pi.quantidade),0)
                             FROM pedido p JOIN pedido_item pi ON pi.pedido_id=p.pedido_id
                             WHERE pi.produto_id=?
                               AND strftime('%Y',p.data_pedido)=?
                               AND strftime('%m',p.data_pedido)=?
                               AND p.status_pedido NOT IN ('CANCELADO','RECUSADO')""",
                          (ref_id, str(ano_v), f"{mes_v:02d}"))
                if r: real_cli, real_qtd = r[0][0], int(r[0][1] or 0)
            elif tipo == "categoria" and ref_id:
                r = query("""SELECT COUNT(DISTINCT p.cliente_id),
                                COALESCE(SUM(pi.quantidade),0)
                             FROM pedido p
                             JOIN pedido_item pi ON pi.pedido_id=p.pedido_id
                             JOIN produto pr ON pi.produto_id=pr.produto_id
                             WHERE pr.categoria_id=? AND p.fornecedor_id=?
                               AND strftime('%Y',p.data_pedido)=?
                               AND strftime('%m',p.data_pedido)=?
                               AND p.status_pedido NOT IN ('CANCELADO','RECUSADO')""",
                          (ref_id, forn_v[0], str(ano_v), f"{mes_v:02d}"))
                if r: real_cli, real_qtd = r[0][0], int(r[0][1] or 0)
            elif tipo == "linha" and ref_id:
                r = query("""SELECT COUNT(DISTINCT p.cliente_id),
                                COALESCE(SUM(pi.quantidade),0)
                             FROM pedido p
                             JOIN pedido_item pi ON pi.pedido_id=p.pedido_id
                             JOIN produto pr ON pi.produto_id=pr.produto_id
                             WHERE pr.linha_id=? AND p.fornecedor_id=?
                               AND strftime('%Y',p.data_pedido)=?
                               AND strftime('%m',p.data_pedido)=?
                               AND p.status_pedido NOT IN ('CANCELADO','RECUSADO')""",
                          (ref_id, forn_v[0], str(ano_v), f"{mes_v:02d}"))
                if r: real_cli, real_qtd = r[0][0], int(r[0][1] or 0)

            tipo_ico = {"produto":"📦","categoria":"🏷️","linha":"📋","livre":"🎯"}.get(tipo,"🎯")

            with st.container(border=True):
                # Linha principal
                c1, c2, c3, c4 = st.columns([3, 1.5, 1.5, 1])
                c1.markdown(f"**{tipo_ico} {desc}**")
                if obs: c1.caption(obs)

                if meta_cli:
                    pct_c = min(real_cli/meta_cli,1.0) if meta_cli else 0
                    cor_c = "🟢" if pct_c>=1 else "🟡" if pct_c>=0.5 else "🔴"
                    c2.metric("Clientes", f"{real_cli}/{meta_cli}",
                              f"{cor_c} {pct_c*100:.0f}%")
                if meta_qtd:
                    pct_q = min(real_qtd/meta_qtd,1.0) if meta_qtd else 0
                    cor_q = "🟢" if pct_q>=1 else "🟡" if pct_q>=0.5 else "🔴"
                    c3.metric("Qtd (Cx)", f"{real_qtd}/{meta_qtd}",
                              f"{cor_q} {pct_q*100:.0f}%")

                if meta_cli and meta_cli > 0:
                    st.progress(min(real_cli/meta_cli,1.0))

                # Edição/exclusão inline
                _key_ed = f"mm_edit_{mmid}"
                if st.session_state.get(_key_ed):
                    st.caption("**Editar meta:**")
                    col_e1, col_e2, col_e3 = st.columns(3)
                    with col_e1:
                        nova_desc = st.text_input("Descrição", value=desc,
                                                  key=f"mm_ed_desc_{mmid}")
                    with col_e2:
                        novo_cli  = st.number_input("Meta clientes", min_value=0,
                                                    value=int(meta_cli or 0),
                                                    key=f"mm_ed_cli_{mmid}")
                    with col_e3:
                        novo_qtd  = st.number_input("Meta qtd (Cx)", min_value=0,
                                                    value=int(meta_qtd or 0),
                                                    key=f"mm_ed_qtd_{mmid}")
                    nova_obs = st.text_input("Observação", value=obs or "",
                                            key=f"mm_ed_obs_{mmid}")
                    col_s2, col_c2 = st.columns(2)
                    if col_s2.button("💾 Salvar", key=f"mm_ed_save_{mmid}",
                                     type="primary", use_container_width=True):
                        conn = conectar()
                        conn.execute("""UPDATE meta_mix SET
                            descricao=?, meta_clientes=?, meta_qtd=?, observacao=?
                            WHERE meta_mix_id=?""",
                            (nova_desc.strip() or desc,
                             novo_cli or None, novo_qtd or None,
                             nova_obs.strip() or None, mmid))
                        conn.commit(); conn.close()
                        st.session_state.pop(_key_ed, None)
                        st.session_state["mm_msg"] = "✅ Meta atualizada."
                        st.rerun()
                    if col_c2.button("Cancelar", key=f"mm_ed_cancel_{mmid}",
                                     use_container_width=True):
                        st.session_state.pop(_key_ed, None); st.rerun()
                else:
                    col_ed, col_del = c4.columns(2)
                    if col_ed.button("✏️", key=f"mm_ed_btn_{mmid}",
                                     help="Editar meta", use_container_width=True):
                        st.session_state[_key_ed] = True; st.rerun()
                    # Exclusão com confirmação
                    _key_del = f"mm_del_confirm_{mmid}"
                    if st.session_state.get(_key_del):
                        if col_del.button("✅", key=f"mm_del_ok_{mmid}",
                                          help="Confirmar exclusão",
                                          use_container_width=True):
                            conn = conectar()
                            conn.execute("UPDATE meta_mix SET ativo=0 WHERE meta_mix_id=?",
                                        (mmid,))
                            conn.commit(); conn.close()
                            st.session_state.pop(_key_del, None)
                            st.session_state["mm_msg"] = "🗑️ Meta removida."
                            st.rerun()
                        st.warning("Clique ✅ para confirmar a exclusão.")
                    else:
                        if col_del.button("🗑️", key=f"mm_del_{mmid}",
                                          help="Remover meta",
                                          use_container_width=True):
                            st.session_state[_key_del] = True; st.rerun()

    st.divider()

    # ── FORMULÁRIO — nova meta ────────────────────────────────────────────
    st.markdown("#### Nova meta de mix")

    col1, col2, col3 = st.columns(3)
    with col1:
        forn_s = st.selectbox("Fornecedor", forns,
                              format_func=lambda x: x[1], key="mm_forn")
        ano_m  = st.selectbox("Ano", list(range(hoje.year, hoje.year+2)),
                              key="mm_ano")
    with col2:
        mes_m  = st.selectbox("Mês", range(1,13),
                              format_func=lambda x: meses[x-1],
                              index=hoje.month-1, key="mm_mes")
        tipo_m = st.selectbox("Tipo de meta",
                              ["Produto específico","Categoria","Linha","Livre"],
                              key="mm_tipo")
    with col3:
        meta_cli = st.number_input("Meta: nº de clientes",
                                   min_value=0, value=0, key="mm_cli",
                                   help="Quantos clientes devem comprar este item")
        meta_qtd = st.number_input("Meta: quantidade (Cx)",
                                   min_value=0, value=0, key="mm_qtd",
                                   help="Opcional — volume total em caixas")

    ref_id = None; ref_desc = ""
    if tipo_m == "Produto específico":
        prods = query("""SELECT p.produto_id,
                           p.descricao_curta || ' (' || p.codigo_produto || ')'
                         FROM produto p WHERE p.fornecedor_id=? AND p.ativo=1
                         ORDER BY p.descricao_curta""", (forn_s[0],))
        if prods:
            prod_s = st.selectbox("Produto", prods,
                                  format_func=lambda x: x[1], key="mm_prod")
            ref_id = prod_s[0]; ref_desc = prod_s[1]
        else:
            st.info("Nenhum produto para este fornecedor.")
    elif tipo_m == "Categoria":
        cats = query("""SELECT DISTINCT cat.categoria_id, cat.nome_categoria
            FROM produto p JOIN categoria cat ON p.categoria_id=cat.categoria_id
            WHERE p.fornecedor_id=? ORDER BY cat.nome_categoria""", (forn_s[0],))
        if cats:
            cat_s = st.selectbox("Categoria", cats,
                                 format_func=lambda x: x[1], key="mm_cat")
            ref_id = cat_s[0]; ref_desc = cat_s[1]
    elif tipo_m == "Linha":
        linhas = query("""SELECT DISTINCT l.linha_id, l.nome_linha
            FROM produto p JOIN linha l ON p.linha_id=l.linha_id
            WHERE p.fornecedor_id=? ORDER BY l.nome_linha""", (forn_s[0],))
        if linhas:
            lin_s = st.selectbox("Linha", linhas,
                                 format_func=lambda x: x[1], key="mm_lin")
            ref_id = lin_s[0]; ref_desc = lin_s[1]
    else:
        ref_desc = st.text_input("Descrição da meta",
                                 placeholder="Ex: Salsichas em hamburguerias",
                                 key="mm_desc_livre")

    obs_m = st.text_input("Observação (opcional)", key="mm_obs")

    # Verificação de duplicata antes de salvar
    if ref_desc:
        tipo_db = {"Produto específico":"produto","Categoria":"categoria",
                   "Linha":"linha","Livre":"livre"}.get(tipo_m,"livre")
        duplic = query("""SELECT meta_mix_id, meta_clientes, meta_qtd FROM meta_mix
            WHERE fornecedor_id=? AND tipo=? AND referencia_id IS ?
              AND descricao=? AND ano=? AND mes=? AND ativo=1""",
            (forn_s[0], tipo_db,
             ref_id,  # IS ? aceita None
             ref_desc.strip(), ano_m, mes_m))
        if duplic:
            st.warning(
                f"⚠️ Já existe uma meta para **{ref_desc}** em "
                f"{meses[mes_m-1]}/{ano_m}. "
                f"Edite-a no painel acima em vez de criar outra.")

    if st.button("💾 Salvar meta", type="primary",
                 use_container_width=True, key="mm_salvar"):
        if not ref_desc.strip() and tipo_m == "Livre":
            st.session_state["mm_err"] = "Preencha a descrição da meta."
            st.rerun()
        elif meta_cli == 0 and meta_qtd == 0:
            st.session_state["mm_err"] = "Defina ao menos uma meta (clientes ou quantidade)."
            st.rerun()
        else:
            tipo_db = {"Produto específico":"produto","Categoria":"categoria",
                       "Linha":"linha","Livre":"livre"}.get(tipo_m,"livre")
            conn = conectar()
            conn.execute("""INSERT INTO meta_mix
                (fornecedor_id, tipo, referencia_id, descricao,
                 ano, mes, meta_qtd, meta_clientes, observacao, ativo)
                VALUES (?,?,?,?,?,?,?,?,?,1)""",
                (forn_s[0], tipo_db, ref_id,
                 ref_desc.strip() or tipo_m,
                 ano_m, mes_m,
                 meta_qtd or None, meta_cli or None,
                 obs_m.strip() or None))
            conn.commit(); conn.close()
            # Muda painel para mostrar o fornecedor/mês recém-salvo
            st.session_state["mm_v_forn"] = forn_s
            st.session_state["mm_v_mes"]  = mes_m
            st.session_state["mm_v_ano"]  = ano_m
            st.session_state["mm_msg"] = (
                f"✅ Meta criada: {ref_desc or tipo_m} — "
                f"{meses[mes_m-1]}/{ano_m}. "
                "Veja no painel acima.")
            st.rerun()