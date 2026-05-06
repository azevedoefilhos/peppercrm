from database import query

print("=== Clientes Akira ===")
for c in query("SELECT cliente_id, nome_fantasia, status FROM cliente WHERE nome_fantasia ILIKE '%akira%'"):
    print(dict(c))

print("\n=== Clientes Amorim ===")
for c in query("SELECT cliente_id, nome_fantasia FROM cliente WHERE nome_fantasia ILIKE '%amorim%'"):
    print(dict(c))

print("\n=== PDVs Akira/Amorim ===")
for p in query("""SELECT p.pdv_id, p.nome_loja, p.ativo, c.nome_fantasia, c.cliente_id
    FROM pdv p JOIN cliente c ON p.cliente_id=c.cliente_id
    WHERE c.nome_fantasia ILIKE '%akira%' OR c.nome_fantasia ILIKE '%amorim%'
    OR p.nome_loja ILIKE '%akira%'"""):
    print(dict(p))

print("\n=== Contatos Akira ===")
for c in query("""SELECT cr.contato_id, cr.assunto, cr.cliente_id, cr.status, cr.data_contato, cr.ativo
    FROM contato_registro cr
    LEFT JOIN cliente c ON cr.cliente_id=c.cliente_id
    WHERE c.nome_fantasia ILIKE '%akira%'"""):
    print(dict(c))

print("\n=== Contatos Amorim ===")
for c in query("""SELECT cr.contato_id, cr.assunto, cr.cliente_id, cr.status, cr.data_contato, cr.ativo
    FROM contato_registro cr
    LEFT JOIN cliente c ON cr.cliente_id=c.cliente_id
    WHERE c.nome_fantasia ILIKE '%amorim%'"""):
    print(dict(c))
