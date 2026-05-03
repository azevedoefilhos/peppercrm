"""
Limpa strings 'nan' do campo ean_concorrente no banco Supabase.
Substitui 'nan' por NULL corretamente.
"""
from database import conectar

conn = conectar()
cur = conn.cursor()

# Conta registros afetados
cur.execute("SELECT COUNT(*) FROM produto_concorrente WHERE ean_concorrente='nan'")
total = cur.fetchone()[0]
print(f"Registros com ean='nan': {total}")

# Limpa
cur.execute("UPDATE produto_concorrente SET ean_concorrente=NULL WHERE ean_concorrente='nan'")
conn.commit()
print(f"✅ {total} registros corrigidos — ean_concorrente='nan' → NULL")

# Verifica outros campos com nan
for campo in ['descricao', 'descricao_curta', 'observacao']:
    cur.execute(f"SELECT COUNT(*) FROM produto_concorrente WHERE {campo}='nan'")
    n = cur.fetchone()[0]
    if n > 0:
        cur.execute(f"UPDATE produto_concorrente SET {campo}=NULL WHERE {campo}='nan'")
        print(f"✅ {n} registros {campo}='nan' → NULL")

conn.commit()
conn.close()
print("Concluído!")
