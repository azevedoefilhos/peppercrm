import os, subprocess

deletar = [
    # Scripts de verificação desta sessão
    "ver_contatos.py", "ver_contatos2.py", "ver_contatos3.py",
    "ver_contatos4.py", "ver_contatos5.py", "ver_contatos6.py",
    "ver_pesquisa.py", "ver_pesquisa2.py", "ver_pesquisa3.py",
    "ver_pesquisa4.py",
    "ver_visitas.py", "ver_visitas2.py",
    "ver_relatorios.py", "ver_relatorios2.py",
    "ver_rel_bugs.py", "ver_rel_completo.py", "ver_rel_where.py",
    "ver_filtro_base.py", "ver_ranking_pdv.py",
    "ver_abas_rel.py", "ver_analise_cons.py",
    "ver_resultado.py", "ver_resultado2.py",
    "ver_resultado3.py", "ver_resultado4.py",
    "ver_despesas.py", "ver_despesas2.py", "ver_despesas_abas.py",
    "ver_pdv_setor.py", "ver_pdv_setor2.py", "ver_where_s.py",
    "ver_where_pq.py", "ver_analise_cons.py",
    "ver_modulos_vendedor.py", "ver_modulos2.py",
    "ver_helper_atual.py", "ver_database_query.py",
    "ver_contatos.py", "ver_mensagens.py", "ver_mensagens2.py",
    "ver_debug_app.py", "ver_pontos.py",
    "mapear_rel.py", "mapear_wheres.py",
    # Scripts de fix desta sessão
    "fix_contatos.py", "fix_contatos2.py",
    "fix_pesquisa.py", "fix_pesquisa2.py",
    "fix_analise_cons.py", "fix_grafia_analise.py",
    "fix_relatorios.py", "fix_relatorios2.py", "fix_relatorios3.py",
    "fix_ranking_competitivo.py", "fix_remove_compet.py",
    "fix_visitas_roteiro.py",
    "fix_despesas.py", "fix_despesas_resultado.py",
    "fix_despesas_abas2.py", "fix_despesas_abas3.py",
    "fix_todos_wheres.py", "fix_filtros_v3.py",
    "fix_cadastros_restante.py", "fix_pdv_setor.py",
    "fix_catalogo_msg.py",
    "add_debug_home.py", "add_debug2.py", "add_debug_clientes.py",
    "remove_debug.py", "remove_debug2.py",
    "patch_filtros_final.py",
    "fix_auth.py",
    "ver_usuarios.py", "ver_pedido_campos.py",
    "ver_permissoes_atual.py",
    "ver_pdv_query.py", "ver_where_p.py",
    "ver_contatos5.py", "ver_catalogo_msg.py",
    "ver_pdv_setor.py", "ver_where_s.py",
    "ver_modulos_vendedor.py",
    "fix_relatorios.py",
    "fix_todos_wheres.py",
    "patch_central_filtros.py",
    "fix_filtros_combo.py",
    "testar_helper.py",
    "check_perm.py",
    "ver_rel_where.py",
    "fix_cadastros_restante.py",
    "ver_resultado2.py",
]

removidos = []
nao_encontrados = []
for f in set(deletar):  # set remove duplicatas
    if os.path.exists(f):
        os.remove(f)
        removidos.append(f)
    else:
        nao_encontrados.append(f)

print(f"Removidos: {len(removidos)}")
print(f"Nao encontrados: {len(nao_encontrados)}")

# Lista o que sobrou
print("\n=== Arquivos .py restantes ===")
for f in sorted(os.listdir('.')):
    if f.endswith('.py'):
        print(f"  {f}")

subprocess.run(["git","add","-A"])
r = subprocess.run(["git","commit","-m","chore: limpeza scripts temporarios sessao filtros perfil"],
                   capture_output=True, text=True)
print("\nCommit:", r.stdout.strip() or r.stderr.strip())
r2 = subprocess.run(["git","push"], capture_output=True, text=True)
print("Push:", r2.stdout.strip() or r2.stderr.strip())
