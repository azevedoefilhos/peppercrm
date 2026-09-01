# roteiros.py — PepperCRM
# Modulo de roteiros inteligentes com otimizacao geografica (Haversine)

import streamlit as st
import math
from datetime import date, timedelta
from database import query, execute_write, conectar
from permissoes import (e_admin, e_master, empresa_id_atual, usuario_id_atual,
                        e_supervisor, e_promotor, e_promotor_vendedor,
                        perfil_atual, e_vendedor, get_lista_clientes)

# ═══════════════════════════════════════════════════════════════
# CONSTANTES
# ═══════════════════════════════════════════════════════════════

DIAS_SEMANA = {1:"Segunda",2:"Terça",3:"Quarta",4:"Quinta",5:"Sexta"}
DIAS_OPTS   = [(k,v) for k,v in DIAS_SEMANA.items()]
FREQ_OPTS   = ["semanal","quinzenal_1_3","quinzenal_2_4","mensal"]
FREQ_LABEL  = {
    "semanal":        "Toda semana",
    "quinzenal_1_3":  "Quinzenal (sem. 1 e 3)",
    "quinzenal_2_4":  "Quinzenal (sem. 2 e 4)",
    "mensal":         "Mensal",
}
TURNO_OPTS = ["Manhã","Tarde"]


def _ir(p):
    st.session_state["pagina"] = p
    st.session_state["_scroll_topo"] = True
    st.rerun()


# ═══════════════════════════════════════════════════════════════
# HAVERSINE — calcula distancia em km entre dois pontos GPS
# ═══════════════════════════════════════════════════════════════

def _haversine(lat1, lon1, lat2, lon2):
    R = 6371
    d_lat = math.radians(float(lat2) - float(lat1))
    d_lon = math.radians(float(lon2) - float(lon1))
    a = (math.sin(d_lat/2)**2 +
         math.cos(math.radians(float(lat1))) *
         math.cos(math.radians(float(lat2))) *
         math.sin(d_lon/2)**2)
    return R * 2 * math.asin(math.sqrt(a))


def _otimizar_rota(pdvs_coords, lat_base=None, lng_base=None):
    """
    Ordena lista de PDVs por rota mais curta usando vizinho mais proximo.
    pdvs_coords: lista de (pdv_id, nome, lat, lng, ...)
    Retorna lista reordenada.
    """
    # Filtra apenas PDVs com coordenadas
    com_coord = [p for p in pdvs_coords if p[2] and p[3]]
    sem_coord  = [p for p in pdvs_coords if not p[2] or not p[3]]

    if len(com_coord) <= 1:
        return pdvs_coords

    # Ponto de partida: base do usuario ou primeiro PDV
    if lat_base and lng_base:
        lat_atual, lng_atual = float(lat_base), float(lng_base)
    else:
        lat_atual = float(com_coord[0][2])
        lng_atual = float(com_coord[0][3])

    restantes = list(com_coord)
    ordenados = []

    while restantes:
        mais_proximo = min(
            restantes,
            key=lambda p: _haversine(lat_atual, lng_atual, p[2], p[3])
        )
        ordenados.append(mais_proximo)
        lat_atual = float(mais_proximo[2])
        lng_atual = float(mais_proximo[3])
        restantes.remove(mais_proximo)

    return ordenados + sem_coord


def _semana_do_mes(d=None):
    """Retorna o numero da semana no mes (1-4)."""
    if d is None:
        d = date.today()
    return (d.day - 1) // 7 + 1


def _pdv_ativo_hoje(frequencia):
    """Verifica se PDV com esta frequencia deve ser visitado esta semana."""
    sem = _semana_do_mes()
    if frequencia == "semanal":
        return True
    elif frequencia == "quinzenal_1_3":
        return sem in (1, 3)
    elif frequencia == "quinzenal_2_4":
        return sem in (2, 4)
    elif frequencia == "mensal":
        return sem == 1
    return True


def _url_maps(pdvs):
    """Monta URL do Google Maps com waypoints."""
    pontos = []
    for p in pdvs:
        if p[2] and p[3]:
            pontos.append(f"{p[2]},{p[3]}")
        else:
            pontos.append(str(p[1]).replace(" ", "+"))
    if not pontos:
        return None
    if len(pontos) == 1:
        return f"https://www.google.com/maps/search/{pontos[0]}"
    origem = pontos[0]
    destino = pontos[-1]
    waypoints = "/".join(pontos[1:-1])
    if waypoints:
        return f"https://www.google.com/maps/dir/{origem}/{waypoints}/{destino}"
    return f"https://www.google.com/maps/dir/{origem}/{destino}"


# ═══════════════════════════════════════════════════════════════
# TELA PRINCIPAL
# ═══════════════════════════════════════════════════════════════

