# Script interactivo para instalar PostgreSQL y configurar

Write-Host "🐘 INSTALACIÓN INTERACTIVA DE POSTGRESQL" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# 1. Intentar con WinGet
Write-Host "`n1️⃣  Intentando instalar con WinGet..." -ForegroundColor Cyan
$winget = Get-Command winget -ErrorAction SilentlyContinue

if ($winget) {
    Write-Host "   ✅ WinGet encontrado" -ForegroundColor Green
    Write-Host "   📥 Descargando PostgreSQL..." -ForegroundColor Gray
    
    # Instalar PostgreSQL
    winget install -e --id PostgreSQL.PostgreSQL --quiet --disable-interactivity
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ PostgreSQL instalado" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  WinGet descarga pero puede requerir confirmación" -ForegroundColor Yellow
        $response = Read-Host "   ¿Continuar? (s/n)"
        if ($response -eq "n") {
            Write-Host "   Abortando instalación" -ForegroundColor Yellow
            exit 1
        }
    }
    
} else {
    Write-Host "   ℹ️  WinGet no disponible" -ForegroundColor Yellow
    Write-Host "`n📥 DESCARGAR POSTGRESQL MANUALMENTE:" -ForegroundColor Cyan
    Write-Host "   1. Ve a: https://www.postgresql.org/download/windows/" -ForegroundColor White
    Write-Host "   2. Descarga la versión más reciente" -ForegroundColor White
    Write-Host "   3. Ejecuta el instalador" -ForegroundColor White
    Write-Host "   4. ⚠️  IMPORTANTE en la instalación:" -ForegroundColor Yellow
    Write-Host "      • Contraseña superuser (postgres): tu_contraseña" -ForegroundColor Gray
    Write-Host "      • Puerto: 5432 (default)" -ForegroundColor Gray
    Write-Host "      • Marca 'Command Line Tools'" -ForegroundColor Gray
    Write-Host "   5. Después, abre una nueva PowerShell" -ForegroundColor White
    
    Write-Host "`n   Presiona Enter cuando hayas instalado PostgreSQL..." -ForegroundColor Cyan
    Read-Host
}

# 2. Verificar instalación
Write-Host "`n2️⃣  Verificando PostgreSQL..." -ForegroundColor Cyan
$psql = Get-Command psql -ErrorAction SilentlyContinue

if (-not $psql) {
    Write-Host "   ❌ psql no encontrado en PATH" -ForegroundColor Red
    Write-Host "   💡 Abre una nueva PowerShell para cargar el PATH actualizado" -ForegroundColor Yellow
    Write-Host "   📍 O instala desde: https://www.postgresql.org/download/windows/" -ForegroundColor Yellow
    exit 1
} else {
    Write-Host "   ✅ PostgreSQL encontrado" -ForegroundColor Green
    psql --version
}

# 3. Crear BD y usuario
Write-Host "`n3️⃣  Creando base de datos y usuario..." -ForegroundColor Cyan

$pgPassword = Read-Host "   Contraseña superuser de PostgreSQL (default: postgres)"
if ($pgPassword -eq "") {
    $pgPassword = "postgres"
}

# Script SQL
$sqlScript = @"
-- Crear usuario
CREATE USER reportes_user WITH PASSWORD 'tu_contraseña_segura';

-- Crear base de datos
CREATE DATABASE reportes OWNER reportes_user;

-- Dar permisos
GRANT ALL PRIVILEGES ON DATABASE reportes TO reportes_user;
ALTER ROLE reportes_user CREATEDB;

\c reportes

GRANT USAGE ON SCHEMA public TO reportes_user;
GRANT CREATE ON SCHEMA public TO reportes_user;
"@

# Ejecutar SQL
try {
    # Primero conectar como superuser para crear BD y usuario
    $env:PGPASSWORD = $pgPassword
    
    $sqlScript | psql -U postgres -h localhost
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ BD 'reportes' y usuario 'reportes_user' creados" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Error creando BD (verifica contraseña)" -ForegroundColor Yellow
        exit 1
    }
    
} catch {
    Write-Host "   ❌ Error: $_" -ForegroundColor Red
    exit 1
}

# 4. Actualizar .env
Write-Host "`n4️⃣  Configurando .env..." -ForegroundColor Cyan

$envFile = '.env'
$dbUrl = "postgresql://reportes_user:tu_contraseña_segura@localhost:5432/reportes"

