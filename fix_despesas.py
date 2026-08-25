import ast, subprocess

with open('despesas.py', 'r', encoding='utf-8') as f:
    c = f.read()

cnt = 0

# Padrao comum aos dois blocos
antigo_std = ('    where = ["d.ativo IS NOT FALSE", "d.data_despesa BETWEEN ? AND ?"]\n'
              '    params = [d_ini, d_fim]')

novo_std   = ('    from permissoes import e_admin, e_master, usuario_id_atual\n'
              '    _uid_pdf = usuario_id_atual()\n'
              '    where = ["d.ativo IS NOT FALSE", "d.data_despesa BETWEEN ? AND ?"]\n'
              '    params = [d_ini, d_fim]\n'
              '    if not (e_admin() or e_master()):\n'
              '        where.append("d.usuario_id=?"); params.append(_uid_pdf)')

n = c.count(antigo_std)
print(f"Ocorrencias: {n}")
if n > 0:
    c = c.replace(antigo_std, novo_std)
    print(f"OK: {n} blocos de despesas filtrados por usuario_id")
    cnt += n
else:
    print("AVISO: padrao nao encontrado")

with open('despesas.py', 'w', encoding='utf-8') as f:
    f.write(c)

try:
    ast.parse(c)
    print(f"Sintaxe OK — {cnt} correcoes")
    subprocess.run(["git","add","despesas.py"])
    r = subprocess.run(["git","commit","-m","fix: despesas relatorio filtrado por usuario_id"],
                       capture_output=True, text=True)
    print("Commit:", r.stdout.strip() or r.stderr.strip())
    r2 = subprocess.run(["git","push"], capture_output=True, text=True)
    print("Push:", r2.stdout.strip() or r2.stderr.strip())
except SyntaxError as e:
    print(f"ERRO linha {e.lineno}: {e.msg}")
