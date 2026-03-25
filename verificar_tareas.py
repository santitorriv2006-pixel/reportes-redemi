#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para verificar integridad de tareas
"""

import pandas as pd
from app import create_app, db
from app.models import Reporte
from sqlalchemy import func

# Revisar Excel convertido
df = pd.read_excel('archivos/Reportes_Convertidos.xlsx')
print('📊 ARCHIVO CONVERTIDO (Reportes_Convertidos.xlsx):')
print('-' * 70)
print(f'  Total registros: {len(df)}')
print(f'  Tareas: {len(df[df["Tipo"] == "Tarea"])}')
print(f'  Solicitudes: {len(df[df["Tipo"] == "Solicitud"])}')
print(f'  Incidentes: {len(df[df["Tipo"] == "Incidente"])}')

# Estadísticas de tareas
tareas_excel = df[df['Tipo'] == 'Tarea']
print(f'\n  Horas totales aprobadas (tareas): {tareas_excel["Horas Aprobadas"].sum():.2f}')
print(f'  Horas totales reales (tareas): {tareas_excel["Horas Reales"].sum():.2f}')
print(f'  Tareas sin WO: {len(tareas_excel[tareas_excel["WO"].isna()])}')
print(f'  Registros duplicados: {len(df) - len(df.drop_duplicates())}')

# Revisar BD
print('\n' + '='*70)
print('📊 BASE DE DATOS (Reportes en BD):')
print('-' * 70)

app = create_app()
with app.app_context():
    tareas_db = Reporte.query.filter_by(tipo='Tarea').all()
    print(f'  Total Tareas en BD: {len(tareas_db)}')
    print(f'  Horas aprobadas (tareas): {sum(t.horas_aprobadas for t in tareas_db):.2f}')
    print(f'  Horas reales (tareas): {sum(t.horas_reales for t in tareas_db):.2f}')
    print(f'  Tareas con WO vacío: {len([t for t in tareas_db if not t.wo or t.wo.strip() == ""])}')
    
    # Contar usuarios únicos
    usuarios_unicos = db.session.query(func.count(func.distinct(Reporte.usuario_asignado))).filter_by(tipo='Tarea').scalar()
    print(f'  Usuarios únicos: {usuarios_unicos}')
    
    # Primeras y últimas tareas
    print(f'\n  Primeras 3 tareas:')
    for i, tarea in enumerate(tareas_db[:3]):
        print(f'    {i+1}. WO={tarea.wo}, Usuario={tarea.usuario_asignado}, Fecha={tarea.fecha}')
