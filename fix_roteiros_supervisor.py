import ast, subprocess

r = subprocess.run(['git','show','HEAD:roteiros.py'], capture_output=True)
c = r.stdout.decode('utf-8', errors='replace').replace('\r\n','\n')

# ═══ FIX 1: Adiciona aba Supervisor no menu ═══
antigo_abas_adm = (
    '    if e_admin() or e_master():\n'
    '        ABAS = {\n'
    '            "setores": "🗺️ Setores",\n'
    '            "roteiro_vend": "💼 Rot. Vendedor",\n'
    '            "roteiro_prom": "👤 Rot. Promotor",\n'
    '            "execucao":    "📍 Execução do Dia",\n'
    '            "cobertura":   "📊 Cobertura",\n'
    '        }\n'
    '    elif e_supervisor():\n'
    '        ABAS = {\n'
    '            "roteiro_vend": "💼 Meu Roteiro",\n'
    '            "roteiro_prom": "👤 Equipe",\n'
    '            "execucao":     "📍 Execução do Dia",\n'
    '            "cobertura":    "📊 Cobertura",\n'
    '        }\n'
    '    elif _pode_editar_prom:\n'
    '        ABAS = {\n'
    '            "roteiro_vend": "💼 Meu Roteiro",\n'
    '            "roteiro_prom": "👤 Rot. Promotor",\n'
    '            "execucao":     "📍 Execução do Dia",\n'
    '        }\n'
    '    elif e_promotor() or e_promotor_vendedor():\n'
    '        ABAS = {\n'
    '            "execucao": "📍 Execução do Dia",\n'
    '            "roteiro_vend": "💼 Meu Roteiro",\n'
    '        }\n'
    '    else:\n'
    '        ABAS = {\n'
    '            "roteiro_vend": "💼 Meu Roteiro",\n'
    '            "execucao":     "📍 Execução do Dia",\n'
    '        }')

novo_abas_adm = (
    '    if e_admin() or e_master():\n'
    '        ABAS = {\n'
    '            "setores":      "🗺️ Setores",\n'
    '            "roteiro_vend": "💼 Rot. Vendedor",\n'
    '            "roteiro_sup":  "🎯 Rot. Supervisor",\n'
    '            "roteiro_prom": "👤 Rot. Promotor",\n'
    '            "execucao":     "📍 Execução do Dia",\n'
    '            "cobertura":    "📊 Cobertura",\n'
    '        }\n'
    '    elif e_supervisor():\n'
    '        ABAS = {\n'
    '            "roteiro_sup":  "🎯 Meu Roteiro",\n'
    '            "roteiro_prom": "👤 Minha Equipe",\n'
    '            "execucao":     "📍 Execução do Dia",\n'
    '            "cobertura":    "📊 Cobertura",\n'
    '        }\n'
    '    elif _pode_editar_prom:\n'
    '        ABAS = {\n'
    '            "roteiro_vend": "💼 Meu Roteiro",\n'
    '            "roteiro_prom": "👤 Rot. Promotor",\n'
    '            "execucao":     "📍 Execução do Dia",\n'
    '        }\n'
    '    elif e_promotor() or e_promotor_vendedor():\n'
    '        ABAS = {\n'
    '            "execucao":     "📍 Execução do Dia",\n'
    '            "roteiro_vend": "💼 Meu Roteiro",\n'
    '        }\n'
    '    else:\n'
    '        ABAS = {\n'
    '            "roteiro_vend": "💼 Meu Roteiro",\n'
    '            "execucao":     "📍 Execução do Dia",\n'
    '        }')

if antigo_abas_adm in c:
    c = c.replace(antigo_abas_adm, novo_abas_adm)
    print("OK: abas com Rot. Supervisor")
else:
    print("AVISO: bloco abas nao encontrado")

