r = __import__('subprocess').run(['git','show','HEAD:roteiros.py'], capture_output=True)
c = r.stdout.decode('utf-8', errors='replace')
linhas = c.split('\n')
for i in range(843, 860):
    print(f"  {i+1}: {linhas[i].rstrip()}")
