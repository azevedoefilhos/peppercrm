#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
lines = src.splitlines()

# Encontra linha do if _salvar
start = None
for i, l in enumerate(lines):
    if '        if _salvar:' in l:
        start = i
        break

if not start:
    print("NAO ENCONTRADO")
    exit()

# Encontra o fim do bloco (conn.commit / st.success / st.rerun)
end = None
for i in range(start, min(start+80, len(lines))):
    if 'st.rerun()' in lines[i] and i > start + 30:
        end = i
        break

print(f"Bloco: linhas {start+1} a {end+1}")
print("Contexto atual:")
for i in range(start, end+1):
    print(i+1, lines[i][:85].encode('ascii','replace').decode())

# Substitui o bloco inteiro por versao correta
novo_bloco = '''        if _salvar:
            if preco <= 0 and not ruptura:
                st.error("Informe o preço ou marque Ruptura.")
                return

            try:
                conn = conectar()
                pid_ref   = produto_id
                pc_id_ref = pc_id if tipo in ("conc", "concorrente") else None

                if pc_id_ref:
                    where_ex = "pesquisa_id=? AND produto_concorrente_id=?"
                    val_ex   = (pq_id, pc_id_ref)
                else:
                    where_ex = "pesquisa_id=? AND produto_id=? AND produto_concorrente_id IS NULL"
                    val_ex   = (pq_id, pid_ref)

                existente = conn.execute(
                    f"SELECT pesquisa_item_id FROM pesquisa_preco_item WHERE {where_ex} LIMIT 1",
                    val_ex).fetchone()

                if existente:
                    conn.execute(
                        "UPDATE pesquisa_preco_item SET "
                        "preco=?, frentes=?, em_oferta=?, ponto_extra=?, "
                        "ruptura=?, observacao=? "
                        "WHERE pesquisa_item_id=?",
                        (preco if not ruptura else None,
                         frentes, 1 if oferta else 0,
                         1 if ponto_extra else 0,
                         1 if ruptura else 0,
                         obs.strip() or None,
                         existente[0]))
                else:
                    conn.execute(
                        "INSERT INTO pesquisa_preco_item "
                        "(pesquisa_id, produto_id, produto_concorrente_id, "
                        "preco, frentes, em_oferta, ponto_extra, ruptura, observacao) "
                        "VALUES (?,?,?,?,?,?,?,?,?)",
                        (pq_id, pid_ref, pc_id_ref,
                         preco if not ruptura else None,
                         frentes, 1 if oferta else 0,
                         1 if ponto_extra else 0,
                         1 if ruptura else 0,
                         obs.strip() or None))

                if prod_vinc_id and pc_id_ref:
                    conn.execute(
                        "INSERT OR IGNORE INTO produto_concorrente_relacao "
                        "(produto_id, produto_concorrente_id, tipo_relacao) "
                        "VALUES (?,?,'indireto')", (prod_vinc_id, pc_id_ref))

                conn.commit()
                conn.close()

                st.session_state.pop(f"ean_input_{pq_id}", None)
                st.session_state.pop(f"ean_buscar_off_{pq_id}", None)
                st.session_state.pop(f"nav_produto_pendente_{pq_id}", None)
                st.session_state.pop(f"campo_busca_{pq_id}", None)
                st.session_state.pop(f"{k}_confirmar_update", None)
                st.session_state[f"ean_ultimo_{pq_id}"] = label
                st.success(f"✅ **{label}** — salvo!")
                st.rerun()

            except Exception as _e:
                st.error(f"Erro ao salvar: {_e}")'''

new_lines = lines[:start] + novo_bloco.splitlines() + lines[end+1:]
pathlib.Path("pesquisa.py").write_text('\n'.join(new_lines), encoding="utf-8")
print("\n✅ Bloco de save substituído")
