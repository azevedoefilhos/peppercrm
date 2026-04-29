# pesquisa.py — PepperCRM — versao 2025-corrigida
# pesquisa.py — PepperCRM
# Coleta de preços no PDV — fluxo linear, estado persistido no banco

import streamlit as st
import os
import pandas as pd
import io
from datetime import date, datetime as _dt
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle,
                                Paragraph, Spacer, HRFlowable, KeepTogether)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from database import execute_write, execute_write, conectar, query, TIPOS_PONTO_EXTRA

UFS = ["SP","AC","AL","AM","AP","BA","CE","DF","ES","GO","MA","MG","MS","MT",
       "PA","PB","PE","PI","PR","RJ","RN","RO","RR","RS","SC","SE","TO"]


def _ir(p):
    st.session_state["pagina"] = p
    st.rerun()


def _brl(v):
    if v is None or v == 0: return "—"
    return f"R$ {v:,.2f}".replace(",","X").replace(".",",").replace("X",".")


def tela_pesquisa():
    # ── Processa ações pendentes de cadastro rápido ──────
    # Executado ANTES de qualquer widget, garantindo ciclo limpo
    _processar_acao_pendente()

    # Roteamento interno: lista | cabecalho | coleta | detalhe
    modo = st.session_state.get("pq_modo", "lista")
    pq_id = st.session_state.get("pq_id")

    if modo == "lista":
        _tela_lista()
    elif modo == "cabecalho":
        _tela_cabecalho()
    elif modo == "coleta" and pq_id:
        _tela_coleta(pq_id)
    elif modo == "detalhe" and pq_id:
        _tela_detalhe(pq_id)
    elif modo == "analise":
        _tela_analise_consolidada()
    else:
        st.session_state["pq_modo"] = "lista"
        st.rerun()


# Chaves de estado do cabeçalho — limpas a cada nova pesquisa
_CAB_KEYS = ["cab_cli_id","cab_pdv_id","_nc_acao","_nc_fn","_nc_cid","_nc_uf",
             "_nc_st","_nc_ob","_nc_erro","_nc_ok","_np_acao","_np_cli_id",
             "_np_nl","_np_tp","_np_nr","_np_end","_np_bai","_np_cid","_np_uf","_np_sp","_np_gr","_np_ob",
             "_np_erro","_np_ok","cab_data"]


def _limpar_estado_cabecalho():
    for k in _CAB_KEYS:
        st.session_state.pop(k, None)


def _processar_acao_pendente():
    """
    Processa ações de cadastro rápido (cliente/PDV) agendadas pelo clique
    do botão. Roda no topo do ciclo ANTES de qualquer widget, garantindo
    que st.rerun() seja sempre obedecido.
    """
    # ── Ação: novo cliente ────────────────────────────────
    if st.session_state.get("_nc_acao") == "salvar":
        fn_  = st.session_state.pop("_nc_fn",  "")
        cid_ = st.session_state.pop("_nc_cid", "")
        uf_  = st.session_state.pop("_nc_uf",  "SP")
        st__ = st.session_state.pop("_nc_st",  "prospecto")
        ob_  = st.session_state.pop("_nc_ob",  "")
        st.session_state.pop("_nc_acao", None)

        if not fn_.strip():
            st.session_state["_nc_erro"] = "Preencha o nome do cliente."
        else:
            existe = query(
                "SELECT cliente_id FROM cliente WHERE LOWER(nome_fantasia)=LOWER(?)",
                (fn_.strip(),))
            if existe:
                st.session_state["_nc_erro"] = (
                    f"Já existe um cliente com o nome '{fn_}'. Selecione-o acima.")
            else:
                conn = conectar()
                conn.execute(
                    "INSERT INTO cliente (nome_fantasia,cidade,estado,observacao,ativo,status) VALUES (?,?,?,?,0,?)",
                    (fn_.strip(), cid_ or None, uf_, ob_ or None, st__))
                conn.commit()
                novo_id = conn.execute(
                    "SELECT cliente_id FROM cliente WHERE nome_fantasia=? ORDER BY cliente_id DESC LIMIT 1",
                    (fn_.strip(),)).fetchone()[0]
                conn.close()
                # Guarda o ID e sinaliza que deve pular direto para PDV
                st.session_state["cab_cli_id"]   = novo_id
                st.session_state["_cab_fase"]    = "pdv"  # avança fase
        st.rerun()

    elif st.session_state.get("_nc_acao") == "cancelar":
        st.session_state.pop("_nc_acao", None)
        st.session_state["pq_modo"] = "lista"
        st.rerun()

    # ── Ação: novo PDV ────────────────────────────────────
    if st.session_state.get("_np_acao") == "salvar":
        cli_id_ = st.session_state.pop("_np_cli_id", None)
        nl_  = st.session_state.pop("_np_nl",  "")
        tp_  = st.session_state.pop("_np_tp",  "Supermercado")
        nr_  = st.session_state.pop("_np_nr",  "")
        end_ = st.session_state.pop("_np_end", "")
        bai_ = st.session_state.pop("_np_bai", "")
        cid_ = st.session_state.pop("_np_cid", "")
        uf_  = st.session_state.pop("_np_uf",  "SP")
        sp_  = st.session_state.pop("_np_sp",  "visitado")
        gr_  = st.session_state.pop("_np_gr",  "")
        ob_  = st.session_state.pop("_np_ob",  "")
        st.session_state.pop("_np_acao", None)

        if not nl_.strip():
            st.session_state["_np_erro"] = "Preencha o nome da loja."
        elif cli_id_ is None:
            st.session_state["_np_erro"] = "Cliente nao identificado. Recomece."
        else:
            existe = query(
                "SELECT pdv_id FROM pdv WHERE cliente_id=? AND LOWER(nome_loja)=LOWER(?)",
                (cli_id_, nl_.strip()))
            if existe:
                st.session_state["_np_erro"] = (
                    f"Este cliente ja tem um PDV com o nome '{nl_}'.")
            else:
                conn = conectar()
                conn.execute(
                    """INSERT INTO pdv
                       (cliente_id, numero_loja, nome_loja, tipo_pdv,
                        endereco, bairro, cidade, estado,
                        gerente, observacao, ativo, status)
                       VALUES (?,?,?,?,?,?,?,?,?,?,0,?)""",
                    (cli_id_, nr_ or None, nl_.strip(), tp_,
                     end_ or None, bai_ or None, cid_ or None, uf_,
                     gr_ or None, ob_ or None, sp_))
                conn.commit()
                novo_pdv_id = conn.execute(
                    "SELECT pdv_id FROM pdv WHERE cliente_id=? AND nome_loja=? ORDER BY pdv_id DESC LIMIT 1",
                    (cli_id_, nl_.strip())).fetchone()[0]
                conn.close()
                st.session_state["cab_pdv_id"]  = novo_pdv_id
                st.session_state["_cab_fase"]   = "fornecedor"
        st.rerun()

    elif st.session_state.get("_np_acao") == "cancelar":
        st.session_state.pop("_np_acao", None)
        st.session_state["pq_modo"] = "lista"
        st.rerun()


# ═══════════════════════════════════════════════════════
# TELA 1 — LISTA DE PESQUISAS
# ═══════════════════════════════════════════════════════

def _tela_lista():
    st.header("Pesquisa de preços")
    if st.button("⬅ Voltar ao menu"):
        _ir("home")

    col1, col2, col3 = st.columns([2,1,1])
    with col2:
        if st.button("➕ Nova pesquisa", type="primary", use_container_width=True):
            _limpar_estado_cabecalho()
            st.session_state["pq_modo"] = "cabecalho"
            st.session_state.pop("pq_id", None)
            st.rerun()
    with col3:
        if st.button("📊 Analise consolidada", use_container_width=True):
            st.session_state["pq_modo"] = "analise"
            st.rerun()

    st.divider()

    # ── Filtros ───────────────────────────────────────
    col1, col2 = st.columns(2)
    with col1:
        filtro_status = st.selectbox("Status",
                                     ["Todos","rascunho","finalizado"],
                                     key="fil_st")
    with col2:
        filtro_per = st.selectbox("Período",
                                  ["30 dias","60 dias","90 dias","Ano atual","Todos"],
                                  key="fil_per")

    # Filtro cliente/PDV e fornecedor
    todos_cli  = [("","Todos os clientes")] + [
        (str(r[0]), r[1]) for r in query(
            "SELECT cliente_id, nome_fantasia FROM cliente ORDER BY nome_fantasia")]
    todos_forn = [("","Todos os fornecedores")] + [
        (str(r[0]), r[1]) for r in query(
            "SELECT fornecedor_id, nome_fantasia FROM fornecedor WHERE ativo=1 ORDER BY nome_fantasia")]

    col1, col2, col3 = st.columns(3)
    with col1:
        fil_cli  = st.selectbox("Cliente / rede", todos_cli,
                                format_func=lambda x: x[1], key="fil_cli")
    with col2:
        fil_forn = st.selectbox("Fornecedor", todos_forn,
                                format_func=lambda x: x[1], key="fil_forn")
    with col3:
        TIPOS_PDV_PQ = ['Todos', 'Supermercado', 'Hipermercado', 'Atacadista', 'Mini Mercado', 'Mercearia', 'Emporio', 'Sacolao', 'Hortifruti', 'Acougue', 'Casa de Carnes', 'Peixaria', 'Padaria', 'Confeitaria', 'Delicatessen', 'Hamburgueria', 'Restaurante', 'Lanchonete', 'Bar / Boteco', 'Clube / Associacao', 'Outro']
        fil_tipo_pdv = st.selectbox("Tipo de PDV", TIPOS_PDV_PQ, key="fil_tipo_pdv_pq")

    where, params = ["1=1"], []
    if filtro_status != "Todos":
        where.append("pp.status=?"); params.append(filtro_status)
    for op, sql in {
        "30 dias":  "pp.data_pesquisa >= date('now','-30 days')",
        "60 dias":  "pp.data_pesquisa >= date('now','-60 days')",
        "90 dias":  "pp.data_pesquisa >= date('now','-90 days')",
        "Ano atual":"pp.data_pesquisa >= date('now','start of year')",
    }.items():
        if filtro_per == op: where.append(sql)
    if fil_cli[0]:
        where.append("pp.cliente_id=?"); params.append(int(fil_cli[0]))
    if fil_forn[0]:
        where.append("pp.fornecedor_id=?"); params.append(int(fil_forn[0]))
    if fil_tipo_pdv != "Todos":
        where.append("pdv.tipo_pdv=?"); params.append(fil_tipo_pdv)

    pesqs = query(f"""
        SELECT pp.pesquisa_id, pp.data_pesquisa,
               COALESCE(cli.nome_fantasia,'—')  AS cliente,
               COALESCE(pdv.nome_loja,'Direto') AS pdv,
               f.nome_fantasia                  AS forn,
               pp.status,
               COUNT(DISTINCT pi.produto_id)    AS prods,
               SUM(CASE WHEN pi.ruptura=1 THEN 1 ELSE 0 END) AS rupturas
        FROM pesquisa_preco pp
        LEFT JOIN cliente cli  ON pp.cliente_id=cli.cliente_id
        LEFT JOIN pdv          ON pp.pdv_id=pdv.pdv_id
        LEFT JOIN fornecedor f ON pp.fornecedor_id=f.fornecedor_id
        LEFT JOIN pesquisa_preco_item pi ON pp.pesquisa_id=pi.pesquisa_id
        WHERE {' AND '.join(where)}
          AND (? = 'Todos' OR COALESCE(pdv.tipo_pdv,'') = ?)
        GROUP BY pp.pesquisa_id, pp.data_pesquisa, cli.nome_fantasia, pdv.nome_loja, f.nome_fantasia, pp.status
        ORDER BY pp.data_pesquisa DESC
    """, tuple(params + [fil_tipo_pdv, fil_tipo_pdv]))

    if not pesqs:
        st.info("Nenhuma pesquisa encontrada.")
        return

    st.caption(f"{len(pesqs)} pesquisa(s) encontrada(s)")

    for r in pesqs:
        pid, data, cli, pdv_n, forn, status, prods, rupturas = r
        icone    = "🟡" if status == "rascunho" else "✅"
        rupt_txt = f"  🔴 {rupturas} ruptura(s)" if rupturas else ""

        with st.container():
            # Linha 1: info
            col1, col2, col3, col4 = st.columns([3.5, 1, 1, 0.7])
            with col1:
                st.markdown(
                    f"**{data}**  |  {cli}  /  {pdv_n}  |  {forn}\n\n"
                    f"{icone} {status.capitalize()}  —  {prods or 0} produto(s){rupt_txt}"
                )
            with col2:
                # Ver: vai direto ao detalhe (resultado limpo)
                if st.button("📋 Ver", key=f"ver_{pid}", use_container_width=True,
                             help="Ver resultado da pesquisa"):
                    st.session_state["pq_id"]   = pid
                    st.session_state["pq_modo"] = "detalhe"
                    st.rerun()
            with col3:
                # Continuar (rascunho) ou Reabrir (finalizado) — ação direta
                if status == "rascunho":
                    if st.button("▶️ Editar", key=f"cont_{pid}",
                                 use_container_width=True, help="Continuar coleta"):
                        st.session_state["pq_id"]   = pid
                        st.session_state["pq_modo"] = "coleta"
                        st.rerun()
                else:
                    if st.button("🔓 Reabrir", key=f"reab_{pid}",
                                 use_container_width=True, help="Reabrir para edição"):
                        conn = conectar()
                        conn.execute(
                            "UPDATE pesquisa_preco SET status='rascunho' WHERE pesquisa_id=?",
                            (pid,))
                        conn.commit(); conn.close()
                        st.session_state["pq_id"]   = pid
                        st.session_state["pq_modo"] = "coleta"
                        st.rerun()
            with col4:
                if st.button("🗑️", key=f"del_{pid}", help="Excluir pesquisa",
                             use_container_width=True):
                    conn = conectar()
                    conn.execute("DELETE FROM pesquisa_preco_item WHERE pesquisa_id=?", (pid,))
                    conn.execute("DELETE FROM pesquisa_preco WHERE pesquisa_id=?", (pid,))
                    conn.commit(); conn.close()
                    st.rerun()
            st.divider()


# ═══════════════════════════════════════════════════════
# TELA 2 — CABEÇALHO (nova pesquisa)
# ═══════════════════════════════════════════════════════

def _tela_cabecalho():
    st.header("Nova pesquisa — local e fornecedor")

    if st.button("⬅ Cancelar"):
        _limpar_estado_cabecalho()
        st.session_state["pq_modo"] = "lista"
        st.rerun()

    st.divider()

    # ── Fase atual ────────────────────────────────────
    # _cab_fase controla qual etapa mostrar:
    #   "cliente"    → mostra seletor de cliente (padrão)
    #   "pdv"        → cliente já escolhido, mostra seletor de PDV
    #   "fornecedor" → cliente+PDV escolhidos, mostra fornecedor
    fase = st.session_state.get("_cab_fase", "cliente")

    # ── Data ─────────────────────────────────────────
    data_pq = st.date_input("📅 Data da pesquisa", value=date.today(), key="cab_data")

    # ════════════════════════════════════════════════
    # PASSO 1 — CLIENTE
    # ════════════════════════════════════════════════
    st.subheader("1. Cliente / rede")

    cli_id_fixo = st.session_state.get("cab_cli_id")

    # Se cliente já foi escolhido/cadastrado, mostra só o resumo + botão trocar
    if cli_id_fixo:
        cli_info = query("SELECT nome_fantasia, cidade, estado FROM cliente WHERE cliente_id=?",
                         (cli_id_fixo,))
        if cli_info:
            nome_c, cid_c, uf_c = cli_info[0]
            col1, col2 = st.columns([4,1])
            col1.success(f"✅ {nome_c}  ({cid_c or '—'}/{uf_c or '—'})")
            if col2.button("Trocar", key="btn_trocar_cli"):
                st.session_state.pop("cab_cli_id", None)
                st.session_state.pop("cab_pdv_id", None)
                st.session_state["_cab_fase"] = "cliente"
                st.rerun()
        cli_id = cli_id_fixo
    else:
        # Mostra seletor
        todos_cli = query("""SELECT cliente_id, nome_fantasia, cidade, estado, status
            FROM cliente ORDER BY
            CASE status WHEN 'ativo' THEN 0 WHEN 'visitado' THEN 1 WHEN 'prospecto' THEN 2 ELSE 3 END,
            nome_fantasia""")

        cli_opts = [(None,"➕ Cadastrar novo cliente/prospecto...")] + [
            (c[0], f"{c[1]}  ({c[2]}/{c[3]})  [{c[4]}]") for c in todos_cli
        ]

        # Sem key fixa — usa key dinâmica para resetar quando necessário
        cli_sel = st.selectbox("Selecione o cliente", cli_opts,
                               format_func=lambda x: x[1],
                               key="cab_cli_sel")

        if cli_sel[0] is None:
            _form_novo_cliente()
            return
        else:
            # Cliente selecionado manualmente — grava e avança
            st.session_state["cab_cli_id"] = cli_sel[0]
            st.session_state["_cab_fase"]  = "pdv"
            cli_id = cli_sel[0]

    # ════════════════════════════════════════════════
    # PASSO 2 — PDV
    # ════════════════════════════════════════════════
    st.subheader("2. PDV / loja")

    pdv_id_fixo = st.session_state.get("cab_pdv_id")

    if pdv_id_fixo and pdv_id_fixo > 0:
        pdv_info = query("SELECT nome_loja, cidade, estado FROM pdv WHERE pdv_id=?",
                         (pdv_id_fixo,))
        if pdv_info:
            nl_p, cid_p, uf_p = pdv_info[0]
            col1, col2 = st.columns([4,1])
            col1.success(f"✅ {nl_p}  ({cid_p or '—'}/{uf_p or '—'})")
            if col2.button("Trocar", key="btn_trocar_pdv"):
                st.session_state.pop("cab_pdv_id", None)
                st.session_state["_cab_fase"] = "pdv"
                st.rerun()
        pdv_id = pdv_id_fixo
    else:
        pdvs = query("""SELECT pdv_id, numero_loja, nome_loja, cidade, estado, status
            FROM pdv WHERE cliente_id=? ORDER BY nome_loja""", (cli_id,))

        pdv_opts = [
            (None, "— Sem PDV (cliente direto / matriz)"),
            (-1,   "➕ Cadastrar novo PDV..."),
        ] + [(p[0], f"{p[2]}  ({p[3]}/{p[4]})  [{p[5]}]  Loja {p[1] or '—'}") for p in pdvs]

        pdv_sel = st.selectbox("Selecione o PDV", pdv_opts,
                               format_func=lambda x: x[1],
                               key="cab_pdv_sel")

        if pdv_sel[0] == -1:
            _form_novo_pdv(cli_id)
            return

        if pdv_sel[0] is not None and pdv_sel[0] > 0:
            # PDV selecionado manualmente
            st.session_state["cab_pdv_id"] = pdv_sel[0]
            st.session_state["_cab_fase"]  = "fornecedor"
            pdv_id = pdv_sel[0]
            info = query("SELECT cidade, estado FROM pdv WHERE pdv_id=?", (pdv_id,))
            if info: st.caption(f"📍 {info[0][0] or '—'} / {info[0][1] or '—'}")
        else:
            # Sem PDV (direto)
            pdv_id = None

    # ════════════════════════════════════════════════
    # PASSO 3 — FORNECEDOR (opcional para pesquisa livre)
    # ════════════════════════════════════════════════
    st.subheader("3. Fornecedor")

    forns = query("SELECT fornecedor_id, nome_fantasia FROM fornecedor WHERE ativo=1 ORDER BY nome_fantasia")

    # Modo de pesquisa — vinculada ou livre
    tipo_pesquisa = st.radio(
        "Tipo de pesquisa",
        ["vinculada", "livre"],
        format_func=lambda x:
            "🏭 Vinculada a um fornecedor que represento" if x == "vinculada"
            else "🔍 Livre — prospecção ou inteligência de mercado (sem fornecedor)",
        key="cab_tipo_pq",
        horizontal=True,
        help=(
            "Vinculada: você coleta preços dos concorrentes de um fornecedor específico. "
            "Livre: você está prospectando uma nova marca ou monitorando uma categoria "
            "sem vínculo com seus representados. Os dados ficam salvos para consulta futura."
        )
    )

    forn_id_pq = None
    forn_nome_pq = "— Pesquisa livre —"

    if tipo_pesquisa == "vinculada":
        if not forns:
            st.warning("Cadastre um fornecedor antes de iniciar uma pesquisa vinculada.")
            return
        col1, col2 = st.columns([2,1])
        with col1:
            forn_sel = st.selectbox(
                "Fornecedor (produtos que você representa)",
                forns, format_func=lambda x: x[1], key="cab_forn")
            forn_id_pq   = forn_sel[0]
            forn_nome_pq = forn_sel[1]
        with col2:
            obs_pq = st.text_input("Observação geral", key="cab_obs")
    else:
        # Pesquisa livre
        col1, col2 = st.columns([2,1])
        with col1:
            marca_livre = st.text_input(
                "Marca ou categoria pesquisada",
                placeholder="Ex: Camil, Massas artesanais, Molhos importados...",
                key="cab_marca_livre",
                help="Informe a marca ou categoria que você está monitorando")
            forn_nome_pq = marca_livre.strip() or "— Pesquisa livre —"
        with col2:
            obs_pq = st.text_input(
                "Observação geral",
                key="cab_obs",
                placeholder="Ex: prospecção para nova representação, análise de mercado...")
        st.info(
            "📋 **Pesquisa livre** — os dados coletados ficam salvos e podem ser "
            "vinculados a um fornecedor depois, caso você feche o contrato de representação. "
            "Use o modo EAN para identificar produtos automaticamente via Open Food Facts."
        )

    st.divider()

    # Resumo final
    cli_info2 = query("SELECT nome_fantasia FROM cliente WHERE cliente_id=?", (cli_id,))
    cli_nome  = cli_info2[0][0] if cli_info2 else "—"
    pdv_nome  = "Direto"
    if pdv_id:
        pdv_info2 = query("SELECT nome_loja FROM pdv WHERE pdv_id=?", (pdv_id,))
        pdv_nome  = pdv_info2[0][0] if pdv_info2 else "—"

    st.info(f"📍 **{cli_nome}**  |  {pdv_nome}  |  {forn_nome_pq}  |  {data_pq}")

    btn_label = "▶️ Iniciar coleta" if tipo_pesquisa == "vinculada" else "▶️ Iniciar pesquisa livre"
    if st.button(btn_label, type="primary",
                 use_container_width=True, key="btn_iniciar"):
        pq_id = execute_write("""INSERT INTO pesquisa_preco
            (data_pesquisa, pdv_id, cliente_id, fornecedor_id, observacao, status)
            VALUES (?,?,?,?,?,'rascunho')
            RETURNING pesquisa_id""",
            (str(data_pq), pdv_id, cli_id, forn_id_pq, obs_pq or None))
        _limpar_estado_cabecalho()
        st.session_state["pq_id"]   = pq_id
        st.session_state["pq_modo"] = "coleta"
        st.rerun()


