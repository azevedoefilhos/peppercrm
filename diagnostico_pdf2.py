# diagnostico_pdf2.py
from dotenv import load_dotenv
load_dotenv()
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database import query

cid = 6

# Simula exatamente o que _gerar_pdf_topico faz
print("=== Query sem fornecedor_id ===")
ints = query("""
    SELECT ci.data_interacao, ci.via_comunicacao, ci.contato_pessoa,
           ci.descricao, ci.resultado, ci.data_followup, ci.ativo
    FROM contato_interacao ci
    WHERE ci.contato_id=?
    ORDER BY ci.data_interacao ASC""", (cid,))

print(f"Total bruto: {len(ints) if ints else 0}")
for r in (ints or []):
    print(f"  r[6]={r[6]} tipo={type(r[6])} | r[6] not in (0,False,None): {r[6] not in (0, False, None)}")

print("\n=== Após filtro r[6] ===")
ints_filtrado = [r for r in (ints or []) if r[6] not in (0, False, None)]
print(f"Total filtrado: {len(ints_filtrado)}")

# Verifica se o botão PDF usa fornecedor_id
print("\n=== Verificando se há fornecedor_id na sessão ===")
print("(Se o PDF foi gerado com filtro de fornecedor, pode estar filtrando errado)")

# Testa com fornecedor_id=None explícito
print("\n=== Query com fornecedor_id None (sem filtro) ===")
fornecedor_id = None
if fornecedor_id:
    ints2 = query("""
        SELECT ci.data_interacao, ci.via_comunicacao, ci.contato_pessoa,
               ci.descricao, ci.resultado, ci.data_followup, ci.ativo
        FROM contato_interacao ci
        WHERE ci.contato_id=?
          AND (ci.fornecedor_id=? OR ci.fornecedor_id IS NULL)
        ORDER BY ci.data_interacao ASC""", (cid, fornecedor_id))
else:
    ints2 = query("""
        SELECT ci.data_interacao, ci.via_comunicacao, ci.contato_pessoa,
               ci.descricao, ci.resultado, ci.data_followup, ci.ativo
        FROM contato_interacao ci
        WHERE ci.contato_id=?
        ORDER BY ci.data_interacao ASC""", (cid,))
print(f"Total: {len(ints2) if ints2 else 0}")

# Verifica como _gerar_pdf_topico é chamada
print("\n=== Procurando chamadas a _gerar_pdf_topico no contatos.py ===")
f = open('contatos.py', encoding='utf-8').read()
for i, l in enumerate(f.splitlines(), 1):
    if '_gerar_pdf_topico' in l:
        print(f"  linha {i}: {l.strip()}")
