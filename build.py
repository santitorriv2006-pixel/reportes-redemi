#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de compilación - Genera el ejecutable .exe y el instalador

Uso:
    python build.py
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def limpiar_builds():
    """Elimina builds anteriores"""
    print("🧹 Limpiando builds anteriores...")
    for carpeta in ['build', 'dist', 'SistemaReportes']:
        if os.path.exists(carpeta):
            shutil.rmtree(carpeta)
            print(f"   ✓ Eliminada carpeta: {carpeta}")

def construir_exe():
    """Construye el ejecutable con PyInstaller"""
    print("\n🔨 Construyendo ejecutable...")
    
    try:
        resultado = subprocess.run(
            [sys.executable, '-m', 'PyInstaller', 'reportes_app.spec', '--distpath', 'dist'],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        
        if resultado.returncode == 0:
            print("   ✅ Ejecutable creado exitosamente")
            return True
        else:
            print(f"   ❌ Error: {resultado.stderr}")
            print(f"   Stdout: {resultado.stdout}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error al construir: {str(e)}")
        return False

def crear_script_inno():
    """Crea el script de Inno Setup"""
    print("\n📦 Creando script de instalador...")
    
    script_content = '''#define MyAppName "Sistema de Gestión de Reportes"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "HITSS"
#define MyAppURL "https://example.com"
#define MyAppExeName "SistemaReportes.exe"
#define SourcePath "dist\\SistemaReportes"

[Setup]
AppId={{3F7F42B8-4D9F-4B5C-8A3E-2F8C1D0E9B4A}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=LICENSE.txt
OutputBaseFilename=SistemaReportes_Instalador
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
Uninstallable=yes
UninstallDisplayIcon={{app}}\\{#MyAppExeName}

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\\Spanish.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: {{en:Create a &desktop shortcut,es:Crear un acceso directo en el &escritorio}}; GroupDescription: "{{en:Additional tasks,es:Tareas adicionales}}:"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{{en:Create a &Quick Launch shortcut,es:Crear un acceso rápido}}"; GroupDescription: "{{en:Additional tasks,es:Tareas adicionales}}:"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
Source: "{#SourcePath}\\{#MyAppExeName}"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "{#SourcePath}\\*"; DestDir: "{{app}}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{{group}}\\{#MyAppName}"; Filename: "{{app}}\\{#MyAppExeName}"; WorkingDir: "{{app}}"
Name: "{{group}}\\{{cm:UninstallProgram,{#MyAppName}}}"; Filename: "{{uninstallexe}}"
Name: "{{commondesktop}}\\{#MyAppName}"; Filename: "{{app}}\\{#MyAppExeName}}"; WorkingDir: "{{app}}"; Tasks: desktopicon
Name: "{{userappdata}}\\Microsoft\\Internet Explorer\\Quick Launch\\{#MyAppName}"; Filename: "{{app}}\\{#MyAppExeName}}"; WorkingDir: "{{app}}"; Tasks: quicklaunchicon

[Run]
Filename: "{{app}}\\{#MyAppExeName}"; Flags: nowait postinstall skipifsilent; Description: "{{en:Launch the application,es:Iniciar la aplicación}}"

[UninstallDelete]
Type: dirifempty; Name: "{{app}}"
Type: dirifempty; Name: "{{app}}\\app"
'''
    
    with open('setup_installer.iss', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("   ✓ Script generado: setup_installer.iss")

def generar_portable():
    """Copia el ejecutable a una carpeta portable"""
    print("\n📌 Creando versión portable...")
    
    portable_dir = 'SistemaReportes_Portable'
    
    if os.path.exists(portable_dir):
        shutil.rmtree(portable_dir)
    
    shutil.copytree('dist/SistemaReportes', portable_dir)
    
    # Crear archivo .env de ejemplo
    env_content = '''# Configuración de la Aplicación
FLASK_ENV=production
FLASK_HOST=127.0.0.1
FLASK_PORT=5000

# Base de Datos
DATABASE_URL=sqlite:///reportes.db

# Correo
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu_correo@gmail.com
MAIL_PASSWORD=tu_contraseña
'''
    
    with open(os.path.join(portable_dir, '.env.example'), 'w') as f:
        f.write(env_content)
    
    # Crear README
    readme_content = '''# Sistema de Gestión de Reportes - Versión Portable

## Cómo usar:

1. Extrae esta carpeta en cualquier ubicación
2. Ejecuta: SistemaReportes.exe
3. El navegador se abrirá automáticamente en http://localhost:5000

## Configuración:

- Edita el archivo .env para cambiar la configuración
- La base de datos SQLite se crea automáticamente

## Notas:

- La primera ejecución creará la base de datos
- Asegúrate de tener puerto 5000 disponible
- Para cambiar el puerto, edita .env
'''
    
    with open(os.path.join(portable_dir, 'LEEME.txt'), 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"   ✓ Versión portable creada: {portable_dir}")

def mostrar_instrucciones():
    """Muestra instrucciones de instalación del instalador"""
    print("\n" + "="*60)
    print("✅ CONSTRUCCIÓN COMPLETADA")
    print("="*60)
    print("\n📁 ARCHIVOS GENERADOS:\n")
    print("1. 📌 VERSIÓN PORTABLE:")
    print("   Carpeta: SistemaReportes_Portable/")
    print("   - Ejecutable: SistemaReportes.exe")
    print("   - Usa directamente sin necesidad de instalador")
    print("   - Copia la carpeta a cualquier ubicación\n")
    
    print("2. 📦 INSTALADOR PROFESIONAL:")
    print("   Script: setup_installer.iss")
    print("   Pasos para generar el instalador:")
    print("   \n   a) Descarga Inno Setup desde:")
    print("      https://www.innosetup.com/idsdownload.php?step=1")
    print("   \n   b) Instala Inno Setup")
    print("   \n   c) Haz clic derecho en setup_installer.iss")
    print("      y selecciona 'Compile with Inno Setup'")
    print("   \n   d) Se generará: SistemaReportes_Instalador.exe\n")
    
    print("="*60)
    print("🚀 PRÓXIMOS PASOS:")
    print("="*60)
    print("✓ Para usar versión portable: ejecuta SistemaReportes.exe")
    print("✓ Para crear instalador: instala Inno Setup y compila .iss")
    print("✓ Comparte SistemaReportes_Instalador.exe con otros usuarios")
    print("="*60 + "\n")

def main():
    print("\n" + "="*60)
    print("🔨 CONSTRUCTOR DE EJECUTABLE - Sistema de Reportes")
    print("="*60 + "\n")
    
    limpiar_builds()
    
    if not construir_exe():
        print("❌ No se pudo construir el ejecutable")
        return False
    
    generar_portable()
    crear_script_inno()
    mostrar_instrucciones()
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
