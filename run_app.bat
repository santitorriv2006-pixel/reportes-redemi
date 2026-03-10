@echo off
REM Script para ejecutar la aplicación Flask
REM Sistema de Reportes Empresariales

cls
echo.
echo ================================================
echo   Sistema de Reportes Empresariales
echo   Iniciando aplicación...
echo ================================================
echo.

REM Cambiar al directorio del proyecto
cd /d "%~dp0"

REM Activar entorno virtual
call venv\Scripts\activate.bat

if errorlevel 1 (
    echo [ERROR] No se pudo activar el entorno virtual
    pause
    exit /b 1
)

echo [OK] Entorno virtual activado
echo.

REM Iniciar la aplicación Flask
echo Iniciando Flask en http://localhost:5000
echo.
echo Presiona Ctrl+C para detener la aplicación
echo.

python run.py

pause
