# Script para instalar PostgreSQL en Windows
# Ejecutar como Administrador

Write-Host "📦 INSTALACIÓN DE POSTGRESQL EN WINDOWS" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Green
Write-Host ""

# Detectar si es admin
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $isAdmin) {
    Write-Host "⚠️  REQUIERE PERMISOS DE ADMINISTRADOR" -ForegroundColor Red
    Write-Host "Por favor, ejecuta PowerShell como Administrador" -ForegroundColor Yellow
    exit 1
}

# Verificar si ya está instalado
Write-Host "`n1️⃣  Verificando si PostgreSQL está instalado..." -ForegroundColor Cyan
$pgCheck = Get-Command psql -ErrorAction SilentlyContinue

if ($pgCheck) {
    Write-Host "   ✅ PostgreSQL ya está instalado" -ForegroundColor Green
    psql --version
    exit 0
}

Write-Host "   ❌ PostgreSQL no encontrado" -ForegroundColor Yellow

# Ofrecer instalación con Chocolatey
Write-Host "`n2️⃣  Verificando si Chocolatey está instalado..." -ForegroundColor Cyan
$choco = Get-Command choco -ErrorAction SilentlyContinue

if ($choco) {
    Write-Host "   ✅ Chocolatey encontrado" -ForegroundColor Green
    
    Write-Host "`n3️⃣  Instalando PostgreSQL con Chocolatey..." -ForegroundColor Cyan
    choco install postgresql -y
    
    Write-Host "`n✅ Instalación completada" -ForegroundColor Green
    Write-Host "`n⚠️  IMPORTANTE:" -ForegroundColor Yellow
    Write-Host "   • Abre una nueva terminal PowerShell para que vea psql" -ForegroundColor White
    Write-Host "   • El usuario y contraseña por defecto son: postgres / postgres" -ForegroundColor White
    Write-Host "   • Verifica: psql --version" -ForegroundColor White
    
} else {
    Write-Host "   ❌ Chocolatey no instalado" -ForegroundColor Yellow
    Write-Host "`n📥 OPCIONES DE INSTALACIÓN:" -ForegroundColor Cyan
    Write-Host "`n   Opción A: Instalar Chocolatey primero" -ForegroundColor White
    Write-Host "   Abre PowerShell como Admin y ejecuta:" -ForegroundColor Gray
    Write-Host '   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.ServiceClient).DownloadString("https://community.chocolatey.org/install.ps1"))' -ForegroundColor Gray
    
    Write-Host "`n   Opción B: Descargar e instalar directo" -ForegroundColor White
    Write-Host "   https://www.postgresql.org/download/windows/" -ForegroundColor Cyan
    Write-Host "   ⚠️  Marca 'Command Line Tools' durante la instalación" -ForegroundColor Yellow
    
    Write-Host "`n   Opción C: Usar la migración rápida" -ForegroundColor White
    Write-Host "   python quick_migrate_to_postgres.py" -ForegroundColor Cyan
    Write-Host "   (No requiere PostgreSQL instalado)" -ForegroundColor Gray
}
