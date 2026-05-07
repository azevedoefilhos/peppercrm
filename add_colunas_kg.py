"""
Adiciona colunas unidade_coleta, peso_coleta e preco_kg
na tabela pesquisa_preco_item do Supabase.
"""
from database import conectar

conn = conectar()

for col, tipo in [
    ("unidade_coleta", "TEXT DEFAULT 'UN'"),
    ("peso_coleta", "REAL"),
    ("preco_kg", "REAL"),
]:
    try:
        conn.execute(f"ALTER TABLE pesquisa_preco_item ADD COLUMN {col} {tipo}")
        conn.commit()
        print(f"OK: coluna {col} adicionada")
    except Exception as e:
        print(f"SKIP {col}: {e}")

conn.close()
print("Concluido!")
