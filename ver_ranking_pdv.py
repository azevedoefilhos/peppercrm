c = open('relatorios.py', encoding='utf-8', errors='replace').read()
linhas = c.split('\n')
print("=== _rel_ranking_pdv ===")
for i in range(589, 680):
    if i < len(linhas):
        l = linhas[i]
        if any(x in l for x in ['CANCELADO','SUSPENSO','status','WHERE','where','params','get_where']):
            print(f"  {i+1}: {l.rstrip()}")
