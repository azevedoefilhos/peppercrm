#!/usr/bin/env python3
"""
Implementa coleta de preço por Kg:
1. Adiciona colunas unidade_coleta e peso_coleta na tabela
2. Adiciona toggle UN/Kg no form de coleta
3. Calcula e salva preco_kg automaticamente
"""
import pathlib
from database import conectar

# === PASSO 1: Adicionar colunas no banco ===
conn = conectar()
try:
    conn.execute("ALTER TABLE pesquisa_preco_item ADD COLUMN unidade_coleta TEXT DEFAULT 'UN'")
    conn.commit()
    print("OK: coluna unidade_coleta adicionada")
except Exception as e:
    print(f"unidade_coleta: {e}")

try:
    conn.execute("ALTER TABLE pesquisa_preco_item ADD COLUMN peso_coleta REAL")
    conn.commit()
    print("OK: coluna peso_coleta adicionada")
except Exception as e:
    print(f"peso_coleta: {e}")

try:
    conn.execute("ALTER TABLE pesquisa_preco_item ADD COLUMN preco_kg REAL")
    conn.commit()
    print("OK: coluna preco_kg adicionada")
except Exception as e:
    print(f"preco_kg: {e}")

conn.close()

# === PASSO 2: Adicionar toggle UN/Kg no form de pesquisa.py ===
src = pathlib.Path("pesquisa.py").read_text(encoding="utf-8")
original = src

# Adiciona toggle UN/Kg apos o campo de preco
OLD = '''    with st.form(key=f"{k}_form", border=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            preco = st.number_input(
                "? Pre\u00e7o (R$) *",
                min_value=0.0, format="%.2f",
                value=_v_preco,
                step=0.01, key=f"{k}_preco")
        with col2:
            frentes = st.number_input(
                "Frentes", min_value=0,
                value=_v_frentes, step=1, key=f"{k}_frt")
        with col3:
            col_of, col_pe = st.columns(2)
            oferta    = col_of.checkbox("Oferta", value=_v_oferta, key=f"{k}_of")
            ponto_extra = col_pe.checkbox("P.Extra", value=_v_pe, key=f"{k}_pe")'''

NEW = '''    with st.form(key=f"{k}_form", border=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            preco = st.number_input(
                "\U0001f4b0 Pre\u00e7o (R$) *",
                min_value=0.0, format="%.2f",
                value=_v_preco,
                step=0.01, key=f"{k}_preco")
        with col2:
            frentes = st.number_input(
                "Frentes", min_value=0,
                value=_v_frentes, step=1, key=f"{k}_frt")
        with col3:
            col_of, col_pe = st.columns(2)
            oferta    = col_of.checkbox("Oferta", value=_v_oferta, key=f"{k}_of")
            ponto_extra = col_pe.checkbox("P.Extra", value=_v_pe, key=f"{k}_pe")

        # Toggle UN/Kg para produtos vendidos por peso
        col_un, col_peso = st.columns([1, 2])
        with col_un:
            unidade_coleta = st.radio("Unidade", ["UN", "Kg"],
                                      horizontal=True, key=f"{k}_un")
        with col_peso:
            peso_coleta = None
            preco_kg = None
            if unidade_coleta == "Kg":
                peso_coleta = st.number_input("Peso coletado (Kg)",
                    min_value=0.001, value=1.0, step=0.001,
                    format="%.3f", key=f"{k}_peso",
                    help="Peso do produto na embalagem pesada")
                if peso_coleta and preco > 0:
                    preco_kg = preco / peso_coleta
                    st.caption(f"= R$ {preco_kg:.2f}/Kg")'''

if OLD in src:
    src = src.replace(OLD, NEW, 1)
    print("OK: toggle UN/Kg adicionado no form")
else:
    print("NAO ENCONTRADO form")

# === PASSO 3: Salvar unidade_coleta, peso_coleta, preco_kg no UPDATE e INSERT ===
# UPDATE
OLD_UP = '''                    conn.execute(
                        "UPDATE pesquisa_preco_item SET "
                        "preco=?, frentes=?, em_oferta=?, ponto_extra=?, "
                        "ruptura=?, observacao=? "
                        "WHERE pesquisa_item_id=?",
                        (preco if not _rup_val else None,
                         frentes, 1 if _oferta_val else 0,
                         1 if _pe_val else 0,
                         1 if _rup_val else 0,
                         obs.strip() or None,
                         existente[0]))'''

NEW_UP = '''                    conn.execute(
                        "UPDATE pesquisa_preco_item SET "
                        "preco=?, frentes=?, em_oferta=?, ponto_extra=?, "
                        "ruptura=?, observacao=?, unidade_coleta=?, peso_coleta=?, preco_kg=? "
                        "WHERE pesquisa_item_id=?",
                        (preco if not _rup_val else None,
                         frentes, 1 if _oferta_val else 0,
                         1 if _pe_val else 0,
                         1 if _rup_val else 0,
                         obs.strip() or None,
                         unidade_coleta, peso_coleta, preco_kg,
                         existente[0]))'''

if OLD_UP in src:
    src = src.replace(OLD_UP, NEW_UP, 1)
    print("OK: UPDATE com unidade_coleta")
else:
    print("NAO ENCONTRADO UPDATE")

# INSERT
OLD_IN = '''                    conn.execute(
                        "INSERT INTO pesquisa_preco_item "
                        "(pesquisa_id, produto_id, produto_concorrente_id, "
                        "preco, frentes, em_oferta, ponto_extra, ruptura, observacao) "
                        "VALUES (?,?,?,?,?,?,?,?,?)",
                        (pq_id, pid_ref, pc_id_ref,
                         preco if not _rup_val else None,
                         frentes, 1 if _oferta_val else 0,
                         1 if _pe_val else 0,
                         1 if _rup_val else 0,
                         obs.strip() or None))'''

NEW_IN = '''                    conn.execute(
                        "INSERT INTO pesquisa_preco_item "
                        "(pesquisa_id, produto_id, produto_concorrente_id, "
                        "preco, frentes, em_oferta, ponto_extra, ruptura, observacao, "
                        "unidade_coleta, peso_coleta, preco_kg) "
                        "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                        (pq_id, pid_ref, pc_id_ref,
                         preco if not _rup_val else None,
                         frentes, 1 if _oferta_val else 0,
                         1 if _pe_val else 0,
                         1 if _rup_val else 0,
                         obs.strip() or None,
                         unidade_coleta, peso_coleta, preco_kg))'''

if OLD_IN in src:
    src = src.replace(OLD_IN, NEW_IN, 1)
    print("OK: INSERT com unidade_coleta")
else:
    print("NAO ENCONTRADO INSERT")

if src != original:
    pathlib.Path("pesquisa.py").write_text(src, encoding="utf-8")
    print("pesquisa.py salvo")
