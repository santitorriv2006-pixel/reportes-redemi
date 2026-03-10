from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from flask import current_app
from app import db
from app.models import Reporte
from app.services import ExportService, EmailService
from logger_config import logger_scheduler
from datetime import datetime
from sqlalchemy import func

def enviar_resumen_reportes():
    """
    Función que se ejecuta según el schedule para enviar reportes
    """
    try:
        with current_app.app_context():
            # Obtener datos resumidos
            resultado = Reporte.query.with_entities(
                Reporte.usuario_asignado,
                func.count(Reporte.wo).label('total_wo'),
                func.sum(Reporte.horas_aprobadas).label('total_aprobadas'),
                func.sum(Reporte.horas_reales).label('total_reales')
            ).group_by(Reporte.usuario_asignado).all()
            
            if not resultado:
                logger_scheduler.info("No hay reportes para enviar")
                return
            
            # Preparar datos para el correo
            reportes_por_usuario = {}
            for row in resultado:
                reportes_por_usuario[row.usuario_asignado] = {
                    'total_wo': row.total_wo,
                    'total_aprobadas': float(row.total_aprobadas),
                    'total_reales': float(row.total_reales)
                }
            
            # Generar archivo Excel global
            archivo_excel = ExportService.export_global_excel()
            
            # Enviar correo
            if EmailService.send_daily_report(reportes_por_usuario, archivo_excel):
                logger_scheduler.info("Resumen enviado exitosamente")
            else:
                logger_scheduler.warning("No se pudo enviar el resumen")
                
    except Exception as e:
        logger_scheduler.error(f"Error en resumen de reportes: {str(e)}")


def init_scheduler(app):
    """
    Inicializa el scheduler de tareas automáticas
    
    Horarios:
    - 08:00 AM: Resumen actual (global)
    - 02:00 PM: Resumen actualizado
    - 05:30 PM: Consolidado final
    """
    
    scheduler = BackgroundScheduler()
    
    # Tarea 1: 08:00 AM
    scheduler.add_job(
        func=enviar_resumen_reportes,
        trigger=CronTrigger(hour=8, minute=0),
        id='resumen_mañana',
        name='Resumen de reportes - Mañana',
        replace_existing=True,
        max_instances=1
    )
    logger_scheduler.info("Programado: 08:00 AM - Resumen matutino")
    
    # Tarea 2: 02:00 PM
    scheduler.add_job(
        func=enviar_resumen_reportes,
        trigger=CronTrigger(hour=14, minute=0),
        id='resumen_tarde',
        name='Resumen de reportes - Tarde',
        replace_existing=True,
        max_instances=1
    )
    logger_scheduler.info("Programado: 02:00 PM - Resumen vespertino")
    
    # Tarea 3: 05:30 PM
    scheduler.add_job(
        func=enviar_resumen_reportes,
        trigger=CronTrigger(hour=17, minute=30),
        id='resumen_noche',
        name='Consolidado final de reportes',
        replace_existing=True,
        max_instances=1
    )
    logger_scheduler.info("Programado: 05:30 PM - Consolidado final")
    
    scheduler.start()
    logger_scheduler.info("Scheduler iniciado correctamente")
    
    return scheduler
