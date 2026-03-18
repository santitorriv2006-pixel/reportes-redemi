from flask import Blueprint, request, jsonify, send_file
from app import db
from app.models import Reporte
from app.services import ExportService
from logger_config import logger_excel
from datetime import datetime

export_bp = Blueprint('export', __name__, url_prefix='/export')

@export_bp.route('/usuario/<usuario>', methods=['GET'])
def export_usuario(usuario):
    """
    Endpoint para descargar reportes de un usuario específico
    
    Parámetros de query:
    - fecha_inicio: Fecha inicio (YYYY-MM-DD)
    - fecha_fin: Fecha fin (YYYY-MM-DD)
    - grupo: Filtrar por grupo
    """
    try:
        # Obtener parámetros
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        grupo = request.args.get('grupo')
        
        # Convertir fechas
        if fecha_inicio:
            try:
                fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            except:
                fecha_inicio = None
        
        if fecha_fin:
            try:
                fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
            except:
                fecha_fin = None
        
        # Generar Excel
        archivo_excel = ExportService.export_usuario_excel(
            usuario=usuario,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            grupo=grupo
        )
        
        if not archivo_excel:
            return jsonify({
                'success': False,
                'message': 'No hay datos para exportar'
            }), 404
        
        filename = ExportService.get_filename_export(usuario=usuario)
        
        logger_excel.info(f"Descarga de usuario {usuario}: {filename}")
        
        return send_file(
            archivo_excel,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        logger_excel.error(f"Error exportando usuario {usuario}: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500


@export_bp.route('/global', methods=['GET'])
def export_global():
    """
    Endpoint para descargar todos los reportes
    
    Parámetros de query:
    - fecha_inicio: Fecha inicio (YYYY-MM-DD)
    - fecha_fin: Fecha fin (YYYY-MM-DD)
    - grupo: Filtrar por grupo
    """
    try:
        # Obtener parámetros
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        grupo = request.args.get('grupo')
        
        # Convertir fechas
        if fecha_inicio:
            try:
                fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            except:
                fecha_inicio = None
        
        if fecha_fin:
            try:
                fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
            except:
                fecha_fin = None
        
        # Generar Excel global
        archivo_excel = ExportService.export_global_excel(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            grupo=grupo
        )
        
        if not archivo_excel:
            return jsonify({
                'success': False,
                'message': 'No hay datos para exportar'
            }), 404
        
        filename = ExportService.get_filename_export()
        
        logger_excel.info(f"Descarga global: {filename}")
        
        return send_file(
            archivo_excel,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        logger_excel.error(f"Error exportando global: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500


@export_bp.route('/filtrado', methods=['GET'])
def export_filtrado():
    """
    Endpoint para descargar reportes con todos los filtros aplicados
    
    Parámetros de query:
    - usuario: Nombre del usuario (parcial, case-insensitive)
    - fecha_inicio: Fecha inicio (YYYY-MM-DD)
    - fecha_fin: Fecha fin (YYYY-MM-DD)
    - grupo: Filtrar por grupo
    - tipo: Filtrar por tipo
    - status: Filtrar por status
    """
    try:
        # Obtener parámetros de filtro
        usuario = request.args.get('usuario')
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        grupo = request.args.get('grupo')
        tipo = request.args.get('tipo')
        status = request.args.get('status')
        
        # Convertir fechas
        if fecha_inicio:
            try:
                fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            except:
                fecha_inicio = None
        
        if fecha_fin:
            try:
                fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
            except:
                fecha_fin = None
        
        # Validar que al menos hay un filtro
        tiene_filtro = any([usuario, fecha_inicio, fecha_fin, grupo, tipo, status])
        
        if not tiene_filtro:
            return jsonify({
                'success': False,
                'message': 'Debe especificar al menos un filtro'
            }), 400
        
        # Generar Excel con filtros
        archivo_excel = ExportService.export_filtrado_excel(
            usuario=usuario,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            grupo=grupo,
            tipo=tipo,
            status=status
        )
        
        if not archivo_excel:
            return jsonify({
                'success': False,
                'message': 'No hay datos para exportar con los filtros especificados'
            }), 404
        
        # Generar nombre de archivo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"reporte_filtrado_{timestamp}.xlsx"
        
        logger_excel.info(f"Descarga filtrada: {filename} - Usuario: {usuario}, Grupo: {grupo}, Tipo: {tipo}")
        
        return send_file(
            archivo_excel,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        logger_excel.error(f"Error exportando filtrado: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500
