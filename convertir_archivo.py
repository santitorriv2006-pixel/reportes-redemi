#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para convertir el archivo EPM al formato requerido por la aplicación
"""

import pandas as pd
from datetime import datetime
import openpyxl

# Archivo original
archivo_original = r'archivos/epm.xlsx'

# Leer todas las hojas
excel_file = pd.ExcelFile(archivo_original)

print("╔════════════════════════════════════════════════════════╗")
print("║  ANALIZANDO ARCHIVO EPM                               ║")
print("╚════════════════════════════════════════════════════════╝\n")

print(f"📊 Hojas encontradas: {len(excel_file.sheet_names)}")
for i, sheet in enumerate(excel_file.sheet_names, 1):
    print(f"   {i}. {sheet}")

print("\n" + "="*60)
print("ANÁLISIS DETALLADO DE CADA HOJA")
print("="*60 + "\n")

for sheet in excel_file.sheet_names:
    df = pd.read_excel(archivo_original, sheet_name=sheet)
    print(f"\n📋 HOJA: {sheet}")
    print(f"   Filas: {len(df)} | Columnas: {len(df.columns)}")
    print(f"   Columnas: {list(df.columns)}")
    print(f"\n   Primeras filas:\n{df.head(2).to_string()}\n")

print("\n" + "="*60)
print("RESUMEN")
print("="*60)
print("""
⚠️  FORMATO ACTUAL:
   El archivo tiene estructura de reportes de EPM/Jira
   con múltiples hojas por tipo de elemento

✅ FORMATO REQUERIDO:
   • WO (string) - Número de trabajo
   • Usuario Asignado (string) - Persona responsable
   • Fecha (date) - Fecha del reporte
   • Horas Aprobadas (float) - Horas registradas
   • Horas Reales (float) - Horas trabajadas
   • Grupo (string) - Equipo/Grupo

💡 SOLUCIÓN:
   Necesitas crear un Excel con ese formato o
   indicar cuáles columnas del archivo actual
   corresponden a cada campo requerido.
""")
