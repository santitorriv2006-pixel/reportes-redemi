#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Reporte de verificación completo de la carga de datos
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from app.models import db, Reporte
import pandas as pd

app = create_app()

with app.app_context():
    print("\n" + "=" * 80)
    print("REPORTE DE VERIFICACIÓN DE DATOS")
    print("=" * 80)
    
    # Leer Excel original
    print("\n📄 DATOS EN EXCEL (Reportes_Convertidos.xlsx):")
    df_excel = pd.read_excel('archivos/Reportes_Convertidos.xlsx')
    
    print(f"  Total registros: {len(df_excel):,}")
    print(f"  Usuarios únicos: {df_excel['Usuario Asignado'].nunique()}")
    print(f"  Grupos únicos: {df_excel['Grupo'].nunique()}")
    print(f"\n  HORAS EN EXCEL:")
    print(f"    Horas Aprobadas: {df_excel['Horas Aprobadas'].sum():,.2f}")
    print(f"    Horas Reales: {df_excel['Horas Reales'].sum():,.2f}")
    print(f"    Diferencia: {(df_excel['Horas Reales'] - df_excel['Horas Aprobadas']).sum():,.2f}")
    
    # Verificar en BD
    print("\n📊 DATOS EN BASE DE DATOS:")
    
    total_bd = db.session.query(db.func.count(Reporte.id)).scalar()
    usuarios_bd = db.session.query(db.func.count(db.func.distinct(Reporte.usuario_asignado))).scalar()
    grupos_bd = db.session.query(db.func.count(db.func.distinct(Reporte.grupo))).scalar()
    
    print(f"  Total registros: {total_bd:,}")
    print(f"  Usuarios únicos: {usuarios_bd}")
    print(f"  Grupos únicos: {grupos_bd}")
    
    total_aprobadas_bd = db.session.query(db.func.sum(Reporte.horas_aprobadas)).scalar() or 0
    total_reales_bd = db.session.query(db.func.sum(Reporte.horas_reales)).scalar() or 0
    
    print(f"\n  HORAS EN BD:")
    print(f"    Horas Aprobadas: {total_aprobadas_bd:,.2f}")
    print(f"    Horas Reales: {total_reales_bd:,.2f}")
    print(f"    Diferencia: {total_reales_bd - total_aprobadas_bd:,.2f}")
    
    # Comparación
    print("\n✓ COMPARACIÓN:")
    excel_aprobadas = df_excel['Horas Aprobadas'].sum()
    excel_reales = df_excel['Horas Reales'].sum()
    
    diff_aprobadas = abs(excel_aprobadas - total_aprobadas_bd)
    diff_reales = abs(excel_reales - total_reales_bd)
    
    print(f"  Diferencia Horas Aprobadas: {diff_aprobadas:.2f} " + ("✅ OK" if diff_aprobadas < 0.01 else "❌ ERROR"))
    print(f"  Diferencia Horas Reales: {diff_reales:.2f} " + ("✅ OK" if diff_reales < 0.01 else "❌ ERROR"))
    
    # Top usuarios por horas
    print("\n👥 TOP 10 USUARIOS (por Horas Reales):")
    usuarios_top = db.session.query(
        Reporte.usuario_asignado,
        db.func.count(Reporte.id).label('registros'),
        db.func.sum(Reporte.horas_aprobadas).label('aprobadas'),
        db.func.sum(Reporte.horas_reales).label('reales')
    ).group_by(Reporte.usuario_asignado).order_by(
        db.func.sum(Reporte.horas_reales).desc()
    ).limit(10).all()
    
    for usuario, registros, aprobadas, reales in usuarios_top:
        print(f"  {usuario[:40]:40} - Registros: {registros:4}, Horas: {reales:9,.2f}")
    
    # Distribución por tipo
    print("\n📋 DISTRIBUCIÓN POR TIPO:")
    tipos = db.session.query(
        Reporte.tipo,
        db.func.count(Reporte.id).label('cantidad'),
        db.func.sum(Reporte.horas_reales).label('total_horas')
    ).group_by(Reporte.tipo).order_by(
        db.func.count(Reporte.id).desc()
    ).all()
    
    for tipo, cantidad, total_horas in tipos:
        print(f"  {tipo:15} - {cantidad:6,} registros - {total_horas:12,.2f} horas")
    
    # Distribución por grupo (top 5)
    print("\n🏢 TOP 5 GRUPOS (por Horas):")
    grupos_top = db.session.query(
        Reporte.grupo,
        db.func.count(Reporte.id).label('registros'),
        db.func.sum(Reporte.horas_reales).label('total_horas')
    ).group_by(Reporte.grupo).order_by(
        db.func.sum(Reporte.horas_reales).desc()
    ).limit(5).all()
    
    for grupo, registros, total_horas in grupos_top:
        print(f"  {grupo[:45]:45} - {registros:5,} registros - {total_horas:10,.2f} horas")
    
    print("\n" + "=" * 80)
    print("✅ VERIFICACIÓN COMPLETADA")
    print("=" * 80 + "\n")
