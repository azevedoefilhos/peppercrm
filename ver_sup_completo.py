r = __import__('subprocess').run(['git','show','HEAD:equipe.py'], capture_output=True)
c = r.stdout.decode('utf-8', errors='replace')
linhas = c.split('\n')
print("=== _tela_supervisores linhas 720-842 ===")
for i in range(719, 842):
    if i < len(linhas):
        print(f"  {i+1}: {linhas[i].rstrip()}")
