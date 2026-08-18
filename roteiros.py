# roteiros.py — PepperCRM
# Modulo de roteiros e atribuicoes de PDVs

import streamlit as st
from database import query, execute_write, conectar
from permissoes import e_admin, e_master, empresa_id_atual, usuario_id_atual, e_supervisor, e_promotor, e_promotor_vendedor

def _ir(p):
    st.session_state["pagina"] = p; st.rerun()

def tela_roteiros():
    st.header("🗓️ Roteiros")
    if st.button("⬅ Voltar"): _ir("home")

    from permissoes import perfil_atual
    perfil = perfil_atual()

    # Abas conforme perfil
    if e_admin() or e_master():
        ABAS = {
            "vend": "💼 Vendedores",
            "prom": "👤 Promotores",
            "sup":  "🎯 Supervisores",
            "meu":  "📅 Meu Roteiro",
        }
    elif e_supervisor():
        ABAS = {"sup": "🎯 Minha Equipe", "meu": "📅 Meu Roteiro"}
    elif e_promotor() or e_promotor_vendedor():
        ABAS = {"meu": "📅 Meu Roteiro"}
    else:
        ABAS = {"vend": "💼 Meu Roteiro"}

    if "rot_aba" not in st.session_state:
        st.session_state["rot_aba"] = list(ABAS.keys())[0]
    cols = st.columns(len(ABAS))
    for col,(k,v) in zip(cols, ABAS.items()):
        ativa = st.session_state["rot_aba"] == k
        if col.button(v, key=f"rotnav_{k}", width="stretch",
                      type="primary" if ativa else "secondary"):
            st.session_state["rot_aba"] = k; st.rerun()
    st.divider()

    a = st.session_state["rot_aba"]
    if a == "vend": _roteiro_vendedor()
    elif a == "prom": _roteiro_promotor()
    elif a == "sup":  _roteiro_supervisor()
    elif a == "meu":  _meu_roteiro()


# ═══════════════════════════════════════════════════════════════
# ROTEIRO VENDEDOR
# ═══════════════════════════════════════════════════════════════

def _roteiro_vendedor():
    eid = empresa_id_atual()
    st.subheader("💼 Atribuição de PDVs por Vendedor")

    vends = query("""SELECT u.usuario_id, u.nome FROM usuario u
        WHERE u.empresa_id=%s
        AND (u.tipo='REPRESENTANTE_ADM' OR u.tipo='REPRESENTANTE'
             OR u.tipo='VENDEDOR' OR u.tipo='MASTER')
        AND u.ativo=1 ORDER BY u.nome""", (eid,)) or []

    if not vends:
        st.info("Nenhum vendedor cadastrado.")
        return

    from permissoes import e_admin, e_master, e_vendedor, usuario_id_atual
    _uid_rv = usuario_id_atual()
    if e_vendedor() and not (e_admin() or e_master()):
        # Vendedor ve apenas seu proprio roteiro
        vend_id = _uid_rv
        vend_nome = next((v[1] for v in vends if v[0] == vend_id), "Meu Roteiro")
        st.info(f"Exibindo roteiro de: **{vend_nome}**")
    else:
        vend_sel = st.selectbox("Vendedor", vends, format_func=lambda x: x[1], key="rv_sel")
        vend_id  = vend_sel[0]

    # PDVs atribuidos
    atts = query("""SELECT av.att_vendedor_id, c.nome_fantasia,
            COALESCE(p.nome_loja,'Matriz') as loja,
            p.cidade, av.dias_visita, av.frequencia, av.ativo, av.pdv_id
        FROM att_vendedor av
        JOIN pdv p ON av.pdv_id=p.pdv_id
        JOIN cliente c ON p.cliente_id=c.cliente_id
        WHERE av.vendedor_id=%s ORDER BY c.nome_fantasia, loja""", (vend_id,)) or []

    if atts:
        st.write(f"**{len(atts)} PDV(s) no roteiro**")
        for av in atts:
            av_id, cli, loja, cidade, dias, freq, ativo, pdv_id = av
            with st.expander(f"{'✅' if ativo else '❌'} {cli} — {loja} | {cidade or '—'}"):
                col1, col2, col3 = st.columns(3)
                col1.write(f"**Dias:** {dias or 'Flexível'}")
                col2.write(f"**Freq:** {freq or '—'}")
                if col3.button("🗑️ Remover", key=f"rv_rem_{av_id}"):
                    execute_write("UPDATE att_vendedor SET ativo=0 WHERE att_vendedor_id=%s", (av_id,))
                    st.rerun()
    else:
        st.info("Nenhum PDV atribuído a este vendedor.")

    st.divider()
    st.subheader("➕ Adicionar PDV")
    from permissoes import e_admin, e_master, e_promotor_vendedor, e_vendedor, usuario_id_atual
    _uid_rot = usuario_id_atual()
    from permissoes import get_lista_clientes
    if e_vendedor() and not (e_admin() or e_master()):
        clientes = get_lista_clientes(so_ativos=True)
    else:
        clientes = get_lista_clientes(so_ativos=True)
    cli_sel  = st.selectbox("Cliente", clientes, format_func=lambda x: x[1], key="rv_cli")
    if cli_sel:
        pdvs = query("SELECT pdv_id, COALESCE(nome_loja,'Matriz') FROM pdv WHERE cliente_id=%s AND ativo!=0",
                     (cli_sel[0],)) or []
        pdv_sel = st.selectbox("PDV", pdvs, format_func=lambda x: x[1], key="rv_pdv")
        col1, col2 = st.columns(2)
        dias_v = col1.text_input("Dias de visita", placeholder="Ex: Seg, Qua", key="rv_dias")
        freq_v = col2.selectbox("Frequência", ["Semanal","Quinzenal","Mensal","Sob demanda"], key="rv_freq")
        if st.button("➕ Adicionar ao roteiro", key="rv_add", type="primary"):
            execute_write("""INSERT INTO att_vendedor (vendedor_id, pdv_id, dias_visita, frequencia, ativo)
                VALUES (%s,%s,%s,%s,1) ON CONFLICT DO NOTHING""",
                (vend_id, pdv_sel[0], dias_v or None, freq_v))
            st.success("PDV adicionado ao roteiro!")
            st.rerun()


