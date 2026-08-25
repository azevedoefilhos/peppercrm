c = open('visitas.py', encoding='utf-8', errors='replace').read()
linhas = c.split('\n')
print("=== Linha 560-595 ===")
for i in range(559, 595):
    if i < len(linhas):
        print(f"  {i+1}: {linhas[i].rstrip()}")
