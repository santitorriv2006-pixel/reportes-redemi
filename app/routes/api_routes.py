from flask import Blueprint, request, jsonify
from app import db
from app.models import Reporte
from logger_config import logger_db
from datetime import datetime
from sqlalchemy import func

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/dashboard/usuario/<usuario>', methods=['GET'])
def dashboard_usuario(usuario):
    """
    Endpoint para obtener datos del dashboard de un usuario específico
    
    Retorna:
    - Horas aprobadas por mes
    - Horas por grupo
    - Comparación horas aprobadas vs reales
    """
    try:
        # Filtros opcionales
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        grupo = request.args.get('grupo')
        status = request.args.get('status')
        tipo = request.args.get('tipo')
        
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
        
        # Query base
        query = Reporte.query.filter_by(usuario_asignado=usuario)
        
        if fecha_inicio:
            query = query.filter(Reporte.fecha >= fecha_inicio)
        if fecha_fin:
            query = query.filter(Reporte.fecha <= fecha_fin)
        if grupo:
            query = query.filter_by(grupo=grupo)
        if status:
            query = query.filter_by(status=status)
        if tipo:
            query = query.filter_by(tipo=tipo)
        
        reportes = query.all()
        
        if not reportes:
            return jsonify({
                'success': True,
                'data': {
                    'horas_por_mes': [],
                    'horas_por_grupo': [],
                    'comparacion_horas': {}
                }
            }), 200
        
        # Horas por mes
        horas_por_mes = {}
        for reporte in reportes:
            mes = reporte.fecha.strftime('%Y-%m')
            if mes not in horas_por_mes:
                horas_por_mes[mes] = {
                    'aprobadas': 0,
                    'reales': 0
                }
            horas_por_mes[mes]['aprobadas'] += reporte.horas_aprobadas
            horas_por_mes[mes]['reales'] += reporte.horas_reales
        
        # Horas por grupo
        horas_por_grupo = {}
        for reporte in reportes:
            grupo_name = reporte.grupo
            if grupo_name not in horas_por_grupo:
                horas_por_grupo[grupo_name] = {
                    'aprobadas': 0,
                    'reales': 0
                }
            horas_por_grupo[grupo_name]['aprobadas'] += reporte.horas_aprobadas
            horas_por_grupo[grupo_name]['reales'] += reporte.horas_reales
        
        # Totales generales
        total_aprobadas = sum(r.horas_aprobadas for r in reportes)
        total_reales = sum(r.horas_reales for r in reportes)
        
        return jsonify({
            'success': True,
            'usuario': usuario,
            'data': {
                'horas_por_mes': [
                    {'mes': mes, **datos}
                    for mes, datos in sorted(horas_por_mes.items())
                ],
                'horas_por_grupo': [
                    {'grupo': grupo, **datos}
                    for grupo, datos in sorted(horas_por_grupo.items())
                ],
                'comparacion_horas': {
                    'aprobadas': round(total_aprobadas, 2),
                    'reales': round(total_reales, 2),
                    'diferencia': round(total_reales - total_aprobadas, 2)
                }
            }
        }), 200
        
    except Exception as e:
        logger_db.error(f"Error en dashboard usuario: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@api_bp.route('/dashboard/global', methods=['GET'])
def dashboard_global():
    """
    Endpoint para obtener datos del dashboard global
    
    Retorna:
    - Top usuarios por horas aprobadas
    - Horas totales por grupo
    - Total horas por mes
    """
    try:
        # Filtros opcionales
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        grupo = request.args.get('grupo')
        status = request.args.get('status')
        tipo = request.args.get('tipo')
        
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
        
        # Query base
        query = Reporte.query
        
        if fecha_inicio:
            query = query.filter(Reporte.fecha >= fecha_inicio)
        if fecha_fin:
            query = query.filter(Reporte.fecha <= fecha_fin)
        if grupo:
            query = query.filter_by(grupo=grupo)
        if status:
            query = query.filter_by(status=status)
        if tipo:
            query = query.filter_by(tipo=tipo)
        
        reportes = query.all()
        
        if not reportes:
            return jsonify({
                'success': True,
                'data': {
                    'top_usuarios': [],
                    'horas_por_grupo': [],
                    'horas_por_mes': {}
                }
            }), 200
        
        # Top usuarios
        usuarios_totales = {}
        for reporte in reportes:
            usuario = reporte.usuario_asignado
            if usuario not in usuarios_totales:
                usuarios_totales[usuario] = {
                    'aprobadas': 0,
                    'reales': 0
                }
            usuarios_totales[usuario]['aprobadas'] += reporte.horas_aprobadas
            usuarios_totales[usuario]['reales'] += reporte.horas_reales
        
        top_usuarios = sorted(
            [
                {'usuario': usuario, **datos}
                for usuario, datos in usuarios_totales.items()
            ],
            key=lambda x: x['aprobadas'],
            reverse=True
        )[:10]
        
        # Horas por grupo
        horas_por_grupo = {}
        for reporte in reportes:
            grupo = reporte.grupo
            if grupo not in horas_por_grupo:
                horas_por_grupo[grupo] = {
                    'aprobadas': 0,
                    'reales': 0
                }
            horas_por_grupo[grupo]['aprobadas'] += reporte.horas_aprobadas
            horas_por_grupo[grupo]['reales'] += reporte.horas_reales
        
        # Horas por mes
        horas_por_mes = {}
        for reporte in reportes:
            mes = reporte.fecha.strftime('%Y-%m')
            if mes not in horas_por_mes:
                horas_por_mes[mes] = {
                    'aprobadas': 0,
                    'reales': 0
                }
            horas_por_mes[mes]['aprobadas'] += reporte.horas_aprobadas
            horas_por_mes[mes]['reales'] += reporte.horas_reales
        
        # Totales generales
        total_aprobadas = sum(r.horas_aprobadas for r in reportes)
        total_reales = sum(r.horas_reales for r in reportes)
        
        return jsonify({
            'success': True,
            'data': {
                'top_usuarios': top_usuarios,
                'horas_por_grupo': [
                    {'grupo': grupo, **datos}
                    for grupo, datos in sorted(horas_por_grupo.items())
                ],
                'horas_por_mes': [
                    {'mes': mes, **datos}
                    for mes, datos in sorted(horas_por_mes.items())
                ],
                'comparacion_horas': {
                    'aprobadas': round(total_aprobadas, 2),
                    'reales': round(total_reales, 2)
                }
            }
        }), 200
        
    except Exception as e:
        logger_db.error(f"Error en dashboard global: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