# ═══════════════════════════════════════════════════════════════
# ROTEIRO PROMOTOR
# ═══════════════════════════════════════════════════════════════

def _roteiro_promotor():
    eid = empresa_id_atual()
    st.subheader("👤 Atribuição de PDVs por Promotor")

    proms = query("""SELECT promotor_id, nome FROM promotor
        WHERE empresa_id=%s AND ativo!=0
        AND (subtipo='PROMOTOR' OR subtipo='PROMOTOR_VENDEDOR')
        ORDER BY nome""", (eid,)) or []

    if not proms:
        st.info("Nenhum promotor cadastrado.")
        return

    prom_sel = st.selectbox("Promotor", proms, format_func=lambda x: x[1], key="rp_sel")
    prom_id  = prom_sel[0]

    atts = query("""SELECT ap.att_promotor_id, c.nome_fantasia,
            COALESCE(p.nome_loja,'Matriz') as loja,
            p.cidade, ap.dia_visita, ap.frequencia_visita, ap.ativo
        FROM att_promotor ap
        JOIN pdv p ON ap.pdv_id=p.pdv_id
        JOIN cliente c ON p.cliente_id=c.cliente_id
        WHERE ap.promotor_id=%s ORDER BY ap.dia_visita, c.nome_fantasia""", (prom_id,)) or []

    DIAS = ["Segunda","Terça","Quarta","Quinta","Sexta","Sábado","Domingo"]

    if atts:
        st.write(f"**{len(atts)} PDV(s) no roteiro**")
        for ap in atts:
            ap_id, cli, loja, cidade, dia, freq, ativo = ap
            with st.expander(f"{'✅' if ativo else '❌'} {dia or '—'} | {cli} — {loja}"):
                col1, col2, col3 = st.columns(3)
                col1.write(f"**Cidade:** {cidade or '—'}")
                col2.write(f"**Freq:** {freq or '—'}")
                if col3.button("🗑️ Remover", key=f"rp_rem_{ap_id}"):
                    execute_write("UPDATE att_promotor SET ativo=0 WHERE att_promotor_id=%s", (ap_id,))
                    st.rerun()

        # Link Google Maps
        coords = query("""SELECT p.latitude, p.longitude, p.nome_loja
            FROM att_promotor ap JOIN pdv p ON ap.pdv_id=p.pdv_id
            WHERE ap.promotor_id=%s AND ap.ativo!=0
            AND p.latitude IS NOT NULL AND p.longitude IS NOT NULL""", (prom_id,)) or []
        if coords and len(coords) >= 2:
            waypoints = "/".join(f"{c[0]},{c[1]}" for c in coords[:9])
            maps_url  = f"https://www.google.com/maps/dir/{waypoints}"
            st.markdown(f"[🗺️ Abrir rota no Google Maps]({maps_url})")
    else:
        st.info("Nenhum PDV atribuído.")

    st.divider()
    st.subheader("➕ Adicionar PDV")
    from permissoes import e_admin, e_master, e_promotor_vendedor, e_vendedor, usuario_id_atual
    _uid_rot = usuario_id_atual()
    from permissoes import get_lista_clientes
    if e_vendedor() and not (e_admin() or e_master()):
        clientes = get_lista_clientes(so_ativos=True)
    else:
        clientes = get_lista_clientes(so_ativos=True)
    cli_sel  = st.selectbox("Cliente", clientes, format_func=lambda x: x[1], key="rp_cli")
    if cli_sel:
        pdvs = query("SELECT pdv_id, COALESCE(nome_loja,'Matriz') FROM pdv WHERE cliente_id=%s AND ativo!=0",
                     (cli_sel[0],)) or []
        pdv_sel = st.selectbox("PDV", pdvs, format_func=lambda x: x[1], key="rp_pdv")
        col1, col2 = st.columns(2)
        dia_v  = col1.selectbox("Dia da semana", ["—"]+DIAS, key="rp_dia")
        freq_v = col2.selectbox("Frequência", ["Semanal","Quinzenal","Mensal"], key="rp_freq")
        if st.button("➕ Adicionar", key="rp_add", type="primary"):
            execute_write("""INSERT INTO att_promotor (promotor_id, pdv_id, dia_visita, frequencia_visita, ativo)
                VALUES (%s,%s,%s,%s,1) ON CONFLICT DO NOTHING""",
                (prom_id, pdv_sel[0], None if dia_v=="—" else dia_v, freq_v))
            st.success("PDV adicionado!")
            st.rerun()


