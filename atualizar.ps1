# =============================================================================
# atualizar.ps1 — PepperCRM
# Copia arquivo(s) modificado(s), commita e faz deploy no Railway via git push
# Como usar: coloque na pasta peppercrm e clique direito -> Executar com PowerShell
# =============================================================================

$pasta = "C:\Users\welov\PycharmProjects\WebSolution\peppercrm"
Set-Location $pasta

# -----------------------------------------------------------------------------
# 1. Copia arquivos novos que estiverem na mesma pasta do .ps1
# -----------------------------------------------------------------------------
$arquivos = @(
    "cadastros.py","crm_app.py","pesquisa.py","contatos.py","relatorios.py",
    "ver_pedidos.py","visitas.py","pedido.py","despesas.py","metas.py",
    "mix_analise.py","analise_competitiva.py","concorrentes.py","comissoes.py",
    "catalogo.py","configuracao.py","database.py","cache_helpers.py",
    "keepalive.py","scanner_ean.py"
)

$copiados = 0
foreach ($arq in $arquivos) {
    $src = Join-Path $PSScriptRoot $arq
    if (Test-Path $src) {
        Copy-Item -Path $src -Destination $pasta -Force
        Write-Host "  OK $arq copiado" -ForegroundColor Green
        $copiados++
    }
}
if ($copiados -eq 0) {
    Write-Host "  Nenhum arquivo .py encontrado na pasta do .ps1." -ForegroundColor Yellow
    Write-Host "  Coloque os arquivos modificados na mesma pasta deste script." -ForegroundColor Yellow
}

# -----------------------------------------------------------------------------
# 2. Remove arquivos de lixo que nao devem ir para o Railway
# -----------------------------------------------------------------------------
$lixo = @(
    "peppercrm_backup.dump","peppercrm_backup.sql","pesquisa_backup.sql",
    "fix_kg_form.py","migrar_clientes_pdvs.py","migrar_pesquisas.py",
    "sincronizar_banco2.py","check_fotos.py","test_despesa.py",
    "kg_form.txt","pesquisa_itens_novos.csv","pesquisa_novos.csv"
)
foreach ($arq in $lixo) {
    $caminho = Join-Path $pasta $arq
    if (Test-Path $caminho) {
        Remove-Item $caminho -Force
        Write-Host "  Removido: $arq" -ForegroundColor DarkGray
    }
}

# -----------------------------------------------------------------------------
# 3. Git commit + push para Railway
# -----------------------------------------------------------------------------
Write-Host ""
Write-Host "Preparando deploy para Railway..." -ForegroundColor Cyan

git add -A

$status = git status --porcelain
if (-not $status) {
    Write-Host "  Nada para commitar - Railway ja esta atualizado." -ForegroundColor Yellow
} else {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
    git commit -m "atualizacao $timestamp"
    Write-Host "  Commit OK" -ForegroundColor Green

    Write-Host "  Enviando para Railway..." -ForegroundColor Cyan
    git push origin main
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  Deploy iniciado! Aguarde ~30s e acesse:" -ForegroundColor Green
        Write-Host "  https://peppercrm-production.up.railway.app/" -ForegroundColor White
    } else {
        Write-Host "  Erro no push. Verifique conexao ou credenciais Git." -ForegroundColor Red
    }
}

# -----------------------------------------------------------------------------
# 4. Reinicia app local
# -----------------------------------------------------------------------------
Write-Host ""
$proc = Get-Process -Name "streamlit" -ErrorAction SilentlyContinue
if ($proc) {
    $proc | Stop-Process -Force
    Start-Sleep -Seconds 1
}
Start-Process "$pasta\IniciarPepperCRM.vbs"
Write-Host "  App local reiniciado em localhost:8501" -ForegroundColor Green
Write-Host ""
Write-Host "Concluido." -ForegroundColor Green
Start-Sleep -Seconds 3
