from database import query

fotos = query("SELECT foto_id, LEFT(foto_path, 50), legenda FROM pesquisa_foto WHERE ativo=1 ORDER BY foto_id DESC LIMIT 5")
for f in fotos:
    print(f"ID:{f[0]} | path_inicio:'{f[1]}' | legenda:{f[2]}")