def tela_roteiros():
    st.header("🗓️ Roteiros")
    if st.button("⬅ Voltar"):
        _ir("home")

    perfil = perfil_atual()
    uid    = usuario_id_atual()
    eid    = empresa_id_atual()

    # Verifica se vendedor tem permissao para editar roteiro de promotores
    _pode_editar_prom = False
    if e_admin() or e_master() or e_supervisor():
        _pode_editar_prom = True
    elif e_vendedor() or perfil in ('REPRESENTANTE','REPRESENTANTE_ADM'):
        row = query("""SELECT pode_editar_roteiro_promotor FROM vendedor
            WHERE usuario_id=%s LIMIT 1""", (uid,)) or []
        if row and row[0][0]:
            _pode_editar_prom = True

    # Monta abas conforme perfil
    ABAS = {}
    if e_admin() or e_master():
        ABAS = {
            "setores": "🗺️ Setores",
            "roteiro_vend": "💼 Rot. Vendedor",
            "roteiro_prom": "👤 Rot. Promotor",
            "execucao":    "📍 Execução do Dia",
            "cobertura":   "📊 Cobertura",
        }
    elif e_supervisor():
        ABAS = {
            "roteiro_vend": "💼 Meu Roteiro",
            "roteiro_prom": "👤 Equipe",
            "execucao":     "📍 Execução do Dia",
            "cobertura":    "📊 Cobertura",
        }
    elif _pode_editar_prom:
        ABAS = {
            "roteiro_vend": "💼 Meu Roteiro",
            "roteiro_prom": "👤 Rot. Promotor",
            "execucao":     "📍 Execução do Dia",
        }
    elif e_promotor() or e_promotor_vendedor():
        ABAS = {
            "execucao": "📍 Execução do Dia",
            "roteiro_vend": "💼 Meu Roteiro",
        }
    else:
        ABAS = {
            "roteiro_vend": "💼 Meu Roteiro",
            "execucao":     "📍 Execução do Dia",
        }

    if "rot_aba" not in st.session_state or \
       st.session_state["rot_aba"] not in ABAS:
        st.session_state["rot_aba"] = list(ABAS.keys())[0]

    cols = st.columns(len(ABAS))
    for col, (k, v) in zip(cols, ABAS.items()):
        ativa = st.session_state["rot_aba"] == k
        if col.button(v, key=f"rotnav_{k}", width="stretch",
                      type="primary" if ativa else "secondary"):
            st.session_state["rot_aba"] = k
            st.rerun()
    st.divider()

    a = st.session_state["rot_aba"]
    if a == "setores":       _tela_setores()
    elif a == "roteiro_vend": _tela_roteiro_vendedor(_pode_editar_prom)
    elif a == "roteiro_prom": _tela_roteiro_promotor()
    elif a == "execucao":    _tela_execucao_dia()
    elif a == "cobertura":   _tela_cobertura()


# ═══════════════════════════════════════════════════════════════
# ABA SETORES
# ═══════════════════════════════════════════════════════════════

def _tela_setores():
    eid = empresa_id_atual()
    st.subheader("🗺️ Setores Geográficos")
    st.caption("Organize os PDVs em setores para otimizar os roteiros de visita.")

    setores = query("""SELECT setor_id, codigo, nome, cidade, ativo
        FROM setor WHERE empresa_id=%s ORDER BY codigo""", (eid,)) or []

    # Lista de setores
    col_h1, col_h2, col_h3, col_h4 = st.columns([1,3,2,1])
    col_h1.markdown("**Código**")
    col_h2.markdown("**Nome**")
    col_h3.markdown("**Cidade**")
    col_h4.markdown("**Ativo**")
    st.divider()

    for s in setores:
        sid, cod, nome, cidade, ativo = s
        c1,c2,c3,c4,c5 = st.columns([1,3,2,0.5,0.5])
        c1.write(cod)
        c2.write(nome)
        c3.write(cidade or "—")
        c4.write("✅" if ativo else "❌")
        if c5.button("✏️", key=f"set_ed_{sid}"):
            st.session_state["set_editar"] = sid

        # Formulario de edicao inline
        if st.session_state.get("set_editar") == sid:
            with st.form(f"form_set_{sid}"):
                nc = st.text_input("Código", value=cod, key=f"set_c_{sid}")
                nn = st.text_input("Nome",   value=nome, key=f"set_n_{sid}")
                nci = st.text_input("Cidade", value=cidade or "", key=f"set_ci_{sid}")
                na = st.checkbox("Ativo", value=ativo, key=f"set_a_{sid}")
                c_s, c_c = st.columns(2)
                if c_s.form_submit_button("💾 Salvar", type="primary"):
                    execute_write("""UPDATE setor SET codigo=%s, nome=%s,
                        cidade=%s, ativo=%s WHERE setor_id=%s""",
                        (nc, nn, nci or None, na, sid))
                    st.session_state.pop("set_editar", None)
                    st.rerun()
                if c_c.form_submit_button("Cancelar"):
                    st.session_state.pop("set_editar", None)
                    st.rerun()

    st.divider()

    # PDVs por setor
    st.markdown("#### 📊 PDVs por setor")
    resumo = query("""SELECT s.nome,
            COUNT(p.pdv_id) as total,
            SUM(CASE WHEN p.aceita_promotor THEN 1 ELSE 0 END) as comporta,
            COUNT(DISTINCT ap.att_promotor_id) as tem_promotor
        FROM setor s
        LEFT JOIN pdv p ON p.setor_id=s.setor_id
        LEFT JOIN att_promotor ap ON ap.pdv_id=p.pdv_id AND ap.ativo!=0
        WHERE s.empresa_id=%s GROUP BY s.setor_id, s.nome
        ORDER BY s.codigo""", (eid,)) or []

    for r in resumo:
        nome_s, total = r[0], r[1]
        comporta = r[2] or 0
        tem_prom = r[3] or 0
        nao_comp = (total or 0) - comporta
        st.write(f"**{nome_s}** — {total or 0} PDVs | "
                 f"{comporta} comportam promotor ({tem_prom} com promotor ativo) | "
                 f"{nao_comp} não comportam")

    st.divider()

    # Novo setor
    with st.expander("➕ Novo setor"):
        with st.form("form_novo_set"):
            nc = st.text_input("Código (ex: S9)", key="set_novo_c")
            nn = st.text_input("Nome completo", key="set_novo_n")
            nci = st.text_input("Cidade principal", key="set_novo_ci")
            if st.form_submit_button("Criar setor", type="primary"):
                if nc and nn:
                    execute_write("""INSERT INTO setor (codigo, nome, cidade, empresa_id)
                        VALUES (%s,%s,%s,%s)""", (nc, nn, nci or None, eid))
                    st.success(f"Setor {nc} criado!")
                    st.rerun()
                else:
                    st.error("Código e nome são obrigatórios.")


