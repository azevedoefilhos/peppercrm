# instalar_arquivos.py
# Copia os arquivos corretos diretamente para a pasta peppercrm
import shutil, os

base = os.path.dirname(os.path.abspath(__file__))

arquivos = {
    'usuarios.py': r'C:\Users\welov\PycharmProjects\WebSolution\peppercrm\usuarios.py',
    'visitas.py':  r'C:\Users\welov\PycharmProjects\WebSolution\peppercrm\visitas.py',
}

for nome, destino in arquivos.items():
    origem = os.path.join(base, nome)
    if os.path.exists(origem):
        shutil.copy2(origem, destino)
        tam_orig = os.path.getsize(origem)
        tam_dest = os.path.getsize(destino)
        print(f"OK {nome}: {tam_orig} bytes -> destino {tam_dest} bytes")
    else:
        print(f"ERRO: {origem} nao encontrado")
