#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Convertidor de archivo EPM a formato de la aplicación de reportes
"""

import pandas as pd
from datetime import datetime
import os

archivo_original = r'archivos/EPM - Solicitudes, Incidentes y Tareas Preview (32).xlsx'
archivo_salida = r'archivos/Reportes_Convertidos.xlsx'

print("╔════════════════════════════════════════════════════════╗")
print("║  CONVERTIENDO ARCHIVO EPM A FORMATO DE REPORTES       ║")
print("╚════════════════════════════════════════════════════════╝\n")

datos_consolidados = []

# 1. SOLICITUDES
print("📋 Procesando: Solicitudes...")
df_solicitudes = pd.read_excel(archivo_original, sheet_name='1-Solicitudes')
solicitudes_procesadas = df_solicitudes[
    df_solicitudes['Work Order ID'].notna() &
    (df_solicitudes['Horas_Aprobadas'].notna() | df_solicitudes['Horas_Reales'].notna())
].copy()

for idx, row in solicitudes_procesadas.iterrows():
    datos_consolidados.append({
        'WO': str(row.get('Work Order ID', '')),
        'Usuario Asignado': str(row.get('Analista Asignado', 'Desconocido')),
        'Fecha': pd.to_datetime(row.get('Submit Date', datetime.now())).date(),
        'Horas Aprobadas': float(row.get('Horas_Aprobadas', 0) or 0),
        'Horas Reales': float(row.get('Horas_Reales', 0) or 0),
        'Grupo': str(row.get('ASGRP', 'General')),
        'Status': str(row.get('Status', 'Pending')).strip() or 'Pending'
    })

print(f"   ✓ {len(solicitudes_procesadas)} solicitudes procesadas")

# 2. INCIDENTES
print("📋 Procesando: Incidentes...")
df_incidentes = pd.read_excel(archivo_original, sheet_name='2-Incidentes')
incidentes_procesados = df_incidentes[
    df_incidentes['Numero'].notna()
].copy()

for idx, row in incidentes_procesados.iterrows():
    datos_consolidados.append({
        'WO': str(row.get('Numero', '')),
        'Usuario Asignado': str(row.get('Analista Asignado', 'Desconocido')),
        'Fecha': pd.to_datetime(row.get('Submit Date', datetime.now())).date(),
        'Horas Aprobadas': float(row.get('HorasAsignado', 0) or 0),
        'Horas Reales': float(row.get('HorasAsignado', 0) or 0),
        'Grupo': str(row.get('Grupo Asignado', 'General')),
        'Status': str(row.get('Estado', 'Pending')).strip() or 'Pending'
    })

print(f"   ✓ {len(incidentes_procesados)} incidentes procesados")

# 3. TAREAS
print("📋 Procesando: Tareas...")
df_tareas = pd.read_excel(archivo_original, sheet_name='3-Tareas')
tareas_procesadas = df_tareas[
    df_tareas['Work Order ID'].notna() &
    df_tareas['Task ID'].notna()
].copy()

for idx, row in tareas_procesadas.iterrows():
    datos_consolidados.append({
        'WO': str(row.get('Work Order ID', '')),
        'Usuario Asignado': str(row.get('Assignee', 'Desconocido')),
        'Fecha': pd.to_datetime(row.get('Create Date', datetime.now())).date(),
        'Horas Aprobadas': float(row.get('HorasAsignado', 0) or 0),
        'Horas Reales': float(row.get('HorasAsignado', 0) or 0),
        'Grupo': str(row.get('Assignee Group', 'General')),
        'Status': str(row.get('Status', 'Pending')).strip() or 'Pending'
    })

print(f"   ✓ {len(tareas_procesadas)} tareas procesadas")

# Crear DataFrame final
df_final = pd.DataFrame(datos_consolidados)

# Limpieza
df_final = df_final.drop_duplicates()
df_final = df_final[df_final['WO'].str.len() > 0]

# ⚠️ CRÍTICO: Llenar valores faltantes en columnas numéricas
df_final['Horas Aprobadas'] = df_final['Horas Aprobadas'].fillna(0).astype(float)
df_final['Horas Reales'] = df_final['Horas Reales'].fillna(0).astype(float)

# Asegurar que no hay NaN en campos críticos
df_final['Usuario Asignado'] = df_final['Usuario Asignado'].fillna('Desconocido').astype(str)
df_final['Grupo'] = df_final['Grupo'].fillna('General').astype(str)
df_final['Status'] = df_final['Status'].fillna('Pending').astype(str)

print(f"\n✅ Total de registros consolidados: {len(df_final)}")

# Guardar
try:
    df_final.to_excel(archivo_salida, index=False, sheet_name='Reportes')
    print(f"\n✓ Archivo guardado: {archivo_salida}")
    print(f"\n📊 PREVISUALIZACIÓN (primeras 5 filas):")
    print(df_final.head(5).to_string())
except Exception as e:
    print(f"❌ Error al guardar: {e}")