# ═══════════════════════════════════════════════════════════════
# ABA ROTEIRO VENDEDOR
# ═══════════════════════════════════════════════════════════════

def _tela_roteiro_vendedor(pode_editar_prom=False):
    uid  = usuario_id_atual()
    eid  = empresa_id_atual()
    perfil = perfil_atual()

    st.subheader("💼 Roteiro de Visitas — Vendedor / Representante")

    # Seletor de usuario (ADM/MASTER ve todos, outros veem apenas si)
    if e_admin() or e_master():
        vends = query("""SELECT u.usuario_id, u.nome, u.tipo FROM usuario u
            WHERE u.empresa_id=%s
            AND u.tipo IN ('MASTER','ADM','REPRESENTANTE_ADM',
                           'REPRESENTANTE','VENDEDOR','SUPERVISOR')
            AND u.ativo=1 ORDER BY u.nome""", (eid,)) or []
        if not vends:
            st.info("Nenhum vendedor cadastrado.")
            return
        vend_sel = st.selectbox("Vendedor / Representante", vends,
                                format_func=lambda x: f"{x[1]} ({x[2]})",
                                key="rv2_sel")
        vend_uid = vend_sel[0]
        vend_nome = vend_sel[1]
    else:
        vend_uid  = uid
        vend_nome = query("SELECT nome FROM usuario WHERE usuario_id=%s LIMIT 1",
                          (uid,)) or [[""]]
        vend_nome = vend_nome[0][0] if vend_nome else "Meu roteiro"
        st.info(f"Roteiro de: **{vend_nome}**")

    # Ponto de base do usuario
    base = query("""SELECT lat_base, lng_base, end_base
        FROM usuario WHERE usuario_id=%s LIMIT 1""", (vend_uid,)) or []
    lat_base = float(base[0][0]) if base and base[0][0] else None
    lng_base = float(base[0][1]) if base and base[0][1] else None
    end_base = base[0][2] if base else None

    with st.expander(f"📍 Ponto de partida: {end_base or 'não definido'}"):
        with st.form("form_base_vend"):
            novo_end = st.text_input("Endereço de partida (residência ou escritório)",
                                     value=end_base or "", key="rv2_end_base")
            col_lat, col_lng = st.columns(2)
            novo_lat = col_lat.text_input("Latitude",
                                           value=str(lat_base) if lat_base else "",
                                           key="rv2_lat_base")
            novo_lng = col_lng.text_input("Longitude",
                                           value=str(lng_base) if lng_base else "",
                                           key="rv2_lng_base")
            if st.form_submit_button("💾 Salvar ponto de partida"):
                execute_write("""UPDATE usuario SET lat_base=%s, lng_base=%s,
                    end_base=%s WHERE usuario_id=%s""",
                    (novo_lat or None, novo_lng or None,
                     novo_end or None, vend_uid))
                st.success("Ponto de partida salvo!")
                st.rerun()

    st.divider()

    # Vista semanal
    hoje = date.today()
    dia_hoje = hoje.weekday() + 1  # 1=Seg...5=Sex

    # Busca roteiro do vendedor
    roteiro = query("""SELECT ri.roteiro_item_id, ri.dia_semana, ri.turno,
            ri.ordem_rota, ri.frequencia, ri.ativo,
            p.pdv_id, COALESCE(p.nome_loja,'Matriz') as loja,
            c.nome_fantasia, p.cidade,
            p.latitude, p.longitude,
            p.horario_recebimento,
            COALESCE(s.nome,'Sem setor') as setor,
            p.aceita_promotor
        FROM roteiro_item ri
        JOIN pdv p ON ri.pdv_id=p.pdv_id
        JOIN cliente c ON p.cliente_id=c.cliente_id
        LEFT JOIN setor s ON p.setor_id=s.setor_id
        WHERE ri.usuario_id=%s AND ri.tipo_roteiro='vendedor' AND ri.ativo=TRUE
        ORDER BY ri.dia_semana, ri.turno, ri.ordem_rota""", (vend_uid,)) or []

    # Organiza por dia
    por_dia = {d: [] for d in range(1, 6)}
    for r in roteiro:
        por_dia[r[1]].append(r)

    total_pdvs = len(roteiro)
    semana_atual = _semana_do_mes(hoje)

    st.markdown(f"**Roteiro semanal — {total_pdvs} PDV(s) cadastrado(s)**")
    st.caption(f"Semana {semana_atual} do mês — hoje é {DIAS_SEMANA.get(dia_hoje,'fim de semana')}")

    # Tabs dos dias
    tabs = st.tabs([f"{DIAS_SEMANA[d]} ({len(por_dia[d])})" for d in range(1,6)])

    for idx, (dia, tab) in enumerate(zip(range(1,6), tabs), 1):
        with tab:
            itens = por_dia[dia]
            is_hoje = (dia == dia_hoje)

            if not itens:
                st.caption("Nenhum PDV neste dia.")
            else:
                # Botao otimizar rota
                col_opt, col_maps = st.columns([1,1])
                if col_opt.button("🧭 Otimizar ordem", key=f"rv2_opt_{dia}"):
                    coords = [(r[6],r[7],r[10],r[11]) for r in itens]
                    ordenados = _otimizar_rota(coords, lat_base, lng_base)
                    for nova_ordem, (pdv_id,_,_,_) in enumerate(ordenados, 1):
                        # Encontra roteiro_item_id
                        for r in itens:
                            if r[6] == pdv_id:
                                execute_write("""UPDATE roteiro_item
                                    SET ordem_rota=%s WHERE roteiro_item_id=%s""",
                                    (nova_ordem, r[0]))
                                break
                    st.success("Ordem otimizada!")
                    st.rerun()

                # Botao iniciar rota
                pdvs_dia = [(r[6],r[7],r[10],r[11]) for r in itens
                            if _pdv_ativo_hoje(r[4])]
                url = _url_maps(pdvs_dia)
                if url and is_hoje:
                    col_maps.link_button("🚗 Iniciar rota de hoje", url,
                                         use_container_width=True)
                elif url:
                    col_maps.link_button("🗺️ Ver rota no Maps", url,
                                         use_container_width=True)

                # Lista PDVs do dia
                manha = [r for r in itens if r[2] == "Manhã"]
                tarde  = [r for r in itens if r[2] == "Tarde"]

                for turno_nome, turno_itens in [("🌅 Manhã", manha), ("🌆 Tarde", tarde)]:
                    if turno_itens:
                        st.markdown(f"**{turno_nome}**")
                        for r in sorted(turno_itens, key=lambda x: x[3]):
                            ri_id, dia_s, turno, ordem, freq, ativo = r[:6]
                            pdv_id, loja, cliente, cidade = r[6:10]
                            lat, lng, horario, setor, aceita_p = r[10:15]

                            ativo_semana = _pdv_ativo_hoje(freq)
                            freq_label = FREQ_LABEL.get(freq, freq)

                            icone = "✅" if ativo_semana else "⏸️"
                            coord_txt = f" 📍" if lat and lng else " (sem GPS)"

                            with st.container(border=True):
                                c1, c2, c3 = st.columns([3, 1.5, 0.8])
                                with c1:
                                    st.markdown(f"**{ordem}. {loja}** — {cliente}")
                                    st.caption(f"{icone} {freq_label} | "
                                               f"{setor} | {cidade or '—'}"
                                               f"{coord_txt}")
                                    if horario:
                                        st.caption(f"🕐 Recebimento: {horario}")
                                with c2:
                                    # Visita registrada hoje?
                                    vis = query("""SELECT visita_id FROM visita_cliente
                                        WHERE pdv_id=%s
                                        AND data_visita=%s
                                        AND usuario_id=%s LIMIT 1""",
                                        (pdv_id, hoje.isoformat(), vend_uid)) or []
                                    if vis:
                                        st.success("Visitado hoje ✓")
                                    elif is_hoje and ativo_semana:
                                        st.warning("Pendente")

                                with c3:
                                    if st.button("🗑️", key=f"rv2_rem_{ri_id}",
                                                 help="Remover do roteiro"):
                                        execute_write("""UPDATE roteiro_item
                                            SET ativo=FALSE WHERE roteiro_item_id=%s""",
                                            (ri_id,))
                                        st.rerun()

    st.divider()

    # Adicionar PDV ao roteiro
    with st.expander("➕ Adicionar PDV ao roteiro"):
        with st.form("form_add_rv"):
            # Clientes da carteira do vendedor selecionado
            # ADM/MASTER: ve todos os clientes da empresa
            if e_admin() or e_master():
                clientes = query("""SELECT c.cliente_id, c.nome_fantasia,
                    COALESCE(c.status,'Ativo') FROM cliente c
                    WHERE c.vendedor_id=%s
                    ORDER BY c.nome_fantasia""", (vend_uid,)) or []
            else:
                clientes = query("""SELECT c.cliente_id, c.nome_fantasia,
                    COALESCE(c.status,'Ativo') FROM cliente c
                    WHERE c.vendedor_id=%s
                    ORDER BY c.nome_fantasia""", (vend_uid,)) or []

            cli_sel = st.selectbox("Cliente", clientes,
                                   format_func=lambda x: f"{x[1]} [{x[2] if len(x)>2 else ''}]", key="rv2_cli")
            if cli_sel:
                pdvs_disp = query("""SELECT p.pdv_id, p.nome_loja, p.cidade,
                        COALESCE(s.nome,'Sem setor')
                    FROM pdv p LEFT JOIN setor s ON p.setor_id=s.setor_id
                    WHERE p.cliente_id=%s AND p.ativo!=0
                    ORDER BY p.nome_loja""", (cli_sel[0],)) or []

                pdv_sel = st.selectbox("PDV", pdvs_disp,
                    format_func=lambda x: f"{x[1] or 'Matriz'} ({x[3]})",
                    key="rv2_pdv")

            col1, col2, col3 = st.columns(3)
            dia_sel  = col1.selectbox("Dia da semana",
                                      [(k,v) for k,v in DIAS_SEMANA.items()],
                                      format_func=lambda x: x[1], key="rv2_dia")
            turno_sel = col2.selectbox("Turno", TURNO_OPTS, key="rv2_turno")
            freq_sel  = col3.selectbox("Frequência", FREQ_OPTS,
                                       format_func=lambda x: FREQ_LABEL[x],
                                       key="rv2_freq")

            if st.form_submit_button("➕ Adicionar ao roteiro", type="primary"):
                if cli_sel and pdv_sel:
                    # Calcula proxima ordem
                    max_ord = query("""SELECT COALESCE(MAX(ordem_rota),0) FROM roteiro_item
                        WHERE usuario_id=%s AND dia_semana=%s AND turno=%s
                        AND tipo_roteiro='vendedor'""",
                        (vend_uid, dia_sel[0], turno_sel)) or [[0]]
                    nova_ord = (max_ord[0][0] or 0) + 1

                    execute_write("""INSERT INTO roteiro_item
                        (tipo_roteiro, usuario_id, pdv_id, dia_semana, turno,
                         ordem_rota, frequencia, ativo, empresa_id, criado_por)
                        VALUES ('vendedor',%s,%s,%s,%s,%s,%s,TRUE,%s,%s)
                        ON CONFLICT (tipo_roteiro,usuario_id,pdv_id,dia_semana,turno)
                        DO UPDATE SET ativo=TRUE, frequencia=EXCLUDED.frequencia""",
                        (vend_uid, pdv_sel[0], dia_sel[0], turno_sel,
                         nova_ord, freq_sel, eid, uid))
                    st.success(f"PDV adicionado ao roteiro de {DIAS_SEMANA[dia_sel[0]]}!")
                    st.rerun()