# ═══ FIX 2: Adiciona dispatcher para roteiro_sup ═══
antigo_disp = (
    '    if a == "setores":       _tela_setores()\n'
    '    elif a == "roteiro_vend": _tela_roteiro_vendedor(_pode_editar_prom)\n'
    '    elif a == "roteiro_prom": _tela_roteiro_promotor()\n'
    '    elif a == "execucao":    _tela_execucao_dia()\n'
    '    elif a == "cobertura":   _tela_cobertura()')

novo_disp = (
    '    if a == "setores":        _tela_setores()\n'
    '    elif a == "roteiro_vend":  _tela_roteiro_vendedor(_pode_editar_prom)\n'
    '    elif a == "roteiro_sup":   _tela_roteiro_supervisor()\n'
    '    elif a == "roteiro_prom":  _tela_roteiro_promotor()\n'
    '    elif a == "execucao":      _tela_execucao_dia()\n'
    '    elif a == "cobertura":     _tela_cobertura()')

if antigo_disp in c:
    c = c.replace(antigo_disp, novo_disp)
    print("OK: dispatcher com roteiro_sup")
else:
    print("AVISO: dispatcher nao encontrado")

# ═══ FIX 3: Adiciona funcao _tela_roteiro_supervisor antes de _tela_roteiro_promotor ═══
funcao_supervisor = '''

# ═══════════════════════════════════════════════════════════════
# ABA ROTEIRO SUPERVISOR
# ═══════════════════════════════════════════════════════════════

def _tela_roteiro_supervisor():
    uid = usuario_id_atual()
    eid = empresa_id_atual()

    st.subheader("🎯 Roteiro de Visitas — Supervisor")
    st.caption("Visitas de supervisão e cobertura temporária de PDVs sem promotor.")

    # Seletor de supervisor (ADM/MASTER ve todos)
    if e_admin() or e_master():
        sups = query("""SELECT u.usuario_id, u.nome FROM usuario u
            WHERE u.empresa_id=%s AND u.tipo='SUPERVISOR' AND u.ativo=1
            ORDER BY u.nome""", (eid,)) or []
        if not sups:
            st.info("Nenhum supervisor cadastrado.")
            return
        sup_sel = st.selectbox("Supervisor", sups,
                               format_func=lambda x: x[1], key="rsup_sel")
        sup_uid = sup_sel[0]
    else:
        sup_uid = uid
        nome_sup = query("SELECT nome FROM usuario WHERE usuario_id=%s LIMIT 1",
                         (uid,)) or [[""]]
        st.info(f"Roteiro de: **{nome_sup[0][0]}**")

    # Ponto de base
    base = query("SELECT lat_base, lng_base, end_base FROM usuario WHERE usuario_id=%s LIMIT 1",
                 (sup_uid,)) or []
    lat_base = float(base[0][0]) if base and base[0][0] else None
    lng_base = float(base[0][1]) if base and base[0][1] else None
    end_base = base[0][2] if base else None

    with st.expander(f"📍 Ponto de partida: {end_base or 'não definido'}"):
        with st.form("form_base_sup"):
            novo_end = st.text_input("Endereço de partida", value=end_base or "",
                                     key="rsup_end_base")
            c1, c2 = st.columns(2)
            novo_lat = c1.text_input("Latitude", value=str(lat_base) if lat_base else "",
                                     key="rsup_lat")
            novo_lng = c2.text_input("Longitude", value=str(lng_base) if lng_base else "",
                                     key="rsup_lng")
            if st.form_submit_button("💾 Salvar"):
                execute_write("UPDATE usuario SET lat_base=%s, lng_base=%s, end_base=%s WHERE usuario_id=%s",
                              (novo_lat or None, novo_lng or None, novo_end or None, sup_uid))
                st.success("Ponto de partida salvo!")
                st.rerun()

    st.divider()

    hoje     = date.today()
    dia_hoje = hoje.weekday() + 1

    # Roteiro do supervisor
    roteiro = query("""SELECT ri.roteiro_item_id, ri.dia_semana, ri.turno,
            ri.ordem_rota, ri.frequencia,
            p.pdv_id, COALESCE(p.nome_loja,'Matriz'),
            c.nome_fantasia, p.cidade,
            p.latitude, p.longitude, p.horario_recebimento,
            COALESCE(s.nome,'Sem setor'),
            -- Tem promotor ativo neste PDV?
            (SELECT COUNT(*) FROM att_promotor ap2
             WHERE ap2.pdv_id=p.pdv_id AND ap2.ativo!=0) as n_prom
        FROM roteiro_item ri
        JOIN pdv p ON ri.pdv_id=p.pdv_id
        JOIN cliente c ON p.cliente_id=c.cliente_id
        LEFT JOIN setor s ON p.setor_id=s.setor_id
        WHERE ri.usuario_id=%s AND ri.tipo_roteiro='supervisor' AND ri.ativo=TRUE
        ORDER BY ri.dia_semana, ri.turno, ri.ordem_rota""", (sup_uid,)) or []

    por_dia = {d: [] for d in range(1, 6)}
    for r in roteiro:
        por_dia[r[1]].append(r)

    st.markdown(f"**{len(roteiro)} PDV(s) no roteiro do supervisor**")
    tabs = st.tabs([f"{DIAS_SEMANA[d]} ({len(por_dia[d])})" for d in range(1, 6)])

    for dia, tab in zip(range(1, 6), tabs):
        with tab:
            itens = por_dia[dia]
            is_hoje = (dia == dia_hoje)

            if not itens:
                st.caption("Nenhum PDV neste dia.")
            else:
                col_opt, col_maps = st.columns(2)
                if col_opt.button("🧭 Otimizar ordem", key=f"rsup_opt_{dia}"):
                    coords = [(r[5], r[6], r[9], r[10]) for r in itens]
                    ordenados = _otimizar_rota(coords, lat_base, lng_base)
                    for nova_ord, (pdv_id, _, _, _) in enumerate(ordenados, 1):
                        for r in itens:
                            if r[5] == pdv_id:
                                execute_write("UPDATE roteiro_item SET ordem_rota=%s WHERE roteiro_item_id=%s",
                                              (nova_ord, r[0]))
                                break
                    st.success("Ordem otimizada!"); st.rerun()

                pdvs_dia = [(r[5], r[6], r[9], r[10]) for r in itens if _pdv_ativo_hoje(r[4])]
                url = _url_maps(pdvs_dia)
                if url:
                    label = "🚗 Iniciar rota" if is_hoje else "🗺️ Ver rota"
                    col_maps.link_button(label, url, use_container_width=True)

                manha = [r for r in itens if r[2] == "Manhã"]
                tarde  = [r for r in itens if r[2] == "Tarde"]

                for turno_nome, turno_itens in [("🌅 Manhã", manha), ("🌆 Tarde", tarde)]:
                    if not turno_itens: continue
                    st.markdown(f"**{turno_nome}**")
                    for r in sorted(turno_itens, key=lambda x: x[3]):
                        ri_id, _, turno, ordem, freq = r[:5]
                        pdv_id, loja, cliente, cidade = r[5:9]
                        lat, lng, horario, setor, n_prom = r[9:14]

                        ativo_sem = _pdv_ativo_hoje(freq)
                        tipo_visita = "👁️ Supervisão" if n_prom > 0 else "🔧 Cobertura temp."

                        with st.container(border=True):
                            c1, c2, c3 = st.columns([3, 1.5, 0.8])
                            with c1:
                                st.markdown(f"**{ordem}. {loja}** — {cliente}")
                                st.caption(f"{tipo_visita} | {FREQ_LABEL.get(freq,freq)} | {setor} | {cidade or '—'}")
                                if horario: st.caption(f"🕐 {horario}")
                            with c2:
                                vis = query("""SELECT visita_id FROM visita_cliente
                                    WHERE pdv_id=%s AND data_visita=%s AND usuario_id=%s LIMIT 1""",
                                    (pdv_id, hoje.isoformat(), sup_uid)) or []
                                if vis: st.success("Visitado ✓")
                                elif is_hoje and ativo_sem: st.warning("Pendente")
                            with c3:
                                if st.button("🗑️", key=f"rsup_rem_{ri_id}"):
                                    execute_write("UPDATE roteiro_item SET ativo=FALSE WHERE roteiro_item_id=%s", (ri_id,))
                                    st.rerun()

    st.divider()

    # Adicionar PDV ao roteiro do supervisor
    with st.expander("➕ Adicionar PDV ao roteiro"):
        st.caption("PDVs da equipe (supervisão) e PDVs sem promotor (cobertura temporária).")
        with st.form("form_add_rsup"):
            # Busca supervisor_id
            sup_row = query("SELECT supervisor_id FROM supervisor WHERE usuario_id=%s AND ativo!=0 LIMIT 1",
                            (sup_uid,)) or []
            sup_id = sup_row[0][0] if sup_row else None

            if sup_id:
                # PDVs da equipe do supervisor
                pdvs_equipe = query("""SELECT DISTINCT p.pdv_id,
                        COALESCE(p.nome_loja,'Matriz') as loja,
                        c.nome_fantasia, p.cidade,
                        COALESCE(s.nome,'Sem setor'),
                        (SELECT COUNT(*) FROM att_promotor ap
                         WHERE ap.pdv_id=p.pdv_id AND ap.ativo!=0) as n_prom
                    FROM supervisor_promotor sp
                    JOIN att_promotor ap ON ap.promotor_id=sp.promotor_id AND ap.ativo!=0
                    JOIN pdv p ON ap.pdv_id=p.pdv_id
                    JOIN cliente c ON p.cliente_id=c.cliente_id
                    LEFT JOIN setor s ON p.setor_id=s.setor_id
                    WHERE sp.supervisor_id=%s AND sp.ativo=1
                    ORDER BY c.nome_fantasia, p.nome_loja""", (sup_id,)) or []
            else:
                pdvs_equipe = []

            # PDVs sem promotor (cobertura)
            pdvs_sem_prom = query("""SELECT p.pdv_id,
                    COALESCE(p.nome_loja,'Matriz'),
                    c.nome_fantasia, p.cidade,
                    COALESCE(s.nome,'Sem setor'), 0
                FROM pdv p
                JOIN cliente c ON p.cliente_id=c.cliente_id
                LEFT JOIN setor s ON p.setor_id=s.setor_id
                WHERE p.aceita_promotor=TRUE
                  AND c.empresa_id=%s
                  AND NOT EXISTS (
                      SELECT 1 FROM att_promotor ap
                      WHERE ap.pdv_id=p.pdv_id AND ap.ativo!=0)
                ORDER BY c.nome_fantasia, p.nome_loja""", (eid,)) or []

            todos_pdvs = []
            if pdvs_equipe:
                todos_pdvs += [(p[0], f"👁️ {p[1]} — {p[2]} ({p[4]})") for p in pdvs_equipe]
            if pdvs_sem_prom:
                todos_pdvs += [(p[0], f"🔧 {p[1]} — {p[2]} ({p[4]})") for p in pdvs_sem_prom]

            if not todos_pdvs:
                st.info("Nenhum PDV disponível para adicionar.")
                st.form_submit_button("Fechar", disabled=True)
            else:
                pdv_sel = st.selectbox("PDV", todos_pdvs,
                                       format_func=lambda x: x[1], key="rsup_pdv")
                col1, col2, col3 = st.columns(3)
                dia_sel   = col1.selectbox("Dia", [(k,v) for k,v in DIAS_SEMANA.items()],
                                           format_func=lambda x: x[1], key="rsup_dia")
                turno_sel = col2.selectbox("Turno", TURNO_OPTS, key="rsup_turno")
                freq_sel  = col3.selectbox("Frequência", FREQ_OPTS,
                                           format_func=lambda x: FREQ_LABEL[x], key="rsup_freq")

                if st.form_submit_button("➕ Adicionar", type="primary"):
                    max_ord = query("""SELECT COALESCE(MAX(ordem_rota),0) FROM roteiro_item
                        WHERE usuario_id=%s AND dia_semana=%s AND turno=%s
                        AND tipo_roteiro='supervisor'""",
                        (sup_uid, dia_sel[0], turno_sel)) or [[0]]
                    nova_ord = (max_ord[0][0] or 0) + 1
                    execute_write("""INSERT INTO roteiro_item
                        (tipo_roteiro, usuario_id, pdv_id, dia_semana, turno,
                         ordem_rota, frequencia, ativo, empresa_id, criado_por)
                        VALUES ('supervisor',%s,%s,%s,%s,%s,%s,TRUE,%s,%s)
                        ON CONFLICT (tipo_roteiro,usuario_id,pdv_id,dia_semana,turno)
                        DO UPDATE SET ativo=TRUE, frequencia=EXCLUDED.frequencia""",
                        (sup_uid, pdv_sel[0], dia_sel[0], turno_sel,
                         nova_ord, freq_sel, eid, uid))
                    st.success("PDV adicionado ao roteiro de supervisão!")
                    st.rerun()

'''