def _form_novo_cliente():
    st.subheader("Cadastrar novo cliente / prospecto")

    # Exibe erro se houve no ciclo anterior
    if "_nc_erro" in st.session_state:
        st.error(st.session_state.pop("_nc_erro"))

    col1, col2 = st.columns(2)
    with col1:
        fn  = st.text_input("Nome / rede *",
                            placeholder="Ex: GPA, Carrefour, Atacadão...",
                            key="nc_fn")
        cid = st.text_input("Cidade", key="nc_cid")
        uf  = st.selectbox("UF", UFS, key="nc_uf")
    with col2:
        st_ = st.selectbox("Status",
                           ["prospecto","visitado","ativo","inativo"],
                           key="nc_status")
        ob  = st.text_input("Observação", key="nc_obs")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Cadastrar e continuar", type="primary",
                     use_container_width=True, key="btn_nc_salvar"):
            st.session_state["_nc_acao"] = "salvar"
            st.session_state["_nc_fn"]   = fn
            st.session_state["_nc_cid"]  = cid
            st.session_state["_nc_uf"]   = uf
            st.session_state["_nc_st"]   = st_
            st.session_state["_nc_ob"]   = ob
            st.rerun()
    with col2:
        if st.button("Cancelar", use_container_width=True, key="btn_nc_cancelar"):
            st.session_state["_nc_acao"] = "cancelar"
            st.rerun()


def _form_novo_pdv(cli_id):
    st.subheader("Cadastrar novo PDV")
    TIPOS_PDV = ["Supermercado","Hipermercado","Atacadista","Mini Mercado","Mercearia","Emporio","Sacolao","Hortifruti","Acougue","Casa de Carnes","Peixaria","Padaria","Confeitaria","Delicatessen","Hamburgueria","Restaurante","Lanchonete","Bar / Boteco","Clube / Associacao","Outro"]

    if "_np_erro" in st.session_state:
        st.error(st.session_state.pop("_np_erro"))

    col1, col2 = st.columns(2)
    with col1:
        nl   = st.text_input("Nome da loja *",
                             placeholder="Ex: Supermercado Bom Preco",
                             key="np_nome")
        tp_  = st.selectbox("Tipo de PDV", TIPOS_PDV, key="np_tipo")
        nr   = st.text_input("Numero / codigo (opcional)", key="np_nr")
        end_ = st.text_input("Endereco", key="np_end",
                             placeholder="Ex: Av. Brasil 1200")
        bai_ = st.text_input("Bairro", key="np_bairro")
        cid_ = st.text_input("Cidade", key="np_cid")
        uf_  = st.selectbox("UF", UFS, index=0, key="np_uf")
    with col2:
        sp_  = st.selectbox("Status",
                            ["visitado","prospecto","ativo","inativo"],
                            key="np_status")
        gr_  = st.text_input("Gerente (opcional)", key="np_gerente")
        ob_  = st.text_input("Observacao", key="np_obs")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Cadastrar PDV e continuar", type="primary",
                     use_container_width=True, key="btn_np_salvar"):
            st.session_state["_np_acao"]    = "salvar"
            st.session_state["_np_cli_id"]  = cli_id
            st.session_state["_np_nl"]      = nl
            st.session_state["_np_tp"]      = tp_
            st.session_state["_np_nr"]      = nr
            st.session_state["_np_end"]     = end_
            st.session_state["_np_bai"]     = bai_
            st.session_state["_np_cid"]     = cid_
            st.session_state["_np_uf"]      = uf_
            st.session_state["_np_sp"]      = sp_
            st.session_state["_np_gr"]      = gr_
            st.session_state["_np_ob"]      = ob_
            st.rerun()
    with col2:
        if st.button("Cancelar", use_container_width=True, key="btn_np_cancelar"):
            st.session_state["_np_acao"] = "cancelar"
            st.rerun()


# ═══════════════════════════════════════════════════════
# TELA 3 — COLETA (coração do sistema)
# ═══════════════════════════════════════════════════════


def _gerenciar_fotos(pq_id):
    """Gerencia múltiplas fotos da gôndola para uma pesquisa."""
    from datetime import datetime as _dt
    import time

    fotos = query(
        "SELECT foto_id, foto_path, legenda FROM pesquisa_foto WHERE pesquisa_id=? AND ativo=1 ORDER BY foto_id",
        (pq_id,)) or []

    # Exibe fotos já cadastradas em grade
    if fotos:
        st.caption(f"{len(fotos)} foto(s) registrada(s)")
        n_cols = min(len(fotos), 3)
        cols   = st.columns(n_cols)
        for i, (fid, fpath, fleg) in enumerate(fotos):
            with cols[i % n_cols]:
                if fpath and os.path.exists(fpath):
                    st.image(fpath, caption=fleg or f"Foto {i+1}",
                             use_container_width=True)
                else:
                    st.caption(f"⚠️ Arquivo não encontrado: {fpath}")
                # Botão excluir individual
                if st.button("🗑️ Excluir", key=f"del_foto_{fid}",
                             use_container_width=True):
                    conn = conectar()
                    conn.execute(
                        "UPDATE pesquisa_foto SET ativo=0 WHERE foto_id=?", (fid,))
                    conn.commit(); conn.close()
                    # Remove arquivo do disco
                    try:
                        if fpath and os.path.exists(fpath):
                            os.remove(fpath)
                    except Exception:
                        pass
                    st.rerun()
    else:
        st.caption("Nenhuma foto registrada ainda.")

    st.divider()

    # Upload de nova(s) foto(s) — accept_multiple_files=True
    novas = st.file_uploader(
        "Adicionar foto(s) da gôndola",
        type=["jpg","jpeg","png","webp"],
        accept_multiple_files=True,
        key=f"fotos_up_{pq_id}",
        help="Selecione uma ou mais fotos. Você pode adicionar legendas antes de salvar."
    )

    if novas:
        st.caption("Adicione uma legenda opcional para cada foto antes de salvar:")
        legendas = []
        for i, arq in enumerate(novas):
            leg = st.text_input(f"Legenda — {arq.name}",
                                placeholder="Ex: Gôndola resfriados, Seção frios...",
                                key=f"leg_foto_{pq_id}_{i}")
            legendas.append(leg)

        if st.button("💾 Salvar fotos", key=f"btn_salvar_fotos_{pq_id}",
                     type="primary", use_container_width=True):
            pasta = os.path.join(os.path.dirname(__file__), "fotos_pesquisa")
            os.makedirs(pasta, exist_ok=True)
            conn  = conectar()
            saved = 0
            for i, arq in enumerate(novas):
                ts       = int(time.time() * 1000)
                nome_arq = f"pq{pq_id}_{ts}_{i}_{arq.name}"
                caminho  = os.path.join(pasta, nome_arq)
                with open(caminho, "wb") as f_out:
                    f_out.write(arq.read())
                conn.execute(
                    """INSERT INTO pesquisa_foto
                       (pesquisa_id, foto_path, legenda, data_upload, ativo)
                       VALUES (?,?,?,?,1)""",
                    (pq_id, caminho,
                     legendas[i].strip() or None,
                     _dt.now().strftime("%Y-%m-%d %H:%M")))
                saved += 1
            conn.commit(); conn.close()
            st.success(f"✅ {saved} foto(s) salva(s)!")
            st.rerun()


def _tela_coleta(pq_id):
    # Carrega dados da pesquisa
    pq = query("""
        SELECT pp.pesquisa_id, pp.data_pesquisa,
               COALESCE(cli.nome_fantasia,'—'),
               COALESCE(pdv.nome_loja, cli.nome_fantasia,'—'),
               COALESCE(pdv.cidade,''), COALESCE(pdv.estado,''),
               f.nome_fantasia, f.fornecedor_id, pp.status
        FROM pesquisa_preco pp
        LEFT JOIN cliente cli  ON pp.cliente_id=cli.cliente_id
        LEFT JOIN pdv          ON pp.pdv_id=pdv.pdv_id
        LEFT JOIN fornecedor f ON pp.fornecedor_id=f.fornecedor_id
        WHERE pp.pesquisa_id=?
    """, (pq_id,))

    if not pq:
        st.error("Pesquisa não encontrada.")
        st.session_state["pq_modo"] = "lista"; st.rerun()
        return

    pid, data, cli, pdv_n, pdv_cid, pdv_uf, forn_n, forn_id, status = pq[0]

    loc = f"{pdv_n}  —  {pdv_cid}/{pdv_uf}" if pdv_cid else pdv_n

    # Exibe fotos da gôndola no detalhe
    fotos_det = query(
        "SELECT foto_id, foto_path, legenda FROM pesquisa_foto WHERE pesquisa_id=? AND ativo=1 ORDER BY foto_id",
        (pq_id,)) or []
    if fotos_det:
        with st.expander(f"📷 Fotos da gôndola ({len(fotos_det)})"):
            cols_f = st.columns(min(len(fotos_det), 3))
            for i, (fid, fpath, fleg) in enumerate(fotos_det):
                if fpath and os.path.exists(fpath):
                    cols_f[i % 3].image(fpath,
                        caption=fleg or f"Foto {i+1}",
                        use_container_width=True)
    st.success(f"📍 **{cli}**  |  {loc}  |  {forn_n}  |  {data}")

    col1, col2, col3, col4 = st.columns([3,1,1,1])
    with col2:
        if st.button("⬅ Lista", use_container_width=True):
            st.session_state["pq_modo"] = "lista"; st.rerun()
    with col3:
        if st.button("✏️ Cabeçalho", use_container_width=True,
                     help="Editar data, cliente, PDV ou fornecedor da pesquisa"):
            st.session_state[f"editar_cab_{pq_id}"] = True
            st.rerun()
    with col4:
        if st.button("✅ Finalizar", type="primary", use_container_width=True):
            conn = conectar()
            conn.execute("UPDATE pesquisa_preco SET status='finalizado' WHERE pesquisa_id=?", (pq_id,))
            conn.commit(); conn.close()
            st.session_state["pq_finalizada_id"] = pq_id
            st.session_state["pq_modo"] = "detalhe"; st.rerun()

    # ── Edição inline do cabeçalho ────────────────────
    if st.session_state.get(f"editar_cab_{pq_id}"):
        pq_full = query("""SELECT cliente_id, fornecedor_id, pdv_id,
                              data_pesquisa, observacao
                           FROM pesquisa_preco WHERE pesquisa_id=?""", (pq_id,))
        if pq_full:
            cli_id_a, forn_id_a, pdv_id_a, data_a, obs_a = pq_full[0]
            _form_editar_cabecalho_pesquisa(pq_id, cli_id_a, forn_id_a,
                                            pdv_id_a, data_a, obs_a)
        if st.button("✖ Fechar edição", key=f"fechar_cab_{pq_id}"):
            st.session_state.pop(f"editar_cab_{pq_id}", None); st.rerun()

    st.divider()

    # ── Upload de múltiplas fotos da gôndola ──────────
    with st.expander("📷 Fotos da gôndola"):
        _gerenciar_fotos(pq_id)

    # ── Alternância de modo ───────────────────────────
    modo_key = f"modo_coleta_{pq_id}"
    if modo_key not in st.session_state:
        st.session_state[modo_key] = "classico"

    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        if st.button(
            "📋 Clássico" if st.session_state[modo_key] != "classico" else "📋 Clássico ✓",
            use_container_width=True,
            type="primary" if st.session_state[modo_key] == "classico" else "secondary",
            key="btn_modo_classico",
            help="Seleciona produto de referência e coleta concorrentes vinculados"
        ):
            st.session_state[modo_key] = "classico"; st.rerun()
    with col_m2:
        if st.button(
            "⚡ Rápido" if st.session_state[modo_key] != "rapido" else "⚡ Rápido ✓",
            use_container_width=True,
            type="primary" if st.session_state[modo_key] == "rapido" else "secondary",
            key="btn_modo_rapido",
            help="Navega por categoria e marca — nossos e concorrentes numa lista"
        ):
            st.session_state[modo_key] = "rapido"; st.rerun()
    with col_m3:
        if st.button(
            "🔢 Por EAN" if st.session_state[modo_key] != "ean" else "🔢 Por EAN ✓",
            use_container_width=True,
            type="primary" if st.session_state[modo_key] == "ean" else "secondary",
            key="btn_modo_ean",
            help="Digite o EAN-13 — app identifica o produto automaticamente"
        ):
            st.session_state[modo_key] = "ean"; st.rerun()

    st.divider()

    if st.session_state[modo_key] == "classico":
        _coleta_modo_classico(pq_id, forn_id)
    elif st.session_state[modo_key] == "rapido":
        _coleta_modo_rapido(pq_id, forn_id)
    else:
        _coleta_modo_ean(pq_id, forn_id)



# ══════════════════════════════════════════════════════════════════════════
# LOOKUP EAN — busca local → Open Food Facts
# ══════════════════════════════════════════════════════════════════════════

def _lookup_ean_local(ean: str):
    """
    Busca o EAN no banco local.
    Retorna dict com tipo ('nosso'|'conc'|None) e dados do produto.
    """
    ean = ean.strip()
    if not ean: return None

    # 1. Produto nosso?
    nosso = query("""
        SELECT p.produto_id, p.descricao_curta, p.descricao,
               p.peso, p.unidade_medida, p.codigo_produto,
               f.nome_fantasia, f.fornecedor_id,
               COALESCE(cat.nome_categoria,'')
        FROM produto p
        JOIN fornecedor f ON p.fornecedor_id=f.fornecedor_id
        LEFT JOIN categoria cat ON p.categoria_id=cat.categoria_id
        WHERE p.ean=? AND p.ativo=1 LIMIT 1""", (ean,))
    if nosso:
        r = nosso[0]
        return {"tipo":"nosso","produto_id":r[0],
                "descricao":r[1] or r[2],"peso":r[3],
                "um":r[4],"codigo":r[5],"marca":r[6],
                "fornecedor_id":r[7],"categoria":r[8],"ean":ean}

    # 2. Concorrente com EAN?
    conc = query("""
        SELECT pc.produto_concorrente_id, pc.descricao_curta, pc.descricao,
               pc.peso, pc.unidade_medida,
               conc.marca_concorrente, conc.fornecedor_id,
               COALESCE(cat.nome_categoria,''),
               COALESCE(pc.auditavel,1)
        FROM produto_concorrente pc
        JOIN concorrente conc ON pc.concorrente_id=conc.concorrente_id
        LEFT JOIN categoria cat ON pc.categoria_id=cat.categoria_id
        WHERE pc.ean_concorrente=? AND pc.ativo=1 LIMIT 1""", (ean,))
    if conc:
        r = conc[0]
        return {"tipo":"conc","pc_id":r[0],
                "descricao":r[1] or r[2],"peso":r[3],
                "um":r[4],"marca":r[5],"fornecedor_id":r[6],
                "categoria":r[7],"auditavel":r[8],"ean":ean}

    return None


def _lookup_ean_openfoodfacts(ean: str):
    """
    Consulta Open Food Facts API (gratuita, sem autenticação).
    Retorna dict com dados do produto ou None se não encontrado.
    """
    import urllib.request, json
    url = f"https://world.openfoodfacts.org/api/v0/product/{ean}.json"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "PepperCRM/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
        if data.get("status") != 1:
            return None
        p = data.get("product", {})

        # Extrai campos relevantes
        marca   = p.get("brands","").split(",")[0].strip()
        desc    = (p.get("product_name_pt") or
                   p.get("product_name") or
                   p.get("generic_name","")).strip()
        qtd_raw = p.get("quantity","")  # ex: "500 g" ou "1 kg"
        peso    = None; um = "g"
        if qtd_raw:
            import re
            m = re.search(r"([\d.,]+)\s*(g|kg|ml|l|un)", qtd_raw.lower())
            if m:
                try:
                    peso = float(m.group(1).replace(",","."))
                    um   = m.group(2)
                except: pass
        cats_raw = p.get("categories_tags", [])
        cat_pt   = ""
        for c in cats_raw:
            if c.startswith("pt:"):
                cat_pt = c[3:].replace("-"," ").title(); break

        if not desc and not marca:
            return None

        return {"tipo":"off","ean":ean,
                "marca":marca,"descricao":desc,
                "peso":peso,"um":um,"categoria":cat_pt,
                "fonte":"Open Food Facts"}
    except Exception:
        return None


def _lookup_ean_concorrentes_sem_ean(ean_digitado: str, forn_id):
    """
    Retorna concorrentes sem EAN cadastrado — para sugerir vinculação.
    """
    return query("""
        SELECT pc.produto_concorrente_id, pc.descricao_curta,
               conc.marca_concorrente
        FROM produto_concorrente pc
        JOIN concorrente conc ON pc.concorrente_id=conc.concorrente_id
        WHERE conc.fornecedor_id=?
          AND (pc.ean_concorrente IS NULL OR pc.ean_concorrente='')
          AND pc.ativo=1
        ORDER BY conc.marca_concorrente, pc.descricao_curta
    """, (forn_id,))


# ══════════════════════════════════════════════════════════════════════════
# MODO EAN — coleta turbo por código de barras
# ══════════════════════════════════════════════════════════════════════════

def _coleta_modo_ean(pq_id, forn_id):
    """
    Modo mais rápido: digita EAN → app identifica o produto →
    usuário só preenche preço e dados da gôndola.
    Fluxo:
      EAN local conhecido     → preenche tudo, usuário só digita preço
      EAN em concorrente s/EAN→ sugere vincular ao cadastro existente
      EAN desconhecido        → busca Open Food Facts → pré-preenche cadastro
      EAN com dados divergentes→ oferece correção
    """
    st.subheader("🔢 Coleta por EAN")
    st.caption(
        "Digite o código de barras EAN-13 do produto. "
        "O app identifica automaticamente — nos seus produtos e nos concorrentes cadastrados. "
        "Produtos desconhecidos são buscados na base pública Open Food Facts."
    )

    # ── Campo EAN ────────────────────────────────────────────────────────
    col_ean, col_btn = st.columns([4,1])
    with col_ean:
        ean_input = st.text_input(
            "EAN-13",
            placeholder="7891234567890",
            key=f"ean_input_{pq_id}",
            label_visibility="collapsed",
            max_chars=14
        )
    with col_btn:
        buscar = st.button("🔍", key=f"ean_buscar_{pq_id}",
                           use_container_width=True,
                           help="Buscar produto")

    ean = ean_input.strip().replace(" ","").replace(".","").replace("-","")

    # Executa lookup ao pressionar Enter (campo preenchido) ou botão
    if not ean:
        # Mostra últimos produtos coletados nesta pesquisa
        _mini_historico_ean(pq_id)
        return

    if len(ean) not in (8, 12, 13):
        st.warning("EAN deve ter 8, 12 ou 13 dígitos.")
        return

    # ── LOOKUP LOCAL ──────────────────────────────────────────────────────
    resultado = _lookup_ean_local(ean)

    if resultado:
        _coleta_ean_produto_encontrado(pq_id, forn_id, resultado, ean)
        return

    # ── EAN não encontrado localmente ─────────────────────────────────────
    st.warning(f"EAN **{ean}** não encontrado na base local.")

    # ── OPÇÃO 1: Vincular a concorrente sem EAN ───────────────────────────
    sem_ean = _lookup_ean_concorrentes_sem_ean(ean, forn_id)
    if sem_ean:
        with st.expander(
            f"🔗 É um produto já cadastrado sem EAN? ({len(sem_ean)} disponíveis)",
            expanded=True
        ):
            st.caption("Selecione o produto se este EAN pertence a um concorrente já cadastrado:")
            opts = [(None,"— Não é nenhum destes —")] +                    [(s[0], f"{s[2]} — {s[1]}") for s in sem_ean]
            sel_vinc = st.selectbox("Produto cadastrado",
                                    opts, format_func=lambda x: x[1],
                                    key=f"ean_vinc_{pq_id}_{ean}")
            if sel_vinc and sel_vinc[0]:
                if st.button("✅ Vincular EAN e registrar preço",
                             key=f"ean_vinc_ok_{pq_id}",
                             type="primary", use_container_width=True):
                    from database import conectar as _con
                    conn = _con()
                    conn.execute(
                        "UPDATE produto_concorrente SET ean_concorrente=? "
                        "WHERE produto_concorrente_id=?",
                        (ean, sel_vinc[0]))
                    conn.commit(); conn.close()
                    st.session_state[f"ean_vinculado_{pq_id}"] = sel_vinc[0]
                    st.session_state[f"ean_input_{pq_id}"] = ""
                    st.success(f"✅ EAN vinculado! Relançando pesquisa...")
                    st.rerun()

    # ── OPÇÃO 2: Busca Open Food Facts ────────────────────────────────────
    st.divider()
    st.markdown("**Ou buscar na base pública:**")
    if st.button("🌐 Buscar na Open Food Facts",
                 key=f"ean_off_{pq_id}", use_container_width=True):
        st.session_state[f"ean_buscar_off_{pq_id}"] = True

    if st.session_state.get(f"ean_buscar_off_{pq_id}"):
        with st.spinner("Consultando Open Food Facts..."):
            off = _lookup_ean_openfoodfacts(ean)

        if off:
            marca_off = off.get("marca","")
            desc_off  = off.get("descricao","")
            peso_off  = off.get("peso","")
            um_off    = off.get("um","")
            st.success(f"Produto encontrado! {marca_off} — {desc_off} {peso_off}{um_off}")
            _form_cadastro_rapido_ean(pq_id, forn_id, ean, off)
        else:
            st.info("Produto não encontrado na Open Food Facts. "
                    "Preencha os dados manualmente abaixo.")
            _form_cadastro_rapido_ean(pq_id, forn_id, ean, None)

    # ── OPÇÃO 3: Cadastrar manualmente ────────────────────────────────────
    with st.expander("✍️ Cadastrar manualmente (sem busca online)"):
        _form_cadastro_rapido_ean(pq_id, forn_id, ean, None)