# ═══════════════════════════════════════════════════════════════
# ABA ROTEIRO PROMOTOR
# ═══════════════════════════════════════════════════════════════

def _tela_roteiro_promotor():
    uid = usuario_id_atual()
    eid = empresa_id_atual()

    st.subheader("👤 Roteiro de Visitas — Promotor")

    # Seletor de promotor
    if e_admin() or e_master():
        proms = query("""SELECT u.usuario_id, u.nome, u.tipo FROM usuario u
            WHERE u.empresa_id=%s
            AND u.tipo IN ('PROMOTOR','PROMOTOR_VENDEDOR')
            AND u.ativo=1 ORDER BY u.nome""", (eid,)) or []
    elif e_supervisor():
        # Apenas promotores da equipe do supervisor
        sup = query("SELECT supervisor_id FROM supervisor WHERE usuario_id=%s LIMIT 1",
                    (uid,)) or []
        sup_id = sup[0][0] if sup else None
        proms = query("""SELECT u.usuario_id, u.nome, u.tipo
            FROM supervisor_promotor sp
            JOIN promotor pr ON sp.promotor_id=pr.promotor_id
            JOIN usuario u ON pr.usuario_id=u.usuario_id
            WHERE sp.supervisor_id=%s AND sp.ativo=1 AND u.ativo=1
            ORDER BY u.nome""", (sup_id,)) or [] if sup_id else []
    else:
        # Vendedor habilitado: promotores dos seus clientes
        proms = query("""SELECT DISTINCT u.usuario_id, u.nome, u.tipo
            FROM promotor pr
            JOIN usuario u ON pr.usuario_id=u.usuario_id
            JOIN att_promotor ap ON ap.promotor_id=pr.promotor_id
            JOIN pdv p ON ap.pdv_id=p.pdv_id
            JOIN cliente c ON p.cliente_id=c.cliente_id
            WHERE c.vendedor_id=%s AND u.ativo=1
            ORDER BY u.nome""", (uid,)) or []

    if not proms:
        st.info("Nenhum promotor disponível.")
        return

    prom_sel = st.selectbox("Promotor", proms,
                            format_func=lambda x: f"{x[1]} ({x[2]})",
                            key="rp2_sel")
    prom_uid = prom_sel[0]

    # Ponto de base do promotor
    base = query("""SELECT lat_base, lng_base, end_base
        FROM usuario WHERE usuario_id=%s LIMIT 1""", (prom_uid,)) or []
    lat_base = float(base[0][0]) if base and base[0][0] else None
    lng_base = float(base[0][1]) if base and base[0][1] else None
    end_base = base[0][2] if base else None

    st.caption(f"📍 Base: {end_base or 'não definida'}")

    # Busca roteiro do promotor
    hoje = date.today()
    dia_hoje = hoje.weekday() + 1

    roteiro = query("""SELECT ri.roteiro_item_id, ri.dia_semana, ri.turno,
            ri.ordem_rota, ri.frequencia, ri.ativo,
            p.pdv_id, COALESCE(p.nome_loja,'Matriz') as loja,
            c.nome_fantasia, p.cidade,
            p.latitude, p.longitude,
            p.horario_recebimento,
            COALESCE(s.nome,'Sem setor') as setor
        FROM roteiro_item ri
        JOIN pdv p ON ri.pdv_id=p.pdv_id
        JOIN cliente c ON p.cliente_id=c.cliente_id
        LEFT JOIN setor s ON p.setor_id=s.setor_id
        WHERE ri.usuario_id=%s AND ri.tipo_roteiro='promotor' AND ri.ativo=TRUE
        ORDER BY ri.dia_semana, ri.turno, ri.ordem_rota""", (prom_uid,)) or []

    por_dia = {d: [] for d in range(1, 6)}
    for r in roteiro:
        por_dia[r[1]].append(r)

    st.markdown(f"**{len(roteiro)} PDV(s) no roteiro**")

    tabs = st.tabs([f"{DIAS_SEMANA[d]} ({len(por_dia[d])})" for d in range(1,6)])

    for dia, tab in zip(range(1,6), tabs):
        with tab:
            itens = por_dia[dia]
            is_hoje = (dia == dia_hoje)

            if not itens:
                st.caption("Nenhum PDV neste dia.")
            else:
                col_opt, col_maps = st.columns([1,1])
                if col_opt.button("🧭 Otimizar ordem", key=f"rp2_opt_{dia}"):
                    coords = [(r[6],r[7],r[10],r[11]) for r in itens]
                    ordenados = _otimizar_rota(coords, lat_base, lng_base)
                    for nova_ord, (pdv_id,_,_,_) in enumerate(ordenados, 1):
                        for r in itens:
                            if r[6] == pdv_id:
                                execute_write("""UPDATE roteiro_item
                                    SET ordem_rota=%s WHERE roteiro_item_id=%s""",
                                    (nova_ord, r[0]))
                                break
                    st.success("Ordem otimizada!")
                    st.rerun()

                pdvs_dia = [(r[6],r[7],r[10],r[11]) for r in itens
                            if _pdv_ativo_hoje(r[4])]
                url = _url_maps(pdvs_dia)
                if url:
                    label = "🚗 Iniciar rota de hoje" if is_hoje else "🗺️ Ver rota"
                    col_maps.link_button(label, url, use_container_width=True)

                manha = [r for r in itens if r[2]=="Manhã"]
                tarde  = [r for r in itens if r[2]=="Tarde"]

                for turno_nome, turno_itens in [("🌅 Manhã", manha), ("🌆 Tarde", tarde)]:
                    if turno_itens:
                        st.markdown(f"**{turno_nome}**")
                        for r in sorted(turno_itens, key=lambda x: x[3]):
                            ri_id = r[0]
                            pdv_id, loja, cliente, cidade = r[6:10]
                            lat, lng, horario, setor = r[10:14]
                            freq = r[4]
                            ordem = r[3]

                            freq_label = FREQ_LABEL.get(freq, freq)
                            ativo_sem = _pdv_ativo_hoje(freq)

                            with st.container(border=True):
                                c1, c2, c3 = st.columns([3, 1.5, 0.8])
                                with c1:
                                    st.markdown(f"**{ordem}. {loja}** — {cliente}")
                                    st.caption(f"{'✅' if ativo_sem else '⏸️'} "
                                               f"{freq_label} | {setor} | {cidade or '—'}")
                                    if horario:
                                        st.caption(f"🕐 {horario}")
                                with c2:
                                    vis = query("""SELECT visita_id FROM visita_cliente
                                        WHERE pdv_id=%s AND data_visita=%s
                                        AND usuario_id=%s LIMIT 1""",
                                        (pdv_id, hoje.isoformat(), prom_uid)) or []
                                    if vis:
                                        st.success("Visitado ✓")
                                    elif is_hoje and ativo_sem:
                                        st.warning("Pendente")
                                with c3:
                                    if st.button("🗑️", key=f"rp2_rem_{ri_id}"):
                                        execute_write("""UPDATE roteiro_item
                                            SET ativo=FALSE WHERE roteiro_item_id=%s""",
                                            (ri_id,))
                                        st.rerun()

    st.divider()

    # Adicionar PDV
    with st.expander("➕ Adicionar PDV ao roteiro do promotor"):
        with st.form("form_add_rp"):
            # Filtra PDVs que aceitam promotor
            # Clientes ativos com PDVs
            if e_admin() or e_master() or e_supervisor():
                clientes_p = query("""SELECT DISTINCT c.cliente_id, c.nome_fantasia
                    FROM cliente c JOIN pdv p ON p.cliente_id=c.cliente_id
                    WHERE p.ativo!=0 AND c.empresa_id=%s AND c.status='Ativo'
                    ORDER BY c.nome_fantasia""", (eid,)) or []
            else:
                clientes_p = query("""SELECT DISTINCT c.cliente_id, c.nome_fantasia
                    FROM cliente c JOIN pdv p ON p.cliente_id=c.cliente_id
                    WHERE p.ativo!=0 AND c.vendedor_id=%s AND c.status='Ativo'
                    ORDER BY c.nome_fantasia""", (uid,)) or []
            cli_p = st.selectbox("Cliente", clientes_p,
                                 format_func=lambda x: x[1], key="rp2_cli")

            if cli_p:
                pdvs_p = query("""SELECT p.pdv_id, p.nome_loja, p.cidade,
                        COALESCE(s.nome,'Sem setor'), p.aceita_promotor
                    FROM pdv p LEFT JOIN setor s ON p.setor_id=s.setor_id
                    WHERE p.cliente_id=%s AND p.ativo!=0
                    ORDER BY p.nome_loja""", (cli_p[0],)) or []

                pdv_p = st.selectbox("PDV", pdvs_p,
                    format_func=lambda x: f"{x[1] or 'Matriz'} ({x[3]})",
                    key="rp2_pdv")

            col1, col2, col3 = st.columns(3)
            dia_p   = col1.selectbox("Dia", [(k,v) for k,v in DIAS_SEMANA.items()],
                                     format_func=lambda x: x[1], key="rp2_dia")
            turno_p = col2.selectbox("Turno", TURNO_OPTS, key="rp2_turno")
            freq_p  = col3.selectbox("Frequência", FREQ_OPTS,
                                     format_func=lambda x: FREQ_LABEL[x],
                                     key="rp2_freq")

            if st.form_submit_button("➕ Adicionar", type="primary"):
                if cli_p and pdv_p:
                    max_ord = query("""SELECT COALESCE(MAX(ordem_rota),0) FROM roteiro_item
                        WHERE usuario_id=%s AND dia_semana=%s AND turno=%s
                        AND tipo_roteiro='promotor'""",
                        (prom_uid, dia_p[0], turno_p)) or [[0]]
                    nova_ord = (max_ord[0][0] or 0) + 1

                    execute_write("""INSERT INTO roteiro_item
                        (tipo_roteiro, usuario_id, pdv_id, dia_semana, turno,
                         ordem_rota, frequencia, ativo, empresa_id, criado_por)
                        VALUES ('promotor',%s,%s,%s,%s,%s,%s,TRUE,%s,%s)
                        ON CONFLICT (tipo_roteiro,usuario_id,pdv_id,dia_semana,turno)
                        DO UPDATE SET ativo=TRUE, frequencia=EXCLUDED.frequencia""",
                        (prom_uid, pdv_p[0], dia_p[0], turno_p,
                         nova_ord, freq_p, eid, uid))
                    st.success("PDV adicionado ao roteiro!")
                    st.rerun()


