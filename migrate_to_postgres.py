#!/usr/bin/env python
"""
Script para migrar de SQLite a PostgreSQL
Soporta migración local o a Render
"""

import os
import sys
from dotenv import load_dotenv
from app import create_app, db
from app.models import *  # Importa todos los modelos
from sqlalchemy import inspect, text
from urllib.parse import urlparse

load_dotenv()

def get_db_config():
    """Obtiene configuración de BD actual y destino"""
    current_url = os.getenv('DATABASE_URL', 'sqlite:///reportes.db')
    
    print("\n" + "="*60)
    print("🔄 MIGRACIÓN SQLite → PostgreSQL")
    print("="*60)
    print(f"\n📍 Base de datos actual: {current_url[:50]}...")
    
    return current_url

def option_local_postgres():
    """Opción 1: PostgreSQL local"""
    print("\n" + "="*60)
    print("OPCIÓN 1: PostgreSQL Local (para testing)")
    print("="*60)
    print("\n❌ PostgreSQL no está instalado en tu computadora")
    print("\n📥 INSTALAR PostgreSQL:")
    print("   Windows: https://bit.ly/pg-windows")
    print("   Mac: brew install postgresql")
    print("   Linux: sudo apt-get install postgresql postgresql-contrib")
    print("\n✅ Después de instalar, configura:")
    print("   1. Abre pgAdmin o psql")
    print("   2. Crea base de datos: CREATE DATABASE reportes;")
    print("   3. Crea usuario: CREATE USER reportes_user WITH PASSWORD 'tu_contraseña';")
    print("   4. Dale permisos: ALTER ROLE reportes_user CREATEDB;")
    print("\n📝 Luego actualiza .env con:")
    print("   DATABASE_URL=postgresql://reportes_user:tu_contraseña@localhost:5432/reportes")

def option_render_postgres():
    """Opción 2: PostgreSQL en Render (recomendado)"""
    print("\n" + "="*60)
    print("OPCIÓN 2: PostgreSQL en Render (⭐ RECOMENDADO)")
    print("="*60)
    print("\n✅ Ventajas:")
    print("   • No requiere instalar nada localmente")
    print("   • Ya funciona en producción")
    print("   • Datos listos para desplegar")
    print("   • Gratis con créditos de Render")
    print("\n📋 Pasos:")
    print("   1. Crea PostgreSQL en Render:")
    print("      Dashboard → New → PostgreSQL")
    print("   2. Copia el Internal Database URL")
    print("   3. Actualiza .env:")
    print("      DATABASE_URL=postgresql://...")
    print("   4. Ejecuta este script nuevamente")
    print("   5. Sube los cambios a GitHub")
    print("   6. El deploy en Render es automático")

def migrate_data(old_url, new_url):
    """Migra datos de SQLite a PostgreSQL"""
    print("\n" + "="*60)
    print("🔄 MIGRANDO DATOS...")
    print("="*60)
    
    try:
        # Crear app con BD actual
        app = create_app()
        
        # Cambiar a BD nueva
        app.config['SQLALCHEMY_DATABASE_URI'] = new_url
        
        with app.app_context():
            print("\n1️⃣  Leyendo datos de SQLite...")
            # Conectar a BD actual
            sqlite_db = db.get_engine(bind='sqlite')
            
            print("2️⃣  Creando tablas en PostgreSQL...")
            # Crear todas las tablas
            db.create_all()
            
            print("3️⃣  Copiando registros...")
            # Obtener todos los modelos registrados
            from app import models
            import inspect as inspect_module
            
            for name, obj in inspect_module.getmembers(models):
                if inspect_module.isclass(obj) and hasattr(obj, '__tablename__'):
                    model = obj
                    tabla = model.__tablename__
                    
                    # Leer registros de SQLite
                    registros = model.query.all()
                    
                    if registros:
                        print(f"   • {tabla}: {len(registros)} registros", end=" ")
                        for registro in registros:
                            db.session.merge(registro)
                        db.session.commit()
                        print("✅")
                    else:
                        print(f"   • {tabla}: vacío")
            
            print("\n✅ Migración completada exitosamente!")
            print(f"\n📊 Resumen:")
            print(f"   De: {old_url[:40]}...")
            print(f"   A:  {new_url[:40]}...")
            
            return True
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\n💡 Soluciones:")
        print("   1. Verifica que PostgreSQL está conectado")
        print("   2. Ve a INSTALL_POSTGRES_TOOLS.md para instalar herramientas")
        print("   3. Contacta al admin si persiste")
        return False

def main():
    """Menú principal"""
    current_url = get_db_config()
    
    # Verificar que es SQLite
    if not current_url.startswith('sqlite'):
        print("\n⚠️  Ya estás usando:", current_url.split(':')[0])
        print("No hay migración necesaria.")
        sys.exit(0)
    
    print("\n¿Cómo deseas hacer la migración?")
    print("\n1. PostgreSQL Local (necesita instalar)")
    print("2. PostgreSQL en Render (⭐ recomendado)")
    print("3. Salir")
    
    choice = input("\nElige opción (1-3): ").strip()
    
    if choice == "1":
        option_local_postgres()
        input("\nPresiona Enter cuando hayas instalado PostgreSQL...")
        
        # Pedir configuración
        user = input("Usuario PostgreSQL (default: postgres): ").strip() or "postgres"
        password = input("Contraseña: ").strip()
        host = input("Host (default: localhost): ").strip() or "localhost"
        port = input("Puerto (default: 5432): ").strip() or "5432"
        dbname = input("Nombre BD (default: reportes): ").strip() or "reportes"
        
        new_url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
        
        # Guardar en .env
        save_config = input("\n¿Guardar en .env? (s/n): ").strip().lower()
        if save_config == 's':
            update_env(new_url)
            migrate_data(current_url, new_url)
    
    elif choice == "2":
        option_render_postgres()
        input("\nPresiona Enter cuando hayas creado PostgreSQL en Render...")
        
        new_url = input("Pega aquí el Internal Database URL de Render: ").strip()
        
        save_config = input("¿Guardar en .env? (s/n): ").strip().lower()
        if save_config == 's':
            update_env(new_url)
            print("\n✅ Configuración actualizada en .env")
            print("📝 Cuando el ambiente sea identico, ejecuta:")
            print("   python migrate_to_postgres.py")
            print("   (esta vez con PostgreSQL disponible)")
    
    else:
        print("Saliendo...")
        sys.exit(0)

def update_env(new_url):
    """Actualiza el .env con la nueva URL"""
    env_file = '.env'
    
    with open(env_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Reemplazar o agregar DATABASE_URL
    found = False
    for i, line in enumerate(lines):
        if line.startswith('DATABASE_URL='):
            lines[i] = f"DATABASE_URL={new_url}\n"
            found = True
            break
    
    if not found:
        lines.insert(0, f"DATABASE_URL={new_url}\n")
    
    with open(env_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"✅ .env actualizado con nueva URL")

if __name__ == '__main__':
    main()
