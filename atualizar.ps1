# =============================================================================
# atualizar.ps1 — PepperCRM
# Coloque na pasta peppercrm. Clique direito -> Executar com PowerShell
# Faz apenas: copia arquivos + git commit + push para Railway
# Para abrir o app local: use o IniciarPepperCRM.vbs normalmente
# =============================================================================

$pasta = "C:\Users\welov\PycharmProjects\WebSolution\peppercrm"
Set-Location $pasta

Write-Host ""
Write-Host "PepperCRM - Atualizacao" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan

# -----------------------------------------------------------------------------
# 1. Copia arquivos .py que estiverem na mesma pasta do .ps1
# -----------------------------------------------------------------------------
$arquivos = @(
    "cadastros.py", "crm_app.py", "pesquisa.py", "contatos.py",
    "relatorios.py", "ver_pedidos.py", "visitas.py", "pedido.py",
    "despesas.py", "metas.py", "mix_analise.py", "analise_competitiva.py",
    "concorrentes.py", "comissoes.py", "catalogo.py", "configuracao.py",
    "database.py", "cache_helpers.py", "keepalive.py", "scanner_ean.py",
    "sincronizar_banco.py", "migrar_comissao_prorrogacao.py"
)

$copiados = 0
foreach ($arq in $arquivos) {
    $src = Join-Path $PSScriptRoot $arq
    if (Test-Path $src) {
        Copy-Item -Path $src -Destination $pasta -Force
        Write-Host "  OK $arq" -ForegroundColor Green
        $copiados++
    }
}

if ($copiados -eq 0) {
    Write-Host "  Nenhum arquivo .py encontrado na pasta deste script." -ForegroundColor Yellow
} else {
    Write-Host "  $copiados arquivo(s) copiado(s)." -ForegroundColor Green
}

# -----------------------------------------------------------------------------
# 2. Remove arquivos obsoletos
# -----------------------------------------------------------------------------
$lixo = @(
    "peppercrm_backup.dump", "peppercrm_backup.sql", "pesquisa_backup.sql",
    "fix_kg_form.py", "migrar_clientes_pdvs.py", "migrar_pesquisas.py",
    "sincronizar_banco2.py", "check_fotos.py", "test_despesa.py",
    "kg_form.txt", "pesquisa_itens_novos.csv", "pesquisa_novos.csv"
)
foreach ($arq in $lixo) {
    $caminho = Join-Path $pasta $arq
    if (Test-Path $caminho) {
        Remove-Item $caminho -Force
        Write-Host "  Removido: $arq" -ForegroundColor DarkGray
    }
}

# -----------------------------------------------------------------------------
# 3. Git: commit + push para Railway
# -----------------------------------------------------------------------------
Write-Host ""
Write-Host "Enviando para Railway..." -ForegroundColor Cyan
git add -A
$status = git status --porcelain
if (-not $status) {
    Write-Host "  Nada para commitar - Railway ja esta atualizado." -ForegroundColor Yellow
} else {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
    git commit -m "atualizacao $timestamp"
    Write-Host "  Commit OK" -ForegroundColor Green
    git push origin main
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  Deploy iniciado! Aguarde ~30s e acesse:" -ForegroundColor Green
        Write-Host "  https://peppercrm-production.up.railway.app/" -ForegroundColor White
    } else {
        Write-Host "  Erro no push. Verifique conexao Git." -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Concluido! Para abrir o app local use o IniciarPepperCRM.vbs" -ForegroundColor Green
Write-Host "Pressione qualquer tecla para fechar..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