# ═══════════════════════════════════════════════════════════════
# ABA EXECUCAO DO DIA
# ═══════════════════════════════════════════════════════════════

def _tela_execucao_dia():
    uid    = usuario_id_atual()
    eid    = empresa_id_atual()
    perfil = perfil_atual()
    hoje   = date.today()
    dia_hoje = hoje.weekday() + 1  # 1=Seg...5=Sex

    st.subheader(f"📍 Execução do Dia — {DIAS_SEMANA.get(dia_hoje,'Fim de semana')}, "
                 f"{hoje.strftime('%d/%m/%Y')}")

    if dia_hoje > 5:
        st.info("Hoje é fim de semana — nenhum roteiro programado.")
        return

    # Resolve qual usuario ver
    if perfil in ('PROMOTOR', 'PROMOTOR_VENDEDOR'):
        exec_uid = uid
    else:
        exec_uid = uid

    # Tipo de roteiro
    tipo = 'promotor' if perfil in ('PROMOTOR','PROMOTOR_VENDEDOR') else 'vendedor'

    roteiro_hoje = query("""SELECT ri.roteiro_item_id, ri.turno, ri.ordem_rota,
            ri.frequencia, p.pdv_id, COALESCE(p.nome_loja,'Matriz'),
            c.nome_fantasia, p.cidade, p.horario_recebimento,
            p.latitude, p.longitude,
            COALESCE(s.nome,'Sem setor')
        FROM roteiro_item ri
        JOIN pdv p ON ri.pdv_id=p.pdv_id
        JOIN cliente c ON p.cliente_id=c.cliente_id
        LEFT JOIN setor s ON p.setor_id=s.setor_id
        WHERE ri.usuario_id=%s AND ri.tipo_roteiro=%s
          AND ri.dia_semana=%s AND ri.ativo=TRUE
        ORDER BY ri.turno, ri.ordem_rota""",
        (exec_uid, tipo, dia_hoje)) or []

    if not roteiro_hoje:
        st.info("Nenhum PDV programado para hoje.")
        return

    # Filtra por frequencia
    ativos = [r for r in roteiro_hoje if _pdv_ativo_hoje(r[3])]
    pausados = [r for r in roteiro_hoje if not _pdv_ativo_hoje(r[3])]

    # Metricas
    visitados = []
    pendentes = []
    for r in ativos:
        pdv_id = r[4]
        vis = query("""SELECT visita_id FROM visita_cliente
            WHERE pdv_id=%s AND data_visita=%s AND usuario_id=%s LIMIT 1""",
            (pdv_id, hoje.isoformat(), exec_uid)) or []
        if vis:
            visitados.append(r)
        else:
            pendentes.append(r)

    col1, col2, col3 = st.columns(3)
    col1.metric("PDVs hoje", len(ativos))
    col2.metric("✅ Visitados", len(visitados))
    col3.metric("⏳ Pendentes", len(pendentes))

    # Progresso
    if ativos:
        prog = len(visitados) / len(ativos)
        st.progress(prog, text=f"{len(visitados)}/{len(ativos)} PDVs concluídos")

    # Botao iniciar rota
    pdvs_pendentes = [(r[4],r[5],r[9],r[10]) for r in pendentes]
    url = _url_maps(pdvs_pendentes)
    if url and pendentes:
        st.link_button("🚗 Navegar pelos pendentes", url,
                       use_container_width=False)

    st.divider()

    # Lista completa
    for turno_nome, turno_letra in [("🌅 Manhã", "Manhã"), ("🌆 Tarde", "Tarde")]:
        turno_itens = [r for r in ativos if r[1] == turno_letra]
        if not turno_itens:
            continue
        st.markdown(f"**{turno_nome}**")
        for r in turno_itens:
            ri_id, turno, ordem, freq = r[:4]
            pdv_id, loja, cliente, cidade, horario = r[4:9]
            lat, lng, setor = r[9:12]

            vis = query("""SELECT visita_id FROM visita_cliente
                WHERE pdv_id=%s AND data_visita=%s AND usuario_id=%s LIMIT 1""",
                (pdv_id, hoje.isoformat(), exec_uid)) or []
            visitado = bool(vis)

            with st.container(border=True):
                c1, c2, c3 = st.columns([3, 1.5, 1])
                with c1:
                    icone = "✅" if visitado else "⏳"
                    st.markdown(f"**{icone} {ordem}. {loja}** — {cliente}")
                    st.caption(f"{setor} | {cidade or '—'}")
                    if horario:
                        st.caption(f"🕐 Recebimento: {horario}")
                with c2:
                    if lat and lng:
                        maps_pdv = f"https://www.google.com/maps?q={lat},{lng}"
                        st.link_button("📍 Como chegar", maps_pdv,
                                       use_container_width=True)
                with c3:
                    if visitado:
                        st.success("Visitado")
                    else:
                        if st.button("📝 Registrar visita",
                                     key=f"exec_vis_{pdv_id}",
                                     use_container_width=True):
                            st.session_state["vis_pdv_pre"] = pdv_id
                            st.session_state["pagina"] = "visitas"
                            st.rerun()

    # PDVs pausados (quinzenal/mensal fora da semana)
    if pausados:
        with st.expander(f"⏸️ PDVs pausados esta semana ({len(pausados)})"):
            for r in pausados:
                loja, cliente = r[5], r[6]
                freq = FREQ_LABEL.get(r[3], r[3])
                st.caption(f"⏸️ {loja} — {cliente} | {freq}")


