#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para revisar duplicados en tareas
"""

import pandas as pd

# Revisar Excel convertido
df = pd.read_excel('archivos/Reportes_Convertidos.xlsx')

print('🔍 ANÁLISIS DE DUPLICADOS EN TAREAS:')
print('-' * 70)

# Encontrar duplicados
duplicados = df[df.duplicated(keep=False)].sort_values('WO')
print(f'Total registros duplicados: {len(duplicados)}')

if len(duplicados) > 0:
    print(f'\nMostrando duplicados:')
    for col in ['WO', 'Usuario Asignado', 'Fecha', 'Horas Aprobadas', 'Horas Reales', 'Tipo']:
        print(f'  {col}')
    
    for idx, row in duplicados.head(10).iterrows():
        print(f"\nWO={row['WO']}, Usuario={row['Usuario Asignado']}, Tipo={row['Tipo']}")
        print(f"  Horas Apr: {row['Horas Aprobadas']}, Horas Real: {row['Horas Reales']}")

# Verificar tareas específicamente
print('\n' + '='*70)
print('📊 ESTADÍSTICAS GENERALES:')
print('-' * 70)

tareas = df[df['Tipo'] == 'Tarea']
print(f'Tareas totales (antes de drop_duplicates): {len(tareas)}')
print(f'Tareas únicas (WO): {len(tareas.drop_duplicates(subset=["WO"]))}')
print(f'Tareas únicas (WO, Usuario, Fecha): {len(tareas.drop_duplicates(subset=["WO", "Usuario Asignado", "Fecha"]))}')

# Horas
print(f'\nHoras Aprobadas (Tareas):')
print(f'  Total: {tareas["Horas Aprobadas"].sum():.2f}')
print(f'  Promedio por tarea: {tareas["Horas Aprobadas"].mean():.2f}')
print(f'  Min/Max: {tareas["Horas Aprobadas"].min():.2f} / {tareas["Horas Aprobadas"].max():.2f}')

print(f'\nHoras Reales (Tareas):')
print(f'  Total: {tareas["Horas Reales"].sum():.2f}')
print(f'  Promedio por tarea: {tareas["Horas Reales"].mean():.2f}')
print(f'  Min/Max: {tareas["Horas Reales"].min():.2f} / {tareas["Horas Reales"].max():.2f}')
