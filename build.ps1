# Script de compilación para PowerShell - Sistema de Reportes

param(
    [switch]$Limpiar,
    [switch]$Portable,
    [switch]$Instalador,
    [switch]$Ejecutar
)

Write-Host "`n" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " 🔨 COMPILADOR - Sistema de Gestión de Reportes" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Activar ambiente virtual
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "🐍 Activando entorno virtual..." -ForegroundColor Yellow
    & "venv\Scripts\Activate.ps1"
    Write-Host "✅ Entorno activado`n" -ForegroundColor Green
}

# Ejecutar compilación
Write-Host "⏳ Compilando aplicación..." -ForegroundColor Yellow
Write-Host "   (Esto puede tomar 2-3 minutos)`n" -ForegroundColor Gray

python build.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ ¡Compilación completada exitosamente!`n" -ForegroundColor Green
    
    if ($Ejecutar) {
        Write-Host "🚀 Iniciando aplicación..." -ForegroundColor Cyan
        & "SistemaReportes_Portable\SistemaReportes.exe"
    }
} else {
    Write-Host "`n❌ Error en la compilación`n" -ForegroundColor Red
    Exit 1
}

Write-Host ""
