@echo off
REM Script de construcción para Windows PowerShell
REM Este script genera el ejecutable .exe

cls
echo ===============================================
echo  Constructor de Ejecutable - Sistema de Reportes
echo ===============================================
echo.

REM Activar ambiente virtual si existe
if exist venv\Scripts\activate.bat (
    echo Activando entorno virtual...
    call venv\Scripts\activate.bat
)

REM Ejecutar script de compilación
python build.py

pause