# ═══════════════════════════════════════════════════════════════
# ROTEIRO SUPERVISOR
# ═══════════════════════════════════════════════════════════════

def _roteiro_supervisor():
    eid = empresa_id_atual()
    uid = usuario_id_atual()
    st.subheader("🎯 Roteiro do Supervisor")

    if e_admin() or e_master():
        sups = query("""SELECT s.supervisor_id, s.nome FROM supervisor s
            WHERE s.empresa_id=%s AND s.ativo!=0 ORDER BY s.nome""", (eid,)) or []
        if not sups:
            st.info("Nenhum supervisor cadastrado. Acesse Equipe → Supervisores.")
            return
        sup_sel = st.selectbox("Supervisor", sups, format_func=lambda x: x[1], key="rs_sel")
        sup_id  = sup_sel[0]
    else:
        row = query("SELECT supervisor_id FROM supervisor WHERE usuario_id=%s LIMIT 1", (uid,)) or []
        if not row:
            st.warning("Supervisor não vinculado. Contate o administrador.")
            return
        sup_id = row[0][0]

    # Promotores da equipe
    st.markdown("**Equipe de promotores**")
    proms_eq = query("""SELECT p.promotor_id, p.nome FROM supervisor_promotor sp
        JOIN promotor p ON p.promotor_id=sp.promotor_id
        WHERE sp.supervisor_id=%s AND sp.ativo=1 AND p.nome!='Sem promotor'
        ORDER BY p.nome""", (sup_id,)) or []

    col_a, col_b = st.columns(2)
    with col_a:
        todos_prom = query("""SELECT p.promotor_id, p.nome FROM promotor p
            WHERE p.empresa_id=%s AND p.ativo!=0 AND p.nome!='Sem promotor'
            AND p.promotor_id NOT IN (
                SELECT promotor_id FROM supervisor_promotor WHERE supervisor_id=%s AND ativo=1
            ) ORDER BY p.nome""", (eid, sup_id)) or []
        if todos_prom:
            add_prom = st.selectbox("Adicionar promotor", todos_prom, format_func=lambda x: x[1], key="rs_add_p")
            if st.button("➕ Vincular", key="rs_btn_p"):
                execute_write("INSERT INTO supervisor_promotor (supervisor_id,promotor_id,empresa_id,ativo) VALUES (%s,%s,%s,1) ON CONFLICT DO NOTHING",
                              (sup_id, add_prom[0], eid))
                st.rerun()
    with col_b:
        if proms_eq:
            rem_prom = st.selectbox("Remover promotor", proms_eq, format_func=lambda x: x[1], key="rs_rem_p")
            if st.button("➖ Desvincular", key="rs_btn_rem_p"):
                execute_write("UPDATE supervisor_promotor SET ativo=0 WHERE supervisor_id=%s AND promotor_id=%s",
                              (sup_id, rem_prom[0]))
                st.rerun()

    if proms_eq:
        st.write(f"Equipe: **{', '.join(p[1] for p in proms_eq)}**")

    # PDVs diretos
    st.divider()
    st.markdown("**PDVs sob supervisão direta** _(sem promotor)_")
    pdvs_dir = query("""SELECT p.pdv_id, p.nome_loja, c.nome_fantasia FROM supervisor_pdv sp
        JOIN pdv p ON p.pdv_id=sp.pdv_id
        JOIN cliente c ON p.cliente_id=c.cliente_id
        WHERE sp.supervisor_id=%s AND sp.ativo=1 ORDER BY p.nome_loja""", (sup_id,)) or []

    for pdv in pdvs_dir:
        pid, nloja, ncli = pdv
        col1, col2 = st.columns([4,1])
        col1.write(f"🏪 **{nloja}** | {ncli}")
        if col2.button("➖", key=f"rs_rem_pdv_{pid}"):
            execute_write("UPDATE supervisor_pdv SET ativo=0 WHERE supervisor_id=%s AND pdv_id=%s",
                          (sup_id, pid))
            st.rerun()

    ids_dir = {p[0] for p in pdvs_dir}
    pdvs_disp = query("""SELECT p.pdv_id, p.nome_loja, c.nome_fantasia FROM pdv p
        JOIN cliente c ON p.cliente_id=c.cliente_id
        WHERE p.empresa_id=%s AND p.ativo!=0 ORDER BY p.nome_loja""", (eid,)) or []
    pdvs_disp = [p for p in pdvs_disp if p[0] not in ids_dir]
    if pdvs_disp:
        add_pdv = st.selectbox("Adicionar PDV direto", pdvs_disp,
                               format_func=lambda x: f"{x[1]} | {x[2]}", key="rs_add_pdv")
        if st.button("➕ Vincular PDV", key="rs_btn_pdv"):
            execute_write("INSERT INTO supervisor_pdv (supervisor_id,pdv_id,empresa_id,ativo) VALUES (%s,%s,%s,1) ON CONFLICT DO NOTHING",
                          (sup_id, add_pdv[0], eid))
            st.rerun()


