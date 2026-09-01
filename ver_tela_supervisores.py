r = __import__('subprocess').run(['git','show','HEAD:equipe.py'], capture_output=True)
c = r.stdout.decode('utf-8', errors='replace')
linhas = c.split('\n')
print("=== _tela_supervisores (657-842) ===")
for i in range(656, 842):
    if i < len(linhas):
        l = linhas[i]
        if any(x in l for x in ['promotor','vincul','equipe','supervisor','atribuir',
                                  'query','INSERT','UPDATE','form','button']):
            print(f"  {i+1}: {l.rstrip()}")
