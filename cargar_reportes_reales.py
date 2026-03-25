#!/usr/bin/env python
"""
Script para cargar reportes reales desde Reportes_Convertidos.xlsx
"""

import pandas as pd
from datetime import datetime
from app import create_app, db
from app.models import Reporte

def cargar_reportes_reales():
    """Carga reportes desde el archivo Reportes_Convertidos.xlsx"""
    
    archivo = 'archivos/Reportes_Convertidos.xlsx'
    
    try:
        # Leer el archivo
        print(f"Leyendo {archivo}...")
        df = pd.read_excel(archivo)
        
        # Mostrar columnas disponibles
        print(f"\n📋 Columnas encontradas:")
        for col in df.columns:
            print(f"  - {col}")
        
        # Mostrar primeras filas
        print(f"\n📊 Primeras filas:")
        print(df.head())
        
        app = create_app()
        with app.app_context():
            # Limpiar datos previos de prueba
            count_previos = Reporte.query.count()
            if count_previos > 0:
                print(f"\n⚠️  Encontrados {count_previos} reportes previos")
                valor = input("¿Eliminar datos de prueba y cargar nuevos? (s/n): ").lower()
                if valor == 's':
                    Reporte.query.delete()
                    db.session.commit()
                    print("✓ Datos de prueba eliminados")
                else:
                    print("Abortando...")
                    return
            
            # Mapear columnas del archivo a columnas de BD
            # Intenta automáticamente encontrar las columnas
            
            columnas_bd = {
                'wo': None,
                'usuario_asignado': None,
                'fecha': None,
                'horas_aprobadas': None,
                'horas_reales': None,
                'grupo': None,
                'status': 'Pending',
                'tipo': 'Solicitud'
            }
            
            # Buscar columnas automáticamente
            for col in df.columns:
                col_lower = col.lower().strip()
                if 'wo' in col_lower:
                    columnas_bd['wo'] = col
                elif 'usuario' in col_lower and 'asignado' in col_lower:
                    columnas_bd['usuario_asignado'] = col
                elif 'fecha' in col_lower:
                    columnas_bd['fecha'] = col
                elif 'aprobada' in col_lower:
                    columnas_bd['horas_aprobadas'] = col
                elif 'real' in col_lower and 'hora' in col_lower:
                    columnas_bd['horas_reales'] = col
                elif 'grupo' in col_lower:
                    columnas_bd['grupo'] = col
                elif 'status' in col_lower or 'estado' in col_lower:
                    columnas_bd['status'] = col
                elif 'tipo' in col_lower:
                    columnas_bd['tipo'] = col
            
            print(f"\n🔄 Mapeo de columnas:")
            for bd_col, excel_col in columnas_bd.items():
                print(f"  {bd_col:20} <- {excel_col}")
            
            # Validar que todas las columnas obligatorias estén presentes
            obligatorias = ['wo', 'usuario_asignado', 'fecha', 'horas_aprobadas', 'horas_reales', 'grupo']
            faltantes = [col for col in obligatorias if columnas_bd[col] is None]
            
            if faltantes:
                print(f"\n❌ Columnas faltantes: {', '.join(faltantes)}")
                print("\nPor favor verifica los nombres de las columnas en el archivo.")
                return
            
            # Cargar reportes
            reportes_cargados = 0
            errores = 0
            
            for idx, row in df.iterrows():
                try:
                    # Convertir fecha
                    fecha = pd.to_datetime(row[columnas_bd['fecha']]).date()
                    
                    # Obtener valor de status (puede ser None o una columna)
                    if columnas_bd['status'] is not None and columnas_bd['status'] in df.columns:
                        status = str(row[columnas_bd['status']]).strip()
                    else:
                        status = 'Pending'
                    
                    # Obtener valor de tipo (puede ser None o una columna)
                    if columnas_bd['tipo'] is not None and columnas_bd['tipo'] in df.columns:
                        tipo = str(row[columnas_bd['tipo']]).strip()
                    else:
                        tipo = 'Solicitud'
                    
                    reporte = Reporte(
                        wo=str(row[columnas_bd['wo']]).strip(),
                        usuario_asignado=str(row[columnas_bd['usuario_asignado']]).strip(),
                        fecha=fecha,
                        horas_aprobadas=float(row[columnas_bd['horas_aprobadas']]),
                        horas_reales=float(row[columnas_bd['horas_reales']]),
                        grupo=str(row[columnas_bd['grupo']]).strip(),
                        status=status,
                        tipo=tipo,
                        fecha_carga=datetime.utcnow()
                    )
                    db.session.add(reporte)
                    reportes_cargados += 1
                    
                except Exception as e:
                    print(f"  ⚠️  Error en fila {idx + 1}: {str(e)}")
                    errores += 1
                    continue
            
            # Guardar
            try:
                db.session.commit()
                print(f"\n✅ Carga completada:")
                print(f"   - Reportes cargados: {reportes_cargados}")
                print(f"   - Errores: {errores}")
                print(f"   - Total en BD: {Reporte.query.count()}")
                
            except Exception as e:
                db.session.rollback()
                print(f"\n❌ Error al guardar: {str(e)}")
    
    except FileNotFoundError:
        print(f"❌ Archivo no encontrado: {archivo}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == '__main__':
    cargar_reportes_reales()
