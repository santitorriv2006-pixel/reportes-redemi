#!/usr/bin/env python
"""
Script para cargar reportes reales sin preguntas interactivas
"""

import pandas as pd
from datetime import datetime
from app import create_app, db
from app.models import Reporte

def cargar_reportes_reales():
    """Carga reportes desde Reportes_Convertidos.xlsx directamente"""
    
    archivo = 'archivos/Reportes_Convertidos.xlsx'
    
    try:
        print(f"Leyendo {archivo}...")
        df = pd.read_excel(archivo)
        
        print(f"✓ Archivo leído: {len(df)} filas")
        
        app = create_app()
        with app.app_context():
            reportes_cargados = 0
            errores = 0
            
            for idx, row in df.iterrows():
                try:
                    # Convertir fecha
                    fecha = pd.to_datetime(row['Fecha']).date()
                    
                    reporte = Reporte(
                        wo=str(row['WO']).strip(),
                        usuario_asignado=str(row['Usuario Asignado']).strip(),
                        fecha=fecha,
                        horas_aprobadas=float(row['Horas Aprobadas']),
                        horas_reales=float(row['Horas Reales']),
                        grupo=str(row['Grupo']).strip(),
                        status=str(row['Status']).strip() if 'Status' in row else 'Pending',
                        tipo='Solicitud',
                        fecha_carga=datetime.utcnow()
                    )
                    db.session.add(reporte)
                    reportes_cargados += 1
                    
                except Exception as e:
                    print(f"⚠️ Error fila {idx + 1}: {str(e)}")
                    errores += 1
                    continue
            
            # Guardar
            try:
                db.session.commit()
                print(f"\n✅ Carga completada:")
                print(f"   ✓ Reportes cargados: {reportes_cargados}")
                print(f"   ✗ Errores: {errores}")
                print(f"   📊 Total en BD: {Reporte.query.count()}")
                
            except Exception as e:
                db.session.rollback()
                print(f"❌ Error al guardar: {str(e)}")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == '__main__':
    cargar_reportes_reales()
