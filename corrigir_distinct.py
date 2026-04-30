#!/usr/bin/env python3
import pathlib

CAMINHO = pathlib.Path("cadastros.py")
texto = CAMINHO.read_text(encoding="utf-8")

ANTIGO = '''          SELECT DISTINCT p.produto_id, p.descricao_curta, p.codigo_produto,
                 COALESCE(cat.nome_categoria,\'—\'), COALESCE(l.nome_linha,\'—\')
          FROM produto p
          JOIN historico_preco h ON h.produto_id = p.produto_id
          LEFT JOIN categoria cat ON p.categoria_id=cat.categoria_id
          LEFT JOIN linha l       ON p.linha_id=l.linha_id
          WHERE {' AND '.join(where_p)}
          ORDER BY cat.nome_categoria, p.descricao_curta'''

NOVO = '''          SELECT DISTINCT p.produto_id, p.descricao_curta, p.codigo_produto,
                 COALESCE(cat.nome_categoria,\'—\'), COALESCE(l.nome_linha,\'—\'),
                 cat.nome_categoria, p.descricao_curta
          FROM produto p
          JOIN historico_preco h ON h.produto_id = p.produto_id
          LEFT JOIN categoria cat ON p.categoria_id=cat.categoria_id
          LEFT JOIN linha l       ON p.linha_id=l.linha_id
          WHERE {' AND '.join(where_p)}
          ORDER BY cat.nome_categoria, p.descricao_curta'''

if ANTIGO in texto:
    novo = texto.replace(ANTIGO, NOVO, 1)
    CAMINHO.write_text(novo, encoding="utf-8")
    print("✅ SELECT DISTINCT corrigido")
else:
    print("⚠️  Padrão não encontrado — verifique manualmente")
