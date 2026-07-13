# d2_faseC_nova_empresa.py
# Cadastra nova empresa e usuario admin no PepperCRM
# Preencha as variaveis abaixo e execute UMA UNICA VEZ

from dotenv import load_dotenv; load_dotenv()
import sys, hashlib, secrets
sys.path.insert(0, '.')
from database import _pg_connect

# ================================================================
# PREENCHA AQUI antes de rodar
# ================================================================
EMPRESA_NOME   = "Nome da Empresa do Amigo Representacoes"
EMPRESA_CNPJ   = ""                          # opcional
EMPRESA_PLANO  = "solo"                      # solo / equipe / escritorio
ADMIN_NOME     = "Nome do Amigo"
ADMIN_EMAIL    = "email@dominio.com.br"      # sera o login
ADMIN_SENHA    = "senha123"                  # trocar no primeiro acesso
# ================================================================

def hash_senha(s):
    return hashlib.sha256(s.encode()).hexdigest()

conn = _pg_connect()
conn.autocommit = False
cur = conn.cursor()

try:
    print("=== Cadastrando nova empresa ===\n")

    # Verifica se email ja existe
    cur.execute("SELECT usuario_id FROM usuario WHERE email=%s", (ADMIN_EMAIL.lower(),))
    if cur.fetchone():
        print(f"ERRO: Email {ADMIN_EMAIL} ja cadastrado.")
        raise SystemExit(1)

    # Limites por plano
    planos = {
        "solo":      {"max_usuarios": 1,  "max_clientes": 150},
        "equipe":    {"max_usuarios": 5,  "max_clientes": 500},
        "escritorio":{"max_usuarios": 15, "max_clientes": 9999},
    }
    limites = planos.get(EMPRESA_PLANO, planos["solo"])

    # 1. Cria empresa
    cur.execute("""
        INSERT INTO empresa (nome, cnpj, email_admin, plano, status,
                             max_usuarios, max_clientes, ativo)
        VALUES (%s, %s, %s, %s, 'ativo', %s, %s, 1)
        RETURNING empresa_id
    """, (EMPRESA_NOME, EMPRESA_CNPJ or None, ADMIN_EMAIL.lower(),
          EMPRESA_PLANO, limites["max_usuarios"], limites["max_clientes"]))
    empresa_id = cur.fetchone()[0]
    print(f"OK empresa criada: empresa_id={empresa_id}")

    # 2. Cria usuario admin
    cur.execute("""
        INSERT INTO usuario (nome, email, senha_hash, tipo, empresa_id, ativo)
        VALUES (%s, %s, %s, 'REPRESENTANTE_ADM', %s, 1)
        RETURNING usuario_id
    """, (ADMIN_NOME, ADMIN_EMAIL.lower(), hash_senha(ADMIN_SENHA), empresa_id))
    usuario_id = cur.fetchone()[0]
    print(f"OK usuario criado: usuario_id={usuario_id}")

    # 3. Cria configuracao inicial
    cur.execute("""
        INSERT INTO configuracao (empresa_nome, empresa_id)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
    """, (EMPRESA_NOME, empresa_id))
    print(f"OK configuracao criada")

    conn.commit()

    print(f"""
=== Empresa cadastrada com sucesso! ===
  empresa_id : {empresa_id}
  nome       : {EMPRESA_NOME}
  plano      : {EMPRESA_PLANO}
  login      : {ADMIN_EMAIL}
  senha      : {ADMIN_SENHA}
  URL        : https://peppercrm-production.up.railway.app
""")

except SystemExit:
    conn.rollback()
except Exception as e:
    conn.rollback()
    print(f"ERRO: {e}")
    raise
finally:
    cur.close()
    conn.close()
