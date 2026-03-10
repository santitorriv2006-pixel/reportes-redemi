@echo off
REM Script de instalación rápida para Windows
REM Ejecutar: setup.bat

setlocal enabledelayedexpansion

cls
echo.
echo ========================================================
echo   Sistema de Reportes Empresariales
echo   Instalacion Rapida para Windows
echo ========================================================
echo.

REM Verificar Python
echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Python no está instalado o no está en PATH
    echo.
    echo Descarga e instala Python desde:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)
echo [OK] Python detectado
echo.

REM Crear entorno virtual
echo Creando entorno virtual...
if exist venv (
    echo [ADVERTENCIA] El directorio venv ya existe
) else (
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] No se pudo crear el entorno virtual
        pause
        exit /b 1
    )
    echo [OK] Entorno virtual creado
)
echo.

REM Activar entorno virtual
echo Activando entorno virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] No se pudo activar el entorno virtual
    pause
    exit /b 1
)
echo [OK] Entorno activado
echo.

REM Actualizar pip
echo Actualizando pip...
python -m pip install --upgrade pip
echo [OK] pip actualizado
echo.

REM Instalar dependencias
echo Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] No se pudieron instalar las dependencias
    pause
    exit /b 1
)
echo [OK] Dependencias instaladas
echo.

REM Crear directorios
echo Creando directorios necesarios...
if not exist uploads (mkdir uploads)
if not exist logs (mkdir logs)
echo [OK] Directorios creados
echo.

REM Verificar archivo .env
if not exist .env (
    echo Creando archivo .env...
    (
        echo # Configuracion de Base de Datos
        echo DATABASE_URL=sqlite:///reportes.db
        echo SQLALCHEMY_TRACK_MODIFICATIONS=False
        echo.
        echo # Configuracion de Flask
        echo FLASK_ENV=development
        echo FLASK_HOST=0.0.0.0
        echo FLASK_PORT=5000
        echo SECRET_KEY=tu_clave_secreta_cambiar_en_produccion
        echo.
        echo # Configuracion de Carga de Archivos
        echo MAX_CONTENT_LENGTH=50000000
        echo UPLOAD_FOLDER=uploads/
        echo ALLOWED_EXTENSIONS=xlsx
        echo.
        echo # Configuracion de Correo ^(OPCIONAL^)
        echo MAIL_SERVER=smtp.gmail.com
        echo MAIL_PORT=587
        echo MAIL_USE_TLS=True
        echo MAIL_USERNAME=tu_email@gmail.com
        echo MAIL_PASSWORD=tu_contraseña_app
        echo MAIL_DEFAULT_SENDER=tu_email@gmail.com
        echo MAIL_RECIPIENTS=email1@empresa.com,email2@empresa.com
        echo.
        echo # Configuracion de Logging
        echo LOG_LEVEL=INFO
        echo LOG_FILE=logs/app.log
    ) > .env
    echo [OK] Archivo .env creado
    echo.
    echo [IMPORTANTE] Edita .env con tu configuracion de correo
) else (
    echo [ADVERTENCIA] El archivo .env ya existe
)
echo.

REM Inicializar base de datos
echo Inicializando base de datos...
python -c "from app import create_app, db; app = create_app(); db.create_all()" 2>nul
if errorlevel 1 (
    echo [ADVERTENCIA] No se pudo inicializar la BD automáticamente
    echo               Esto se hará al ejecutar la aplicación
) else (
    echo [OK] Base de datos inicializada
)
echo.

REM Mostrar instrucciones finales
cls
echo.
echo ========================================================
echo   INSTALACION COMPLETADA!
echo ========================================================
echo.
echo [OK] Sistema listo para usar
echo.
echo PROXIMOS PASOS:
echo.
echo 1. EDITAR CONFIGURACION ^(Opcional pero recomendado^):
echo    - Abre el archivo ".env"
echo    - Configura tu correo ^(MAIL_USERNAME, MAIL_PASSWORD^)
echo    - Cambia SECRET_KEY por una clave segura
echo.
echo 2. EJECUTAR LA APLICACION:
echo    - En este terminal, ejecuta:
echo.
echo    python run.py
echo.
echo 3. ACCEDER:
echo    - Abre tu navegador
echo    - Ve a: http://localhost:5000
echo    - ^!Listo^!
echo.
echo DOCUMENTACION:
echo   - README.md           : Guia principal
echo   - GUIA_DE_USO.md      : Como usar
echo   - TECHNICAL_DOCS.md   : Detalles tecnicos
echo   - EJEMPLO_EXCEL.md    : Formato de Excel
echo.
echo ========================================================
echo.

pause
exit /b 0
