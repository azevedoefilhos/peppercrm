#!/usr/bin/env python3
"""
Corrige INSERTs diretos em pesquisa.py que usam cur.execute com ?
substituindo por execute_write do database.py.
"""
import pathlib, sys

CAMINHO = pathlib.Path("pesquisa.py")
if not CAMINHO.exists():
    print("ERRO: pesquisa.py nao encontrado.")
    sys.exit(1)

texto = CAMINHO.read_text(encoding="utf-8")

# Corrige o INSERT de pesquisa_preco
ANTIGO = '''        conn = conectar()
        cur  = conn.cursor()
        cur.execute("""INSERT INTO pesquisa_preco
            (data_pesquisa, pdv_id, cliente_id, fornecedor_id, observacao, status)
            VALUES (?,?,?,?,?,'rascunho')""",
            (str(data_pq), pdv_id, cli_id, forn_id_pq, obs_pq or None))
        pq_id = cur.lastrowid
        conn.commit(); conn.close()'''

NOVO = '''        pq_id = execute_write("""INSERT INTO pesquisa_preco
            (data_pesquisa, pdv_id, cliente_id, fornecedor_id, observacao, status)
            VALUES (?,?,?,?,?,'rascunho')
            RETURNING pesquisa_id""",
            (str(data_pq), pdv_id, cli_id, forn_id_pq, obs_pq or None))'''

if ANTIGO in texto:
    novo = texto.replace(ANTIGO, NOVO, 1)
    CAMINHO.write_text(novo, encoding="utf-8")
    print("✅ INSERT pesquisa_preco corrigido.")
else:
    print("⚠️  Padrão exato não encontrado — verifique manualmente linhas 502-509.")
    sys.exit(1)

# Verifica se execute_write está importado
c = CAMINHO.read_text(encoding="utf-8")
if "execute_write" not in c[:500]:
    # Adiciona ao import
    novo2 = c.replace(
        "from database import",
        "from database import execute_write,",
        1
    )
    if novo2 != c:
        CAMINHO.write_text(novo2, encoding="utf-8")
        print("✅ execute_write adicionado ao import.")
    else:
        print("⚠️  Verifique se execute_write está importado no topo de pesquisa.py")
else:
    print("✅ execute_write já está importado.")

# Conta outros padrões similares
import re
ocorrencias = re.findall(r'cur\.lastrowid|conn = conectar\(\)\s*\n\s*cur\s*=\s*conn\.cursor', c)
if ocorrencias:
    print(f"⚠️  Ainda há {len(ocorrencias)} ocorrência(s) de padrão direto — revise manualmente.")
else:
    print("✅ Nenhuma outra ocorrência de padrão direto encontrada.")