# ═══════════════════════════════════════════════════════════════
# MEU ROTEIRO (visao pessoal)
# ═══════════════════════════════════════════════════════════════

def _meu_roteiro():
    from permissoes import perfil_atual
    uid    = usuario_id_atual()
    eid    = empresa_id_atual()
    perfil = perfil_atual()
    st.subheader("📅 Meu Roteiro")

    if perfil in ('PROMOTOR',):
        row = query("SELECT promotor_id FROM promotor WHERE usuario_id=%s LIMIT 1", (uid,)) or []
        if not row:
            st.warning("Promotor não vinculado. Contate o administrador.")
            return
        prom_id = row[0][0]
        atts = query("""SELECT c.nome_fantasia, COALESCE(p.nome_loja,'Matriz'),
                p.cidade, ap.dia_visita, ap.frequencia_visita
            FROM att_promotor ap
            JOIN pdv p ON ap.pdv_id=p.pdv_id
            JOIN cliente c ON p.cliente_id=c.cliente_id
            WHERE ap.promotor_id=%s AND ap.ativo!=0
            ORDER BY ap.dia_visita, c.nome_fantasia""", (prom_id,)) or []
        if atts:
            for a in atts:
                st.write(f"📅 **{a[3] or '—'}** | 🏪 {a[1]} | {a[0]} | {a[2] or '—'}")
        else:
            st.info("Nenhum PDV no seu roteiro ainda.")

    elif perfil == 'SUPERVISOR':
        _roteiro_supervisor()

    else:
        _roteiro_vendedor()
