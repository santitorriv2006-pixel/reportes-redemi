#!/usr/bin/env python
"""
Alternativa rápida: Migración SQLite → PostgreSQL sin instalar localmente
Usa un dump de SQL para migración posterior a Render
"""

import os
import sqlite3
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def export_sqlite_schema_and_data():
    """
    Exporta SQLite con estructura lista para PostgreSQL
    Esto es más seguro y compatible que hacer dump directo
    """
    
    db_url = os.getenv('DATABASE_URL', 'sqlite:///reportes.db')
    
    # Intentar encontrar el archivo en múltiples ubicaciones
    possible_paths = [
        db_url.replace('sqlite:///', ''),
        'instance/reportes.db',
        'reportes.db',
    ]
    
    db_path = None
    for path in possible_paths:
        if os.path.exists(path):
            db_path = path
            break
    
    if not db_path:
        print(f"❌ No se encontró la BD en: {possible_paths}")
        return False
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 1. Exportar dump SQLite estándar
    print("📤 Exportando SQLite...")
    sqlite_dump = f"migration_sqlite_{timestamp}.sql"
    
    try:
        conn = sqlite3.connect(db_path)
        with open(sqlite_dump, 'w', encoding='utf-8') as f:
            for line in conn.iterdump():
                f.write(f'{line}\n')
        conn.close()
        print(f"   ✅ {sqlite_dump}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # 2. Crear archivo de migración PostgreSQL
    print("🔄 Convirtiendo a PostgreSQL...")
    postgres_dump = f"migration_postgres_{timestamp}.sql"
    
    try:
        with open(sqlite_dump, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Cambios de sintaxis SQLite → PostgreSQL
        postgres_content = content.replace('AUTOINCREMENT', '')
        postgres_content = postgres_content.replace("'||'", "||")
        
        with open(postgres_dump, 'w', encoding='utf-8') as f:
            f.write(postgres_content)
        
        print(f"   ✅ {postgres_dump}")
        print(f"\n📊 Archivos generados:")
        print(f"   • {sqlite_dump} ({os.path.getsize(sqlite_dump)/1024:.1f} KB)")
        print(f"   • {postgres_dump} ({os.path.getsize(postgres_dump)/1024:.1f} KB)")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("⚡ MIGRACIÓN RÁPIDA: SQLite → PostgreSQL (sin instalar)")
    print("="*60)
    print("\nEsta opción:")
    print("✅ No requiere PostgreSQL instalado")
    print("✅ Genera archivos listos para Render")
    print("✅ Puedes revisar antes de subir")
    
    if export_sqlite_schema_and_data():
        print("\n📝 PRÓXIMOS PASOS:")
        print("   1. Sube archivos a GitHub:")
        print("      git add migration_*.sql")
        print("      git commit -m 'Add PostgreSQL migration files'")
        print("      git push")
        print("\n   2. En Render:")
        print("      • Crea PostgreSQL database")
        print("      • Deploy automático desde GitHub")
        print("      • En shell: psql < migration_postgres_*.sql")
        print("\n   3. Actualiza .env:")
        print("      DATABASE_URL=postgresql://...")
        
        return True
    
    return False

if __name__ == '__main__':
    import sys
    success = main()
    sys.exit(0 if success else 1)
