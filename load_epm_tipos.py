#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para cargar archivo EPM con mapeo de columnas específico por hoja
"""

import pandas as pd
import sys
import os
sys.path.insert(0, '.')

from app.models import db, Reporte
from app import create_app
from datetime import datetime

app = create_app()

# Mapeos específicos por hoja
COLUMN_MAPPINGS = {
    '1-Solicitudes': {
        'work_order': 'Work Order ID',
        'usuario': 'Analista Asignado',
        'fecha': 'Submit Date',
        'horas_aprobadas': 'Horas_Aprobadas',
        'horas_reales': 'Horas_Reales',
        'grupo': 'ASGRP',
        'status': 'Status'
    },
    '2-Incidentes': {
        'work_order': 'Numero',
        'usuario': 'Analista Asignado',
        'fecha': 'Submit Date',
        'horas_aprobadas': 'HorasAsignado',
        'horas_reales': 'HorasAsignado',
        'grupo': 'Grupo Asignado',
        'status': 'Estado'
    },
    '3-Tareas': {
        'work_order': 'Work Order ID',
        'usuario': 'Assignee',
        'fecha': 'Create Date',
        'horas_aprobadas': 'HorasAsignado',
        'horas_reales': 'HorasAsignado',
        'grupo': 'Assignee Group',
        'status': 'Status'
    }
}

SHEET_TYPE_MAP = {
    '1-Solicitudes': 'Solicitud',
    '2-Incidentes': 'Incidente',
    '3-Tareas': 'Tarea'
}

print("\n" + "="*70)
print("  CARGANDO DATOS EPM CON TIPOS Y MAPEO DE COLUMNAS")
print("="*70 + "\n")

with app.app_context():
    # Primero vaciar tabla anterior
    print("🗑️  Limpiando tabla de reportes...")
    Reporte.query.delete()
    db.session.commit()
    print("✅ Tabla limpiada\n")
    
    archivo = 'archivos/EPM - Solicitudes, Incidentes y Tareas Preview (32).xlsx'
    
    if not os.path.exists(archivo):
        print(f"❌ Archivo no encontrado: {archivo}")
        sys.exit(1)
    
    excel_file = pd.ExcelFile(archivo)
    total_registros = 0
    
    for sheet_name in excel_file.sheet_names:
        if sheet_name not in COLUMN_MAPPINGS:
            print(f"⏭️  Ignorando hoja: {sheet_name}")
            continue
        
        tipo = SHEET_TYPE_MAP[sheet_name]
        mapping = COLUMN_MAPPINGS[sheet_name]
        
        print(f"📥 Procesando: {sheet_name} (Tipo: {tipo})")
        
        try:
            df = pd.read_excel(archivo, sheet_name=sheet_name)
            print(f"   {len(df)} registros leídos")
            
            # Verificar columnas requeridas
            cols_faltantes = []
            for key, col in mapping.items():
                if col not in df.columns:
                    cols_faltantes.append(col)
            
            if cols_faltantes:
                print(f"   ⚠️  Columnas faltantes: {cols_faltantes}")
                print(f"   Columnas disponibles: {list(df.columns)}\n")
                continue
            
            # Procesar cada fila
            contador = 0
            errores = 0
            for idx, row in df.iterrows():
                try:
                    # Validar datos críticos
                    wo = str(row[mapping['work_order']]).strip() if pd.notna(row[mapping['work_order']]) else None
                    usuario = str(row[mapping['usuario']]).strip() if pd.notna(row[mapping['usuario']]) else None
                    
                    if not wo or not usuario:
                        continue
                    
                    # Convertir horas
                    try:
                        horas_aprob = float(row[mapping['horas_aprobadas']]) if pd.notna(row[mapping['horas_aprobadas']]) else 0
                    except:
                        horas_aprob = 0
                    
                    try:
                        horas_real = float(row[mapping['horas_reales']]) if pd.notna(row[mapping['horas_reales']]) else 0
                    except:
                        horas_real = 0
                    
                    # Convertir fecha
                    try:
                        fecha = pd.to_datetime(row[mapping['fecha']]).date()
                    except:
                        fecha = datetime.now().date()
                    
                    reporte = Reporte(
                        wo=wo,
                        usuario_asignado=usuario,
                        fecha=fecha,
                        horas_aprobadas=horas_aprob,
                        horas_reales=horas_real,
                        grupo=str(row[mapping['grupo']]).strip() if pd.notna(row[mapping['grupo']]) else 'Sin Grupo',
                        status=str(row[mapping['status']]).strip() if pd.notna(row[mapping['status']]) else 'Pending',
                        tipo=tipo
                    )
                    db.session.add(reporte)
                    contador += 1
                    total_registros += 1
                    
                    if contador % 2000 == 0:
                        print(f"   ⏳ {contador} registros procesados...")
                except Exception as e:
                    errores += 1
                    continue
            
            print(f"   ✅ {contador} registros agregados")
            if errores > 0:
                print(f"   ⚠️  {errores} errores ignorados\n")
            else:
                print()
            
        except Exception as e:
            print(f"   ❌ Error procesando {sheet_name}: {str(e)}\n")
            continue
    
    print(f"💾 Guardando {total_registros} registros en la base de datos...")
    try:
        db.session.commit()
        print("✅ Datos cargados exitosamente\n")
        
        # Verificar tipos
        tipos_count = db.session.query(Reporte.tipo, db.func.count(Reporte.id)).group_by(Reporte.tipo).all()
        print("📊 Resumen por tipo:")
        for tipo, count in tipos_count:
            print(f"   - {tipo}: {count} registros")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error al guardar: {str(e)}")
