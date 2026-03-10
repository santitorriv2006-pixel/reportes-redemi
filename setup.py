#!/usr/bin/env python
"""
Script de puesta en marcha rápida
Ejecutar: python setup.py
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(text):
    """Imprime un encabezado"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def check_python():
    """Verifica que Python 3.8+ esté instalado"""
    print_header("Verificando Python")
    
    if sys.version_info < (3, 8):
        print("❌ Se requiere Python 3.8 o superior")
        print(f"📦 Versión actual: {sys.version}")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} detectado")

def create_venv():
    """Crea un entorno virtual"""
    print_header("Creando entorno virtual")
    
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("⚠️  El entorno virtual ya existe")
        return
    
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Entorno virtual creado correctamente")
    except Exception as e:
        print(f"❌ Error creando entorno virtual: {e}")
        sys.exit(1)

def get_pip_command():
    """Obtiene el comando pip según el OS"""
    if os.name == 'nt':  # Windows
        return "venv\\Scripts\\pip"
    else:  # Linux/Mac
        return "venv/bin/pip"

def install_requirements():
    """Instala las dependencias"""
    print_header("Instalando dependencias")
    
    pip = get_pip_command()
    
    try:
        subprocess.run([pip, "install", "--upgrade", "pip"], check=True)
        subprocess.run([pip, "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencias instaladas correctamente")
    except Exception as e:
        print(f"❌ Error instalando dependencias: {e}")
        sys.exit(1)

def create_env_file():
    """Crea archivo .env si no existe"""
    print_header("Configurando variables de entorno")
    
    env_file = Path(".env")
    
    if env_file.exists():
        print("⚠️  Archivo .env ya existe")
        return
    
    # Crear archivo .env con valores por defecto
    env_content = """# Configuración de Base de Datos
DATABASE_URL=sqlite:///reportes.db
SQLALCHEMY_TRACK_MODIFICATIONS=False

# Configuración de Flask
FLASK_ENV=development
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
SECRET_KEY=tu_clave_secreta_cambiar_en_produccion

# Configuración de Carga de Archivos
MAX_CONTENT_LENGTH=50000000
UPLOAD_FOLDER=uploads/
ALLOWED_EXTENSIONS=xlsx

# Configuración de Correo (OPCIONAL)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_contraseña_app
MAIL_DEFAULT_SENDER=tu_email@gmail.com
MAIL_RECIPIENTS=email1@empresa.com,email2@empresa.com

# Configuración de Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
"""
    
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print("✅ Archivo .env creado")
    print("⚠️  IMPORTANTE: Edita .env con tu configuración de correo")

def create_directories():
    """Crea directorios necesarios"""
    print_header("Creando directorios")
    
    dirs = ["uploads", "logs"]
    
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"✅ Directorio '{dir_name}' listo")

def initialize_database():
    """Inicializa la base de datos"""
    print_header("Inicializando base de datos")
    
    try:
        from app import create_app, db
        
        app = create_app()
        
        with app.app_context():
            db.create_all()
            print("✅ Base de datos inicializada")
            
    except Exception as e:
        print(f"❌ Error inicializando BD: {e}")
        sys.exit(1)

def load_sample_data():
    """Carga datos de ejemplo"""
    print_header("¿Cargar datos de ejemplo?")
    
    response = input("¿Deseas cargar datos de ejemplo? (s/n): ").lower()
    
    if response in ['s', 'si', 'yes', 'y']:
        try:
            exec(open('init_db.py').read())
            print("✅ Datos de ejemplo cargados")
        except Exception as e:
            print(f"⚠️  No se cargaron datos de ejemplo: {e}")
    else:
        print("⏭️  Saltando datos de ejemplo")

def print_final_instructions():
    """Imprime instrucciones finales"""
    print_header("¡Instalación completada!")
    
    print("""
╔════════════════════════════════════════════════════════════════╗
║            Sistema de Reportes Empresariales                   ║
║                      Listo para usar                           ║
╚════════════════════════════════════════════════════════════════╝

📋 PRÓXIMOS PASOS:

1. EDITAR CONFIGURACIÓN:
   - Abre el archivo ".env"
   - Configura tu correo (MAIL_USERNAME, MAIL_PASSWORD, MAIL_RECIPIENTS)
   - Cambia SECRET_KEY por una clave segura

2. INICIAR LA APLICACIÓN:
   
   En Windows:
   > venv\\Scripts\\activate
   > python run.py
   
   En Linux/Mac:
   $ source venv/bin/activate
   $ python run.py

3. ACCEDER A LA APLICACIÓN:
   - Abre tu navegador
   - Ve a: http://localhost:5000
   - ¡Listo! 🎉

📚 DOCUMENTACIÓN:

   - README.md                 → Guía principal
   - GUIA_DE_USO.md           → Cómo usar la aplicación
   - TECHNICAL_DOCS.md        → Documentación técnica

💡 FUNCIONALIDADES:

   ✓ Cargar archivos Excel
   ✓ Buscar y filtrar reportes
   ✓ Generar gráficos dinámicos
   ✓ Exportar a Excel
   ✓ Enviar reportes automáticos

📧 CONFIGURACIÓN DE CORREO (Opcional):

   Si usas Gmail:
   1. Habilita autenticación de dos factores
   2. Genera una contraseña de aplicación
   3. Usa esa contraseña en .env

   Documentación: https://support.google.com/accounts/answer/185833

⚡ DESARROLLO:

   - Logs en: logs/app.log
   - BD en: reportes.db
   - Uploads en: uploads/

🐛 PROBLEMAS:

   Si algo no funciona:
   1. Verifica que todas las dependencias estén instaladas
   2. Comprueba que el puerto 5000 esté libre
   3. Lee TECHNICAL_DOCS.md para solucionar problemas

═════════════════════════════════════════════════════════════════

¡Gracias por usar el Sistema de Reportes Empresariales! 🚀

    """)

def main():
    """Función principal"""
    
    print("""
╔════════════════════════════════════════════════════════════════╗
║     SETUP - Sistema de Reportes Empresariales                  ║
║                  Puesta en Marcha Rápida                       ║
╚════════════════════════════════════════════════════════════════╝
    """)
    
    # Ejecutar pasos de instalación
    check_python()
    create_venv()
    install_requirements()
    create_directories()
    create_env_file()
    initialize_database()
    load_sample_data()
    print_final_instructions()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Instalación cancelada por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        sys.exit(1)
