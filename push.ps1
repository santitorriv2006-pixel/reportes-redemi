# Script para subir el proyecto a GitHub - PowerShell

param(
    [string]$Mensaje = ""
)

Write-Host "`n" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " 📤 SUBIDOR DE PROYECTOS A GITHUB" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Activar ambiente virtual si existe
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "🐍 Activando entorno virtual..." -ForegroundColor Yellow
    & "venv\Scripts\Activate.ps1"
    Write-Host "✅ Entorno activado`n" -ForegroundColor Green
}

# Obtener mensaje del commit
if ([string]::IsNullOrEmpty($Mensaje)) {
    $FechaHora = Get-Date -Format "dd/MM/yyyy HH:mm:ss"
    $Mensaje = "actualizaciones - $FechaHora"
}

Write-Host "📝 Mensaje del commit: '$Mensaje'" -ForegroundColor Cyan

# Verificar estatus
Write-Host "`n📊 Verificando cambios..." -ForegroundColor Yellow
$Status = git status --porcelain
if ($Status) {
    Write-Host "✓ Cambios detectados:" -ForegroundColor Green
    Write-Host $Status
} else {
    Write-Host "⚠️ No hay cambios detectados" -ForegroundColor Yellow
}

# Confirmación
Write-Host "`n¿Deseas continuar? (S/N): " -ForegroundColor Yellow -NoNewline
$Respuesta = Read-Host
if ($Respuesta -ne "s" -and $Respuesta -ne "S") {
    Write-Host "❌ Operación cancelada" -ForegroundColor Red
    exit
}

# Paso 1: Agregar cambios
Write-Host "`n" + "="*60
Write-Host "📌 Paso 1: Agregando cambios" -ForegroundColor Cyan
Write-Host "="*60
Write-Host "Ejecutando: git add -A`n"
git add -A

if ($?) {
    Write-Host "✅ Cambios agregados`n" -ForegroundColor Green
} else {
    Write-Host "❌ Error agregando cambios" -ForegroundColor Red
    exit 1
}

# Paso 2: Crear commit
Write-Host "="*60
Write-Host "📌 Paso 2: Creando commit" -ForegroundColor Cyan
Write-Host "="*60
Write-Host "Ejecutando: git commit -m '$Mensaje'`n"
git commit -m "$Mensaje"

if ($?) {
    Write-Host "✅ Commit creado`n" -ForegroundColor Green
} else {
    Write-Host "⚠️ Posiblemente no hay cambios nuevos`n" -ForegroundColor Yellow
}

# Paso 3: Push a GitHub
Write-Host "="*60
Write-Host "📌 Paso 3: Subiendo a GitHub" -ForegroundColor Cyan
Write-Host "="*60
Write-Host "Ejecutando: git push origin main`n"
git push origin main

if ($?) {
    Write-Host "✅ Push completado`n" -ForegroundColor Green
} else {
    Write-Host "❌ Error al subir a GitHub" -ForegroundColor Red
    Write-Host "💡 Intenta:" -ForegroundColor Yellow
    Write-Host "   1. Verifica tu conexión a internet" -ForegroundColor Yellow
    Write-Host "   2. Verifica tu acceso a GitHub (token/contraseña)" -ForegroundColor Yellow
    Write-Host "   3. Ejecuta manualmente: git push origin main" -ForegroundColor Yellow
    exit 1
}

# Mostrar resultado final
Write-Host "="*60
Write-Host "✅ ¡PROYECTO SUBIDO A GITHUB EXITOSAMENTE!" -ForegroundColor Green
Write-Host "="*60

# Último commit
Write-Host "`n📌 Último commit:" -ForegroundColor Cyan
git log --oneline -1

Write-Host "`n🎉 Todos los cambios están en GitHub`n" -ForegroundColor Green
