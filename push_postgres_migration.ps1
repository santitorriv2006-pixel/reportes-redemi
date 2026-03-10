# Script para subir migración PostgreSQL a GitHub
# Ejecutar desde PowerShell

Write-Host "📤 SUBIENDO MIGRACIÓN POSTGRESQL A GITHUB" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green

# 1. Ver archivos
Write-Host "`n1️⃣  Archivos de migración encontrados:" -ForegroundColor Cyan
Get-ChildItem -Filter "migration_*.sql" | foreach { 
    $size = (Get-Item $_.FullName).Length / 1MB
    Write-Host "   • $($_.Name) ($([math]::Round($size, 2)) MB)" -ForegroundColor Yellow 
}

# 2. Revisar antes de subir
Write-Host "`n2️⃣  Vista previa del archivo PostgreSQL:" -ForegroundColor Cyan
$pgFile = Get-ChildItem -Filter "migration_postgres_*.sql" | Select-Object -First 1
if ($pgFile) {
    Write-Host "   Primeras líneas:" -ForegroundColor Gray
    Get-Content $pgFile.FullName | Select-Object -First 10 | foreach { Write-Host "   $_" -ForegroundColor Gray }
    Write-Host "   ... (continúa)" -ForegroundColor Gray
}

# 3. Agregar a git
Write-Host "`n3️⃣  Agregando archivos a git..." -ForegroundColor Cyan
git add migration_*.sql
git add .env.example
git add migrate_to_postgres.py
git add quick_migrate_to_postgres.py

Write-Host "   ✅ Archivos en staging" -ForegroundColor Green

# 4. Status
Write-Host "`n4️⃣  Estado de git:" -ForegroundColor Cyan
git status

# 5. Commit
Write-Host "`n5️⃣  Preparando commit..." -ForegroundColor Cyan
$message = Read-Host "Mensaje de commit (default: 'Migrate to PostgreSQL')"
if ($message -eq "") {
    $message = "Migrate database to PostgreSQL"
}
git commit -m $message

# 6. Push
Write-Host "`n6️⃣  Subiendo a GitHub..." -ForegroundColor Cyan
$response = Read-Host "¿Hacer push ahora? (s/n)"
if ($response.ToLower() -eq "s") {
    git push origin main
    Write-Host "`n✅ ¡Enviado a GitHub!" -ForegroundColor Green
} else {
    Write-Host "`nNo olvides: git push origin main" -ForegroundColor Yellow
}

# 7. Instrucciones finales
Write-Host "`n" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "📋 PRÓXIMOS PASOS EN RENDER" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════" -ForegroundColor Cyan

Write-Host "`n1️⃣  Crea PostgreSQL en Render:" -ForegroundColor White
Write-Host "    Dashboard → New → PostgreSQL" -ForegroundColor Gray
Write-Host "    • Name: reportes-db" -ForegroundColor Gray
Write-Host "    • Database: reportes" -ForegroundColor Gray
Write-Host "    • Copia: Internal Database URL" -ForegroundColor Gray

Write-Host "`n2️⃣  Actualiza .env:" -ForegroundColor White
Write-Host "    DATABASE_URL=postgresql://user:pass@dpg-xxxxx.render.internal:5432/reportes" -ForegroundColor Gray

Write-Host "`n3️⃣  Crea Web Service en Render:" -ForegroundColor White
Write-Host "    Dashboard → New → Web Service" -ForegroundColor Gray
Write-Host "    • Build: pip install -r requirements.txt" -ForegroundColor Gray
Write-Host "    • Start: gunicorn app:app" -ForegroundColor Gray

Write-Host "`n4️⃣  Restaura la BD en Render:" -ForegroundColor White
Write-Host "    Web Service → Shell" -ForegroundColor Gray
Write-Host "    psql < migration_postgres_20260310_*.sql" -ForegroundColor Gray

Write-Host "`n5️⃣  Haz push cuando esté todo configurado:" -ForegroundColor White
Write-Host "    git push origin main" -ForegroundColor Gray
Write-Host "    (El deploy es automático)" -ForegroundColor Gray

Write-Host "`n` -ForegroundColor Cyan
Write-Host "✅ ¡Base de datos migrada a PostgreSQL!" -ForegroundColor Green
Write-Host "📖 Lee RENDER_DEPLOYMENT.md para detalles" -ForegroundColor Cyan
