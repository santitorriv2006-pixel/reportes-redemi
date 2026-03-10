# Script de instalación para PowerShell
# Uso: powershell -ExecutionPolicy Bypass -File install.ps1

Write-Host "
╔════════════════════════════════════════════════════════════════╗
║    Sistema de Reportes Empresariales - INSTALACION            ║
║              Guía de Instalación Automática                    ║
╚════════════════════════════════════════════════════════════════╝
" -ForegroundColor Cyan

# Paso 1: Verificar Python
Write-Host "[1/6] Verificando Python..." -ForegroundColor Blue
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python no está instalado o no está en PATH" -ForegroundColor Red
    Write-Host "  Descarga desde: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Paso 2: Crear entorno virtual
Write-Host "`n[2/6] Creando entorno virtual..." -ForegroundColor Blue
if (Test-Path "venv") {
    Write-Host "⚠ Entorno virtual ya existe" -ForegroundColor Yellow
} else {
    python -m venv venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Entorno virtual creado" -ForegroundColor Green
    } else {
        Write-Host "✗ Error creando entorno virtual" -ForegroundColor Red
        exit 1
    }
}

# Paso 3: Activar entorno e instalar dependencias
Write-Host "`n[3/6] Instalando dependencias..." -ForegroundColor Blue
$pythonExe = "venv\Scripts\python.exe"
$pipExe = "venv\Scripts\pip.exe"

if (Test-Path $pipExe) {
    & $pipExe install --upgrade pip | Out-Null
    & $pipExe install -r requirements.txt
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Dependencias instaladas" -ForegroundColor Green
    } else {
        Write-Host "✗ Error instalando dependencias" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✗ pip no encontrado" -ForegroundColor Red
    exit 1
}

# Paso 4: Crear directorios
Write-Host "`n[4/6] Creando directorios..." -ForegroundColor Blue
$dirs = @("uploads", "logs")
foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
        Write-Host "✓ Directorio creado: $dir" -ForegroundColor Green
    } else {
        Write-Host "✓ Directorio existe: $dir" -ForegroundColor Green
    }
}

# Paso 5: Crear archivo .env si no existe
Write-Host "`n[5/6] Configurando variables de entorno..." -ForegroundColor Blue
if (-not (Test-Path ".env")) {
    $envContent = @"
# ===== BASE DE DATOS =====
DATABASE_URL=sqlite:///reportes.db
SQLALCHEMY_TRACK_MODIFICATIONS=False

# ===== FLASK =====
FLASK_ENV=development
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
SECRET_KEY=dev-secret-key-change-in-production

# ===== ARCHIVOS =====
MAX_CONTENT_LENGTH=50000000
UPLOAD_FOLDER=uploads/
ALLOWED_EXTENSIONS=xlsx

# ===== CORREO (Opcional) =====
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_contraseña_app
MAIL_RECIPIENTS=email1@empresa.com

# ===== LOGGING =====
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
"@
    Set-Content -Path ".env" -Value $envContent -Encoding UTF8
    Write-Host "✓ Archivo .env creado" -ForegroundColor Green
    Write-Host "⚠ IMPORTANTE: Edita .env con tus credenciales de correo" -ForegroundColor Yellow
} else {
    Write-Host "✓ Archivo .env ya existe" -ForegroundColor Green
}

# Paso 6: Inicializar base de datos
Write-Host "`n[6/6] Inicializando base de datos..." -ForegroundColor Blue
try {
    & $pythonExe init_db.py 2>$null
    Write-Host "✓ Base de datos inicializada" -ForegroundColor Green
} catch {
    Write-Host "⚠ BD se creará automáticamente al ejecutar" -ForegroundColor Yellow
}

# Resumen final
Write-Host "
╔════════════════════════════════════════════════════════════════╗
║         ✅ INSTALACION COMPLETADA EXITOSAMENTE                 ║
╚════════════════════════════════════════════════════════════════╝
" -ForegroundColor Green

Write-Host "
📋 PROXIMOS PASOS:

1. CONFIGURAR (Opcional):
   - Abre el archivo: .env
   - Edita MAIL_USERNAME y MAIL_PASSWORD con tus credenciales

2. EJECUTAR LA APLICACION:
   
   Opción A - Activar entorno manualmente:
      .\venv\Scripts\Activate.ps1
      python run.py

   Opción B - Ejecutar directamente:
      .\venv\Scripts\python.exe run.py

3. ACCEDER:
   - Abre tu navegador
   - Ve a: http://localhost:5000
   - ¡Listo!

📚 DOCUMENTACION:
   - QUICK_START.txt       : Inicio rápido
   - GUIA_DE_USO.md        : Cómo usar la aplicación
   - TECHNICAL_DOCS.md     : Documentación técnica
   - DEPLOYMENT.md         : Deployment a producción
" -ForegroundColor Cyan

Write-Host "Presiona Enter para salir..." -ForegroundColor Gray
Read-Host
