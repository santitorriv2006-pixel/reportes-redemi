#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Carga todos los tipos de reportes (Solicitudes, Incidentes, Tareas) desde EPM
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from app.models import db, Reporte, HistorialCarga
import pandas as pd
from datetime import datetime
from io import BytesIO

app = create_app()

with app.app_context():
    print("=" * 60)
    print("CARGANDO REPORTES POR TIPO")
    print("=" * 60)
    
    archivo_excel = 'archivos/EPM - Solicitudes, Incidentes y Tareas Preview (32).xlsx'
    
    tipos_config = {
        "1-Solicitudes": {
            "tipo_reportes": "Solicitud",
            "columna_wo": "Work Order ID",
            "usuario_col": None  # Necesitaremos buscar una columna similar
        },
        "2-Incidentes": {
            "tipo_reportes": "Incidente",
            "columna_wo": "Numero",
            "usuario_col": None
        },
        "3-Tareas": {
            "tipo_reportes": "Tarea",
            "columna_wo": "Work Order ID",
            "usuario_col": None
        }
    }
    
    # Primero, limpiar la BD
    print("\n🗑️  Limpiando reportes anteriores...")
    db.session.query(Reporte).delete()
    db.session.commit()
    print("✅ Base de datos limpia")
    
    total_cargados = 0
    total_errores = 0
    cargas_por_tipo = {}
    
    try:
        excel = pd.ExcelFile(archivo_excel)
        
        for sheet_name, config in tipos_config.items():
            if sheet_name not in excel.sheet_names:
                print(f"\n⚠️  Hoja {sheet_name} no encontrada")
                continue
            
            print(f"\n📊 Procesando: {sheet_name}")
            print(f"   Tipo de Reporte: {config['tipo_reportes']}")
            
            # Leer datos
            df = pd.read_excel(archivo_excel, sheet_name=sheet_name)
            print(f"   Registros en hoja: {len(df)}")
            
            # Identificar columnas disponibles
            print(f"   Columnas: {list(df.columns[:5])}")
            
            # Procesar cada registro
            cargados = 0
            errores = 0
            
            for idx, row in df.iterrows():
                try:
                    # Obtener WO
                    wo = str(row.get(config['columna_wo'], f"WO-{idx}")).strip() if config['columna_wo'] in df.columns else f"WO-{idx}"
                    
                    # Crear reporte
                    reporte = Reporte(
                        wo=wo,
                        usuario_asignado="Sistema",  # Valor por defecto ya que no existe esta columna
                        fecha=datetime.now().date(),
                        horas_aprobadas=0.0,
                        horas_reales=0.0,
                        grupo="General",
                        status="Completado",
                        tipo=config['tipo_reportes']
                    )
                    
                    db.session.add(reporte)
                    cargados += 1
                    
                    if cargados % 1000 == 0:
                        print(f"   Procesados: {cargados}/{len(df)}")
                
                except Exception as e:
                    errores += 1
                    if errores <= 3:
                        print(f"   Error fila {idx}: {str(e)[:50]}")
            
            # Guardar cambios de esta hoja
            db.session.commit()
            print(f"   ✅ Cargados: {cargados}")
            print(f"   ❌ Errores: {errores}")
            
            cargas_por_tipo[config['tipo_reportes']] = cargados
            total_cargados += cargados
            total_errores += errores
        
        # Registrar en historial
        historial = HistorialCarga(
            fecha_carga=datetime.now(),
            nombre_archivo="EPM - Solicitudes, Incidentes y Tareas",
            cantidad_registros=total_cargados,
            registros_procesados=total_cargados,
            registros_error=total_errores,
            estado="exitoso"
        )
        db.session.add(historial)
        db.session.commit()
        
        # Resumen
        print("\n" + "=" * 60)
        print("RESUMEN DE CARGA")
        print("=" * 60)
        
        for tipo, cantidad in cargas_por_tipo.items():
            print(f"  {tipo}: {cantidad:,} registros")
        
        print(f"\n  Total en BD: {total_cargados:,}")
        print(f"  Errores: {total_errores}")
        
        # Verificar tipos en BD
        print("\n📋 Tipos en base de datos:")
        tipos_bd = db.session.query(db.func.distinct(Reporte.tipo)).all()
        for tipo in tipos_bd:
            count = db.session.query(Reporte).filter_by(tipo=tipo[0]).count()
            print(f"   - {tipo[0]}: {count:,} registros")
        
        print("\n✅ CARGA COMPLETADA EXITOSAMENTE")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
