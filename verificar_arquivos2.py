# verificar_arquivos2.py
import os

checks = {
    'usuarios.py': [
        ('PROMOTOR_VENDEDOR na lista perfis', 'PROMOTOR_VENDEDOR'),
        ('Vincular a promotor existente', 'Vincular a promotor'),
        ('Vincular a supervisor existente', 'Vincular a supervisor'),
        ('Editar dados usuario', 'Editar dados'),
        ('Desativar com carteira', 'desat_pendente'),
        ('Verificar exclusao', 'Verificar exclus'),
    ],
    'visitas.py': [
        ('Aba Supervisores em promotores', 'sup_aba'),
        ('_tela_cadastro_supervisores', '_tela_cadastro_supervisores'),
        ('Supervisores cadastrados', 'Supervisores cadastrados'),
        ('_tela_supervisor', '_tela_supervisor'),
        ('tipo_visita no INSERT', 'tipo_visita_reg'),
        ('Botao Supervisao', 'Supervisao'),
    ],
}

for arquivo, verificacoes in checks.items():
    tam = os.path.getsize(arquivo)
    txt = open(arquivo, encoding='utf-8').read()
    print(f"\n=== {arquivo} ({tam} bytes) ===")
    for desc, chave in verificacoes:
        ok = chave in txt
        print(f"  {'OK' if ok else 'FALTA'} — {desc}")
