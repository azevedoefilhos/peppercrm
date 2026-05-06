from database import query
cols = query("""SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_name='pesquisa_preco_item' 
    ORDER BY ordinal_position""")
for c in cols:
    print(c[0], c[1])
