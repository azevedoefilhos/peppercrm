# criar_usuario.py
from dotenv import load_dotenv
load_dotenv()
import os, sys, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database import execute_write, query

def hash_senha(senha):
    return hashlib.sha256(senha.encode('utf-8')).hexdigest()

# Verifica se já existe
rows = query("SELECT usuario_id FROM usuario WHERE email = ?", ("fernando",))
if rows:
    print("Usuário já existe — atualizando senha...")
    execute_write(
        "UPDATE usuario SET senha_hash=?, ativo=1 WHERE email=?",
        (hash_senha("pepper2026"), "fernando")
    )
else:
    execute_write(
        "INSERT INTO usuario (nome, email, senha_hash, tipo, ativo) VALUES (?,?,?,?,1)",
        ("Fernando Azevedo Jr.", "fernando", hash_senha("pepper2026"), "REPRESENTANTE_ADM")
    )

rows = query("SELECT usuario_id, nome, email, tipo, ativo FROM usuario")
print("Usuários cadastrados:")
for r in (rows or []):
    print(f"  id={r[0]} nome={r[1]} email={r[2]} tipo={r[3]} ativo={r[4]}")
print("OK")
