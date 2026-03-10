#!/usr/bin/env python
"""
Script para restaurar la base de datos desde un archivo SQL
Funciona tanto con SQLite como PostgreSQL
"""

import os
import sqlite3
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def restore_sqlite(sql_file, db_path):
    """Restaura SQLite desde archivo SQL"""
    os.makedirs(os.path.dirname(db_path) or '.', exist_ok=True)
    
    try:
        if os.path.exists(db_path):
            backup_path = f"{db_path}.backup"
            os.rename(db_path, backup_path)
            print(f"📦 Backup anterior: {backup_path}")
        
        conn = sqlite3.connect(db_path)
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
            conn.executescript(sql_script)
        
        conn.commit()
        conn.close()
        
        print(f"✅ SQLite restaurada: {db_path}")
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def restore_postgresql(sql_file, db_url):
    """Restaura PostgreSQL usando psql"""
    try:
        # Parsear URL: postgresql://user:pass@host:5432/dbname
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
        
        # Comando psql
        cmd = [
            'psql',
            f'--host={host}',
            f'--port={port}',
            f'--username={user}',
            f'--dbname={db}',
            f'--file={sql_file}'
        ]
        
        env = os.environ.copy()
        env['PGPASSWORD'] = password
        
        print(f"📥 Restaurando en PostgreSQL ({host})...")
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ PostgreSQL restaurada desde: {sql_file}")
            return True
        else:
            print(f"❌ Error psql: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("💡 Asegúrate de tener psql instalado:")
        print("   Windows: https://www.postgresql.org/download/windows/")
        print("   Linux: sudo apt-get install postgresql-client")
        print("   Mac: brew install postgresql")
        return False

def restore_database(sql_file=None):
    """
    Restaura la BD desde archivo SQL
    Detecta si es SQLite o PostgreSQL automáticamente
    """
    
    if not sql_file:
        backups = sorted(Path('.').glob('database_backup_*.sql'), reverse=True)
        if backups:
            sql_file = str(backups[0])
            print(f"📁 Usando backup más reciente: {sql_file}")
        else:
            print("❌ Uso: python restore_db.py <archivo.sql>")
            return False
    
    if not os.path.exists(sql_file):
        print(f"❌ No se encontró: {sql_file}")
        return False
    
    db_url = os.getenv('DATABASE_URL', 'sqlite:///reportes.db')
    
    print(f"🗄️  Restaurando desde: {sql_file}\n")
    
    if db_url.startswith('sqlite'):
        db_path = db_url.replace('sqlite:///', '')
        success = restore_sqlite(sql_file, db_path)
    elif db_url.startswith('postgres'):
        success = restore_postgresql(sql_file, db_url)
    else:
        print(f"❌ Tipo de BD no soportado: {db_url}")
        success = False
    
    return success

if __name__ == '__main__':
    sql_file = sys.argv[1] if len(sys.argv) > 1 else None
    success = restore_database(sql_file)
    sys.exit(0 if success else 1)