def _coleta_ean_produto_encontrado(pq_id, forn_id, resultado, ean):
    """Exibe o produto encontrado e abre direto os campos de coleta."""
    tipo = resultado["tipo"]

    if tipo == "nosso":
        _marca = resultado.get("marca","")
        _desc  = resultado.get("descricao","")
        _peso  = resultado.get("peso","")
        _um    = resultado.get("um","")
        st.success(f"Produto proprio: {_marca} — {_desc} {_peso}{_um}")
        # Produto nosso: registra na pesquisa como item de referencia
        # Produto nosso: registra na pesquisa como item de referência
        _form_coleta_rapida_ean(pq_id,
                                 tipo="nosso",
                                 produto_id=resultado["produto_id"],
                                 pc_id=None,
                                 label=resultado["descricao"],
                                 ean=ean)
    else:
        aud_label = "Auditavel" if resultado.get("auditavel",1) else "Nao auditavel"
        _m3 = resultado.get("marca","")
        _d3 = resultado.get("descricao","")
        _p3 = resultado.get("peso","")
        _u3 = resultado.get("um","")
        st.info(f"Concorrente encontrado: {_m3} — {_d3} {_p3}{_u3} | {aud_label}")
        _form_coleta_rapida_ean(pq_id,
                                 produto_id=None,
                                 pc_id=resultado["pc_id"],
                                 label=resultado["descricao"],
                                 ean=ean)


def _form_coleta_rapida_ean(pq_id, tipo, produto_id, pc_id, label, ean):
    """
    Formulário ultra-enxuto de coleta de dados da gôndola.
    Foco total em velocidade — só os campos essenciais.
    """
    k = f"ean_coleta_{pq_id}_{ean}"

    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            preco = st.number_input(
                "💰 Preço (R$) *",
                min_value=0.0, format="%.2f",
                step=0.01, key=f"{k}_preco")
        with col2:
            frentes = st.number_input(
                "Frentes", min_value=0,
                value=1, step=1, key=f"{k}_frt")
        with col3:
            col_of, col_pe = st.columns(2)
            oferta    = col_of.checkbox("Oferta", key=f"{k}_of")
            ponto_extra = col_pe.checkbox("P.Extra", key=f"{k}_pe")

        ruptura = st.checkbox("⚠️ Ruptura (sem estoque)", key=f"{k}_rup")

        # Vínculo com produto próprio (só para concorrentes)
        prod_vinc_id = None
        if tipo == "conc":
            # Busca produtos nossos do mesmo fornecedor para vincular
            prods_n = query("""SELECT produto_id, descricao_curta, codigo_produto
                FROM produto WHERE fornecedor_id=(
                    SELECT conc.fornecedor_id FROM produto_concorrente pc
                    JOIN concorrente conc ON pc.concorrente_id=conc.concorrente_id
                    WHERE pc.produto_concorrente_id=?
                ) AND ativo=1 ORDER BY descricao_curta""", (pc_id,)) if pc_id else []
            if prods_n:
                pv_opts = [(None,"— sem vínculo —")] + list(prods_n)
                pv_sel  = st.selectbox(
                    "Vincular ao produto próprio",
                    pv_opts,
                    format_func=lambda x: x[1] if x[0] is None
                                else f"{x[1]} ({x[2]})",
                    key=f"{k}_vinc")
                prod_vinc_id = pv_sel[0] if pv_sel else None

        obs = st.text_input("Observação (opcional)", key=f"{k}_obs",
                            placeholder="Ex: produto em destaque no fim do corredor")

        if st.button(f"💾 Salvar e próximo EAN",
                     type="primary", use_container_width=True,
                     key=f"{k}_salvar"):
            if preco <= 0 and not ruptura:
                st.error("Informe o preço ou marque Ruptura.")
                return

            conn = conectar()

            # Determina produto_id de referência
            pid_ref    = produto_id if tipo == "nosso" else None
            pc_id_ref  = pc_id     if tipo == "conc"  else None

            # Verifica se já existe item desta pesquisa + produto
            where_ex  = "pesquisa_id=? AND " +                         ("produto_id=?" if pid_ref else "produto_concorrente_id=?")
            val_ex    = (pq_id, pid_ref if pid_ref else pc_id_ref)
            existente = conn.execute(
                f"SELECT pesquisa_item_id FROM pesquisa_preco_item WHERE {where_ex} LIMIT 1",
                val_ex).fetchone()

            if existente:
                conn.execute("""UPDATE pesquisa_preco_item SET
                    preco=?, frentes=?, em_oferta=?, ponto_extra=?,
                    ruptura=?, observacao=?
                    WHERE pesquisa_item_id=?""",
                    (preco if not ruptura else None,
                     frentes, 1 if oferta else 0,
                     1 if ponto_extra else 0,
                     1 if ruptura else 0,
                     obs.strip() or None,
                     existente[0]))
            else:
                conn.execute("""INSERT INTO pesquisa_preco_item
                    (pesquisa_id, produto_id, produto_concorrente_id,
                     preco, frentes, em_oferta, ponto_extra, ruptura,
                     observacao)
                    VALUES (?,?,?,?,?,?,?,?,?)""",
                    (pq_id,
                     pid_ref, pc_id_ref,
                     preco if not ruptura else None,
                     frentes, 1 if oferta else 0,
                     1 if ponto_extra else 0,
                     1 if ruptura else 0,
                     obs.strip() or None))

            # Registra vínculo se informado
            if prod_vinc_id and pc_id_ref:
                conn.execute("""INSERT OR IGNORE INTO produto_concorrente_relacao
                    (produto_id, produto_concorrente_id, tipo_relacao)
                    VALUES (?,?,'indireto')""", (prod_vinc_id, pc_id_ref))

            conn.commit(); conn.close()

            # Limpa campo EAN para próxima leitura
            st.session_state.pop(f"ean_input_{pq_id}", None)
            st.session_state.pop(f"ean_buscar_off_{pq_id}", None)
            st.session_state[f"ean_ultimo_{pq_id}"] = label
            st.success(f"✅ **{label}** — salvo! Digite o próximo EAN.")
            st.rerun()


def _form_cadastro_rapido_ean(pq_id, forn_id, ean, dados_off):
    """
    Cadastra produto novo (concorrente) com dados pré-preenchidos do OFF
    e já abre o formulário de coleta de preço na sequência.
    """
    k = f"cad_ean_{pq_id}_{ean}"

    st.markdown("**Dados do produto novo:**")
    col1, col2 = st.columns(2)
    with col1:
        # Marcas concorrentes já cadastradas + opção nova
        marcas_ex = query("""SELECT concorrente_id, marca_concorrente
            FROM concorrente WHERE fornecedor_id=? AND ativo=1
            ORDER BY marca_concorrente""", (forn_id,))
        marca_opts = ["➕ Nova marca..."] + [m[1] for m in marcas_ex]
        marca_sel  = st.selectbox("Marca *", marca_opts, key=f"{k}_marca",
                                  index=(
                                      next((i+1 for i,m in enumerate(marcas_ex)
                                            if dados_off and
                                            dados_off.get("marca","").lower() in m[1].lower()),
                                           0) if dados_off else 0
                                  ))
        if marca_sel == "➕ Nova marca...":
            nova_marca = st.text_input("Nome da nova marca",
                                       value=dados_off.get("marca","") if dados_off else "",
                                       key=f"{k}_nova_marca")
        else:
            nova_marca = ""

        desc = st.text_input("Descrição completa *",
                             value=dados_off.get("descricao","") if dados_off else "",
                             key=f"{k}_desc")
        desc_c = st.text_input("Descrição curta (máx 56)",
                               value=(dados_off.get("descricao","")[:56]
                                      if dados_off else ""),
                               key=f"{k}_desc_c", max_chars=56)

    with col2:
        cats = query("SELECT categoria_id, nome_categoria FROM categoria "
                     "WHERE ativo=1 ORDER BY nome_categoria")
        cat_opts = [(None,"— sem categoria —")] + list(cats)
        # Tenta pré-selecionar pela categoria retornada pelo OFF
        cat_idx = 0
        if dados_off and dados_off.get("categoria"):
            for i, (cid, cnome) in enumerate(cats):
                if dados_off["categoria"].lower() in cnome.lower():
                    cat_idx = i+1; break
        cat_sel = st.selectbox("Categoria", cat_opts,
                               format_func=lambda x: x[1],
                               index=cat_idx, key=f"{k}_cat")

        peso = st.number_input("Peso/Volume",
                               value=float(dados_off.get("peso") or 0) if dados_off else 0.0,
                               min_value=0.0, format="%.0f",
                               key=f"{k}_peso")
        um   = st.selectbox("Unidade",
                            ["g","Kg","ml","L","UN"],
                            index=["g","Kg","ml","L","UN"].index(
                                dados_off.get("um","g") if dados_off and
                                dados_off.get("um","g") in ["g","Kg","ml","L","UN"]
                                else "g"),
                            key=f"{k}_um")
        auditavel = st.radio("Classificação",
                             [True, False],
                             format_func=lambda x:
                                "📊 Auditável" if x else "🚫 Não auditável",
                             key=f"{k}_aud", horizontal=True)

    # Preço — campo principal em destaque
    st.markdown("**Preço e dados da gôndola:**")
    col_p1, col_p2, col_p3 = st.columns(3)
    preco   = col_p1.number_input("💰 Preço (R$) *", min_value=0.0,
                                   format="%.2f", step=0.01, key=f"{k}_preco")
    frentes = col_p2.number_input("Frentes", min_value=0, value=1,
                                   key=f"{k}_frt")
    col_of, col_pe, col_ru = col_p3.columns(3)
    oferta      = col_of.checkbox("Oferta",   key=f"{k}_of")
    ponto_extra = col_pe.checkbox("P.Extra",  key=f"{k}_pe")
    ruptura     = col_ru.checkbox("Ruptura",  key=f"{k}_rup")

    if st.button("💾 Cadastrar produto e salvar preço",
                 type="primary", use_container_width=True,
                 key=f"{k}_salvar"):
        _nome = nova_marca.strip() if marca_sel=="➕ Nova marca..." else marca_sel
        if not _nome:
            st.error("Informe a marca."); return
        if not desc.strip():
            st.error("Informe a descrição."); return
        if preco <= 0 and not ruptura:
            st.error("Informe o preço ou marque Ruptura."); return

        conn = conectar()
        # Marca
        dup = conn.execute(
            "SELECT concorrente_id FROM concorrente "
            "WHERE LOWER(marca_concorrente)=LOWER(?) AND fornecedor_id=? AND ativo=1",
            (_nome, forn_id)).fetchone()
        if dup:
            conc_id = dup[0]
        else:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO concorrente (fornecedor_id, marca_concorrente, ativo) "
                "VALUES (?,?,1)", (forn_id, _nome))
            conc_id = cur.lastrowid

        # Produto concorrente
        cur = conn.cursor()
        cur.execute("""INSERT INTO produto_concorrente
            (concorrente_id, categoria_id, descricao, descricao_curta,
             peso, unidade_medida, ean_concorrente, auditavel, observacao, ativo)
            VALUES (?,?,?,?,?,?,?,?,?,1)""",
            (conc_id,
             cat_sel[0] if cat_sel and cat_sel[0] else None,
             desc.strip(), desc_c.strip() or None,
             peso or None, um, ean, 1 if auditavel else 0))
        pc_novo = cur.lastrowid
        conn.commit()

        # Item da pesquisa
        conn.execute("""INSERT INTO pesquisa_preco_item
            (pesquisa_id, produto_concorrente_id, preco,
             frentes, em_oferta, ponto_extra, ruptura)
            VALUES (?,?,?,?,?,?,?)""",
            (pq_id, pc_novo,
             preco if not ruptura else None,
             frentes, 1 if oferta else 0,
             1 if ponto_extra else 0,
             1 if ruptura else 0))
        conn.commit(); conn.close()

        st.session_state.pop(f"ean_input_{pq_id}", None)
        st.session_state.pop(f"ean_buscar_off_{pq_id}", None)
        st.session_state[f"ean_ultimo_{pq_id}"] = desc.strip()
        st.success(f"✅ **{desc.strip()}** cadastrado e preço salvo! Próximo EAN:")
        st.rerun()


def _mini_historico_ean(pq_id):
    """Exibe os últimos itens coletados nesta pesquisa para referência."""
    itens = query("""
        SELECT COALESCE(p.descricao_curta, pc.descricao_curta,'—') AS nome,
               COALESCE(conc.marca_concorrente, f.nome_fantasia,'—') AS marca,
               ppi.preco, ppi.em_oferta, ppi.ruptura, ppi.ponto_extra
        FROM pesquisa_preco_item ppi
        LEFT JOIN produto p         ON ppi.produto_id=p.produto_id
        LEFT JOIN fornecedor f      ON p.fornecedor_id=f.fornecedor_id
        LEFT JOIN produto_concorrente pc ON ppi.produto_concorrente_id=pc.produto_concorrente_id
        LEFT JOIN concorrente conc   ON pc.concorrente_id=conc.concorrente_id
        WHERE ppi.pesquisa_id=?
        ORDER BY ppi.pesquisa_item_id DESC LIMIT 8
    """, (pq_id,))

    if not itens:
        st.caption("Nenhum item coletado ainda nesta pesquisa.")
        return

    st.caption(f"**Últimos {len(itens)} item(ns) coletados:**")
    for nome, marca, preco, oferta, rupt, pe in itens:
        badges = ""
        if oferta: badges += " 🏷️"
        if pe:     badges += " ⭐"
        if rupt:   badges += " ❌"
        preco_s = (f"R$ {preco:,.2f}".replace(",","X").replace(".",",").replace("X",".")
                   if preco else "Ruptura")
        st.caption(f"• **{marca}** {nome} — {preco_s}{badges}")


def _coleta_modo_classico(pq_id, forn_id):
    """Modo original: seleciona MEU produto primeiro, depois coleta concorrentes vinculados."""
    st.subheader("Selecione o produto a pesquisar")

    cats_disp = query("""
        SELECT DISTINCT cat.categoria_id, cat.nome_categoria
        FROM produto p JOIN categoria cat ON p.categoria_id=cat.categoria_id
        WHERE p.fornecedor_id=? AND p.ativo=1
        ORDER BY cat.nome_categoria
    """, (forn_id,))

    col1, col2 = st.columns(2)
    with col1:
        cat_opts = [(None,"— Todas as categorias")] + list(cats_disp)
        cat_sel  = st.selectbox("Categoria", cat_opts, format_func=lambda x: x[1], key="col_cat")
        cat_id   = cat_sel[0] if cat_sel else None

    if cat_id:
        prods = query("""SELECT produto_id, codigo_produto, descricao_curta, descricao
            FROM produto WHERE fornecedor_id=? AND categoria_id=? AND ativo=1
            ORDER BY descricao_curta""", (forn_id, cat_id))
    else:
        prods = query("""SELECT produto_id, codigo_produto, descricao_curta, descricao
            FROM produto WHERE fornecedor_id=? AND ativo=1
            ORDER BY descricao_curta""", (forn_id,))

    if not prods:
        st.warning("Nenhum produto encontrado para este fornecedor.")
        return

    with col2:
        prod_sel = st.selectbox("Produto de referência", prods,
                                format_func=lambda x: x[2] or x[3] or x[1],
                                key="col_prod")

    prod_id   = prod_sel[0]
    prod_nome = prod_sel[2] or prod_sel[3] or f"#{prod_id}"

    total_prods  = len(prods)
    prods_feitos = query("""SELECT COUNT(DISTINCT produto_id) FROM pesquisa_preco_item
        WHERE pesquisa_id=? AND produto_id IS NOT NULL""", (pq_id,))
    qtd_feitos = prods_feitos[0][0] if prods_feitos else 0
    st.progress(qtd_feitos / total_prods if total_prods else 0,
                text=f"{qtd_feitos} de {total_prods} produto(s) com dados coletados")

    st.divider()
    _bloco_coleta_produto(pq_id, prod_id, prod_nome)

    with st.expander("➕ Encontrou um concorrente novo na gôndola?"):
        _form_novo_concorrente_rapido(pq_id, prod_id, prod_nome, forn_id)


def _coleta_modo_rapido(pq_id, forn_id):
    """
    Modo Rápido: navega Categoria → Marca → Produto (nosso 🟢 ou concorrente 🔴).
    Ao selecionar, resolve o vínculo e abre direto os campos de coleta.
    Preparado para futura leitura de código de barras (EAN).
    """
    st.subheader("⚡ Modo Rápido — selecione qualquer produto")
    st.caption("Nossos produtos 🟢 e concorrentes 🔴 numa lista unificada por categoria e marca.")

    # ── Passo 1: Categoria ────────────────────────────
    # Categorias com produtos nossos OU concorrentes ativos
    cats = query("""
        SELECT DISTINCT cat.categoria_id, cat.nome_categoria FROM categoria cat
        WHERE cat.ativo=1 AND (
            EXISTS (SELECT 1 FROM produto p
                    WHERE p.categoria_id=cat.categoria_id AND p.fornecedor_id=? AND p.ativo=1)
            OR
            EXISTS (SELECT 1 FROM produto_concorrente pc
                    JOIN concorrente conc ON pc.concorrente_id=conc.concorrente_id
                    WHERE pc.categoria_id=cat.categoria_id AND conc.fornecedor_id=? AND pc.ativo=1)
        )
        ORDER BY cat.nome_categoria
    """, (forn_id, forn_id))

    cat_opts = [(None,"— Todas as categorias")] + list(cats)
    cat_sel  = st.selectbox("1. Categoria", cat_opts,
                            format_func=lambda x: x[1], key=f"rp_cat_{pq_id}")
    cat_id   = cat_sel[0]

    # ── Passo 2: Marca ────────────────────────────────
    # Marcas: nossos fornecedores + marcas concorrentes que competem com o fornecedor
    if cat_id:
        marcas_nossas = query("""
            SELECT DISTINCT f.fornecedor_id AS id, f.nome_fantasia AS nome, 'nosso' AS tipo
            FROM produto p JOIN fornecedor f ON p.fornecedor_id=f.fornecedor_id
            WHERE p.fornecedor_id=? AND p.categoria_id=? AND p.ativo=1
        """, (forn_id, cat_id))
        marcas_conc = query("""
            SELECT DISTINCT conc.concorrente_id AS id, conc.marca_concorrente AS nome, 'conc' AS tipo
            FROM produto_concorrente pc
            JOIN concorrente conc ON pc.concorrente_id=conc.concorrente_id
            WHERE conc.fornecedor_id=? AND pc.categoria_id=? AND pc.ativo=1 AND conc.ativo=1
        """, (forn_id, cat_id))
    else:
        marcas_nossas = query("""
            SELECT DISTINCT f.fornecedor_id, f.nome_fantasia, 'nosso'
            FROM produto p JOIN fornecedor f ON p.fornecedor_id=f.fornecedor_id
            WHERE p.fornecedor_id=? AND p.ativo=1
        """, (forn_id,))
        marcas_conc = query("""
            SELECT DISTINCT conc.concorrente_id, conc.marca_concorrente, 'conc'
            FROM produto_concorrente pc
            JOIN concorrente conc ON pc.concorrente_id=conc.concorrente_id
            WHERE conc.fornecedor_id=? AND pc.ativo=1 AND conc.ativo=1
        """, (forn_id,))

    todas_marcas = (
        [(id_, f"🟢 {nome}", tipo) for id_, nome, tipo in marcas_nossas] +
        [(id_, f"🔴 {nome}", tipo) for id_, nome, tipo in marcas_conc]
    )
    todas_marcas.sort(key=lambda x: x[1])

    if not todas_marcas:
        st.info("Nenhum produto cadastrado para esta categoria.")
        return

    todas_marcas_opts = [(None, "— Todas as marcas", None)] + todas_marcas
    marca_sel = st.selectbox("2. Marca", todas_marcas_opts,
                             format_func=lambda x: x[1], key=f"rp_marca_{pq_id}")
    marca_id   = marca_sel[0]
    marca_tipo = marca_sel[2]

    # ── Passo 3: Produto ──────────────────────────────
    # Lista unificada: nossos 🟢 + concorrentes 🔴
    def _buscar_produtos_rapido(cat_id, marca_id, marca_tipo):
        """Retorna lista de produtos filtrada pela marca selecionada.
        - marca nossa  → só nossos produtos dessa marca/categoria
        - marca conc   → só produtos dessa marca concorrente
        - sem marca    → nossos + concorrentes da categoria (lista unificada)
        """
        prods = []

        # ── Nossos produtos ───────────────────────────
        # Só busca se NÃO houver uma marca concorrente selecionada
        if marca_tipo != "conc":
            filtros_n = ["p.fornecedor_id=?", "p.ativo=1"]
            params_n  = [forn_id]
            if cat_id:
                filtros_n.append("p.categoria_id=?"); params_n.append(cat_id)
            # marca_tipo == "nosso": filtro de fornecedor já cobre (é o mesmo forn_id)

            nossos = query(f"""
                SELECT p.produto_id, p.descricao_curta, p.codigo_produto
                FROM produto p WHERE {' AND '.join(filtros_n)}
                ORDER BY p.descricao_curta
            """, tuple(params_n))

            for pid_n, desc_n, cod_n in nossos:
                label = f"🟢 {desc_n or cod_n or f'#{pid_n}'}"
                prods.append(("nosso", pid_n, None, label))

        # ── Concorrentes ──────────────────────────────
        # Só busca se NÃO houver uma marca nossa selecionada
        if marca_tipo != "nosso":
            filtros_c = ["conc.fornecedor_id=?", "pc.ativo=1", "conc.ativo=1"]
            params_c  = [forn_id]
            if cat_id:
                filtros_c.append("pc.categoria_id=?"); params_c.append(cat_id)
            if marca_id and marca_tipo == "conc":
                # Marca concorrente específica selecionada — filtra por ela
                filtros_c.append("conc.concorrente_id=?"); params_c.append(marca_id)

            concorrentes = query(f"""
                SELECT pc.produto_concorrente_id, pc.descricao_curta,
                       conc.marca_concorrente
                FROM produto_concorrente pc
                JOIN concorrente conc ON pc.concorrente_id=conc.concorrente_id
                WHERE {' AND '.join(filtros_c)}
                ORDER BY conc.marca_concorrente, pc.descricao_curta
            """, tuple(params_c))

            for pc_id_c, desc_c, marca_c in concorrentes:
                label = f"🔴 {marca_c}  —  {desc_c or f'#{pc_id_c}'}"
                prods.append(("conc", pc_id_c, None, label))

        return prods

    lista_prods = _buscar_produtos_rapido(cat_id, marca_id, marca_tipo)

    if not lista_prods:
        st.info("Nenhum produto encontrado para os filtros selecionados.")
        return

    prod_opts = [(None, None, None, "— Selecione um produto")] + lista_prods
    prod_sel_r = st.selectbox("3. Produto", prod_opts,
                              format_func=lambda x: x[3], key=f"rp_prod_{pq_id}")

    if not prod_sel_r or prod_sel_r[0] is None:
        return

    tipo_sel, id_sel, _, label_sel = prod_sel_r

    st.divider()

    # ── Resolução do produto selecionado ─────────────
    # Função central: futuramente receberá EAN do leitor de câmera
    _resolver_e_coletar(pq_id, forn_id, tipo_sel, id_sel, label_sel)


