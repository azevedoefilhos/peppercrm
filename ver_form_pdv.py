r = __import__('subprocess').run(['git','show','HEAD:cadastros.py'], capture_output=True)
c = r.stdout.decode('utf-8', errors='replace')
linhas = c.split('\n')

# Ver _form_novo_pdv (linha 2691)
print("=== Novo PDV linha 2685-2710 ===")
for i in range(2684, 2715):
    print(f"  {i+1}: {linhas[i].rstrip()}")

print("\n=== Editar PDV linha 2845-2870 ===")
for i in range(2844, 2875):
    print(f"  {i+1}: {linhas[i].rstrip()}")
