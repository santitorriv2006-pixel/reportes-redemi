#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Carga reportes con datos correctos: usuarios, grupos, horas, etc.
Combina datos de Reportes_Convertidos.xlsx con tipos del EPM
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from app.models import db, Reporte, HistorialCarga
import pandas as pd
from datetime import datetime

app = create_app()

with app.app_context():
    print("=" * 70)
    print("CARGANDO REPORTES CON DATOS COMPLETOS")
    print("=" * 70)
    
    # Limpiar BD
    print("\n🗑️  Limpiando reportes anteriores...")
    db.session.query(Reporte).delete()
    db.session.commit()
    print("✅ Base de datos limpia")
    
    # Leer datos originales
    print("\n📖 Leyendo Reportes_Convertidos.xlsx...")
    try:
        df_original = pd.read_excel('archivos/Reportes_Convertidos.xlsx')
        print(f"✅ Archivo leído: {len(df_original)} registros")
        print(f"   Columnas: {list(df_original.columns)}")
    except Exception as e:
        print(f"❌ Error leyendo Excel: {e}")
        sys.exit(1)
    
    # Leer tipos del EPM
    print("\n📖 Leyendo tipos del EPM...")
    tipos_dict = {}
    
    try:
        excel = pd.ExcelFile('archivos/epm.xlsx')
        
        sheets_tipos = {
            "1-Solicitudes": "Solicitud",
            "2-Incidentes": "Incidente", 
            "3-Tareas": "Tarea"
        }
        
        for sheet_name, tipo_nombre in sheets_tipos.items():
            if sheet_name in excel.sheet_names:
                df = pd.read_excel('archivos/EPM - Solicitudes, Incidentes y Tareas Preview (32).xlsx', 
                                  sheet_name=sheet_name)
                
                # Extraer WOs por tipo
                if "Work Order ID" in df.columns:
                    wolist = df['Work Order ID'].dropna().unique()
                    for wo in wolist:
                        tipos_dict[str(wo)] = tipo_nombre
                elif "Numero" in df.columns:
                    wolist = df['Numero'].dropna().unique()
                    for wo in wolist:
                        tipos_dict[str(wo)] = tipo_nombre
                
                print(f"✅ {tipo_nombre}: {len(df)} registros mapeados")
    except Exception as e:
        print(f"⚠️  No se pudieron leer tipos: {e}")
    
    # Cargar reportes
    print("\n📊 Cargando reportes...")
    total_cargados = 0
    total_errores = 0
    
    for idx, row in df_original.iterrows():
        try:
            wo = str(row['WO']).strip()
            
            # Obtener tipo del diccionario, si no existe usar Solicitud por defecto
            tipo = tipos_dict.get(wo, 'Solicitud')
            
            # Convertir fecha
            try:
                fecha = pd.to_datetime(row['Fecha']).date()
            except:
                fecha = datetime.now().date()
            
            # Crear reporte con datos originales
            reporte = Reporte(
                wo=wo,
                usuario_asignado=str(row['Usuario Asignado']).strip(),
                fecha=fecha,
                horas_aprobadas=float(row['Horas Aprobadas']) if pd.notna(row['Horas Aprobadas']) else 0.0,
                horas_reales=float(row['Horas Reales']) if pd.notna(row['Horas Reales']) else 0.0,
                grupo=str(row['Grupo']).strip() if pd.notna(row['Grupo']) else "General",
                status=str(row['Status']).strip() if pd.notna(row['Status']) else "Pendiente",
                tipo=tipo
            )
            
            db.session.add(reporte)
            total_cargados += 1
            
            if (idx + 1) % 5000 == 0:
                print(f"   Procesados: {idx + 1}/{len(df_original)}")
                db.session.commit()
        
        except Exception as e:
            total_errores += 1
            if total_errores <= 3:
                print(f"   ⚠️  Error fila {idx}: {str(e)[:60]}")
    
    # Guardar cambios finales
    db.session.commit()
    
    # Registrar en historial
    historial = HistorialCarga(
        fecha_carga=datetime.now(),
        nombre_archivo="Reportes_Convertidos.xlsx + EPM tipos",
        cantidad_registros=total_cargados,
        registros_procesados=total_cargados,
        registros_error=total_errores,
        estado="exitoso"
    )
    db.session.add(historial)
    db.session.commit()
    
    # Resumen
    print("\n" + "=" * 70)
    print("RESUMEN DE CARGA")
    print("=" * 70)
    print(f"  Total cargados: {total_cargados:,}")
    print(f"  Errores: {total_errores}")
    
    # Estadísticas
    print("\n📊 ESTADÍSTICAS:")
    
    # Usuarios únicos
    usuarios = db.session.query(db.func.count(db.func.distinct(Reporte.usuario_asignado))).scalar()
    print(f"  Usuarios únicos: {usuarios}")
    
    # Grupos únicos
    grupos = db.session.query(db.func.count(db.func.distinct(Reporte.grupo))).scalar()
    print(f"  Grupos únicos: {grupos}")
    
    # Tipos
    tipos = db.session.query(db.func.distinct(Reporte.tipo)).all()
    print(f"  Tipos de reportes:")
    for tipo in tipos:
        count = db.session.query(Reporte).filter_by(tipo=tipo[0]).count()
        print(f"    - {tipo[0]}: {count:,}")
    
    # Distribuición por grupo
    print(f"\n  Top 5 grupos:")
    grupos_stats = db.session.query(
        Reporte.grupo, 
        db.func.count(Reporte.id).label('cantidad')
    ).group_by(Reporte.grupo).order_by(db.func.count(Reporte.id).desc()).limit(5).all()
    
    for grupo, cantidad in grupos_stats:
        print(f"    - {grupo}: {cantidad:,}")
    
    # Distribuición por usuario (top 5)
    print(f"\n  Top 5 usuarios:")
    usuarios_stats = db.session.query(
        Reporte.usuario_asignado, 
        db.func.count(Reporte.id).label('cantidad')
    ).group_by(Reporte.usuario_asignado).order_by(db.func.count(Reporte.id).desc()).limit(5).all()
    
    for usuario, cantidad in usuarios_stats:
        print(f"    - {usuario}: {cantidad:,}")
    
    print("\n✅ CARGA COMPLETADA EXITOSAMENTE")
