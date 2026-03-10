# Script para subir base de datos a GitHub
# Ejecutar desde PowerShell en el directorio del proyecto

Write-Host "📦 Iniciando proceso de exportación de BD..." -ForegroundColor Green

# 1. Exportar BD
Write-Host "`n1️⃣  Exportando base de datos..." -ForegroundColor Cyan
Write-Host "    (Detecta automáticamente SQLite o PostgreSQL)" -ForegroundColor Gray
python export_db.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ Exportación completada" -ForegroundColor Green
} else {
    Write-Host "`n❌ Error en exportación" -ForegroundColor Red
    exit 1
}

# 2. Ver archivos para agregar
Write-Host "`n2️⃣  Archivos a subir:" -ForegroundColor Cyan
Get-ChildItem -Filter "database_backup_*.sql" | foreach { Write-Host "   - $($_.Name)" -ForegroundColor Yellow }

# 3. Agregrar a git
Write-Host "`n3️⃣  Agregando a git..." -ForegroundColor Cyan
git add database_backup_*.sql
git add .env.example
git add .gitignore
git add export_db.py
git add restore_db.py
git add RENDER_DEPLOYMENT.md

Write-Host "✅ Archivos agregados a staging" -ForegroundColor Green

# 4. Ver status
Write-Host "`n4️⃣  Estado de git:" -ForegroundColor Cyan
git status

# 5. Commit
Write-Host "`n5️⃣  Haciendo commit..." -ForegroundColor Cyan
$message = Read-Host "Escribe un mensaje para el commit (default: 'Add database backup and Render deployment guide')"
if ($message -eq "") {
    $message = "Add database backup and Render deployment guide"
}
git commit -m $message

# 6. Push
Write-Host "`n6️⃣  Subiendo a GitHub..." -ForegroundColor Cyan
Write-Host "Ejecuta: git push origin main" -ForegroundColor Yellow
Write-Host "O presiona Enter para hacerlo automáticamente:" -ForegroundColor Yellow

$response = Read-Host "¿Hacer push ahora? (s/n)"
if ($response.ToLower() -eq "s") {
    git push origin main
    Write-Host "`n✅ ¡Listo! Tu BD está en GitHub" -ForegroundColor Green
    Write-Host "`n📖 PRÓXIMOS PASOS:" -ForegroundColor Cyan
    Write-Host "   1. Lee RENDER_DEPLOYMENT.md (instrucciones completas)" -ForegroundColor White
    Write-Host "   2. Crea PostgreSQL en Render" -ForegroundColor White
    Write-Host "   3. Crea Web Service enlazado a GitHub" -ForegroundColor White
    Write-Host "   4. Configura variables de entorno" -ForegroundColor White
    Write-Host "   5. El deploy es automático cuando hagas push" -ForegroundColor White
} else {
    Write-Host "`nNo olvides hacer push después: git push origin main" -ForegroundColor Yellow
}

Write-Host "`n📖 Lee RENDER_DEPLOYMENT.md para los próximos pasos" -ForegroundColor Cyan

