c = open('resultado_operacional.py', encoding='utf-8', errors='replace').read()
linhas = c.split('\n')

print("=== Primeiras 60 linhas ===")
for i in range(60):
    print(f"  {i+1}: {linhas[i].rstrip()}")

print("\n=== Queries principais ===")
for i, l in enumerate(linhas, 1):
    if 'query(' in l or 'FROM pedido' in l or 'FROM despesa' in l or 'FROM comissao' in l:
        print(f"  {i}: {l.rstrip()}")
