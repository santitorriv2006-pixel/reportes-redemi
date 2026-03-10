# Script de inicialización con datos de ejemplo
# Ejecutar con: python init_db.py

from app import create_app, db
from app.models import Reporte
from datetime import datetime, timedelta
import random

def init_database():
    """Inicializa la base de datos con datos de ejemplo"""
    
    app = create_app()
    
    with app.app_context():
        # Eliminar tablas existentes
        db.drop_all()
        db.create_all()
        
        print("📊 Inicializando base de datos con datos de ejemplo...")
        
        # Datos de ejemplo
        usuarios = [
            'Juan Pérez', 'María García', 'Carlos López',
            'Ana Martínez', 'José Rodríguez', 'Laura Fernández',
            'Miguel Sánchez', 'Isabel Gómez', 'Antonio Ruiz',
            'Francisca Díaz'
        ]
        
        grupos = ['Desarrollo', 'QA', 'DevOps', 'Análisis', 'Diseño']
        
        # Crear reportes de ejemplo (últimos 3 meses)
        fecha_inicio = datetime.now() - timedelta(days=90)
        registros_creados = 0
        
        for dia in range(90):
            fecha = fecha_inicio + timedelta(days=dia)
            
            # 3-5 registros por día
            for _ in range(random.randint(3, 5)):
                reporte = Reporte(
                    wo=f"WO-{random.randint(1000, 9999)}",
                    usuario_asignado=random.choice(usuarios),
                    fecha=fecha.date(),
                    horas_aprobadas=round(random.uniform(4, 8), 2),
                    horas_reales=round(random.uniform(4, 10), 2),
                    grupo=random.choice(grupos),
                    fecha_carga=datetime.utcnow()
                )
                db.session.add(reporte)
                registros_creados += 1
        
        db.session.commit()
        
        print(f"✅ Base de datos inicializada correctamente")
        print(f"📈 Se crearon {registros_creados} registros de ejemplo")
        print(f"👥 Usuarios: {', '.join(usuarios)}")
        print(f"🏢 Grupos: {', '.join(grupos)}")

if __name__ == '__main__':
    init_database()
