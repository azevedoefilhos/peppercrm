# verificar_amorim.py
from dotenv import load_dotenv
load_dotenv()
import sys; sys.path.insert(0, '.')
from database import query

print("=== Tópicos do Amorim Burger ===")
rows = query("""
    SELECT cr.contato_id, cr.assunto, cr.data_contato, cr.status
    FROM contato_registro cr
    JOIN cliente c ON cr.cliente_id = c.cliente_id
    WHERE c.nome_fantasia ILIKE '%Amorim%'
    ORDER BY cr.contato_id DESC
""")
for r in (rows or []):
    print(f"  contato_id={r[0]} assunto={r[1][:50]} data={r[2]}")

    # contato_x_fornecedor
    cxf = query("SELECT fornecedor_id FROM contato_x_fornecedor WHERE contato_id=?", (r[0],))
    print(f"    contato_x_fornecedor: {[x[0] for x in cxf] if cxf else 'VAZIO'}")

    # contato_fornecedor_topico
    cft = query("SELECT cft_id, fornecedor_id FROM contato_fornecedor_topico WHERE contato_id=?", (r[0],))
    print(f"    contato_fornecedor_topico: {[(x[0],x[1]) for x in cft] if cft else 'VAZIO'}")
