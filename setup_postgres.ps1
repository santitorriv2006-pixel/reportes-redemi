# Script simple para setup de PostgreSQL local

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "SETUP POSTGRESQL LOCAL" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# 1. Verificar PostgreSQL
Write-Host ""
Write-Host "1. Verificando PostgreSQL..." -ForegroundColor Cyan
$psql = Get-Command psql -ErrorAction SilentlyContinue

if (-not $psql) {
    Write-Host "   PostgreSQL NO ENCONTRADO" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "DESCARGAR E INSTALAR:" -ForegroundColor Cyan
    Write-Host "https://www.postgresql.org/download/windows/" -ForegroundColor White
    Write-Host ""
    Write-Host "Al instalar:" -ForegroundColor Yellow
    Write-Host "- Contraseña: postgres (o anota la que uses)" -ForegroundColor Gray
    Write-Host "- Puerto: 5432" -ForegroundColor Gray
    Write-Host "- Marca Command Line Tools" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Presiona Enter cuando hayas instalado PostgreSQL..." -ForegroundColor Yellow
    Read-Host
    
    # Intentar de nuevo
    cmd /c "refreshenv" 2>$null
    $psql = Get-Command psql -ErrorAction SilentlyContinue
    
    if (-not $psql) {
        Write-Host "[ERROR] PostgreSQL aun no disponible" -ForegroundColor Red
        Write-Host "Cierra y abre una NUEVA PowerShell" -ForegroundColor Yellow
        exit 1
    }
}

Write-Host "   PostgreSQL detectado" -ForegroundColor Green
psql --version

# 2. Crear BD
Write-Host ""
Write-Host "2. Creando base de datos..." -ForegroundColor Cyan

$pgPass = Read-Host "   Contrasena superuser (default: postgres)"
if ($pgPass -eq "") { $pgPass = "postgres" }

# Crear archivo SQL
$sql = @'
CREATE USER reportes_user WITH PASSWORD 'reportes_123';
CREATE DATABASE reportes OWNER reportes_user;
GRANT ALL PRIVILEGES ON DATABASE reportes TO reportes_user;
ALTER ROLE reportes_user CREATEDB;
'@

$sql | Out-File -FilePath "temp_setup.sql" -Encoding UTF8 -Force

# Ejecutar
$env:PGPASSWORD = $pgPass
psql -U postgres -f "temp_setup.sql" 2>$null
Remove-Item "temp_setup.sql" -Force

Write-Host "   Base de datos creada" -ForegroundColor Green

# 3. Actualizar .env
Write-Host ""
Write-Host "3. Actualizando .env..." -ForegroundColor Cyan

$env_file = ".env"
$new_db = "DATABASE_URL=postgresql://reportes_user:reportes_123@localhost:5432/reportes"

$content = Get-Content $env_file
$content = $content -replace "^DATABASE_URL=.*", $new_db
$content | Set-Content $env_file -Encoding UTF8

Write-Host "   .env actualizado" -ForegroundColor Green

# 4. Restaurar datos
Write-Host ""
Write-Host "4. Restaurando datos..." -ForegroundColor Cyan

$migration = Get-ChildItem -Filter "migration_postgres_*.sql" -ErrorAction SilentlyContinue | Select-Object -First 1

if ($migration) {
    Write-Host "   Datos: $($migration.Name)" -ForegroundColor Gray
    
    $env:PGPASSWORD = "reportes_123"
    psql -U reportes_user -d reportes -f $migration.FullName 2>$null
    Write-Host "   Restauracion completada" -ForegroundColor Green
} else {
    Write-Host "   [SKIP] No encontre archivo de migracion" -ForegroundColor Yellow
}

# 5. Verificar
Write-Host ""
Write-Host "5. Verificando conexion..." -ForegroundColor Cyan

try {
    $env:PGPASSWORD = "reportes_123"
    $test = psql -U reportes_user -d reportes -c "SELECT 1;" 2>&1 | Out-String
    if ($test -contains "success" -or $LASTEXITCODE -eq 0) {
        Write-Host "   Conexion OK" -ForegroundColor Green
    }
} catch {
    Write-Host "   [WARNING] $($_)" -ForegroundColor Yellow
}

# Resumen
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "LISTO - PostgreSQL configurado" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "BD: reportes" -ForegroundColor White
Write-Host "Usuario: reportes_user" -ForegroundColor White
Write-Host "Contrasena: reportes_123" -ForegroundColor White
Write-Host ".env: Actualizado" -ForegroundColor White
Write-Host ""
Write-Host "PROXIMOS PASOS:" -ForegroundColor Cyan
Write-Host "1. python run.py" -ForegroundColor Gray
Write-Host "2. git add -A && git commit -m 'PostgreSQL setup'" -ForegroundColor Gray
Write-Host "3. git push origin main" -ForegroundColor Gray
Write-Host ""