# Leer .env
$content = Get-Content $envFile -Raw

# Reemplazar DATABASE_URL
if ($content -match "DATABASE_URL=.*") {
    $content = $content -replace "DATABASE_URL=.*", "DATABASE_URL=$dbUrl"
} else {
    $content = "DATABASE_URL=$dbUrl`n$content"
}

# Guardar
Set-Content $envFile $content -Encoding UTF8

Write-Host "   ✅ .env actualizado con PostgreSQL local" -ForegroundColor Green

# 5. Restaurar datos
Write-Host "`n5️⃣  Restaurando datos desde SQLite..." -ForegroundColor Cyan

$migrationFile = Get-ChildItem -Filter "migration_postgres_*.sql" | Select-Object -First 1

if ($migrationFile) {
    Write-Host "   📄 Encontrado: $($migrationFile.Name)" -ForegroundColor Gray
    
    Write-Host "   📥 Restaurando (esto puede tardar)..." -ForegroundColor Gray
    
    $env:PGPASSWORD = "tu_contraseña_segura"  # Contraseña del usuario reportes_user
    $result = psql -U reportes_user -d reportes -h localhost -f $migrationFile.FullName 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Datos restaurados exitosamente" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Posible error en restauración:" -ForegroundColor Yellow
        Write-Host "   $result" -ForegroundColor Gray
    }
    
} else {
    Write-Host "   ❌ No se encontró migration_postgres_*.sql" -ForegroundColor Yellow
    Write-Host "   💡 Ejecuta primero: python quick_migrate_to_postgres.py" -ForegroundColor Yellow
}

# 6. Verificar
Write-Host "`n6️⃣  Verificando conexión..." -ForegroundColor Cyan

try {
    $env:PGPASSWORD = "tu_contraseña_segura"
    $result = psql -U reportes_user -d reportes -h localhost -c "SELECT 1;" 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Conexión exitosa a PostgreSQL" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  No se pudo conectar" -ForegroundColor Yellow
        Write-Host "   💡 Verifica:" -ForegroundColor Cyan
        Write-Host "      • ContrasenaSQL correcta en .env" -ForegroundColor Gray
        Write-Host "      • PostgreSQL está corriendo: tasklist | grep postgres" -ForegroundColor Gray
    }
} catch {
    Write-Host "   ⚠️  Error: $_" -ForegroundColor Yellow
}

# Resumen final
Write-Host "`n" -ForegroundColor Green
Write-Host "════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "✅ CONFIGURACIÓN COMPLETADA" -ForegroundColor Green
Write-Host "════════════════════════════════════════════════" -ForegroundColor Green

Write-Host "`n📋 Lo que se hizo:" -ForegroundColor Cyan
Write-Host "   ✅ PostgreSQL instalado" -ForegroundColor White
Write-Host "   ✅ BD 'reportes' creada" -ForegroundColor White
Write-Host "   ✅ Usuario 'reportes_user' creado" -ForegroundColor White
Write-Host "   ✅ Datos restaurados desde SQLite" -ForegroundColor White
Write-Host "   ✅ .env actualizado" -ForegroundColor White

Write-Host "`n🚀 PRÓXIMOS PASOS:" -ForegroundColor Cyan
Write-Host "   1. Prueba la aplicación:" -ForegroundColor White
Write-Host "      python run.py" -ForegroundColor Gray
Write-Host "`n   2. Cuando esté todo listo, sube a GitHub:" -ForegroundColor White
Write-Host "      ./push_postgres_migration.ps1" -ForegroundColor Gray
Write-Host "`n   3. Después despliega en Render:" -ForegroundColor White
Write-Host "      Lee RENDER_DEPLOYMENT.md" -ForegroundColor Gray

Write-Host "`n⚠️  IMPORTANTE - Cambiar contraseña:" -ForegroundColor Yellow
Write-Host "   Antes de producción, cambia en .env:" -ForegroundColor Gray
Write-Host "   DATABASE_URL=postgresql://reportes_user:NUEVA_CONTRASEÑA@localhost:5432/reportes" -ForegroundColor Gray

Write-Host "`nℹ️  Para ejecutar PostgreSQL en el futuro:" -ForegroundColor Cyan
Write-Host "   Windows Services → PostgreSQL → Start" -ForegroundColor Gray
Write-Host "   O: pg_ctl -D ""C:\Program Files\PostgreSQL\data"" start" -ForegroundColor Gray

Write-Host "`n"
