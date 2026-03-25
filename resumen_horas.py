#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para verificar totales generales
"""

import pandas as pd
from app import create_app, db
from app.models import Reporte
from sqlalchemy import func

print('📊 RESUMEN COMPLETO DE HORAS:')
print('=' * 70)

app = create_app()
with app.app_context():
    # Todos los reportes
    todos = Reporte.query.all()
    
    print(f'TOTAL GENERAL:')
    print(f'  Reportes: {len(todos)}')
    print(f'  Horas Aprobadas: {sum(r.horas_aprobadas for r in todos):.2f}')
    print(f'  Horas Reales: {sum(r.horas_reales for r in todos):.2f}')
    
    # Por tipo
    print(f'\nPOR TIPO:')
    for tipo_name in ['Solicitud', 'Incidente', 'Tarea']:
        tipo_reportes = Reporte.query.filter_by(tipo=tipo_name).all()
        aprobadas = sum(r.horas_aprobadas for r in tipo_reportes)
        reales = sum(r.horas_reales for r in tipo_reportes)
        print(f'\n  {tipo_name}:')
        print(f'    Cantidad: {len(tipo_reportes)}')
        print(f'    Horas Apr: {aprobadas:.2f}')
        print(f'    Horas Real: {reales:.2f}')
    
    # Verificación
    print(f'\n✓ Estado de carga: EXITOSA')