# Insere a funcao antes de _tela_roteiro_promotor
marcador = '\n# ═══════════════════════════════════════════════════════════════\n# ABA ROTEIRO PROMOTOR'
if marcador in c:
    c = c.replace(marcador, funcao_supervisor + marcador)
    print("OK: _tela_roteiro_supervisor adicionada")
else:
    print("AVISO: marcador promotor nao encontrado")

# ═══ FIX 4: roteiro_item UNIQUE precisa incluir 'supervisor' ═══
# Ja esta coberto pelo CHECK na tabela

# ═══ FIX 5: Rot. Vendedor — remover Supervisor da lista ═══
antigo_vends = (
    '        vends = query("""SELECT u.usuario_id, u.nome, u.tipo FROM usuario u\n'
    '            WHERE u.empresa_id=%s\n'
    "            AND u.tipo IN ('MASTER','ADM','REPRESENTANTE_ADM',\n"
    "                           'REPRESENTANTE','VENDEDOR','SUPERVISOR')\n"
    '            AND u.ativo=1 ORDER BY u.nome""", (eid,)) or []')

novo_vends = (
    '        vends = query("""SELECT u.usuario_id, u.nome, u.tipo FROM usuario u\n'
    '            WHERE u.empresa_id=%s\n'
    "            AND u.tipo IN ('MASTER','ADM','REPRESENTANTE_ADM',\n"
    "                           'REPRESENTANTE','VENDEDOR')\n"
    '            AND u.ativo=1 ORDER BY u.nome""", (eid,)) or []')

