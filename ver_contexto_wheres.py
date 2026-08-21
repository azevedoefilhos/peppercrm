import os

def ver_linhas(fname, linhas_alvo, n=3):
    if not os.path.exists(fname): return
    c = open(fname, encoding='utf-8', errors='replace').read()
    linhas = c.split('\n')
    print(f"\n=== {fname} ===")
    for alvo in linhas_alvo:
        print(f"\n--- linha {alvo} ---")
        for i in range(max(0, alvo-2), min(len(linhas), alvo+n)):
            print(f"  {i+1}: {linhas[i].rstrip()}")

ver_linhas('cadastros.py',  [1550, 1990, 2526, 3060])
ver_linhas('contatos.py',   [140])
ver_linhas('relatorios.py', [850, 997, 1294])
ver_linhas('despesas.py',   [565, 628])
