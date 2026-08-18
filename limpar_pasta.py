import os, subprocess

deletar = [
    # Diagnósticos
    "diag_dictrow.py","diag_dictrow3.py","diag_equipe.py","diag_or.py",
    "diag_query.py","diag_query2.py","diag_rls.py","diag_rotas.py",
    "diag_filtros.py","diagnostico.py","diagnostico_pdf.py",
    "diagnostico_pdf2.py","diagnostico_pdf3.py",
    "verificar_amorim.py","verificar_arquivos.py","verificar_arquivos2.py",
    "verificar_contatos.py","verificar_git.py","verificar_github.py",
    "verificar_modulos.py","verificar_pdv.py","verificar_tipo_cliente.py",
    "verificar_filtros.py","ver_pontos.py","ver_usuario.py",
    "testar_catalogo.py","testar_modelos.py","testar_modulos.py",
    "mapear2.py","mapear_estrutura.py",
    "ler_get_menu.py","ler_pedido.py","ler_pedido2.py",
    "ler_permissoes.py","ler_roteiros.py","check_perm.py",
    # Fix/patch já aplicados
    "fix_equipe_atomico.py","fix_equipe_py.py",
    "fix_equipe_v2.py","fix_equipe_v3.py","fix_equipe_v4.py",
    "fix_equipe_v5.py","fix_equipe_v6.py","fix_equipe_v7.py",
    "fix_usuarios_py.py","fix_usuarios_v2.py","fix_usuarios_v3.py",
    "fix_configuracao.py","fix_crm_app.py","fix_crm_app_rotas.py",
    "fix_config_combo.py","fix_combo.py","fix_conta.py",
    "fix_relatorios.py","fix_colunas_vendedor.py",
    "fix_visitas_sintaxe.py","fix_visitas_indent.py","fix_visitas_todas_indent.py",
    "fix_filtros_combo.py",
    # Restauradores
    "restaurar_configuracao.py","restaurar_crm_app.py","restaurar_equipe.py",
    "restaurar_equipe_final.py","restaurar_permissoes.py","restaurar_roteiros.py",
    "restaurar_usuarios.py","restaurar_visitas.py","restaurar_d1b_etapa5_equipe.py",
    "instalar_arquivos.py","instalar_equipe_git.py",
    # Patches
    "patch_equipe.py","patch_equipe2.py","patch_equipe3.py","patch_equipe4.py",
    "patch_equipe_enrico.py","patch_modulos_vendedor.py","patch_pedido_perfil.py",
    "patch_permissoes_modulos.py","patch_roteiros.py","patch_roteiros_pv.py",
    "patch_configuracao_perfil.py","patch_filtros_perfil.py","patch_filtros_v2.py",
    "patch_todos_filtros.py","patch_central_filtros.py",
    # Scripts de banco já executados
    "d1b_add_subtipo_promotor.py","d1b_add_whatsapp_usuario.py",
    "d1b_etapa1_banco.py","d1b_etapa3_banco.py","d1b_etapa4_supervisor.py",
    "d1b_etapa5_equipe.py","d1b_verificar_banco.py",
    "d2_fase0_empresa.py","d2_faseA.py","d2_faseB_ativar_rls.py",
    "d2_faseB_rls.py","d2_faseC_nova_empresa.py",
    "corrigir_amorim.py","corrigir_numpy.py","corrigir_query_lenta.py",
    "corrigir_tipos_tabela.py","corrigir_tipos_tabela2.py",
    "migrar_comissao_prorrogacao.py","migrar_mensagem_modelo.py",
    "desabilitar_dashboard.py","sincronizar_banco.py","atualizar_database.py",
    "criar_usuario.py","listar_tabelas.py","medir_dashboard.py",
    "atribuir_carteira_fernando.py",
    # Outros
    "restaurar_streamlit_158.py","diagnostico_contatos.py",
    "fix_equipe_v2.py","fix_equipe_py.py",
]

removidos = []
nao_encontrados = []

for f in deletar:
    if os.path.exists(f):
        os.remove(f)
        removidos.append(f)
    else:
        nao_encontrados.append(f)

print(f"Removidos: {len(removidos)} arquivos")
print(f"Não encontrados: {len(nao_encontrados)} arquivos")

# Commit da limpeza
subprocess.run(["git","add","-A"])
r = subprocess.run(["git","commit","-m","chore: limpeza de scripts temporarios e diagnosticos"],
                   capture_output=True, text=True)
print("Commit:", r.stdout.strip() or r.stderr.strip())
r2 = subprocess.run(["git","push"], capture_output=True, text=True)
print("Push:", r2.stdout.strip() or r2.stderr.strip())

print("\n=== Arquivos restantes ===")
for f in sorted(os.listdir('.')):
    if f.endswith('.py') or f.endswith('.toml') or f.endswith('.txt'):
        print(f"  {f}")
