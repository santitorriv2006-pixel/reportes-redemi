from flask import Blueprint, render_template, request, jsonify, send_file
from flask_login import login_required
from app import db
from app.models import Reporte, HistorialCarga
from app.services import ExcelProcessingService, ExportService
from logger_config import logger_excel, logger_db
from config import Config
from datetime import datetime
import os

upload_bp = Blueprint('upload', __name__, url_prefix='/upload')

@upload_bp.route('/archivo', methods=['GET', 'POST'])
@login_required
def upload_archivo():
    """
    Endpoint para cargar archivos Excel
    Valida, procesa y almacena en la base de datos
    """
    
    if request.method == 'GET':
        return render_template('upload.html')
    
    try:
        # Verificar que se envió un archivo
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'message': 'No se proporcionó archivo'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'message': 'Archivo vacío'
            }), 400
        
        # Validar extensión
        if not ExcelProcessingService.allowed_file(file.filename):
            return jsonify({
                'success': False,
                'message': 'Solo se permiten archivos .xlsx'
            }), 400
        
        # Crear directorio de uploads si no existe
        if not os.path.exists(Config.UPLOAD_FOLDER):
            os.makedirs(Config.UPLOAD_FOLDER)
        
        # Guardar archivo temporalmente
        filepath = os.path.join(Config.UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        logger_excel.info(f"Archivo guardado: {filepath}")
        
        # Validar archivo
        es_valido, mensaje_error, df = ExcelProcessingService.validate_file(filepath)
        
        if not es_valido:
            logger_excel.error(f"Validación fallida: {mensaje_error}")
            os.remove(filepath)
            return jsonify({
                'success': False,
                'message': mensaje_error
            }), 400
        
        # Obtener estadísticas
        stats = ExcelProcessingService.get_file_stats(df)
        
        # Preparar registros para base de datos
        registros = ExcelProcessingService.prepare_for_database(df)
        
        # Insertar en base de datos
        registros_insertados = 0
        registros_error = 0
        
        try:
            for registro in registros:
                try:
                    nuevo_reporte = Reporte(**registro)
                    db.session.add(nuevo_reporte)
                    registros_insertados += 1
                except Exception as e:
                    logger_db.warning(f"Error insertando registro: {str(e)}")
                    registros_error += 1
                    db.session.rollback()
            
            # Commit de la transacción
            db.session.commit()
            logger_db.info(f"Se insertaron {registros_insertados} registros")
            
        except Exception as e:
            logger_db.error(f"Error en transacción: {str(e)}")
            db.session.rollback()
            os.remove(filepath)
            return jsonify({
                'success': False,
                'message': f'Error al guardar en base de datos: {str(e)}'
            }), 500
        
        # Registrar en historial de cargas
        try:
            estado = 'exitoso' if registros_error == 0 else 'parcial'
            historial = HistorialCarga(
                nombre_archivo=file.filename,
                cantidad_registros=len(registros),
                registros_procesados=registros_insertados,
                registros_error=registros_error,
                estado=estado,
                usuario_carga=request.remote_addr
            )
            db.session.add(historial)
            db.session.commit()
            logger_db.info(f"Historial de carga registrado: {estado}")
        except Exception as e:
            logger_db.warning(f"Error registrando historial: {str(e)}")
        
        # Limpiar archivo temporal
        try:
            os.remove(filepath)
        except:
            pass
        
        return jsonify({
            'success': True,
            'message': f'Archivo procesado correctamente',
            'statistics': {
                'registros_insertados': registros_insertados,
                'registros_error': registros_error,
                'total_registros': len(registros),
                **stats
            }
        }), 200
        
    except Exception as e:
        logger_excel.error(f"Error no manejado en upload: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500


@upload_bp.route('/historial', methods=['GET'])
def historial_cargas():
    """
    Endpoint para obtener historial de cargas
    """
    try:
        # Parámetros de paginación
        page = request.args.get('page', 1, type=int)
        per_page = Config.ITEMS_PER_PAGE
        
        # Consultar historial
        cargas = HistorialCarga.query.order_by(
            HistorialCarga.fecha_carga.desc()
        ).paginate(page=page, per_page=per_page)
        
        return jsonify({
            'success': True,
            'historial': [carga.to_dict() for carga in cargas.items],
            'total': cargas.total,
            'pages': cargas.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        logger_db.error(f"Error obteniendo historial: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
