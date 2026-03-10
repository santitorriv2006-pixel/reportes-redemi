#!/usr/bin/env python
"""
Script para cargar datos de prueba en la base de datos
Esto permite verificar que los reportes se muestran correctamente
"""

from datetime import datetime, timedelta
from app import create_app, db
from app.models import Reporte
import random

def cargar_datos_prueba():
    """Carga reportes de prueba en la BD"""
    
    app = create_app()
    
    with app.app_context():
        # Verificar si ya hay datos
        if Reporte.query.count() > 0:
            print(f"✓ La BD ya tiene {Reporte.query.count()} reportes")
            return
        
        # Datos de ejemplo
        usuarios = ['Santiago Torres', 'Juan Pérez', 'María García', 'Carlos López', 'Ana Martínez']
        grupos = ['GRUPO A', 'GRUPO B', 'GRUPO C', 'SOPORTE', 'DESARROLLO']
        status_opciones = ['Pending', 'In Progress', 'Completed', 'Closed']
        tipos = ['Solicitud', 'Incidente', 'Tarea']
        
        # Generar 50 reportes de prueba
        reportes = []
        fecha_base = datetime.now().date()
        
        for i in range(1, 51):
            reporte = Reporte(
                wo=f'WO-2026-{i:04d}',
                usuario_asignado=random.choice(usuarios),
                fecha=fecha_base - timedelta(days=random.randint(0, 30)),
                horas_aprobadas=round(random.uniform(4, 8), 2),
                horas_reales=round(random.uniform(3.5, 9), 2),
                grupo=random.choice(grupos),
                status=random.choice(status_opciones),
                tipo=random.choice(tipos),
                fecha_carga=datetime.utcnow()
            )
            reportes.append(reporte)
        
        # Guardar en BD
        try:
            db.session.bulk_save_objects(reportes)
            db.session.commit()
            print(f"✅ Se cargaron {len(reportes)} reportes de prueba")
            
            # Mostrar resumen
            total = Reporte.query.count()
            usuarios_unicos = db.session.query(
                Reporte.usuario_asignado
            ).distinct().count()
            
            print(f"📊 Total reportes: {total}")
            print(f"👥 Usuarios únicos: {usuarios_unicos}")
            print("\n✓ Los reportes ya deberían aparecer!")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error al cargar datos: {str(e)}")

if __name__ == '__main__':
    print("Cargando datos de prueba...")
    cargar_datos_prueba()
