#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para verificación exhaustiva de solicitudes
"""

import pandas as pd
from app import create_app, db
from app.models import Reporte
from sqlalchemy import func

print('🔍 VERIFICACIÓN EXHAUSTIVA DE SOLICITUDES')
print('=' * 80)

# 1. Verificar EPM original
print('\n1️⃣ VERIFICANDO ARCHIVO EPM ORIGINAL:')
print('-' * 80)

try:
    df_epm_orig = pd.read_excel('archivos/EPM 59.xlsx', sheet_name='1-Solicitudes')
    print(f'  ✓ Archivos EPM: {len(df_epm_orig)} registros en hoja 1-Solicitudes')
    
    # Contar solicitudes válidas
    solicitudes_validas_orig = df_epm_orig[
        df_epm_orig['Work Order ID'].notna() &
        (df_epm_orig['Horas_Aprobadas'].notna() | df_epm_orig['Horas_Reales'].notna())
    ]
    print(f'  ✓ Solicitudes válidas (con horas): {len(solicitudes_validas_orig)}')
    
    # Estadísticas
    print(f'\n  Estadísticas EPM original:')
    print(f'    Total Horas Aprobadas: {solicitudes_validas_orig["Horas_Aprobadas"].fillna(0).sum():.2f}')
    print(f'    Total Horas Reales: {solicitudes_validas_orig["Horas_Reales"].fillna(0).sum():.2f}')
    print(f'    Usuarios únicos: {solicitudes_validas_orig["Analista Asignado"].nunique()}')
    
except Exception as e:
    print(f'  ❌ Error: {e}')

# 2. Verificar archivo convertido
print('\n2️⃣ VERIFICANDO ARCHIVO CONVERTIDO:')
print('-' * 80)

try:
    df_convertido = pd.read_excel('archivos/Reportes_Convertidos.xlsx')
    solicitudes_convertidas = df_convertido[df_convertido['Tipo'] == 'Solicitud']
    
    print(f'  ✓ Solicitudes en convertido: {len(solicitudes_convertidas)}')
    print(f'    Total Horas Aprobadas: {solicitudes_convertidas["Horas Aprobadas"].sum():.2f}')
    print(f'    Total Horas Reales: {solicitudes_convertidas["Horas Reales"].sum():.2f}')
    
    # Validaciones
    print(f'\n  Validaciones:')
    print(f'    WO vacíos: {len(solicitudes_convertidas[solicitudes_convertidas["WO"].isna()])}')
    print(f'    Usuarios vacíos: {len(solicitudes_convertidas[solicitudes_convertidas["Usuario Asignado"].isna()])}')
    print(f'    Fechas vacías: {len(solicitudes_convertidas[solicitudes_convertidas["Fecha"].isna()])}')
    print(f'    Status vacío: {len(solicitudes_convertidas[solicitudes_convertidas["Status"].isna()])}')
    print(f'    Grupo vacío: {len(solicitudes_convertidas[solicitudes_convertidas["Grupo"].isna()])}')
    
except Exception as e:
    print(f'  ❌ Error: {e}')

# 3. Verificar BD
print('\n3️⃣ VERIFICANDO EN BASE DE DATOS:')
print('-' * 80)

app = create_app()
with app.app_context():
    solicitudes_bd = Reporte.query.filter_by(tipo='Solicitud').all()
    
    print(f'  ✓ Solicitudes en BD: {len(solicitudes_bd)}')
    print(f'    Total Horas Aprobadas: {sum(s.horas_aprobadas for s in solicitudes_bd):.2f}')
    print(f'    Total Horas Reales: {sum(s.horas_reales for s in solicitudes_bd):.2f}')
    
    # Validaciones en BD
    print(f'\n  Validaciones en BD:')
    print(f'    WO vacíos: {len([s for s in solicitudes_bd if not s.wo or s.wo.strip() == ""])}')
    print(f'    Usuarios vacíos: {len([s for s in solicitudes_bd if not s.usuario_asignado])}')
    print(f'    Status vacío: {len([s for s in solicitudes_bd if not s.status])}')
    print(f'    Grupo vacío: {len([s for s in solicitudes_bd if not s.grupo])}')
    print(f'    Horas aprobadas negativas: {len([s for s in solicitudes_bd if s.horas_aprobadas < 0])}')
    print(f'    Horas reales negativas: {len([s for s in solicitudes_bd if s.horas_reales < 0])}')
    
    # Status únicos
    status_unicos = db.session.query(func.distinct(Reporte.status)).filter_by(tipo='Solicitud').all()
    print(f'\n  Status únicos en Solicitudes: {[s[0] for s in status_unicos]}')
    
    # Distribución de status
    print(f'\n  Distribución por status:')
    for status in [s[0] for s in status_unicos]:
        count = Reporte.query.filter_by(tipo='Solicitud', status=status).count()
        horas = sum(r.horas_reales for r in Reporte.query.filter_by(tipo='Solicitud', status=status).all())
        print(f'    {status}: {count} solicitudes ({horas:.2f} horas)')
    
    # Muestra de solicitudes
    print(f'\n  Primeras 5 solicitudes:')
    for i, sol in enumerate(solicitudes_bd[:5]):
        print(f'    {i+1}. WO={sol.wo}, Usuario={sol.usuario_asignado}, Status={sol.status}, Horas={sol.horas_reales}')

# 4. Comparación
print('\n4️⃣ COMPARACIÓN EPM → CONVERTIDO → BD:')
print('-' * 80)

print(f'  EPM original:           {len(solicitudes_validas_orig):>6} solicitudes')
print(f'  Archivo convertido:     {len(solicitudes_convertidas):>6} solicitudes')
print(f'  Base de datos:          {len(solicitudes_bd):>6} solicitudes')

if len(solicitudes_validas_orig) == len(solicitudes_convertidas) == len(solicitudes_bd):
    print(f'\n  ✅ PERFECTO: Los números coinciden en todas las etapas')
else:
    print(f'\n  ⚠️  DIFERENCIAS DETECTADAS')

print(f'\n✓ Verificación completada')
