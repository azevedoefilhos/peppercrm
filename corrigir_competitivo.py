#!/usr/bin/env python3
import pathlib, re

CAMINHO = pathlib.Path("relatorios.py")
src = CAMINHO.read_text(encoding="utf-8")

# Busca pelo padrao com regex
padrao = re.compile(
    r'(SELECT DISTINCT p\.produto_id, p\.descricao_curta, p\.codigo_produto,\s*\n'
    r'\s*p\.peso, p\.unidade_medida,\s*\n'
    r'\s*COALESCE\(cat\.nome_categoria,[^\)]+\)\s*\n'
    r'\s*FROM produto p\s*\n'
    r'\s*LEFT JOIN categoria cat ON p\.categoria_id=cat\.categoria_id\s*\n'
    r'\s*JOIN produto_concorrente_relacao pcr ON pcr\.produto_id=p\.produto_id\s*\n'
    r'\s*WHERE \{[^\}]+\}\s*\n'
    r'\s*)(ORDER BY cat\.nome_categoria, p\.descricao_curta)',
    re.MULTILINE
)

if padrao.search(src):
    src2 = padrao.sub(
        lambda m: m.group(1).replace('SELECT DISTINCT', 'SELECT', 1) +
        'GROUP BY p.produto_id, p.descricao_curta, p.codigo_produto, p.peso, p.unidade_medida, cat.nome_categoria\n        ORDER BY cat.nome_categoria, p.descricao_curta',
        src, count=1
    )
    CAMINHO.write_text(src2, encoding="utf-8")
    print("✅ Corrigido via regex")
else:
    # Tenta substituicao direta por linha
    lines = src.splitlines()
    for i, l in enumerate(lines):
        if 'SELECT DISTINCT p.produto_id' in l and i > 1280:
            lines[i] = l.replace('SELECT DISTINCT', 'SELECT')
            # Procura ORDER BY e adiciona GROUP BY antes
            for j in range(i, min(i+15, len(lines))):
                if 'ORDER BY cat.nome_categoria' in lines[j]:
                    lines.insert(j, '        GROUP BY p.produto_id, p.descricao_curta, p.codigo_produto, p.peso, p.unidade_medida, cat.nome_categoria')
                    print("✅ Corrigido por inserção de linha")
                    break
            break
    CAMINHO.write_text('\n'.join(lines), encoding="utf-8")
