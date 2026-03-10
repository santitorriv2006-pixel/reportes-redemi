#!/usr/bin/env python
"""
Script para exportar la base de datos (SQLite o PostgreSQL)
que puede ser versionado en GitHub y restaurado en Render.
"""

import os
import sqlite3
import subprocess
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def export_sqlite(db_path):
    """Exporta SQLite a archivo SQL"""
    if not os.path.exists(db_path):
        print(f"❌ Error: No se encontró {db_path}")
        return False
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_file = f"database_backup_sqlite_{timestamp}.sql"
    
    try:
        conn = sqlite3.connect(db_path)
        with open(export_file, 'w', encoding='utf-8') as f:
            for line in conn.iterdump():
                f.write(f'{line}\n')
        conn.close()
        
        size_kb = os.path.getsize(export_file) / 1024
        print(f"✅ SQLite exportada: {export_file} ({size_kb:.2f} KB)")
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def export_postgresql(db_url):
    """Exporta PostgreSQL usando pg_dump"""
    # Parsear: postgresql://user:pass@host:5432/dbname
    try:
        # Extraer componentes
        if '://' in db_url:
            parts = db_url.replace('postgresql://', '').replace('postgres://', '')
            if '@' in parts:
                auth, host_db = parts.split('@')
                user, password = auth.split(':')
                host, db = host_db.rsplit('/', 1)
                if ':' in host:
                    host, port = host.split(':')
                else:
                    port = '5432'
            else:
                print("❌ Formato URL inválido")
                return False
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_file = f"database_backup_postgres_{timestamp}.sql"
        
        # Comando pg_dump
        cmd = [
            'pg_dump',
            f'--host={host}',
            f'--port={port}',
            f'--username={user}',
            f'--dbname={db}',
            '--format=plain',
            f'--file={export_file}'
        ]
        
        # Usar variable de entorno para contraseña
        env = os.environ.copy()
        env['PGPASSWORD'] = password
        
        print(f"📤 Descargando PostgreSQL desde {host}...")
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        if result.returncode == 0:
            size_kb = os.path.getsize(export_file) / 1024
            print(f"✅ PostgreSQL exportada: {export_file} ({size_kb:.2f} KB)")
            return True
        else:
            print(f"❌ Error pg_dump: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("💡 Asegúrate de tener pg_dump instalado:")
        print("   Windows: https://www.postgresql.org/download/windows/")
        print("   Linux: sudo apt-get install postgresql-client")
        print("   Mac: brew install postgresql")
        return False

def export_database():
    """Exporta la base de datos (detecta SQLite o PostgreSQL)"""
    db_url = os.getenv('DATABASE_URL', 'sqlite:///reportes.db')
    
    print("🗄️  Exportando base de datos...\n")
    
    if db_url.startswith('sqlite'):
        # SQLite
        db_path = db_url.replace('sqlite:///', '')
        success = export_sqlite(db_path)
    elif db_url.startswith('postgres'):
        # PostgreSQL
        success = export_postgresql(db_url)
    else:
        print(f"❌ Tipo de BD no soportado: {db_url}")
        success = False
    
    if success:
        print("\n📝 Próximos pasos:")
        print("   1. Revisa el archivo SQL antes de subirlo")
        print("   2. git add database_backup_*.sql")
        print("   3. git commit -m 'Add database backup'")
        print("   4. git push")
    
    return success

if __name__ == '__main__':
    import sys
    sys.exit(0 if export_database() else 1)