# ═══════════════════════════════════════════════════════════════
# ABA COBERTURA E ALERTAS
# ═══════════════════════════════════════════════════════════════

def _tela_cobertura():
    eid = empresa_id_atual()
    uid = usuario_id_atual()
    hoje = date.today()

    st.subheader("📊 Cobertura e Alertas")
    st.caption("PDVs com visitas atrasadas em relação ao roteiro programado.")

    # Filtros
    col1, col2 = st.columns(2)
    dias_atraso = col1.number_input("Alertar PDVs sem visita há mais de X dias",
                                    min_value=1, max_value=60, value=7,
                                    key="cob_dias")

    # Busca PDVs com roteiro mas sem visita recente
    limite = (hoje - timedelta(days=int(dias_atraso))).isoformat()

    atrasados = query("""SELECT DISTINCT
            u.nome as colaborador, u.tipo,
            COALESCE(p.nome_loja,'Matriz') as loja,
            c.nome_fantasia, p.cidade,
            COALESCE(s.nome,'Sem setor'),
            MAX(v.data_visita) as ultima_visita,
            ri.frequencia
        FROM roteiro_item ri
        JOIN usuario u ON ri.usuario_id=u.usuario_id
        JOIN pdv p ON ri.pdv_id=p.pdv_id
        JOIN cliente c ON p.cliente_id=c.cliente_id
        LEFT JOIN setor s ON p.setor_id=s.setor_id
        LEFT JOIN visita_cliente v ON v.pdv_id=p.pdv_id
            AND v.usuario_id=ri.usuario_id
        WHERE ri.ativo=TRUE AND u.empresa_id=%s
        GROUP BY u.nome, u.tipo, p.nome_loja, c.nome_fantasia,
                 p.cidade, s.nome, ri.frequencia, ri.roteiro_item_id
        HAVING MAX(v.data_visita) < %s OR MAX(v.data_visita) IS NULL
        ORDER BY ultima_visita ASC NULLS FIRST, u.nome""",
        (eid, limite)) or []

    if not atrasados:
        st.success(f"✅ Todos os PDVs foram visitados nos últimos {dias_atraso} dias!")
        return

    st.error(f"⚠️ {len(atrasados)} PDV(s) sem visita há mais de {dias_atraso} dias")

    # Agrupa por colaborador
    por_colab = {}
    for r in atrasados:
        colab = r[0]
        if colab not in por_colab:
            por_colab[colab] = []
        por_colab[colab].append(r)

    for colab, itens in por_colab.items():
        tipo = itens[0][1]
        with st.expander(f"👤 {colab} ({tipo}) — {len(itens)} PDV(s) atrasado(s)"):
            for r in itens:
                _, _, loja, cliente, cidade, setor, ultima, freq = r
                freq_label = FREQ_LABEL.get(freq, freq or "—")
                ultima_txt = ultima or "Nunca visitado"
                st.write(f"🔴 **{loja}** — {cliente} | {setor}")
                st.caption(f"Última visita: {ultima_txt} | Freq: {freq_label} | {cidade or '—'}")
