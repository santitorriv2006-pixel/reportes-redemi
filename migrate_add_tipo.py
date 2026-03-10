#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de migración para agregar columna 'tipo' a la tabla reportes
"""

import sys
sys.path.insert(0, '.')

from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        # Para SQLite
        inspector = db.inspect(db.engine)
        columns = [c['name'] for c in inspector.get_columns('reportes')]
        
        if 'tipo' not in columns:
            print("Agregando columna 'tipo' a la tabla reportes...")
            
            # SQLite syntax
            db.session.execute(text("""
                ALTER TABLE reportes 
                ADD COLUMN tipo VARCHAR(50) DEFAULT 'Solicitud'
            """))
            
            db.session.commit()
            print("✅ Columna 'tipo' agregada exitosamente")
        else:
            print("✅ La columna 'tipo' ya existe")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\nIMPORTANTE: Si usas PostgreSQL, ejecuta esto manualmente:")
        print("ALTER TABLE reportes ADD COLUMN tipo VARCHAR(50) DEFAULT 'Solicitud';")
