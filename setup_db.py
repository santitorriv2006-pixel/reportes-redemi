#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para configurar la base de datos e importar datos del Excel
"""

import pandas as pd
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, '.')

from app.models import db, Reporte
from app import create_app

# Crear app
app = create_app()

print("\n" + "="*70)
print("  SETUP DE BASE DE DATOS E IMPORTACIÓN DE DATOS")
print("="*70 + "\n")

with app.app_context():
    print("📊 Paso 1: Creando tablas en la base de datos...")
    db.create_all()
    print("   ✅ Tablas creadas exitosamente\n")
    
    print("📥 Paso 2: Leyendo archivo Reportes_Convertidos.xlsx...")
    df = pd.read_excel('archivos/Reportes_Convertidos.xlsx')
    print(f"   ✅ {len(df)} registros leídos\n")
    
    print("💾 Paso 3: Importando datos a la base de datos...")
    for idx, row in df.iterrows():
        reporte = Reporte(
            wo=str(row['WO']),
            usuario_asignado=str(row['Usuario Asignado']),
            fecha=pd.to_datetime(row['Fecha']).date(),
            horas_aprobadas=float(row['Horas Aprobadas']),
            horas_reales=float(row['Horas Reales']),
            grupo=str(row['Grupo']),
            status=str(row['Status']),
            fecha_carga=pd.Timestamp.now().date()
        )
        db.session.add(reporte)
        
        if (idx + 1) % 5000 == 0:
            print(f"   ⏳ {idx + 1} registros procesados...")
    
    print("   Guardando cambios...")
    db.session.commit()
    
    # Verificar
    total = db.session.query(Reporte).count()
    print(f"   ✅ {total} registros importados\n")
    
    # Mostrar estadísticas
    print("📊 Paso 4: Estadísticas de la importación...")
    
    # Status
    status_list = db.session.query(Reporte.status).distinct().order_by(Reporte.status).all()
    print(f"\n   Status disponibles ({len(status_list)}):")
    for s in status_list:
        count = db.session.query(Reporte).filter_by(status=s[0]).count()
        print(f"      • {s[0]}: {count} registros")
    
    # Usuarios
    usuarios = db.session.query(Reporte.usuario_asignado).distinct().count()
    print(f"\n   Usuarios únicos: {usuarios}")
    
    # Grupos
    grupos = db.session.query(Reporte.grupo).distinct().count()
    print(f"   Grupos únicos: {grupos}")
    
    # Horas
    total_horas_aprobadas = db.session.query(db.func.sum(Reporte.horas_aprobadas)).scalar() or 0
    total_horas_reales = db.session.query(db.func.sum(Reporte.horas_reales)).scalar() or 0
    print(f"   Total Horas Aprobadas: {total_horas_aprobadas:,.2f}")
    print(f"   Total Horas Reales: {total_horas_reales:,.2f}")

print("\n" + "="*70)
print("  ✅ SETUP COMPLETADO EXITOSAMENTE")
print("="*70 + "\n")
print("🚀 Ahora puedes ejecutar: python run.py\n")
