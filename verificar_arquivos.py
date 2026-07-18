# verificar_arquivos.py
for f in ['usuarios.py', 'visitas.py']:
    txt = open(f, encoding='utf-8').read()
    print(f"=== {f} ({len(txt)} bytes) ===")
    print(f"  supervisor cadastrados: {'Supervisores cadastrados' in txt}")
    print(f"  vinculo promotor: {'Vincular a promotor' in txt}")
    print(f"  vinculo supervisor: {'Vincular a supervisor' in txt}")
    print(f"  _tela_cadastro_supervisores: {'_tela_cadastro_supervisores' in txt}")
    print()