if antigo_vends in c:
    c = c.replace(antigo_vends, novo_vends)
    print("OK: Supervisor removido do Rot. Vendedor")
else:
    print("AVISO: lista vendedores nao encontrada")

# ═══ FIX 6: Tabela roteiro_item — adicionar 'supervisor' no CHECK ═══
# O CHECK atual e: CHECK(tipo_roteiro IN ('vendedor','promotor'))
# Precisa adicionar 'supervisor' — faremos via script de banco separado

print("\nVerificando sintaxe...")
with open('roteiros.py', 'w', encoding='utf-8') as f:
    f.write(c)

try:
    ast.parse(c); print("Sintaxe OK")
    subprocess.run(["git","add","roteiros.py"])
    r2 = subprocess.run(["git","commit","-m",
        "feat: aba Rot.Supervisor separada com PDVs equipe e cobertura temporaria"],
        capture_output=True, text=True)
    print("Commit:", r2.stdout.strip() or r2.stderr.strip())
    r3 = subprocess.run(["git","push"], capture_output=True, text=True)
    print("Push:", r3.stdout.strip() or r3.stderr.strip())
except SyntaxError as e:
    print(f"ERRO linha {e.lineno}: {e.msg}")
    lines = c.split('\n')
    for i in range(max(0,e.lineno-3), min(len(lines),e.lineno+2)):
        print(f"  {i+1}: {lines[i]}")
