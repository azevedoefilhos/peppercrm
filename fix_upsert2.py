#!/usr/bin/env python3
import pathlib

src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
original = src

OLD = '''def _upsert_item(pq_id, prod_id, pc_id, dados):
    preco, oferta, frentes, ruptura, pe, tpe, obs = dados
    conn = conectar()
    conn.execute("""DELETE FROM pesquisa_preco_item
        WHERE pesquisa_id=? AND produto_id=? AND produto_concorrente_id=?""",
        (pq_id, prod_id, pc_id))
    conn.execute("""INSERT INTO pesquisa_preco_item
        (pesquisa_id, produto_id, produto_concorrente_id,
         preco, em_oferta, frentes, ruptura, ponto_extra, tipo_ponto_extra, observaca
        VALUES (?,?,?,?,?,?,?,?,?,?)""",
        (pq_id, prod_id, pc_id, preco, oferta, frentes, ruptura, pe, tpe, obs))
    conn.commit(); conn.close()'''

# Busca pelo inicio da funcao
idx = src.find('def _upsert_item(pq_id, prod_id, pc_id, dados):\n    preco, oferta, frentes, ruptura, pe, tpe, obs = dados')
if idx >= 0:
    end_idx = src.find('conn.commit(); conn.close()', idx) + len('conn.commit(); conn.close()')
    old_block = src[idx:end_idx]
    new_block = '''def _upsert_item(pq_id, prod_id, pc_id, dados):
    if len(dados) == 10:
        preco, oferta, frentes, ruptura, pe, tpe, obs, unidade_coleta, peso_coleta, preco_kg = dados
    else:
        preco, oferta, frentes, ruptura, pe, tpe, obs = dados
        unidade_coleta, peso_coleta, preco_kg = 'UN', None, None
    conn = conectar()
    conn.execute("""DELETE FROM pesquisa_preco_item
        WHERE pesquisa_id=? AND produto_id=? AND produto_concorrente_id=?""",
        (pq_id, prod_id, pc_id))
    conn.execute("""INSERT INTO pesquisa_preco_item
        (pesquisa_id, produto_id, produto_concorrente_id,
         preco, em_oferta, frentes, ruptura, ponto_extra, tipo_ponto_extra, observacao,
         unidade_coleta, peso_coleta, preco_kg)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (pq_id, prod_id, pc_id, preco, oferta, frentes, ruptura, pe, tpe, obs,
         unidade_coleta, peso_coleta, preco_kg))
    conn.commit(); conn.close()'''
    src = src.replace(old_block, new_block, 1)
    pathlib.Path("pesquisa.py").write_text(src, encoding="utf-8")
    print("OK")
else:
    print("NAO ENCONTRADO")
