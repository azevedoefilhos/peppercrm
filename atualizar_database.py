#!/usr/bin/env python3
"""
Reescreve o bloco de conexão do database.py para usar parâmetros individuais
(host, port, dbname, user, password) em vez de URL — elimina problemas de
encoding de senha com caracteres especiais como # @ !
"""
import re, sys, pathlib

CAMINHO = pathlib.Path("database.py")

if not CAMINHO.exists():
    print("ERRO: database.py não encontrado na pasta atual.")
    sys.exit(1)

NOVO_BLOCO = '''def _get_pg_password():
    import os
    return os.environ.get("SUPABASE_DB_PASSWORD", "")

def conectar():
    import psycopg2
    return psycopg2.connect(
        host="aws-1-sa-east-1.pooler.supabase.com",
        port=5432,
        dbname="postgres",
        user="postgres.yunzqndswpwttejlgeaa",
        password=_get_pg_password(),
        sslmode="require",
        connect_timeout=15,
    )
'''

texto = CAMINHO.read_text(encoding="utf-8")

# Remove _get_pg_url e def conectar() antiga
padrao = re.compile(
    r'def _get_pg_url\(\).*?(?=\ndef \w|\Z)',
    re.DOTALL
)

if padrao.search(texto):
    novo_texto = padrao.sub(NOVO_BLOCO, texto, count=1)
    print("Padrão _get_pg_url encontrado e substituído.")
else:
    # Fallback: substitui def conectar() sozinha
    padrao2 = re.compile(r'def conectar\(\):.*?(?=\ndef \w|\Z)', re.DOTALL)
    if padrao2.search(texto):
        novo_texto = padrao2.sub(NOVO_BLOCO, texto, count=1)
        print("Padrão conectar() encontrado e substituído.")
    else:
        print("ERRO: nenhum padrão encontrado. Edite manualmente.")
        sys.exit(1)

CAMINHO.write_text(novo_texto, encoding="utf-8")

# Verificação
c = CAMINHO.read_text(encoding="utf-8")
print("✅ database.py atualizado!" if "host=" in c and "pooler.supabase.com" in c else "⚠️ Verifique manualmente!")
print(f"  host= individual: {'✅' if 'host=' in c else '❌'}")
print(f"  pooler host:      {'✅' if 'aws-1-sa-east-1.pooler.supabase.com' in c else '❌'}")
print(f"  URL antiga:       {'✅ removida' if '_get_pg_url' not in c else '⚠️ ainda presente'}")