def _resolver_e_coletar(pq_id, forn_id, tipo_sel, id_sel, label_sel):
    """
    Resolve o contexto do produto selecionado e exibe os campos de coleta.
    Ponto de integração futuro para leitura de EAN por câmera:
    basta chamar _resolver_e_coletar(pq_id, forn_id, tipo, id, label)
    com os dados obtidos do EAN.
    """

    if tipo_sel == "nosso":
        # ── Produto nosso ─────────────────────────────
        st.markdown(f"### {label_sel}")
        st.caption("Coletando dados do seu produto")
        meu = query("""SELECT pesquisa_item_id, preco, em_oferta, frentes,
                ruptura, ponto_extra, tipo_ponto_extra, observacao
            FROM pesquisa_preco_item
            WHERE pesquisa_id=? AND produto_id=? AND produto_concorrente_id IS NULL
            LIMIT 1""", (pq_id, id_sel))

        _card_item_editavel(
            key_prefix=f"rp_m_{pq_id}_{id_sel}",
            label=label_sel,
            cor="🟢",
            item_id=meu[0][0] if meu else None,
            dados_atuais=meu[0][1:] if meu else None,
            on_save=lambda d: _upsert_item(pq_id, id_sel, None, d)
        )

    else:
        # ── Produto concorrente ───────────────────────
        # Busca vínculos com nossos produtos
        vinculos = query("""
            SELECT rel.produto_id, p.descricao_curta, rel.tipo_relacao
            FROM produto_concorrente_relacao rel
            JOIN produto p ON rel.produto_id=p.produto_id
            WHERE rel.produto_concorrente_id=? AND p.fornecedor_id=?
            ORDER BY rel.tipo_relacao, p.descricao_curta
        """, (id_sel, forn_id))

        if not vinculos:
            # Sem vínculo — abre mini-form de cadastro/vínculo inline
            st.info(f"**{label_sel}** ainda não está vinculado a nenhum produto seu.")
            st.caption("Informe qual produto seu ele concorre e registre o preço agora:")
            # Reutiliza o form de novo concorrente rápido adaptado
            _form_vincular_e_coletar(pq_id, forn_id, id_sel, label_sel)

        elif len(vinculos) == 1:
            # Vínculo único — registra direto, apenas informa a referência
            prod_id_vinc, prod_nome_vinc, tipo_rel = vinculos[0]
            icone_rel = "🎯 Direto" if tipo_rel == "direto" else "↔️ Indireto"
            st.markdown(f"### {label_sel}")
            col_inf, col_btn = st.columns([3,1])
            col_inf.caption(f"📎 Referência automática: **🟢 {prod_nome_vinc}**  |  {icone_rel}")
            with col_btn:
                novo_tipo_v = "indireto" if tipo_rel == "direto" else "direto"
                if st.button(f"→ {novo_tipo_v.capitalize()}",
                             key=f"chg_tipo_{pq_id}_{id_sel}_{prod_id_vinc}",
                             help=f"Alterar tipo de concorrência para {novo_tipo_v}",
                             use_container_width=True):
                    rel = query("""SELECT relacao_id FROM produto_concorrente_relacao
                        WHERE produto_id=? AND produto_concorrente_id=?""",
                        (prod_id_vinc, id_sel))
                    if rel:
                        conn = conectar()
                        conn.execute("""UPDATE produto_concorrente_relacao
                            SET tipo_relacao=? WHERE relacao_id=?""",
                            (novo_tipo_v, rel[0][0]))
                        conn.commit(); conn.close()
                        st.success(f"Tipo alterado para {novo_tipo_v}!")
                        st.rerun()

            conc_item = query("""SELECT pesquisa_item_id, preco, em_oferta, frentes,
                    ruptura, ponto_extra, tipo_ponto_extra, observacao
                FROM pesquisa_preco_item
                WHERE pesquisa_id=? AND produto_id=? AND produto_concorrente_id=?
                LIMIT 1""", (pq_id, prod_id_vinc, id_sel))

            _card_item_editavel(
                key_prefix=f"rp_c_{pq_id}_{prod_id_vinc}_{id_sel}",
                label=label_sel,
                cor="🔴" if tipo_rel == "direto" else "🟠",
                item_id=conc_item[0][0] if conc_item else None,
                dados_atuais=conc_item[0][1:] if conc_item else None,
                on_save=lambda d: _upsert_item(pq_id, prod_id_vinc, id_sel, d)
            )

        else:
            # Múltiplos vínculos — exibe a lista e pede a escolha
            st.markdown(f"### {label_sel}")
            st.caption(f"⚠️ Este concorrente compete com {len(vinculos)} produtos seus. Selecione o de referência para esta coleta:")
            ref_opts = [(v[0], f"🟢 {v[1]}  —  {'🎯 Direto' if v[2]=='direto' else '↔️ Indireto'}") for v in vinculos]
            ref_sel = st.selectbox("Produto de referência", ref_opts,
                                   format_func=lambda x: x[1],
                                   key=f"rp_ref_{pq_id}_{id_sel}")
            prod_id_vinc = ref_sel[0]
            tipo_rel_m = next((v[2] for v in vinculos if v[0] == prod_id_vinc), "direto")

            conc_item = query("""SELECT pesquisa_item_id, preco, em_oferta, frentes,
                    ruptura, ponto_extra, tipo_ponto_extra, observacao
                FROM pesquisa_preco_item
                WHERE pesquisa_id=? AND produto_id=? AND produto_concorrente_id=?
                LIMIT 1""", (pq_id, prod_id_vinc, id_sel))

            _card_item_editavel(
                key_prefix=f"rp_cm_{pq_id}_{prod_id_vinc}_{id_sel}",
                label=label_sel,
                cor="🔴" if tipo_rel_m == "direto" else "🟠",
                item_id=conc_item[0][0] if conc_item else None,
                dados_atuais=conc_item[0][1:] if conc_item else None,
                on_save=lambda d: _upsert_item(pq_id, prod_id_vinc, id_sel, d)
            )


