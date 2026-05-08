#!/usr/bin/env python3
import pathlib

lines = pathlib.Path("pesquisa.py").read_text(encoding="utf-8").splitlines()

novo = [
    '',
    '    # Status visual: busca itens ja pesquisados',
    '    _pesq = query("SELECT produto_id, produto_concorrente_id, preco, em_oferta, ponto_extra, ruptura FROM pesquisa_preco_item WHERE pesquisa_id=?", (pq_id,))',
    '    _mp = {}',
    '    for _r in _pesq:',
    '        if _r[0]: _mp[("n", int(_r[0]))] = (_r[2], _r[3], _r[4], _r[5])',
    '        if _r[1]: _mp[("c", int(_r[1]))] = (_r[2], _r[3], _r[4], _r[5])',
    '',
    '    def _lbl(tk, ik, mk, dk):',
    '        base = f"{mk} \u2014 {dk}"',
    '        d = _mp.get((tk, ik))',
    '        if not d: return base',
    '        pr, of, pe, ru = d',
    '        if ru: return f"\u2713 {base}  \u00b7  Ruptura"',
    '        ps = f"R$ {pr:,.2f}".replace(",","X").replace(".",",").replace("X",".") if pr else "?"',
    '        ex = (" Of." if of else "") + (" PE" if pe else "")',
    '        return f"\u2713 {base}  \u00b7  {ps}{ex}"',
    '',
    '    if nossos:',
    '        st.markdown("**\U0001f7e2 Nossos:**")',
    '        for pid, desc, marca in nossos:',
    '            lbl = _lbl("n", pid, marca, desc)',
    '            if st.button(lbl, key=f"campo_nav_n_{pq_id}_{pid}", use_container_width=True):',
    '                resultado = {"tipo":"nosso","produto_id":pid,"descricao":desc,"marca":marca,"ean":None,"pc_id":None}',
    '                st.session_state[f"nav_produto_pendente_{pq_id}"] = {"resultado": resultado, "ean": ""}',
    '                st.rerun()',
    '',
    '    if concs:',
    '        st.markdown("**\U0001f534 Concorrentes:**")',
    '        for pc_id, desc, marca, ean in concs:',
    '            lbl = _lbl("c", pc_id, marca, desc)',
    '            if st.button(lbl, key=f"campo_nav_c_{pq_id}_{pc_id}", use_container_width=True):',
    '                resultado = {"tipo":"conc","pc_id":pc_id,"descricao":desc,"marca":marca,"ean":ean,"auditavel":1}',
    '                st.session_state[f"nav_produto_pendente_{pq_id}"] = {"resultado": resultado, "ean": ean or ""}',
    '                st.rerun()',
]

# Substitui linhas 1154-1179 (indices 1154-1179, antes do "if nossos" ha uma linha em branco)
new_lines = lines[:1154] + novo + lines[1179:]
pathlib.Path("pesquisa.py").write_text('\n'.join(new_lines), encoding="utf-8")
print(f"OK: inserido na primeira instancia")
