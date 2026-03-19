@echo off
REM Script para subir el proyecto a GitHub - Batch
REM Uso: push.bat "mensaje del commit"

setlocal enabledelayedexpansion

echo.
echo ============================================================
echo  204 SUBIDOR DE PROYECTOS A GITHUB
echo ============================================================
echo.

REM Activar ambiente virtual si existe
if exist venv\Scripts\activate.bat (
    echo 🐍 Activando entorno virtual...
    call venv\Scripts\activate.bat
    echo ✅ Entorno activado
    echo.
)

REM Obtener mensaje del commit
if "%~1"=="" (
    for /f "tokens=2-4 delimiters=/ " %%a in ('date /t') do (set datestamp=%%c%%a%%b)
    for /f "tokens=1-2 delimiters=/:" %%a in ('time /t') do (set timestamp=%%a%%b)
    set Mensaje=actualizaciones - %datestamp% %timestamp%
) else (
    set Mensaje=%*
)

echo 📝 Mensaje del commit: !Mensaje!

REM Verificar estatus
echo.
echo 📊 Verificando cambios...
for /f %%A in ('git status --porcelain ^| find /c /v ""') do set /A count=%%A
if !count! gtr 0 (
    echo ✓ Cambios detectados:
    git status --porcelain
) else (
    echo ⚠️ No hay cambios detectados
)

REM Confirmación
echo.
set /p Respuesta="¿Deseas continuar? (S/N): "
if /i not "%Respuesta%"=="s" (
    echo ❌ Operación cancelada
    exit /b 0
)

REM Paso 1: Agregar cambios
echo.
echo ============================================================
echo 📌 Paso 1: Agregando cambios
echo ============================================================
echo Ejecutando: git add -A
echo.
git add -A

if errorlevel 1 (
    echo ❌ Error agregando cambios
    exit /b 1
)
echo ✅ Cambios agregados
echo.

REM Paso 2: Crear commit
echo ============================================================
echo 📌 Paso 2: Creando commit
echo ============================================================
echo Ejecutando: git commit -m "!Mensaje!"
echo.
git commit -m "!Mensaje!"

if errorlevel 1 (
    echo ⚠️ Posiblemente no hay cambios nuevos
) else (
    echo ✅ Commit creado
)
echo.

REM Paso 3: Push a GitHub
echo ============================================================
echo 📌 Paso 3: Subiendo a GitHub
echo ============================================================
echo Ejecutando: git push origin main
echo.
git push origin main

if errorlevel 1 (
    echo ❌ Error al subir a GitHub
    echo.
    echo 💡 Intenta:
    echo    1. Verifica tu conexión a internet
    echo    2. Verifica tu acceso a GitHub (token/contraseña)
    echo    3. Ejecuta manualmente: git push origin main
    exit /b 1
)
echo ✅ Push completado
echo.

REM Mostrar resultado final
echo ============================================================
echo ✅ ¡PROYECTO SUBIDO A GITHUB EXITOSAMENTE!
echo ============================================================
echo.
echo 📌 Último commit:
git log --oneline -1
echo.
echo 🎉 Todos los cambios están en GitHub
echo.