def _form_vincular_e_coletar(pq_id, forn_id, pc_id, label_conc):
    """
    Para concorrente sem vínculo: vincula a um produto nosso e coleta o preço.
    Tudo inline, sem sair da tela de coleta.
    """
    cats = query("SELECT categoria_id, nome_categoria FROM categoria WHERE ativo=1 ORDER BY nome_categoria")

    # Pré-seleciona categoria do produto concorrente
    cat_conc = query("SELECT categoria_id FROM produto_concorrente WHERE produto_concorrente_id=?", (pc_id,))
    cat_id_ref = cat_conc[0][0] if cat_conc and cat_conc[0][0] else None

    if cat_id_ref:
        prods_disp = query("""SELECT produto_id, codigo_produto, descricao_curta
            FROM produto WHERE fornecedor_id=? AND categoria_id=? AND ativo=1
            ORDER BY descricao_curta""", (forn_id, cat_id_ref))
    else:
        prods_disp = query("""SELECT produto_id, codigo_produto, descricao_curta
            FROM produto WHERE fornecedor_id=? AND ativo=1
            ORDER BY descricao_curta""", (forn_id,))

    if not prods_disp:
        st.warning("Nenhum produto nosso encontrado para vincular.")
        return

    with st.form(f"vincular_coletar_{pq_id}_{pc_id}", clear_on_submit=False):
        st.markdown("**Vincular ao produto de referência**")
        prod_ref = st.selectbox("Meu produto de referência", prods_disp,
                                format_func=lambda x: f"{x[1]} — {x[2]}")
        tipo_rel = st.selectbox("Tipo de concorrência", ["direto","indireto"])

        st.markdown("**Dados na gôndola agora**")
        col1, col2 = st.columns(2)
        with col1:
            preco_v   = st.number_input("💰 Preço (R$)", min_value=0.0, step=0.01, format="%.2f")
            oferta_v  = st.checkbox("🏷️ Em oferta")
            frentes_v = st.number_input("🧱 Frentes", min_value=0)
        with col2:
            ruptura_v = st.checkbox("⚠️ Ruptura")
            pe_v      = st.checkbox("📍 Ponto extra")
            tpe_v = None
            if pe_v:
                tpe_v = st.selectbox("Tipo", TIPOS_PONTO_EXTRA)
        obs_v = st.text_input("Observação")

        salvar_v = st.form_submit_button("✓ Vincular e registrar", type="primary")

    if salvar_v:
        if preco_v == 0 and not ruptura_v:
            st.warning("Informe o preço ou marque Ruptura.")
            return
        conn = conectar()
        # Cria vínculo
        try:
            conn.execute("""INSERT OR IGNORE INTO produto_concorrente_relacao
                (produto_id, produto_concorrente_id, tipo_relacao) VALUES (?,?,?)""",
                (prod_ref[0], pc_id, tipo_rel))
            conn.commit()
        except Exception: pass
        # Registra o item
        conn.execute("""DELETE FROM pesquisa_preco_item
            WHERE pesquisa_id=? AND produto_id=? AND produto_concorrente_id=?""",
            (pq_id, prod_ref[0], pc_id))
        conn.execute("""INSERT INTO pesquisa_preco_item
            (pesquisa_id, produto_id, produto_concorrente_id,
             preco, em_oferta, frentes, ruptura, ponto_extra, tipo_ponto_extra, observacao)
            VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (pq_id, prod_ref[0], pc_id,
             preco_v or None, 1 if oferta_v else 0,
             frentes_v or None, 1 if ruptura_v else 0,
             1 if pe_v else 0, tpe_v if pe_v else None, obs_v or None))
        conn.commit(); conn.close()
        st.success(f"Vinculado e registrado com sucesso!")
        st.rerun()


def _trocar_referencia(pq_id, forn_id, pc_id, prod_id_atual, prod_nome_atual):
    """Permite trocar o produto de referência inline no modo rápido."""
    prods = query("""SELECT produto_id, codigo_produto, descricao_curta
        FROM produto WHERE fornecedor_id=? AND ativo=1
        ORDER BY descricao_curta""", (forn_id,))
    if not prods: return

    ids_prods = [p[0] for p in prods]
    idx_atual = ids_prods.index(prod_id_atual) if prod_id_atual in ids_prods else 0

    with st.form(f"trocar_ref_{pq_id}_{pc_id}"):
        novo_ref = st.selectbox("Novo produto de referência", prods, index=idx_atual,
                                format_func=lambda x: f"{x[1]} — {x[2]}")
        novo_tipo = st.selectbox("Tipo", ["direto","indireto"])
        if st.form_submit_button("Confirmar troca"):
            conn = conectar()
            # Remove vínculo antigo e cria novo
            conn.execute("""DELETE FROM produto_concorrente_relacao
                WHERE produto_id=? AND produto_concorrente_id=?""",
                (prod_id_atual, pc_id))
            try:
                conn.execute("""INSERT OR IGNORE INTO produto_concorrente_relacao
                    (produto_id, produto_concorrente_id, tipo_relacao) VALUES (?,?,?)""",
                    (novo_ref[0], pc_id, novo_tipo))
                conn.commit()
                st.success(f"Referência atualizada para '{novo_ref[2]}'!")
                st.rerun()
            except Exception as e:
                st.error(str(e))
            finally:
                conn.close()


def _bloco_coleta_produto(pq_id, prod_id, prod_nome):
    """Renderiza campos de coleta para meu produto + todos os concorrentes vinculados."""

    # ── MEU PRODUTO ───────────────────────────────────
    st.markdown(f"### {prod_nome}")

    meu = query("""SELECT pesquisa_item_id, preco, em_oferta, frentes, ruptura, ponto_extra, tipo_ponto_extra, observacao
        FROM pesquisa_preco_item
        WHERE pesquisa_id=? AND produto_id=? AND produto_concorrente_id IS NULL
        LIMIT 1""", (pq_id, prod_id))

    _card_item_editavel(
        key_prefix=f"m_{pq_id}_{prod_id}",
        label=f"Meu produto — {prod_nome}",
        cor="🟢",
        item_id=meu[0][0] if meu else None,
        dados_atuais=meu[0][1:] if meu else None,
        on_save=lambda d: _upsert_item(pq_id, prod_id, None, d)
    )

    # ── CONCORRENTES VINCULADOS ───────────────────────
    concs = query("""
        SELECT pc.produto_concorrente_id,
               conc.marca_concorrente,
               pc.descricao_curta,
               rel.tipo_relacao
        FROM produto_concorrente_relacao rel
        JOIN produto_concorrente pc   ON rel.produto_concorrente_id=pc.produto_concorrente_id
        JOIN concorrente conc         ON pc.concorrente_id=conc.concorrente_id
        WHERE rel.produto_id=? AND pc.ativo=1 AND conc.ativo=1
        ORDER BY rel.tipo_relacao DESC, conc.marca_concorrente
    """, (prod_id,))

    if not concs:
        st.caption("💡 Nenhum concorrente vinculado a este produto. Configure em Concorrentes → Relações.")
    else:
        for pc_id, marca, desc_c, tipo_rel in concs:
            icone = "🎯" if tipo_rel == "direto" else "↔️"
            label = f"{marca}  —  {desc_c or ''}"

            conc_item = query("""SELECT pesquisa_item_id, preco, em_oferta, frentes, ruptura,
                    ponto_extra, tipo_ponto_extra, observacao
                FROM pesquisa_preco_item
                WHERE pesquisa_id=? AND produto_id=? AND produto_concorrente_id=?
                LIMIT 1""", (pq_id, prod_id, pc_id))

            _card_item_editavel(
                key_prefix=f"c_{pq_id}_{prod_id}_{pc_id}",
                label=f"{icone} {label}",
                cor="🔴" if tipo_rel == "direto" else "🟠",
                item_id=conc_item[0][0] if conc_item else None,
                dados_atuais=conc_item[0][1:] if conc_item else None,
                on_save=lambda d, _pc=pc_id: _upsert_item(pq_id, prod_id, _pc, d)
            )


def _card_item_editavel(key_prefix, label, cor, item_id, dados_atuais, on_save):
    """Card de coleta com modo visualização, edição e exclusão inline."""
    editando   = st.session_state.get(f"edit_{key_prefix}", False)
    confirmando = st.session_state.get(f"del_{key_prefix}", False)

    if dados_atuais and not editando and not confirmando:
        # ── Modo visualização ─────────────────────────
        preco, oferta, frentes, ruptura, pe, tpe, obs = dados_atuais
        with st.container():
            col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 1, 1, 1, 1.4])
            col1.markdown(f"{cor} **{label}**")
            col2.markdown(f"💰 **{_brl(preco)}**")
            col3.caption("🏷️" if oferta else "—")
            col4.caption(f"🧱 {frentes}" if frentes else "—")
            col5.caption("📍" if pe else "—")
            with col6:
                b1, b2 = st.columns(2)
                with b1:
                    if st.button("✏️", key=f"btn_edit_{key_prefix}",
                                 help="Editar este registro",
                                 use_container_width=True):
                        st.session_state[f"edit_{key_prefix}"] = True
                        st.rerun()
                with b2:
                    if st.button("🗑️", key=f"btn_del_{key_prefix}",
                                 help="Excluir este registro da pesquisa",
                                 use_container_width=True):
                        st.session_state[f"del_{key_prefix}"] = True
                        st.rerun()

    elif confirmando:
        # ── Confirmação de exclusão ───────────────────
        st.warning(
            f"Excluir o registro de **{label}** desta pesquisa? "
            f"O produto concorrente em si **não** será excluído."
        )
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Confirmar exclusão", key=f"conf_del_{key_prefix}",
                         type="primary", use_container_width=True):
                if item_id:
                    conn = conectar()
                    conn.execute(
                        "DELETE FROM pesquisa_preco_item WHERE pesquisa_item_id=?",
                        (item_id,)
                    )
                    conn.commit(); conn.close()
                st.session_state.pop(f"del_{key_prefix}", None)
                st.rerun()
        with col2:
            if st.button("Cancelar", key=f"canc_del_{key_prefix}",
                         use_container_width=True):
                st.session_state.pop(f"del_{key_prefix}", None)
                st.rerun()

    else:
        # ── Modo edição / entrada ─────────────────────
        with st.container():
            st.markdown(f"{cor} **{label}**")
            defaults = dados_atuais or (None, 0, 0, 0, 0, None, None)
            preco_d, oferta_d, frentes_d, ruptura_d, pe_d, tpe_d, obs_d = defaults

            with st.form(f"form_{key_prefix}"):
                col1, col2 = st.columns(2)
                with col1:
                    preco    = st.number_input("💰 Preço (R$) *", min_value=0.0,
                                               value=float(preco_d or 0),
                                               step=0.01, format="%.2f",
                                               key=f"preco_{key_prefix}")
                    em_oferta = st.checkbox("🏷️ Em oferta", value=bool(oferta_d),
                                            key=f"oferta_{key_prefix}")
                    frentes  = st.number_input("🧱 Frentes de gôndola",
                                               min_value=0, value=int(frentes_d or 0),
                                               key=f"frentes_{key_prefix}")
                with col2:
                    ruptura  = st.checkbox("⚠️ Ruptura (ausente)", value=bool(ruptura_d),
                                           key=f"ruptura_{key_prefix}")
                    pe       = st.checkbox("📍 Ponto extra", value=bool(pe_d),
                                           key=f"pe_{key_prefix}")
                    tpe = None
                    if pe:
                        tpe = st.selectbox("Tipo de ponto extra",
                                           TIPOS_PONTO_EXTRA,
                                           index=TIPOS_PONTO_EXTRA.index(tpe_d)
                                                 if tpe_d in TIPOS_PONTO_EXTRA else 0,
                                           key=f"tpe_{key_prefix}")
                    obs = st.text_input("Observação", value=obs_d or "",
                                        key=f"obs_{key_prefix}")

                col_s, col_c = st.columns(2)
                with col_s:
                    salvar = st.form_submit_button("✓ Salvar", type="primary")
                with col_c:
                    cancelar = st.form_submit_button("Cancelar")

            if salvar:
                if preco == 0 and not ruptura:
                    st.warning("Informe o preço ou marque Ruptura.")
                else:
                    on_save((preco or None, 1 if em_oferta else 0,
                             frentes or None, 1 if ruptura else 0,
                             1 if pe else 0, tpe if pe else None, obs or None))
                    st.session_state.pop(f"edit_{key_prefix}", None)
                    st.rerun()

            if cancelar:
                st.session_state.pop(f"edit_{key_prefix}", None)
                st.rerun()


def _upsert_item(pq_id, prod_id, pc_id, dados):
    preco, oferta, frentes, ruptura, pe, tpe, obs = dados
    conn = conectar()
    conn.execute("""DELETE FROM pesquisa_preco_item
        WHERE pesquisa_id=? AND produto_id=? AND produto_concorrente_id=?""",
        (pq_id, prod_id, pc_id))
    conn.execute("""INSERT INTO pesquisa_preco_item
        (pesquisa_id, produto_id, produto_concorrente_id,
         preco, em_oferta, frentes, ruptura, ponto_extra, tipo_ponto_extra, observacao)
        VALUES (?,?,?,?,?,?,?,?,?,?)""",
        (pq_id, prod_id, pc_id, preco, oferta, frentes, ruptura, pe, tpe, obs))
    conn.commit(); conn.close()


def _form_novo_concorrente_rapido(pq_id, prod_id, prod_nome, forn_id):
    """Cadastra marca + produto concorrente inline, vincula e já coleta o preço."""
    st.caption(f"Encontrou um concorrente de '{prod_nome}' que ainda não está na base? Cadastre aqui.")

    cats = query("SELECT categoria_id, nome_categoria FROM categoria WHERE ativo=1 ORDER BY nome_categoria")
    marcas_existentes = query("""SELECT conc.concorrente_id, conc.marca_concorrente
        FROM concorrente conc WHERE conc.fornecedor_id=? AND conc.ativo=1
        ORDER BY conc.marca_concorrente""", (forn_id,))

    # Busca a categoria do produto de referência para pré-selecionar
    cat_do_prod = query("""SELECT p.categoria_id, cat.nome_categoria
        FROM produto p LEFT JOIN categoria cat ON p.categoria_id=cat.categoria_id
        WHERE p.produto_id=?""", (prod_id,))
    cat_id_ref  = cat_do_prod[0][0] if cat_do_prod and cat_do_prod[0][0] else None
    cat_nome_ref = cat_do_prod[0][1] if cat_do_prod and cat_do_prod[0][1] else None

    # Monta lista de categorias com a do produto de referência no índice correto
    cats_opts   = [(None,"—")] + list(cats)
    cat_ids     = [c[0] for c in cats_opts]
    idx_cat_ref = cat_ids.index(cat_id_ref) if cat_id_ref and cat_id_ref in cat_ids else 0

    # Selectbox de marca FORA do form para permitir reatividade
    if cat_nome_ref:
        st.caption(f"💡 Categoria pré-selecionada: **{cat_nome_ref}** (mesma do produto de referência)")
    marca_opts = ["➕ Nova marca..."] + [m[1] for m in marcas_existentes]
    marca_sel  = st.selectbox("Marca", marca_opts, key=f"nc_mk_{prod_id}")
    nova_marca = ""
    if marca_sel == "➕ Nova marca...":
        nova_marca = st.text_input("Nome da nova marca *", key=f"nc_nm_{prod_id}",
                                   placeholder="Ex: Castelo, Heinz, Minhoto...")

    with st.form(f"f_novo_conc_{pq_id}_{prod_id}", clear_on_submit=True):
        st.markdown("**Identificação do produto**")
        col1, col2 = st.columns(2)
        with col1:
            ean_conc   = st.text_input("EAN-13 (código de barras)",
                                       placeholder="Digite ou escaneie...",
                                       key=f"nc_ean_{prod_id}")
            desc       = st.text_input("Descrição completa *",
                                       placeholder="Ex: Vinagre de Maçã Castelo 750ml",
                                       key=f"nc_desc_{prod_id}")
            desc_c     = st.text_input("Descrição curta", max_chars=56, key=f"nc_dc_{prod_id}")
        with col2:
            cat_sel    = st.selectbox("Categoria", cats_opts, index=idx_cat_ref,
                                      format_func=lambda x: x[1], key=f"nc_cat_{prod_id}")
            peso       = st.number_input("Peso/volume", min_value=0.0, format="%.3f",
                                         key=f"nc_peso_{prod_id}")
            um         = st.selectbox("Unidade", ["UN","kg","g","L","ml"], key=f"nc_um_{prod_id}")
            auditavel  = st.checkbox("📊 Auditável",
                                     value=True,
                                     key=f"nc_aud_{prod_id}",
                                     help="Desmarque se está na gôndola mas NÃO é concorrente — registrado para contexto, ignorado nas métricas.")
            tipo_rel   = st.selectbox("Tipo de concorrência",
                                      ["direto","indireto"],
                                      key=f"nc_tipo_{prod_id}",
                                      help="Direto = disputa o mesmo cliente. Indireto = categoria próxima.",
                                      disabled=not st.session_state.get(f"nc_aud_{prod_id}", True))

        obs_nc = st.text_input(
            "Observação",
            placeholder="Ex: marca própria fabricada pela Heinz, importado via La Pastina...",
            key=f"nc_obs_{prod_id}",
            help="Use para registrar fabricante de marca própria, importador, ou qualquer informação relevante do produto")

        st.markdown("**Dados na gôndola agora**")
        col1, col2 = st.columns(2)
        with col1:
            preco_n   = st.number_input("💰 Preço (R$)", min_value=0.0,
                                        step=0.01, format="%.2f", key=f"nc_preco_{prod_id}")
            oferta_n  = st.checkbox("🏷️ Em oferta", key=f"nc_of_{prod_id}")
            frentes_n = st.number_input("🧱 Frentes", min_value=0, key=f"nc_fr_{prod_id}")
        with col2:
            ruptura_n = st.checkbox("⚠️ Ruptura", key=f"nc_ru_{prod_id}")
            pe_n      = st.checkbox("📍 Ponto extra", key=f"nc_pe_{prod_id}")
            tpe_n = None
            if pe_n:
                tpe_n = st.selectbox("Tipo", TIPOS_PONTO_EXTRA, key=f"nc_tpe_{prod_id}")

        salvar = st.form_submit_button("Cadastrar, vincular e registrar preço ✓", type="primary")

    if salvar:
        if not desc.strip():
            st.error("Descrição completa é obrigatória.")
            return

        conn = conectar()
        # Determina conc_id
        if marca_sel == "➕ Nova marca...":
            if not nova_marca.strip():
                st.error("Informe o nome da nova marca.")
                conn.close(); return
            conc_id = execute_write(
                "INSERT INTO concorrente (fornecedor_id, marca_concorrente, ativo) VALUES (?,?,1) RETURNING concorrente_id",
                (forn_id, nova_marca.strip()))
        else:
            idx = [m[1] for m in marcas_existentes].index(marca_sel)
            conc_id = marcas_existentes[idx][0]

        # Cria produto concorrente
        pc_id_novo = execute_write("""INSERT INTO produto_concorrente
            (concorrente_id, categoria_id, descricao, descricao_curta,
             peso, unidade_medida, ean_concorrente, auditavel, ativo)
            VALUES (?,?,?,?,?,?,?,?,1)
            RETURNING produto_concorrente_id""",
            (conc_id,
             cat_sel[0] if cat_sel and cat_sel[0] else None,
             desc.strip(), desc_c.strip() or None,
             peso or None, um,
             ean_conc.strip() or None,
             1 if auditavel else 0))

        # Vincula ao produto de referência
        conn.execute("""INSERT OR IGNORE INTO produto_concorrente_relacao
            (produto_id, produto_concorrente_id, tipo_relacao) VALUES (?,?,?)""",
            (prod_id, pc_id_novo, tipo_rel))

        # Registra o preço
        conn.execute("""INSERT INTO pesquisa_preco_item
            (pesquisa_id, produto_id, produto_concorrente_id,
             preco, em_oferta, frentes, ruptura, ponto_extra, tipo_ponto_extra)
            VALUES (?,?,?,?,?,?,?,?,?)""",
            (pq_id, prod_id, pc_id_novo,
             preco_n or None,
             1 if oferta_n else 0,
             frentes_n or None,
             1 if ruptura_n else 0,
             1 if pe_n else 0,
             tpe_n if pe_n else None))
        conn.commit(); conn.close()
        # Limpa campos de nova marca para evitar pré-preenchimento na próxima pesquisa
        for _k in [f"nc_mk_{prod_id}", f"nc_nm_{prod_id}", f"nc_ean_{prod_id}",
                   f"nc_desc_{prod_id}", f"nc_dc_{prod_id}", f"nc_obs_{prod_id}"]:
            st.session_state.pop(_k, None)
        st.success(f"'{desc_c or desc}' cadastrado, vinculado e registrado!")
        st.rerun()


# ═══════════════════════════════════════════════════════
# TELA 4 — DETALHE / COMPARATIVO
# ═══════════════════════════════════════════════════════

def _form_editar_cabecalho_pesquisa(pq_id, cli_id_atual, forn_id_atual, pdv_id_atual, data_atual, obs_atual):
    """Corrige PDV, fornecedor, data e observacao de uma pesquisa ja salva.
    Cliente NAO e editavel — trocar de cliente corromperia os dados coletados.
    Busca PDVs e fornecedores independente do status ativo/prospecto do cliente."""
    import datetime as _datetime

    # Busca nome do cliente atual (independente de ser ativo ou nao)
    cli_info = query("SELECT nome_fantasia FROM cliente WHERE cliente_id=?", (cli_id_atual,))
    cli_nome = cli_info[0][0] if cli_info else f"Cliente #{cli_id_atual}"

    # Fornecedores ativos
    forns    = query("SELECT fornecedor_id, nome_fantasia FROM fornecedor WHERE ativo=1 ORDER BY nome_fantasia")
    forn_ids = [f[0] for f in forns]
    idx_forn = forn_ids.index(forn_id_atual) if forn_id_atual in forn_ids else 0

    # PDVs do cliente da pesquisa (independente de ativo — inclui prospectos)
    pdvs_e = query("""SELECT pdv_id, nome_loja, cidade FROM pdv
        WHERE cliente_id=? ORDER BY nome_loja""", (cli_id_atual,))
    pdv_opts_e = [(None, "— Sem PDV (entrega direta ao cliente)")] + [
        (p[0], f"{p[1]} ({p[2] or ''})") for p in pdvs_e]
    pdv_ids_e  = [p[0] for p in pdv_opts_e]
    idx_pdv_e  = pdv_ids_e.index(pdv_id_atual) if pdv_id_atual in pdv_ids_e else 0

    # Aviso explicativo
    st.info(
        f"📍 **{cli_nome}** — o cliente não pode ser alterado pois os dados "
        "já foram coletados para ele. Abaixo você pode corrigir a **data**, "
        "o **PDV**, o **fornecedor** ou a **observação**."
    )

    # Fornecedor nao editavel — exibe apenas como informacao
    forn_info = query("SELECT nome_fantasia FROM fornecedor WHERE fornecedor_id=?", (forn_id_atual,))
    forn_nome_atual = forn_info[0][0] if forn_info else f"Fornecedor #{forn_id_atual}"

    with st.form(f"edit_cab_pq_{pq_id}"):
        col1, col2 = st.columns(2)
        with col1:
            pdv_e  = st.selectbox("PDV", pdv_opts_e, index=idx_pdv_e,
                                  format_func=lambda x: x[1],
                                  key=f"ecp_pdv_{pq_id}",
                                  help="Selecione o PDV correto para esta pesquisa")
        with col2:
            st.text_input("Fornecedor", value=forn_nome_atual, disabled=True,
                          key=f"ecp_forn_ro_{pq_id}",
                          help="Nao editavel — os produtos pesquisados pertencem a este fornecedor")

        try:
            data_val = _datetime.date.fromisoformat(str(data_atual).strip()[:10])
        except Exception:
            data_val = _datetime.date.today()
        col3, col4 = st.columns(2)
        with col3:
            data_e = st.date_input("📅 Data da pesquisa", value=data_val,
                                   key=f"ecp_data_{pq_id}")
        with col4:
            obs_e  = st.text_input("Observação", value=obs_atual or "",
                                   key=f"ecp_obs_{pq_id}",
                                   placeholder="Ex: gôndola reformada, preço promocional...")

        salvar = st.form_submit_button("💾 Salvar alterações", type="primary",
                                       use_container_width=True)

    if salvar:
        novo_pdv_id = pdv_e[0]
        conn = conectar()
        conn.execute("""UPDATE pesquisa_preco SET
            pdv_id=?, data_pesquisa=?, observacao=?
            WHERE pesquisa_id=?""",
            (novo_pdv_id, str(data_e), obs_e or None, pq_id))
        conn.commit(); conn.close()
        pdv_label = pdv_e[1] if novo_pdv_id else "Sem PDV"
        # Sinaliza sucesso no session_state para mostrar apos rerun
        st.session_state[f"pq_cab_salvo_{pq_id}"] = (
            f"PDV corrigido para **{pdv_label}**  |  Data: {data_e}"
        )
        st.rerun()


def _tela_detalhe(pq_id):
    pq = query("""
        SELECT pp.pesquisa_id, pp.data_pesquisa,
               COALESCE(cli.nome_fantasia,'—'),
               COALESCE(pdv.nome_loja, cli.nome_fantasia,'—'),
               COALESCE(pdv.cidade,''), COALESCE(pdv.estado,''),
               f.nome_fantasia, f.fornecedor_id, pp.status, pp.observacao,
               pp.cliente_id, pp.pdv_id
        FROM pesquisa_preco pp
        LEFT JOIN cliente cli  ON pp.cliente_id=cli.cliente_id
        LEFT JOIN pdv          ON pp.pdv_id=pdv.pdv_id
        LEFT JOIN fornecedor f ON pp.fornecedor_id=f.fornecedor_id
        WHERE pp.pesquisa_id=?""", (pq_id,))

    if not pq:
        st.session_state["pq_modo"] = "lista"; st.rerun(); return

    pid, data, cli, pdv_n, pdv_cid, pdv_uf, forn_n, forn_id, status, obs, cli_id, pdv_id_atual = pq[0]

    icone_s = "✅" if status == "finalizado" else "🟡 Rascunho"

    # Banner de integracao com visitas (aparece ao finalizar)
    if st.session_state.get("pq_finalizada_id") == pq_id and status == "finalizado":
        st.success("Pesquisa finalizada! Deseja registrar esta visita ao PDV?")
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            if st.button("📋 Registrar visita agora", type="primary",
                         use_container_width=True, key="btn_reg_visita"):
                # Pre-preenche dados da visita com info da pesquisa
                st.session_state["vis_pre_cli_id"]  = cli_id if "cli_id" in dir() else None
                st.session_state["vis_pre_pesq_id"] = pq_id
                st.session_state["vis_modo"] = "nova"
                st.session_state.pop("pq_finalizada_id", None)
                st.session_state["pagina"] = "visitas"
                st.rerun()
        with col_v2:
            if st.button("Continuar sem registrar", use_container_width=True,
                         key="btn_skip_visita"):
                st.session_state.pop("pq_finalizada_id", None)
                st.rerun()
    loc = f"{pdv_n}  —  {pdv_cid}/{pdv_uf}" if pdv_cid else pdv_n

    # Cabeçalho
    st.header(f"Resultado da pesquisa  {icone_s}")
    col_a, col_b = st.columns([3,1])
    with col_a:
        st.markdown(
            f"**📍 {cli}**  |  {loc}  |  **{forn_n}**  |  {data}"
        )
        if obs: st.caption(f"Observação: {obs}")
    with col_b:
        if st.button("⬅ Voltar à lista", use_container_width=True, key="det_voltar"):
            st.session_state["pq_modo"] = "lista"; st.rerun()

    # Botões de ação
    col1, col2, col3 = st.columns(3)
    with col1:
        if status == "rascunho" and st.button("▶️ Continuar coleta",
                                              use_container_width=True, key="det_cont"):
            st.session_state["pq_modo"] = "coleta"; st.rerun()
    with col2:
        if status == "finalizado" and st.button("🔓 Reabrir para edição",
                                               use_container_width=True, key="det_reab"):
            conn = conectar()
            conn.execute("UPDATE pesquisa_preco SET status='rascunho' WHERE pesquisa_id=?", (pq_id,))
            conn.commit(); conn.close()
            st.session_state["pq_modo"] = "coleta"; st.rerun()
    with col3:
        pass  # reservado

    # Banner de sucesso da correcao de cabecalho (persiste apos rerun)
    cab_salvo_msg = st.session_state.pop(f"pq_cab_salvo_{pq_id}", None)
    if cab_salvo_msg:
        st.success(f"Cabecalho salvo: {cab_salvo_msg}")

    # Expander de correcao de cabecalho — disponivel sempre
    lbl_exp = "✅ Cabecalho salvo" if cab_salvo_msg else "✏️ Corrigir cabecalho da pesquisa"
    with st.expander(lbl_exp, expanded=False):
        _form_editar_cabecalho_pesquisa(pq_id, cli_id, forn_id,
                                        pdv_id_atual,
                                        data, obs)

    st.divider()

    # Opção: comparar com tabela de preços do cliente
    tabelas_cli = query("""
        SELECT tp.tabela_preco_id, tp.nome_tabela, tp.prazo_pagamento
        FROM cliente_fornecedor cf
        JOIN tabela_preco tp ON cf.tabela_preco_id=tp.tabela_preco_id
        WHERE cf.cliente_id=? AND cf.fornecedor_id=? AND cf.ativo=1
    """, (cli_id, forn_id)) if cli_id else []

    tabelas_extra = query("""
        SELECT tabela_preco_id, nome_tabela, prazo_pagamento
        FROM tabela_preco WHERE fornecedor_id=? AND ativo=1
        ORDER BY nome_tabela
    """, (forn_id,))

    todas_tabs = list({r[0]:r for r in (tabelas_cli + tabelas_extra)}.values())
    usar_tabela = False
    tab_id_sel  = None
    if todas_tabs:
        col1, col2 = st.columns([3,1])
        with col1:
            tab_opts = [(None,"— Sem comparação de preço")] + [
                (t[0], f"{t[1]} ({t[2]})") for t in todas_tabs]
            tab_sel = st.selectbox("Comparar preços com tabela de venda:",
                                   tab_opts, format_func=lambda x: x[1],
                                   key="det_tab")
            tab_id_sel = tab_sel[0]
            usar_tabela = tab_id_sel is not None

    st.divider()

    # Produtos pesquisados — busca tanto pelo produto_id direto
    # quanto pelo produto_id herdado dos itens de concorrente (compatibilidade)
    prods_r = query("""
        SELECT DISTINCT pi.produto_id, pr.descricao_curta
        FROM pesquisa_preco_item pi
        JOIN produto pr ON pi.produto_id=pr.produto_id
        WHERE pi.pesquisa_id=? AND pi.produto_id IS NOT NULL
        ORDER BY pr.descricao_curta
    """, (pq_id,))

    if not prods_r:
        # Diagnóstico: mostra o que existe no banco para essa pesquisa
        raw = query("""
            SELECT pi.pesquisa_item_id, pi.produto_id, pi.produto_concorrente_id,
                   pi.preco, pi.ruptura
            FROM pesquisa_preco_item pi
            WHERE pi.pesquisa_id=?
        """, (pq_id,))
        if raw:
            st.warning(
                f"Esta pesquisa tem {len(raw)} item(ns) no banco, mas nenhum com "
                f"`produto_id` preenchido. Isso indica que foram gravados apenas "
                f"itens de concorrentes sem produto de referência associado, "
                f"ou que houve um problema de gravação. "
                f"Use **🔓 Reabrir para edição** e refaça a coleta."
            )
            st.dataframe(pd.DataFrame(raw, columns=["item_id","produto_id","concorrente_id","preco","ruptura"]),
                         use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum item registrado nesta pesquisa. Use 🔓 Reabrir para edição.")
        return

    linhas_export   = []
    rupturas_total  = 0
    pe_total        = 0

    # Funções auxiliares para comparação por kg/L
    def _normalizar_peso(peso, unidade):
        """Converte peso/volume para kg ou L (unidade base)."""
        if not peso or peso <= 0:
            return None, None
        u = (unidade or "").lower().strip()
        if u in ("kg", "l", ""):   return peso, "kg/L"
        if u == "g":               return peso / 1000, "kg"
        if u in ("ml",):           return peso / 1000, "L"
        if u in ("un", "cx", "pc"): return None, None
        return peso, u

    def _preco_vol(preco, peso, unidade):
        """Retorna preço por kg ou L, ou None se não aplicável."""
        p_norm, _ = _normalizar_peso(peso, unidade)
        if not preco or not p_norm: return None
        return round(preco / p_norm, 4)

    def _fmt_dif(dif, pct):
        """Formata diferença com valor e percentual."""
        if dif is None: return "—"
        s = f"+{_brl(dif)}" if dif > 0 else _brl(dif)
        p = f" ({'+' if pct and pct>0 else ''}{pct:.1f}%)" if pct is not None else ""
        return f"{s}{p}"

    for pid_r, pnome_r in prods_r:
        # Preço UNITÁRIO da tabela de venda (preco_caixa / unidades_caixa)
        preco_tab       = None
        preco_tab_label = None
        preco_tab_vol   = None   # preço por kg ou L da tabela
        if usar_tabela:
            pt = query("""
                SELECT tpi.preco_caixa,
                       COALESCE(p.unidades_caixa, 1) AS un_cx,
                       p.unidade_medida,
                       p.peso
                FROM tabela_preco_item tpi
                JOIN produto p ON tpi.produto_id=p.produto_id
                WHERE tpi.tabela_preco_id=? AND tpi.produto_id=?
            """, (tab_id_sel, pid_r))
            if pt:
                preco_cx, un_cx, um_p, peso_p = pt[0]
                un_cx = un_cx if un_cx and un_cx > 0 else 1
                preco_tab = round(preco_cx / un_cx, 4)
                preco_tab_label = (
                    f"{_brl(preco_tab)}/un  "
                    f"(cx {_brl(preco_cx)}  c/ {un_cx} un)"
                )
                # Preço por kg/L do nosso produto (para comparação indireta)
                preco_tab_vol = _preco_vol(preco_tab, peso_p, um_p)

        proprio = query("""SELECT preco, em_oferta, frentes, ruptura, ponto_extra, tipo_ponto_extra
            FROM pesquisa_preco_item
            WHERE pesquisa_id=? AND produto_id=? AND produto_concorrente_id IS NULL
            LIMIT 1""", (pq_id, pid_r))

        concs_r = query("""
            SELECT conc.marca_concorrente, pc.descricao_curta,
                   pi.preco, pi.frentes, pi.em_oferta,
                   pi.ruptura, pi.ponto_extra, pi.tipo_ponto_extra,
                   COALESCE(rel.tipo_relacao,'—'),
                   pc.peso, pc.unidade_medida
            FROM pesquisa_preco_item pi
            JOIN produto_concorrente pc   ON pi.produto_concorrente_id=pc.produto_concorrente_id
            JOIN concorrente conc         ON pc.concorrente_id=conc.concorrente_id
            LEFT JOIN produto_concorrente_relacao rel
                   ON rel.produto_id=? AND rel.produto_concorrente_id=pc.produto_concorrente_id
            WHERE pi.pesquisa_id=? AND pi.produto_id=?
            ORDER BY rel.tipo_relacao, conc.marca_concorrente
        """, (pid_r, pq_id, pid_r))

        # Score de competitividade baseado nos concorrentes diretos
        score_icon  = ""
        score_tip   = ""
        if concs_r and proprio:
            preco_meu = proprio[0][0]
            diretos   = [c for c in concs_r if c[8] == "direto" and c[2]]
            if preco_meu and diretos:
                media_conc = sum(c[2] for c in diretos) / len(diretos)
                dif_pct    = (preco_meu - media_conc) / media_conc * 100
                if dif_pct <= -5:
                    score_icon = "  🟢"
                    score_tip  = f"Você está {abs(dif_pct):.1f}% mais barato que a media dos concorrentes diretos"
                elif dif_pct >= 5:
                    score_icon = "  🔴"
                    score_tip  = f"Você está {dif_pct:.1f}% mais caro que a media dos concorrentes diretos"
                else:
                    score_icon = "  🟡"
                    score_tip  = f"Preço similar à media dos concorrentes diretos (dif: {dif_pct:+.1f}%)"

        titulo = f"**{pnome_r}**{score_icon}"
        if proprio and proprio[0][3]: titulo += "  ⚠️ RUPTURA"

        with st.expander(titulo, expanded=True):
            if score_tip:
                st.caption(f"Score: {score_tip}")
            # ── Meu produto ───────────────────────────────
            if proprio:
                vp, of, fr, ru, pe, tpe = proprio[0]
                rupturas_total += int(ru or 0)
                pe_total       += int(pe or 0)

                st.markdown("**🟢 Meu produto**")
                col1, col2, col3, col4, col5 = st.columns(5)
                col1.metric("Preço pesquisado", _brl(vp))
                if usar_tabela:
                    col2.metric("Meu preço unit. (tab.)", _brl(preco_tab))
                    if preco_tab_label:
                        col2.caption(preco_tab_label)
                    diff_tab = round(vp - preco_tab, 2) if (vp and preco_tab) else None
                    pct_tab  = round((vp - preco_tab) / preco_tab * 100, 1) if (vp and preco_tab) else None
                    sinal    = f"+{_brl(diff_tab)}" if diff_tab and diff_tab > 0 else _brl(diff_tab)
                    sinal_pct = f" ({'+' if pct_tab and pct_tab>0 else ''}{pct_tab:.1f}%)" if pct_tab else ""
                    col3.metric("Dif. (PDV - tab.)", f"{sinal}{sinal_pct}" if diff_tab else "—",
                                help="Preço pesquisado no PDV menos seu preço unitário da tabela")
                else:
                    col2.metric("Frentes", fr or "—")
                    col3.caption("")
                col4.caption("🏷️ Oferta" if of else "—")
                col5.caption(f"📍 {tpe}" if pe else ("⚠️ Ruptura" if ru else "—"))
                if usar_tabela and fr:
                    st.caption(f"Frentes: {fr}")
            else:
                st.caption("🟢 Meu produto — não pesquisado neste PDV.")

            # ── Concorrentes ─────────────────────────────
            if not concs_r:
                st.caption("Nenhum concorrente registrado para este produto.")
            else:
                st.markdown("**Concorrentes:**")
                rows_tab = []
                for mc, dc, pc_v, fc, of_c, ru_c, pe_c, tpe_c, tipo, peso_c, um_c in concs_r:
                    preco_base = proprio[0][0] if proprio else None

                    # ── Diferença vs preço pesquisado ─────
                    diff_conc = round(pc_v - preco_base, 2) if (pc_v and preco_base) else None
                    pct_conc  = round((pc_v - preco_base) / preco_base * 100, 1) if (pc_v and preco_base) else None

                    # ── Diferença vs tabela (valor + %) ──
                    diff_tab_c = round(pc_v - preco_tab, 2) if (pc_v and preco_tab) else None
                    pct_tab_c  = round((pc_v - preco_tab) / preco_tab * 100, 1) if (pc_v and preco_tab) else None

                    def _fmt_dif(dif, pct):
                        if dif is None: return "—"
                        s = f"+{_brl(dif)}" if dif > 0 else _brl(dif)
                        p = f" ({'+' if pct and pct>0 else ''}{pct:.1f}%)" if pct is not None else ""
                        return f"{s}{p}"

                    # ── Preço por kg/L (só para indireto) ─
                    dif_vol_str = "—"
                    if tipo == "indireto" and usar_tabela and pc_v:
                        # Busca peso do NOSSO produto diretamente (não depende de preco_tab_vol)
                        peso_meu_db = query("""
                            SELECT p.peso, p.unidade_medida
                            FROM produto p WHERE p.produto_id=?
                        """, (pid_r,))
                        peso_meu_v  = peso_meu_db[0][0] if peso_meu_db else None
                        um_meu_v    = peso_meu_db[0][1] if peso_meu_db else None

                        if preco_tab and peso_meu_v and peso_c:
                            preco_meu_vol  = _preco_vol(preco_tab, peso_meu_v, um_meu_v)
                            preco_conc_vol = _preco_vol(pc_v, peso_c, um_c)
                            if preco_meu_vol and preco_conc_vol:
                                dif_v = round(preco_conc_vol - preco_meu_vol, 4)
                                pct_v = round(dif_v / preco_meu_vol * 100, 1)
                                _, um_meu_label  = _normalizar_peso(peso_meu_v, um_meu_v)
                                _, um_c_label    = _normalizar_peso(peso_c, um_c)
                                # Usa a mesma unidade base (ambos devem ser kg ou L)
                                label = um_meu_label or um_c_label or "kg/L"
                                dif_vol_str = (
                                    f"{_fmt_dif(dif_v, pct_v)}  "
                                    f"(conc: {_brl(preco_conc_vol)}/{label}"
                                    f" | meu: {_brl(preco_meu_vol)}/{label})"
                                )
                            elif not preco_meu_vol:
                                dif_vol_str = "⚠️ sem peso no produto"
                            elif not preco_conc_vol:
                                dif_vol_str = "⚠️ sem peso no concorrente"
                        elif not preco_tab:
                            dif_vol_str = "—"  # sem tabela selecionada
                        elif not peso_meu_v:
                            dif_vol_str = "⚠️ cadastre peso no produto"
                        elif not peso_c:
                            dif_vol_str = "⚠️ cadastre peso no concorrente"

                    row = {
                        "Marca":    mc,
                        "Produto":  dc or "—",
                        "Tipo":     "🎯 Direto" if tipo=="direto" else ("↔️ Indireto" if tipo=="indireto" else "—"),
                        "Preço":    _brl(pc_v),
                        "Frentes":  fc or "—",
                        "Oferta":   "🏷️" if of_c else "—",
                        "Ruptura":  "⚠️" if ru_c else "—",
                        "Pt.Extra": tpe_c if pe_c else "—",
                    }
                    if usar_tabela:
                        row["Dif. vs minha tab."] = _fmt_dif(diff_tab_c, pct_tab_c)
                        if tipo == "indireto":
                            row["Dif. vs tab. (kg/L)"] = dif_vol_str
                    else:
                        row["Dif. vs meu preço"] = _fmt_dif(diff_conc, pct_conc)

                    rows_tab.append(row)
                    linhas_export.append({
                        "Produto meu":      pnome_r,
                        "Preço pesq.":      preco_base or 0,
                        "Preço unit. tab.": preco_tab or 0,
                        "Concorrente":      mc,
                        "Prod. conc.":      dc,
                        "Preço conc.":      pc_v or 0,
                        "Tipo":             tipo,
                        "Dif. vs pesq.":    diff_conc or 0,
                        "% vs pesq.":       pct_conc or 0,
                        "Dif. vs tab.":     diff_tab_c or 0,
                        "% vs tab.":        pct_tab_c or 0,
                        "Dif. vs tab.(kg/L)": dif_vol_str if tipo=="indireto" else "n/a",
                        "Frentes conc.":    fc,
                        "Oferta":           "Sim" if of_c else "Não",
                        "Ruptura":          "Sim" if ru_c else "Não",
                        "Ponto extra":      tpe_c or "Não",
                    })
                st.dataframe(pd.DataFrame(rows_tab), use_container_width=True, hide_index=True)

    # Resumo
    st.divider()
    col1, col2, col3 = st.columns(3)
    col1.metric("Produtos pesquisados", len(prods_r))
    col2.metric("Rupturas detectadas",  rupturas_total)
    col3.metric("Pontos extras",        pe_total)

    # Historico de precos por produto neste PDV
    st.divider()
    pdv_id_det = query("SELECT pdv_id FROM pesquisa_preco WHERE pesquisa_id=?", (pq_id,))
    pdv_id_det = pdv_id_det[0][0] if pdv_id_det else None

    with st.expander("📈 Historico de precos neste PDV", expanded=False):
        if not pdv_id_det:
            st.caption("Pesquisa sem PDV — historico nao disponivel.")
        else:
            prod_hist_opts = [(p[0], p[1]) for p in prods_r]
            sel_prod_h = st.selectbox("Produto",
                                      prod_hist_opts,
                                      format_func=lambda x: x[1],
                                      key=f"hist_prod_{pq_id}")
            if sel_prod_h:
                hist = query("""
                    SELECT pp.data_pesquisa,
                           ROUND(pi_n.preco, 2) AS preco_nosso,
                           COUNT(DISTINCT pi_c.produto_concorrente_id) AS qtd_conc,
                           ROUND(AVG(CASE WHEN rel.tipo_relacao='direto'
                                    THEN pi_c.preco END), 2)           AS media_direto,
                           ROUND(MIN(CASE WHEN rel.tipo_relacao='direto'
                                    THEN pi_c.preco END), 2)           AS min_direto,
                           ROUND(MAX(CASE WHEN rel.tipo_relacao='direto'
                                    THEN pi_c.preco END), 2)           AS max_direto
                    FROM pesquisa_preco pp
                    LEFT JOIN pesquisa_preco_item pi_n
                           ON pi_n.pesquisa_id=pp.pesquisa_id
                          AND pi_n.produto_id=?
                          AND pi_n.produto_concorrente_id IS NULL
                    LEFT JOIN pesquisa_preco_item pi_c
                           ON pi_c.pesquisa_id=pp.pesquisa_id
                          AND pi_c.produto_id=?
                          AND pi_c.produto_concorrente_id IS NOT NULL
                    LEFT JOIN produto_concorrente_relacao rel
                           ON rel.produto_id=?
                          AND rel.produto_concorrente_id=pi_c.produto_concorrente_id
                    WHERE pp.pdv_id=?
                      AND pp.status='finalizado'
                      AND pp.fornecedor_id=?
                    GROUP BY pp.pesquisa_id
                    ORDER BY pp.data_pesquisa DESC
                    LIMIT 12
                """, (sel_prod_h[0], sel_prod_h[0], sel_prod_h[0], pdv_id_det, forn_id))

                if not hist or all(r[1] is None for r in hist):
                    st.info("Nenhum historico de preco encontrado para este produto neste PDV.")
                else:
                    df_h = pd.DataFrame(hist,
                        columns=["Data","Meu preco","Conc. diretos","Media conc.","Min conc.","Max conc."])

                    # Score por linha
                    def _score_hist(row):
                        if row["Meu preco"] and row["Media conc."]:
                            dif = (row["Meu preco"] - row["Media conc."]) / row["Media conc."] * 100
                            if dif <= -5:   return "🟢 Mais barato"
                            elif dif >= 5:  return "🔴 Mais caro"
                            else:           return "🟡 Similar"
                        return "—"
                    df_h["Score"] = df_h.apply(_score_hist, axis=1)

                    # Formata valores
                    for col in ["Meu preco","Media conc.","Min conc.","Max conc."]:
                        df_h[col] = df_h[col].apply(
                            lambda v: f"R$ {v:,.2f}".replace(",","X").replace(".",",").replace("X",".")
                            if v and v > 0 else "—")

                    st.dataframe(df_h, use_container_width=True, hide_index=True)
                    st.caption(f"Ultimas {len(df_h)} pesquisa(s) finalizadas neste PDV para {sel_prod_h[1]}")

    # Exportar
    if linhas_export:
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as w:
            pd.DataFrame(linhas_export).to_excel(w, index=False, sheet_name="Comparativo")
        buf.seek(0)
        st.download_button("⬇️ Exportar comparativo Excel", data=buf,
                           file_name=f"pesquisa_{pq_id}_{cli}_{data}.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


# ═══════════════════════════════════════════════════════
# ANALISE CONSOLIDADA DE PESQUISAS
# ═══════════════════════════════════════════════════════



# ═══════════════════════════════════════════════════════
# GERADOR DE PDF — ANALISE CONSOLIDADA
# ═══════════════════════════════════════════════════════

def _pdf_estilos():
    """Retorna dicionario com todos os estilos padronizados."""
    styles = getSampleStyleSheet()
    VERDE  = colors.HexColor("#2d6a4f")
    VERDE_C= colors.HexColor("#d8f3dc")
    CINZA  = colors.HexColor("#555555")
    CINZA_C= colors.HexColor("#f8f9fa")

    return {
        "titulo":   ParagraphStyle("titulo", parent=styles["Normal"],
                        fontSize=18, fontName="Helvetica-Bold",
                        textColor=VERDE, spaceAfter=2),
        "subtit":   ParagraphStyle("subtit", parent=styles["Normal"],
                        fontSize=9, textColor=CINZA, spaceAfter=6),
        "secao":    ParagraphStyle("secao", parent=styles["Normal"],
                        fontSize=11, fontName="Helvetica-Bold",
                        textColor=VERDE, spaceBefore=10, spaceAfter=4),
        "label":    ParagraphStyle("label", parent=styles["Normal"],
                        fontSize=7, fontName="Helvetica-Bold",
                        textColor=CINZA),
        "normal":   ParagraphStyle("normal", parent=styles["Normal"],
                        fontSize=8),
        "normal_r": ParagraphStyle("normal_r", parent=styles["Normal"],
                        fontSize=8, alignment=TA_RIGHT),
        "hdr_tab":  ParagraphStyle("hdr_tab", parent=styles["Normal"],
                        fontSize=7, fontName="Helvetica-Bold",
                        textColor=colors.white),
        "cell":     ParagraphStyle("cell", parent=styles["Normal"],
                        fontSize=7),
        "cell_r":   ParagraphStyle("cell_r", parent=styles["Normal"],
                        fontSize=7, alignment=TA_RIGHT),
        "rodape":   ParagraphStyle("rodape", parent=styles["Normal"],
                        fontSize=6, textColor=CINZA, alignment=TA_CENTER),
        "verde":    VERDE,
        "verde_c":  VERDE_C,
        "cinza_c":  CINZA_C,
    }


def _pdf_cabecalho(elementos, s, titulo_rel, subtitulo, filtros):
    """Bloco de cabecalho padrao para todos os PDFs de analise."""
    rep = query("SELECT nome_fantasia, fone, email FROM representante WHERE ativo=1 LIMIT 1")
    rep_nome = rep[0][0] if rep else "PepperCRM"

    # Linha topo: nome empresa | titulo relatorio
    topo = Table([[
        Paragraph(f"<b>{rep_nome}</b>", s["titulo"]),
        Paragraph(titulo_rel, ParagraphStyle("tr", parent=s["titulo"],
                  alignment=TA_RIGHT, fontSize=14)),
    ]], colWidths=[10*cm, 7.5*cm])
    topo.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
    elementos.append(topo)
    elementos.append(Paragraph(subtitulo, s["subtit"]))
    elementos.append(HRFlowable(width="100%", thickness=2,
                                color=s["verde"], spaceAfter=6))

    # Filtros aplicados
    if filtros:
        filt_txt = "  |  ".join(filtros)
        elementos.append(Paragraph(f"Filtros: {filt_txt}", s["subtit"]))

    elementos.append(Paragraph(
        f"Gerado em {_dt.now().strftime('%d/%m/%Y %H:%M')}  —  PepperCRM",
        s["rodape"]))
    elementos.append(Spacer(1, 0.3*cm))


def _pdf_tabela(dados_rows, colunas, col_widths, s, zebra=True):
    """Gera um objeto Table formatado com cabecalho verde."""
    header = [Paragraph(c, s["hdr_tab"]) for c in colunas]
    rows   = [header]
    for row in dados_rows:
        linha = []
        for i, val in enumerate(row):
            txt = str(val) if val is not None else "—"
            alinha = s["cell_r"] if any(txt.startswith(x) for x in ["R$","+","-"])                      else s["cell"]
            linha.append(Paragraph(txt, alinha))
        rows.append(linha)

    t = Table(rows, colWidths=col_widths, repeatRows=1)
    styles_t = [
        ("BACKGROUND",    (0,0), (-1,0),  s["verde"]),
        ("TEXTCOLOR",     (0,0), (-1,0),  colors.white),
        ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 7),
        ("TOPPADDING",    (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ("LEFTPADDING",   (0,0), (-1,-1), 4),
        ("GRID",          (0,0), (-1,-1), 0.3, colors.HexColor("#cccccc")),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]
    if zebra:
        styles_t.append(("ROWBACKGROUNDS", (0,1), (-1,-1),
                         [colors.white, s["cinza_c"]]))
    t.setStyle(TableStyle(styles_t))
    return t


def _pdf_metricas(metricas, s):
    """Linha de metricas: lista de (label, valor)."""
    cells = [[Paragraph(m[0], s["label"]),
              Paragraph(str(m[1]), ParagraphStyle("mv", parent=s["normal"],
                         fontName="Helvetica-Bold", fontSize=10))]
             for m in metricas]
    t = Table([cells[0]], colWidths=[4.5*cm]*len(cells))
    # Cria uma linha com pares label+valor por metrica
    rows_met = []
    for m in metricas:
        rows_met.append([Paragraph(m[0], s["label"]),
                         Paragraph(str(m[1]),
                                   ParagraphStyle("mv", parent=s["normal"],
                                                  fontName="Helvetica-Bold",
                                                  fontSize=10, textColor=s["verde"]))])
    n = len(rows_met)
    cw = [17.5*cm / n] * n
    flat_labels = [r[0] for r in rows_met]
    flat_vals   = [r[1] for r in rows_met]
    t2 = Table([flat_labels, flat_vals],
               colWidths=cw)
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), s["cinza_c"]),
        ("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("TOPPADDING",   (0,0),(-1,-1),4),
        ("BOX",         (0,0),(-1,-1),0.5, s["verde"]),
        ("INNERGRID",   (0,0),(-1,-1),0.3, colors.HexColor("#dddddd")),
    ]))
    return t2


def _gerar_pdf_por_produto(df, prod_nome, forn_nome, preco_tab_unit, filtros_desc):
    s   = _pdf_estilos()
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=landscape(A4),
                            leftMargin=1.5*cm, rightMargin=1.5*cm,
                            topMargin=1.5*cm, bottomMargin=1.5*cm)
    el  = []

    _pdf_cabecalho(el, s,
        "Analise por Produto",
        f"Produto: {prod_nome}  |  Fornecedor: {forn_nome}",
        filtros_desc)

    metricas = [
        ("PDVs pesquisados",       df["Cliente — PDV"].nunique()),
        ("Marcas concorrentes",    df["Marca"].nunique()),
        ("Menor preco (medio)",    _brl(df["Preco medio num"].min())),
        ("Maior preco (medio)",    _brl(df["Preco medio num"].max())),
    ]
    if preco_tab_unit:
        metricas.append(("Meu preco unit. (tabela)", _brl(preco_tab_unit)))
    el.append(_pdf_metricas(metricas, s))
    el.append(Spacer(1, 0.4*cm))

    # Tabela de dados
    colunas = ["Cliente — PDV","Tipo PDV","Marca","Produto concorrente",
               "Tipo rel.","Ult. preco","Preco medio","Min","Max","Pesquisas","Ultima data"]
    if preco_tab_unit:
        colunas += ["Meu unit.","Dif. vs tab.","Score"]

    cw_base = [3.5*cm, 1.8*cm, 2.2*cm, 3.0*cm, 1.5*cm,
               1.8*cm, 1.8*cm, 1.8*cm, 1.8*cm, 1.2*cm, 1.8*cm]
    if preco_tab_unit:
        cw_base += [1.8*cm, 2.2*cm, 2.0*cm]

    rows = []
    for _, row in df.iterrows():
        linha = [
            row.get("Cliente — PDV","—"),
            row.get("Tipo PDV","—"),
            row.get("Marca","—"),
            row.get("Produto concorrente","—"),
            row.get("Tipo rel.","—"),
            row.get("Ultimo preco","—"),
            row.get("Preco medio","—"),
            row.get("Min","—"),
            row.get("Max","—"),
            str(row.get("Pesquisas","—")),
            str(row.get("Ultima data","—"))[:10],
        ]
        if preco_tab_unit:
            linha += [
                row.get("Meu preco unit.","—"),
                row.get("Dif. vs tab.","—"),
                row.get("Score","—"),
            ]
        rows.append(linha)

    el.append(_pdf_tabela(rows, colunas, cw_base, s))
    doc.build(el)
    buf.seek(0)
    return buf


def _gerar_pdf_por_marca(df, marca_nome, forn_nome, tab_nome, filtros_desc):
    s   = _pdf_estilos()
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=landscape(A4),
                            leftMargin=1.5*cm, rightMargin=1.5*cm,
                            topMargin=1.5*cm, bottomMargin=1.5*cm)
    el  = []

    _pdf_cabecalho(el, s,
        "Analise por Marca Concorrente",
        f"Marca: {marca_nome}  |  Fornecedor ref.: {forn_nome}  |  Tabela: {tab_nome or '—'}",
        filtros_desc)

    metricas = [
        ("Produtos pesquisados",  df["Produto concorrente"].nunique()),
        ("PDVs onde aparece",     df["Cliente — PDV"].nunique()),
        ("Categorias",            df["Categoria"].nunique()),
    ]
    el.append(_pdf_metricas(metricas, s))
    el.append(Spacer(1, 0.4*cm))

    for cat in sorted(df["Categoria"].unique()):
        df_cat = df[df["Categoria"] == cat]
        el.append(Paragraph(f"📦  {cat}", s["secao"]))

        colunas = ["Produto concorrente","Nosso produto","Tipo rel.",
                   "Cliente — PDV","Tipo PDV","Preco"]
        tem_tab = "Meu preco unit." in df_cat.columns and df_cat["Meu preco unit."].notna().any()
        if tem_tab:
            colunas += ["Meu preco unit.","Dif. vs tab.","Score"]
        colunas.append("Data")

        cw = [3.5*cm, 3.0*cm, 1.5*cm, 3.5*cm, 1.8*cm, 1.8*cm]
        if tem_tab:
            cw += [1.8*cm, 2.2*cm, 2.0*cm]
        cw.append(1.8*cm)

        rows = []
        for _, row in df_cat.iterrows():
            linha = [
                row.get("Produto concorrente","—"),
                row.get("Nosso produto","—") or "—",
                row.get("Tipo rel.","—"),
                row.get("Cliente — PDV","—"),
                row.get("Tipo PDV","—"),
                row.get("Preco","—"),
            ]
            if tem_tab:
                linha += [
                    row.get("Meu preco unit.","—"),
                    row.get("Dif. vs tab.","—"),
                    row.get("Score","—"),
                ]
            linha.append(str(row.get("Data","—"))[:10])
            rows.append(linha)

        el.append(KeepTogether(_pdf_tabela(rows, colunas, cw, s)))
        el.append(Spacer(1, 0.3*cm))

    doc.build(el)
    buf.seek(0)
    return buf


def _gerar_pdf_por_categoria(df, cat_nome, filtros_desc):
    s   = _pdf_estilos()
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            leftMargin=1.5*cm, rightMargin=1.5*cm,
                            topMargin=1.5*cm, bottomMargin=1.5*cm)
    el  = []

    _pdf_cabecalho(el, s,
        "Analise por Categoria",
        f"Categoria: {cat_nome}",
        filtros_desc)

    total_occ = df["Ocorrencias"].sum()
    metricas  = [
        ("Marcas encontradas",   len(df)),
        ("Total de ocorrencias", int(total_occ)),
        ("PDVs com a categoria", int(df["PDVs"].max())),
    ]
    el.append(_pdf_metricas(metricas, s))
    el.append(Spacer(1, 0.5*cm))

    colunas = ["Marca","Produtos","PDVs","Ocorrencias","Share (%)","Preco medio","Preco min","Preco max"]
    cw      = [4.5*cm, 2.0*cm, 2.0*cm, 2.5*cm, 2.0*cm, 2.5*cm, 2.5*cm, 2.5*cm]

    rows = []
    for _, row in df.iterrows():
        rows.append([
            row.get("Marca","—"),
            str(row.get("Produtos pesq.","—")),
            str(row.get("PDVs","—")),
            str(row.get("Ocorrencias","—")),
            f"{row.get('Share (%)',0):.1f}%",
            _brl(row.get("Preco medio")) if row.get("Preco medio") else "—",
            _brl(row.get("Preco min"))   if row.get("Preco min")   else "—",
            _brl(row.get("Preco max"))   if row.get("Preco max")   else "—",
        ])

    el.append(_pdf_tabela(rows, colunas, cw, s))
    doc.build(el)
    buf.seek(0)
    return buf


def _gerar_pdf_por_pdv(df, pdv_label, forn_nome, tab_nome, filtros_desc):
    s   = _pdf_estilos()
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=landscape(A4),
                            leftMargin=1.5*cm, rightMargin=1.5*cm,
                            topMargin=1.5*cm, bottomMargin=1.5*cm)
    el  = []

    _pdf_cabecalho(el, s,
        "Analise por PDV",
        f"PDV: {pdv_label}  |  Fornecedor: {forn_nome}  |  Tabela: {tab_nome or '—'}",
        filtros_desc)

    metricas = [
        ("Pesquisas",          df["Pesquisa #"].nunique()),
        ("Marcas encontradas", df["Marca"].nunique()),
        ("Categorias",         df["Categoria"].nunique()),
    ]
    el.append(_pdf_metricas(metricas, s))
    el.append(Spacer(1, 0.4*cm))

    for cat in sorted(df["Categoria"].unique()):
        df_cat = df[df["Categoria"] == cat]
        el.append(Paragraph(f"📦  {cat}", s["secao"]))

        tem_tab = "Meu unit. (tab.)" in df_cat.columns and df_cat["Meu unit. (tab.)"].notna().any()
        colunas = ["Data","Nosso produto","Marca","Produto concorrente","Tipo rel.","Preco conc."]
        cw      = [1.8*cm, 3.5*cm, 2.5*cm, 3.5*cm, 1.8*cm, 2.0*cm]
        if tem_tab:
            colunas += ["Meu unit. (tab.)","Dif. vs tab.","Score"]
            cw      += [2.0*cm, 2.5*cm, 2.0*cm]

        rows = []
        for _, row in df_cat.iterrows():
            linha = [
                str(row.get("Data","—"))[:10],
                row.get("Nosso produto","—") or "—",
                row.get("Marca","—"),
                row.get("Produto concorrente","—"),
                row.get("Tipo rel.","—"),
                row.get("Preco conc.","—"),
            ]
            if tem_tab:
                linha += [
                    row.get("Meu unit. (tab.)","—"),
                    row.get("Dif. vs tab.","—"),
                    row.get("Score","—"),
                ]
            rows.append(linha)

        el.append(KeepTogether(_pdf_tabela(rows, colunas, cw, s)))
        el.append(Spacer(1, 0.3*cm))

    doc.build(el)
    buf.seek(0)
    return buf


def _tela_analise_consolidada():
    st.header("Analise Consolidada de Pesquisas")
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Voltar a lista", use_container_width=True):
            st.session_state["pq_modo"] = "lista"; st.rerun()

    st.divider()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        forns = query("SELECT fornecedor_id, nome_fantasia FROM fornecedor WHERE ativo=1 ORDER BY nome_fantasia")
        forn_opts = [(None, "Todos os fornecedores")] + [(f[0], f[1]) for f in forns]
        fil_forn  = st.selectbox("Fornecedor ref.", forn_opts, format_func=lambda x: x[1], key="ac_forn")
    with col2:
        # Categorias filtradas pelo fornecedor selecionado
        if fil_forn[0]:
            cats_raw = query("""
                SELECT DISTINCT cat.categoria_id, cat.nome_categoria
                FROM produto p
                JOIN categoria cat ON p.categoria_id=cat.categoria_id
                WHERE p.fornecedor_id=? AND p.ativo=1 AND cat.ativo=1
                ORDER BY cat.nome_categoria
            """, (fil_forn[0],))
        else:
            cats_raw = query("SELECT categoria_id, nome_categoria FROM categoria WHERE ativo=1 ORDER BY nome_categoria")
        cat_opts = [(None, "Todas as categorias")] + [(c[0], c[1]) for c in cats_raw]
        fil_cat  = st.selectbox("Categoria", cat_opts, format_func=lambda x: x[1], key="ac_cat")
    with col3:
        per_opts = ["30 dias", "60 dias", "90 dias", "6 meses", "1 ano", "Todos"]
        fil_per  = st.selectbox("Periodo", per_opts, key="ac_per")
    with col4:
        tipo_rel_fil = st.selectbox("Tipo de relacao",
                                    ["Diretos e Indiretos", "Apenas diretos", "Apenas indiretos"],
                                    key="ac_tipo_rel")

    per_sql = {
        "30 dias": "pp.data_pesquisa >= date('now','-30 days')",
        "60 dias": "pp.data_pesquisa >= date('now','-60 days')",
        "90 dias": "pp.data_pesquisa >= date('now','-90 days')",
        "6 meses": "pp.data_pesquisa >= date('now','-6 months')",
        "1 ano":   "pp.data_pesquisa >= date('now','-1 year')",
    }
    where_base  = ["pp.status='finalizado'"]
    params_base = []
    if fil_forn[0]:
        where_base.append("pp.fornecedor_id=?"); params_base.append(fil_forn[0])
    if fil_per in per_sql:
        where_base.append(per_sql[fil_per])

    tipo_rel_where = ""
    if tipo_rel_fil == "Apenas diretos":
        tipo_rel_where = "AND rel.tipo_relacao='direto'"
    elif tipo_rel_fil == "Apenas indiretos":
        tipo_rel_where = "AND rel.tipo_relacao='indireto'"

    cat_where  = "AND pc.categoria_id=?" if fil_cat[0] else ""
    cat_params = [fil_cat[0]] if fil_cat[0] else []

    st.divider()
    ABAS_AC = {"prod":"Por produto","marca":"Por marca","cat":"Por categoria","pdv":"Por PDV"}
    if "ac_aba" not in st.session_state: st.session_state["ac_aba"] = "prod"
    cols = st.columns(4)
    for col,(k,v) in zip(cols, ABAS_AC.items()):
        ativa = st.session_state["ac_aba"] == k
        if col.button(v, key=f"acnav_{k}", use_container_width=True,
                      type="primary" if ativa else "secondary"):
            st.session_state["ac_aba"] = k; st.rerun()
    a = st.session_state["ac_aba"]
    if a=="prod":  _ac_por_produto(where_base, params_base, tipo_rel_where, cat_where, cat_params, fil_forn[0])
    elif a=="marca":_ac_por_marca(where_base, params_base, tipo_rel_where, cat_where, cat_params, fil_forn[0])
    elif a=="cat": _ac_por_categoria(where_base, params_base, fil_forn[0])
    elif a=="pdv": _ac_por_pdv(where_base, params_base, tipo_rel_where, cat_where, cat_params, fil_forn[0])


def _label_pdv(pdv_nome, cliente_nome):
    """Sempre retorna 'Cliente — PDV' para evitar ambiguidade."""
    if not pdv_nome or pdv_nome in ("—", "None", "Matriz"):
        return f"{cliente_nome or '?'} — Matriz"
    return f"{cliente_nome or '?'} — {pdv_nome}"


def _label_tabela(tab):
    """tab = (id, nome, preco_cx, un_cx, um, peso). Retorna string legivel."""
    nome    = tab[1]
    preco_cx= tab[2] or 0
    un_cx   = tab[3] if tab[3] and tab[3] > 0 else 1
    unit    = round(preco_cx / un_cx, 4)
    return (f"{nome}  |  cx: {_brl(preco_cx)}"
            f"  (c/ {un_cx} un)  |  unit: {_brl(unit)}")


def _score_icon(preco_conc, preco_meu):
    if not preco_conc or not preco_meu: return "—"
    dif = (preco_conc - preco_meu) / preco_meu * 100
    if dif <= -5:  return "🟢 Mais barato"
    if dif >= 5:   return "🔴 Mais caro"
    return "🟡 Similar"


def _dif_str(preco_conc, preco_meu):
    if not preco_conc or not preco_meu: return "—"
    dif = preco_conc - preco_meu
    pct = dif / preco_meu * 100
    sinal = "+" if dif > 0 else ""
    return f"{sinal}{pct:.1f}%  ({sinal}{_brl(round(dif,2))})"


# ── ABA 1: Por produto ────────────────────────────────

def _ac_por_produto(where_base, params_base, tipo_rel_where, cat_where, cat_params, forn_id_global):
    st.subheader("Comparativo por produto")
    st.caption("Selecione um produto seu e veja como os concorrentes se posicionam em todos os PDVs pesquisados.")

    forns_p = query("SELECT fornecedor_id, nome_fantasia FROM fornecedor WHERE ativo=1 ORDER BY nome_fantasia")
    if forn_id_global:
        forns_p = [f for f in forns_p if f[0] == forn_id_global] or forns_p
    forn_p  = st.selectbox("Fornecedor", forns_p, format_func=lambda x: x[1], key="ac_p_forn")
    prod_id = forn_p[0]

    # Filtra produtos pelo fornecedor E pela categoria global (se selecionada)
    if cat_params:
        prods_p = query("""SELECT p.produto_id, p.descricao_curta, p.codigo_produto
            FROM produto p WHERE p.fornecedor_id=? AND p.categoria_id=? AND p.ativo=1
            ORDER BY p.descricao_curta""", (forn_p[0], cat_params[0]))
    else:
        prods_p = query("""SELECT p.produto_id, p.descricao_curta, p.codigo_produto
            FROM produto p WHERE p.fornecedor_id=? AND p.ativo=1
            ORDER BY p.descricao_curta""", (forn_p[0],))
    if not prods_p:
        st.info("Nenhum produto cadastrado para este fornecedor na categoria selecionada."); return

    prod_sel = st.selectbox("Produto", prods_p,
                            format_func=lambda x: f"{x[2]} — {x[1]}",
                            key="ac_p_prod")
    prod_id  = prod_sel[0]

    # Tabela de preco para comparacao
    tabs = query("""SELECT tp.tabela_preco_id, tp.nome_tabela, tpi.preco_caixa,
                           p.unidades_caixa, p.unidade_medida, p.peso
                    FROM tabela_preco tp
                    JOIN tabela_preco_item tpi ON tpi.tabela_preco_id=tp.tabela_preco_id
                    JOIN produto p ON tpi.produto_id=p.produto_id
                    WHERE tpi.produto_id=? AND tp.ativo=1
                    ORDER BY tp.nome_tabela""", (prod_id,))
    preco_tab_unit = None
    if tabs:
        tab_opts  = [(None, "— Sem comparacao de tabela")] + [
            (t[0], _label_tabela(t)) for t in tabs]
        tab_sel_p = st.selectbox("Comparar com tabela de preco", tab_opts,
                                 format_func=lambda x: x[1], key="ac_p_tab")
        if tab_sel_p[0]:
            t = next(t for t in tabs if t[0] == tab_sel_p[0])
            un_cx = t[3] if t[3] and t[3] > 0 else 1
            preco_tab_unit = round(t[2] / un_cx, 4)
            st.caption(f"Meu preco unitario: **{_brl(preco_tab_unit)}**  "
                       f"(R$ {t[2]:,.2f}/cx ÷ {un_cx} unidades)".replace(",","X").replace(".",",").replace("X",",").replace("R$ ","R$ "))

    # Query principal
    dados = query(f"""
        SELECT
            cli.nome_fantasia                                AS cliente,
            COALESCE(pdv.nome_loja,'Matriz')                AS pdv_nome,
            COALESCE(pdv.tipo_pdv,'—')                      AS tipo_pdv,
            conc.marca_concorrente                          AS marca,
            pc.descricao_curta                              AS prod_conc,
            COALESCE(rel.tipo_relacao,'—')                  AS tipo_rel,
            ROUND(AVG(ppi.preco), 2)                        AS preco_medio,
            ROUND(MIN(ppi.preco), 2)                        AS preco_min,
            ROUND(MAX(ppi.preco), 2)                        AS preco_max,
            COUNT(DISTINCT pp.pesquisa_id)                  AS pesquisas,
            MAX(pp.data_pesquisa)                           AS ultima_data,
            (SELECT ppi2.preco FROM pesquisa_preco_item ppi2
             JOIN pesquisa_preco pp2 ON ppi2.pesquisa_id=pp2.pesquisa_id
             WHERE ppi2.produto_concorrente_id=ppi.produto_concorrente_id
               AND pp2.pdv_id=pp.pdv_id
             ORDER BY pp2.data_pesquisa DESC LIMIT 1)       AS ultimo_preco
        FROM pesquisa_preco_item ppi
        JOIN pesquisa_preco pp      ON ppi.pesquisa_id=pp.pesquisa_id
        JOIN produto_concorrente pc ON ppi.produto_concorrente_id=pc.produto_concorrente_id
        JOIN concorrente conc       ON pc.concorrente_id=conc.concorrente_id
        LEFT JOIN produto_concorrente_relacao rel
               ON rel.produto_id=? AND rel.produto_concorrente_id=ppi.produto_concorrente_id
        LEFT JOIN pdv   ON pp.pdv_id=pdv.pdv_id
        LEFT JOIN cliente cli ON pp.cliente_id=cli.cliente_id
        WHERE ppi.produto_id=?
          AND {' AND '.join(where_base)}
          {tipo_rel_where}
          {cat_where}
        GROUP BY pp.pdv_id, ppi.produto_concorrente_id
        ORDER BY marca, preco_medio
    """, tuple([prod_id, prod_id] + params_base + cat_params))

    if not dados:
        st.info("Nenhum dado encontrado para este produto no periodo selecionado."); return

    df = pd.DataFrame(dados, columns=["Cliente","PDV nome","Tipo PDV","Marca","Produto concorrente",
                                       "Tipo rel.","Preco medio","Min","Max","Pesquisas",
                                       "Ultima data","Ultimo preco"])
    df["Cliente — PDV"] = df.apply(lambda r: _label_pdv(r["PDV nome"], r["Cliente"]), axis=1)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("PDVs pesquisados",      df["Cliente — PDV"].nunique())
    col2.metric("Marcas concorrentes",   df["Marca"].nunique())
    col3.metric("Menor preco encontrado",_brl(df["Preco medio"].min()))
    col4.metric("Maior preco encontrado",_brl(df["Preco medio"].max()))

    if preco_tab_unit:
        df["Meu preco unit."] = _brl(preco_tab_unit)
        df["Score"]           = df["Ultimo preco"].apply(lambda v: _score_icon(v, preco_tab_unit))
        df["Dif. vs tab."]    = df["Ultimo preco"].apply(lambda v: _dif_str(v, preco_tab_unit))

    # PDV mais barato e mais caro (pelo ultimo preco)
    # PDV mais barato e mais caro — usa cliente(r[0]) e pdv_nome(r[1]) que estao no df
    dados_com_label = [
        (_label_pdv(r[1], r[0]), r[11])
        for r in dados if r[11]
    ]
    if dados_com_label:
        mais_barato = min(dados_com_label, key=lambda x: x[1])
        mais_caro   = max(dados_com_label, key=lambda x: x[1])
        c1, c2 = st.columns(2)
        c1.success(f"PDV mais barato: **{mais_barato[0]}** — {_brl(mais_barato[1])}")
        c2.error(f"PDV mais caro: **{mais_caro[0]}** — {_brl(mais_caro[1])}")

    # Formata para exibicao
    df_show = df.copy()
    for col in ["Preco medio","Min","Max","Ultimo preco"]:
        df_show[col] = df_show[col].apply(lambda v: _brl(v) if v else "—")

    cols_show = ["Cliente — PDV","Tipo PDV","Marca","Produto concorrente","Tipo rel.",
                 "Ultimo preco","Preco medio","Min","Max","Pesquisas","Ultima data"]
    if preco_tab_unit:
        cols_show += ["Meu preco unit.","Dif. vs tab.","Score"]
    st.dataframe(df_show[cols_show], use_container_width=True, hide_index=True)

    col_xe, col_xp = st.columns(2)
    with col_xe:
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as w:
            df_show[cols_show].to_excel(w, index=False, sheet_name="Por produto")
        buf.seek(0)
        st.download_button("⬇️ Exportar Excel", data=buf,
                           file_name=f"analise_produto_{prod_sel[1]}.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           use_container_width=True)
    with col_xp:
        # Prepara df para o PDF — usa df original (antes da formatacao)
        df_pdf = df.copy()
        # "Preco medio" no df original ainda e numerico
        df_pdf["Preco medio num"] = pd.to_numeric(df["Preco medio"], errors="coerce")
        # Formata colunas de preco para exibicao no PDF
        for _c in ["Preco medio","Min","Max","Ultimo preco"]:
            if _c in df_pdf.columns:
                df_pdf[_c] = df_pdf[_c].apply(lambda v: _brl(v) if v and not pd.isna(v) else "—")
        if preco_tab_unit:
            df_pdf["Meu preco unit."] = _brl(preco_tab_unit)
        filtros_desc = [
            f"Periodo: {st.session_state.get('ac_per','—')}",
            f"Tipo rel.: {st.session_state.get('ac_tipo_rel','—')}",
        ]
        buf_pdf = _gerar_pdf_por_produto(
            df_pdf, prod_sel[1], forn_p[1] if forn_p else "—",
            preco_tab_unit, filtros_desc)
        st.download_button("⬇️ Exportar PDF", data=buf_pdf,
                           file_name=f"analise_produto_{prod_sel[1]}.pdf",
                           mime="application/pdf",
                           use_container_width=True)


# ── ABA 2: Por marca concorrente ──────────────────────

def _ac_por_marca(where_base, params_base, tipo_rel_where, cat_where, cat_params, forn_id_global):
    st.subheader("Comparativo por marca concorrente")
    st.caption("Todos os produtos de uma marca pesquisados, organizados por categoria, com comparativo vs sua tabela.")

    # Filtro de marcas pelo fornecedor global
    if forn_id_global:
        marcas = query("""SELECT conc.concorrente_id, conc.marca_concorrente, f.nome_fantasia
            FROM concorrente conc JOIN fornecedor f ON conc.fornecedor_id=f.fornecedor_id
            WHERE conc.ativo=1 AND conc.fornecedor_id=? ORDER BY conc.marca_concorrente""",
            (forn_id_global,))
    else:
        marcas = query("""SELECT conc.concorrente_id, conc.marca_concorrente, f.nome_fantasia
            FROM concorrente conc JOIN fornecedor f ON conc.fornecedor_id=f.fornecedor_id
            WHERE conc.ativo=1 ORDER BY conc.marca_concorrente""")
    if not marcas:
        st.info("Nenhuma marca concorrente cadastrada."); return

    col1, col2 = st.columns(2)
    with col1:
        marca_sel = st.selectbox("Marca concorrente", marcas,
                                 format_func=lambda x: f"{x[1]}  ({x[2]})", key="ac_m_marca")
    with col2:
        # Tabela de referencia
        if forn_id_global:
            tabs_m = query("""SELECT tp.tabela_preco_id, tp.nome_tabela, NULL, NULL, NULL, NULL
                FROM tabela_preco tp WHERE tp.fornecedor_id=? AND tp.ativo=1
                ORDER BY tp.nome_tabela""", (forn_id_global,))
        else:
            tabs_m = query("""SELECT tp.tabela_preco_id, tp.nome_tabela, NULL, NULL, NULL, NULL
                FROM tabela_preco tp WHERE tp.ativo=1 ORDER BY tp.nome_tabela""")
        tab_m_opts = [(None, "— Sem comparacao de tabela")] + [(t[0], t[1]) for t in tabs_m]
        tab_m_sel  = st.selectbox("Tabela de preco para comparar", tab_m_opts,
                                   format_func=lambda x: x[1], key="ac_m_tab")

    dados = query(f"""
        SELECT
            COALESCE(cat.nome_categoria, 'Sem categoria')   AS categoria,
            pc.descricao_curta                               AS produto_conc,
            pr.descricao_curta                               AS prod_nosso,
            pr.produto_id                                    AS prod_nosso_id,
            COALESCE(rel.tipo_relacao,'—')                   AS tipo_rel,
            cli.nome_fantasia                                AS cliente,
            COALESCE(pdv.nome_loja,'Matriz')                 AS pdv_nome,
            COALESCE(pdv.tipo_pdv,'—')                      AS tipo_pdv,
            ROUND(ppi.preco, 2)                              AS preco,
            pp.data_pesquisa                                 AS data
        FROM pesquisa_preco_item ppi
        JOIN pesquisa_preco pp      ON ppi.pesquisa_id=pp.pesquisa_id
        JOIN produto_concorrente pc ON ppi.produto_concorrente_id=pc.produto_concorrente_id
        JOIN concorrente conc       ON pc.concorrente_id=conc.concorrente_id
        LEFT JOIN categoria cat     ON pc.categoria_id=cat.categoria_id
        LEFT JOIN produto_concorrente_relacao rel
               ON rel.produto_concorrente_id=ppi.produto_concorrente_id
        LEFT JOIN produto pr        ON rel.produto_id=pr.produto_id
        LEFT JOIN pdv               ON pp.pdv_id=pdv.pdv_id
        LEFT JOIN cliente cli       ON pp.cliente_id=cli.cliente_id
        WHERE conc.concorrente_id=?
          AND {' AND '.join(where_base)}
          {tipo_rel_where}
          {cat_where}
        ORDER BY categoria, pc.descricao_curta, pp.data_pesquisa DESC
    """, tuple([marca_sel[0]] + params_base + cat_params))

    if not dados:
        st.info("Nenhuma pesquisa encontrada para esta marca no periodo selecionado."); return

    df = pd.DataFrame(dados, columns=["Categoria","Produto concorrente","Nosso produto",
                                       "Prod nosso id","Tipo rel.","Cliente","PDV nome",
                                       "Tipo PDV","Preco","Data"])
    df["Cliente — PDV"] = df.apply(lambda r: _label_pdv(r["PDV nome"], r["Cliente"]), axis=1)

    # Busca preco unitario da tabela para cada produto nosso
    preco_tab_por_prod = {}
    if tab_m_sel[0]:
        prods_ids = df["Prod nosso id"].dropna().unique()
        for pid in prods_ids:
            r = query("""SELECT tpi.preco_caixa, COALESCE(p.unidades_caixa,1)
                FROM tabela_preco_item tpi JOIN produto p ON tpi.produto_id=p.produto_id
                WHERE tpi.tabela_preco_id=? AND tpi.produto_id=?""",
                (tab_m_sel[0], int(pid)))
            if r:
                un = r[0][1] if r[0][1] and r[0][1] > 0 else 1
                preco_tab_por_prod[int(pid)] = round(r[0][0] / un, 4)

    def _get_tab(row):
        pid = row["Prod nosso id"]
        if pid and not pd.isna(pid):
            return preco_tab_por_prod.get(int(pid))
        return None

    df["Meu preco unit."] = df.apply(_get_tab, axis=1)
    df["Score"]           = df.apply(lambda r: _score_icon(r["Preco"], r["Meu preco unit."]), axis=1)
    df["Dif. vs tab."]    = df.apply(lambda r: _dif_str(r["Preco"], r["Meu preco unit."]), axis=1)

    col1, col2, col3 = st.columns(3)
    col1.metric("Produtos pesquisados",  df["Produto concorrente"].nunique())
    col2.metric("PDVs onde aparece",     df["Cliente — PDV"].nunique())
    col3.metric("Categorias",            df["Categoria"].nunique())

    st.divider()
    for cat in sorted(df["Categoria"].unique()):
        df_cat = df[df["Categoria"] == cat]
        with st.expander(
            f"📦 {cat}  —  {df_cat['Produto concorrente'].nunique()} produto(s)  |  {df_cat['Cliente — PDV'].nunique()} PDV(s)",
            expanded=True):

            # Resumo por produto concorrente
            def first_notnull(s):
                v = s.dropna()
                return v.iloc[0] if len(v) > 0 else None

            resumo = df_cat.groupby("Produto concorrente").agg(
                Nosso_produto=("Nosso produto",   lambda x: first_notnull(x) or "—"),
                Tipo_rel=("Tipo rel.",             lambda x: x.iloc[0]),
                Preco_min=("Preco",                "min"),
                Preco_medio=("Preco",              "mean"),
                Preco_max=("Preco",                "max"),
                Score=("Score",                    lambda x: x.iloc[0]),
                Meu_preco=("Meu preco unit.",      lambda x: first_notnull(x)),
                PDVs=("Cliente — PDV",             "nunique"),
                Ultima_data=("Data",               "max"),
            ).reset_index()

            resumo["Preco min"]   = resumo["Preco_min"].apply(_brl)
            resumo["Preco medio"] = resumo["Preco_medio"].apply(lambda v: _brl(round(v,2)))
            resumo["Preco max"]   = resumo["Preco_max"].apply(_brl)
            resumo["Meu unit."]   = resumo["Meu_preco"].apply(lambda v: _brl(v) if v else "—")
            resumo = resumo.rename(columns={"Nosso_produto":"Nosso produto","Tipo_rel":"Tipo rel.",
                                             "Ultima_data":"Ultima data","PDVs":"PDVs"})

            cols_res = ["Produto concorrente","Nosso produto","Tipo rel.","Score",
                        "Preco min","Preco medio","Preco max"]
            if tab_m_sel[0]:
                cols_res += ["Meu unit."]
            cols_res += ["PDVs","Ultima data"]
            st.dataframe(resumo[cols_res], use_container_width=True, hide_index=True)

            # Detalhe por PDV
            with st.expander("Ver detalhe por PDV"):
                df_det = df_cat.copy()
                df_det["Preco"]         = df_det["Preco"].apply(_brl)
                df_det["Meu preco unit."]= df_det["Meu preco unit."].apply(
                    lambda v: _brl(v) if v and not pd.isna(v) else "—")
                cols_det = ["Produto concorrente","Cliente — PDV","Tipo PDV","Preco"]
                if tab_m_sel[0]:
                    cols_det += ["Meu preco unit.","Dif. vs tab.","Score"]
                cols_det += ["Data"]
                st.dataframe(df_det[cols_det], use_container_width=True, hide_index=True)

    # Exportar
    df_exp = df.copy()
    df_exp["Preco"]          = df_exp["Preco"].apply(_brl)
    df_exp["Meu preco unit."]= df_exp["Meu preco unit."].apply(
        lambda v: _brl(v) if v and not pd.isna(v) else "—")
    col_xe, col_xp = st.columns(2)
    with col_xe:
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as w:
            df_exp[["Categoria","Produto concorrente","Nosso produto","Tipo rel.",
                    "Cliente — PDV","Tipo PDV","Preco","Meu preco unit.",
                    "Dif. vs tab.","Score","Data"]].to_excel(
                w, index=False, sheet_name="Por marca")
        buf.seek(0)
        st.download_button("⬇️ Exportar Excel", data=buf,
                           file_name=f"analise_marca_{marca_sel[1]}.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           use_container_width=True)
    with col_xp:
        filtros_desc = [
            f"Periodo: {st.session_state.get('ac_per','—')}",
            f"Tipo rel.: {st.session_state.get('ac_tipo_rel','—')}",
        ]
        tab_nome_m = tab_m_sel[1] if tab_m_sel[0] else None
        forn_nome_m = next((f[1] for f in (query("SELECT fornecedor_id, nome_fantasia FROM fornecedor WHERE ativo=1") or []) if f[0] == forn_id_global), "—") if forn_id_global else "Todos"
        buf_pdf = _gerar_pdf_por_marca(df_exp, marca_sel[1], forn_nome_m, tab_nome_m, filtros_desc)
        st.download_button("⬇️ Exportar PDF", data=buf_pdf,
                           file_name=f"analise_marca_{marca_sel[1]}.pdf",
                           mime="application/pdf",
                           use_container_width=True)


# ── ABA 3: Por categoria ──────────────────────────────

def _ac_por_categoria(where_base, params_base, forn_id_global):
    st.subheader("Comparativo por categoria")
    st.caption("Share de presenca e posicionamento de preco por marca dentro da categoria.")

    if forn_id_global:
        cats = query("""SELECT DISTINCT cat.categoria_id, cat.nome_categoria
            FROM produto p JOIN categoria cat ON p.categoria_id=cat.categoria_id
            WHERE p.fornecedor_id=? AND p.ativo=1 AND cat.ativo=1
            ORDER BY cat.nome_categoria""", (forn_id_global,))
    else:
        cats = query("SELECT categoria_id, nome_categoria FROM categoria WHERE ativo=1 ORDER BY nome_categoria")
    if not cats:
        st.info("Nenhuma categoria encontrada."); return

    cat_sel = st.selectbox("Categoria", cats, format_func=lambda x: x[1], key="ac_c_cat")

    dados = query(f"""
        SELECT
            conc.marca_concorrente,
            COUNT(DISTINCT ppi.produto_concorrente_id) AS produtos,
            COUNT(DISTINCT pp.pdv_id)                  AS pdvs,
            COUNT(DISTINCT pp.pesquisa_id)             AS ocorrencias,
            ROUND(AVG(ppi.preco), 2)                   AS preco_medio,
            ROUND(MIN(ppi.preco), 2)                   AS preco_min,
            ROUND(MAX(ppi.preco), 2)                   AS preco_max
        FROM pesquisa_preco_item ppi
        JOIN pesquisa_preco pp      ON ppi.pesquisa_id=pp.pesquisa_id
        JOIN produto_concorrente pc ON ppi.produto_concorrente_id=pc.produto_concorrente_id
        JOIN concorrente conc       ON pc.concorrente_id=conc.concorrente_id
        WHERE pc.categoria_id=?
          AND {' AND '.join(where_base)}
        GROUP BY conc.concorrente_id
        ORDER BY ocorrencias DESC
    """, tuple([cat_sel[0]] + params_base))

    if not dados:
        st.info("Nenhuma pesquisa encontrada para esta categoria no periodo."); return

    df = pd.DataFrame(dados, columns=["Marca","Produtos pesq.","PDVs","Ocorrencias",
                                       "Preco medio","Preco min","Preco max"])
    total_occ     = df["Ocorrencias"].sum()
    df["Share (%)"] = (df["Ocorrencias"] / total_occ * 100).round(1)

    col1, col2, col3 = st.columns(3)
    col1.metric("Marcas encontradas",   len(df))
    col2.metric("Total de ocorrencias", int(total_occ))
    col3.metric("PDVs com a categoria", int(df["PDVs"].max()))

    st.bar_chart(df[["Marca","Share (%)"]].set_index("Marca"))

    df_show = df.copy()
    for col in ["Preco medio","Preco min","Preco max"]:
        df_show[col] = df_show[col].apply(_brl)
    st.dataframe(df_show, use_container_width=True, hide_index=True)

    col_xe, col_xp = st.columns(2)
    with col_xe:
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as w:
            df.to_excel(w, index=False, sheet_name="Por categoria")
        buf.seek(0)
        st.download_button("⬇️ Exportar Excel", data=buf,
                           file_name=f"analise_categoria_{cat_sel[1]}.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           use_container_width=True)
    with col_xp:
        filtros_desc = [f"Periodo: {st.session_state.get('ac_per','—')}"]
        buf_pdf = _gerar_pdf_por_categoria(df, cat_sel[1], filtros_desc)
        st.download_button("⬇️ Exportar PDF", data=buf_pdf,
                           file_name=f"analise_categoria_{cat_sel[1]}.pdf",
                           mime="application/pdf",
                           use_container_width=True)


# ── ABA 4: Por PDV ────────────────────────────────────

def _ac_por_pdv(where_base, params_base, tipo_rel_where, cat_where, cat_params, forn_id_global):
    st.subheader("Comparativo por PDV")
    st.caption("Selecione um PDV e veja todos os concorrentes pesquisados, com opcao de confrontar com sua tabela de preco.")

    # 1. Seleciona fornecedor
    forns_p = query("SELECT fornecedor_id, nome_fantasia FROM fornecedor WHERE ativo=1 ORDER BY nome_fantasia")
    if forn_id_global:
        forns_p = [f for f in forns_p if f[0] == forn_id_global] or forns_p
    forn_p = st.selectbox("Fornecedor", forns_p, format_func=lambda x: x[1], key="ac_pdv_forn")

    # 2. Seleciona PDV (somente PDVs que tem pesquisa finalizada para este fornecedor)
    pdvs_c = query("""
        SELECT DISTINCT cli.cliente_id, cli.nome_fantasia,
               pdv.pdv_id, COALESCE(pdv.nome_loja,'Matriz') AS pdv_nome
        FROM pesquisa_preco pp
        JOIN cliente cli ON pp.cliente_id=cli.cliente_id
        LEFT JOIN pdv ON pp.pdv_id=pdv.pdv_id
        WHERE pp.fornecedor_id=? AND pp.status='finalizado'
        ORDER BY cli.nome_fantasia, pdv_nome
    """, (forn_p[0],))
    if not pdvs_c:
        st.info("Nenhuma pesquisa finalizada encontrada para este fornecedor."); return

    pdv_opts = [(r[0], r[2], f"{r[1]} — {r[3]}") for r in pdvs_c]
    pdv_sel  = st.selectbox("Cliente — PDV", pdv_opts,
                            format_func=lambda x: x[2], key="ac_pdv_pdv")
    cli_id_sel = pdv_sel[0]
    pdv_id_sel = pdv_sel[1]

    # 3. Lista de pesquisas disponiveis para este PDV
    pesqs_pdv = query("""
        SELECT pp.pesquisa_id, pp.data_pesquisa, pp.status
        FROM pesquisa_preco pp
        WHERE pp.fornecedor_id=? AND pp.cliente_id=?
          AND (pp.pdv_id=? OR (pp.pdv_id IS NULL AND ? IS NULL))
          AND pp.status='finalizado'
        ORDER BY pp.data_pesquisa DESC
    """, (forn_p[0], cli_id_sel, pdv_id_sel, pdv_id_sel))

    if not pesqs_pdv:
        st.info("Nenhuma pesquisa finalizada para este PDV."); return

    col1, col2 = st.columns(2)
    with col1:
        pesq_opts = [(None, "Todas as pesquisas do periodo")] + [
            (p[0], f"#{p[0]}  {p[1][:10]}") for p in pesqs_pdv]
        pesq_sel  = st.selectbox("Pesquisa especifica (opcional)", pesq_opts,
                                  format_func=lambda x: x[1], key="ac_pdv_pesq")
    with col2:
        # Tabela de preco
        tabs_pdv = query("""SELECT tp.tabela_preco_id, tp.nome_tabela, tpi.preco_caixa,
                               p.unidades_caixa, p.unidade_medida, p.peso
                            FROM tabela_preco tp
                            JOIN tabela_preco_item tpi ON tpi.tabela_preco_id=tp.tabela_preco_id
                            JOIN produto p ON tpi.produto_id=p.produto_id
                            WHERE tp.fornecedor_id=? AND tp.ativo=1
                            GROUP BY tp.tabela_preco_id
                            ORDER BY tp.nome_tabela""", (forn_p[0],))
        tab_pdv_opts = [(None, "— Sem comparacao de tabela")] + [
            (t[0], t[1]) for t in tabs_pdv]
        tab_pdv_sel  = st.selectbox("Tabela de preco para comparar", tab_pdv_opts,
                                     format_func=lambda x: x[1], key="ac_pdv_tab")

    # Monta where da pesquisa
    where_pdv  = list(where_base)
    params_pdv = list(params_base)
    where_pdv.append("pp.cliente_id=?"); params_pdv.append(cli_id_sel)
    if pdv_id_sel:
        where_pdv.append("pp.pdv_id=?"); params_pdv.append(pdv_id_sel)
    else:
        where_pdv.append("pp.pdv_id IS NULL")
    if pesq_sel[0]:
        where_pdv.append("pp.pesquisa_id=?"); params_pdv.append(pesq_sel[0])

    dados = query(f"""
        SELECT
            pp.pesquisa_id,
            pp.data_pesquisa,
            COALESCE(cat.nome_categoria,'Sem categoria')    AS categoria,
            pr.produto_id,
            pr.descricao_curta                              AS nosso_produto,
            conc.marca_concorrente                          AS marca,
            pc.descricao_curta                              AS prod_conc,
            pc.produto_concorrente_id,
            COALESCE(rel.tipo_relacao,'—')                  AS tipo_rel,
            ROUND(ppi.preco, 2)                             AS preco_conc
        FROM pesquisa_preco_item ppi
        JOIN pesquisa_preco pp      ON ppi.pesquisa_id=pp.pesquisa_id
        JOIN produto_concorrente pc ON ppi.produto_concorrente_id=pc.produto_concorrente_id
        JOIN concorrente conc       ON pc.concorrente_id=conc.concorrente_id
        LEFT JOIN categoria cat     ON pc.categoria_id=cat.categoria_id
        LEFT JOIN produto_concorrente_relacao rel
               ON rel.produto_concorrente_id=ppi.produto_concorrente_id
        LEFT JOIN produto pr        ON rel.produto_id=pr.produto_id
        WHERE {' AND '.join(where_pdv)}
          {tipo_rel_where}
          {cat_where}
        ORDER BY categoria, pp.data_pesquisa DESC, marca
    """, tuple(params_pdv + cat_params))

    if not dados:
        st.info("Nenhum item encontrado para este PDV no periodo selecionado."); return

    df = pd.DataFrame(dados, columns=["Pesquisa #","Data","Categoria","Prod nosso id",
                                       "Nosso produto","Marca","Produto concorrente",
                                       "Pc id","Tipo rel.","Preco conc."])

    # Busca preco unitario da tabela por produto nosso
    preco_tab_por_prod = {}
    if tab_pdv_sel[0]:
        for pid in df["Prod nosso id"].dropna().unique():
            r = query("""SELECT tpi.preco_caixa, COALESCE(p.unidades_caixa,1)
                FROM tabela_preco_item tpi JOIN produto p ON tpi.produto_id=p.produto_id
                WHERE tpi.tabela_preco_id=? AND tpi.produto_id=?""",
                (tab_pdv_sel[0], int(pid)))
            if r:
                un = r[0][1] if r[0][1] and r[0][1] > 0 else 1
                preco_tab_por_prod[int(pid)] = round(r[0][0] / un, 4)

    def _get_tab2(row):
        pid = row["Prod nosso id"]
        if pid and not pd.isna(pid): return preco_tab_por_prod.get(int(pid))
        return None

    df["Meu unit. (tab.)"] = df.apply(_get_tab2, axis=1)
    df["Score"]            = df.apply(lambda r: _score_icon(r["Preco conc."], r["Meu unit. (tab.)"]), axis=1)
    df["Dif. vs tab."]     = df.apply(lambda r: _dif_str(r["Preco conc."], r["Meu unit. (tab.)"]), axis=1)

    col1, col2, col3 = st.columns(3)
    col1.metric("Pesquisas",             df["Pesquisa #"].nunique())
    col2.metric("Marcas encontradas",    df["Marca"].nunique())
    col3.metric("Categorias",            df["Categoria"].nunique())

    # Agrupado por categoria
    for cat in sorted(df["Categoria"].unique()):
        df_cat = df[df["Categoria"] == cat]
        with st.expander(f"📦 {cat}  —  {df_cat['Marca'].nunique()} marca(s)", expanded=True):
            df_show = df_cat.copy()
            df_show["Preco conc."]     = df_show["Preco conc."].apply(_brl)
            df_show["Meu unit. (tab.)"]= df_show["Meu unit. (tab.)"].apply(
                lambda v: _brl(v) if v and not pd.isna(v) else "—")
            cols_s = ["Data","Nosso produto","Marca","Produto concorrente","Tipo rel.","Preco conc."]
            if tab_pdv_sel[0]:
                cols_s += ["Meu unit. (tab.)","Dif. vs tab.","Score"]
            st.dataframe(df_show[cols_s], use_container_width=True, hide_index=True)

    # Exportar
    df_exp = df.copy()
    df_exp["Preco conc."]     = df_exp["Preco conc."].apply(_brl)
    df_exp["Meu unit. (tab.)"]= df_exp["Meu unit. (tab.)"].apply(
        lambda v: _brl(v) if v and not pd.isna(v) else "—")
    col_xe, col_xp = st.columns(2)
    slug = pdv_sel[2].replace(" ","_").replace("/","_")
    with col_xe:
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as w:
            df_exp[["Data","Categoria","Nosso produto","Marca","Produto concorrente",
                    "Tipo rel.","Preco conc.","Meu unit. (tab.)","Dif. vs tab.","Score"]].to_excel(
                w, index=False, sheet_name="Por PDV")
        buf.seek(0)
        st.download_button("⬇️ Exportar Excel", data=buf,
                           file_name=f"analise_pdv_{slug}.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           use_container_width=True)
    with col_xp:
        filtros_desc = [
            f"Periodo: {st.session_state.get('ac_per','—')}",
            f"Tipo rel.: {st.session_state.get('ac_tipo_rel','—')}",
        ]
        tab_nome_pdv = tab_pdv_sel[1] if tab_pdv_sel[0] else None
        buf_pdf = _gerar_pdf_por_pdv(
            df_exp, pdv_sel[2], forn_p[1], tab_nome_pdv, filtros_desc)
        st.download_button("⬇️ Exportar PDF", data=buf_pdf,
                           file_name=f"analise_pdv_{slug}.pdf",
                           mime="application/pdf",
                           use_container_width=True)