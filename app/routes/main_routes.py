from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from app import db
from app.models import Reporte
from logger_config import logger_db
from config import Config
from datetime import datetime
from sqlalchemy import func

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Página principal"""
    return render_template('index.html')


@main_bp.route('/reportes', methods=['GET'])
@login_required
def reportes():
    """
    Endpoint para obtener reportes con filtros dinámicos
    Si es una solicitud desde navegador, renderiza el template HTML
    Si es AJAX, retorna JSON
    """
    # Si no es AJAX, renderizar template
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            # Pre-cargar datos iniciales para mejorar UX
            usuarios = db.session.query(Reporte.usuario_asignado).distinct().order_by(Reporte.usuario_asignado).limit(500).all()
            grupos = db.session.query(Reporte.grupo).distinct().order_by(Reporte.grupo).limit(200).all()
            status_list = db.session.query(Reporte.status).distinct().order_by(Reporte.status).limit(50).all()
            tipos_list = db.session.query(Reporte.tipo).distinct().order_by(Reporte.tipo).limit(50).all()
            total_reportes = Reporte.query.count()
            
            return render_template('reportes.html', 
                                 pre_total_reportes=total_reportes,
                                 usuarios_precargados=[u[0] for u in usuarios if u[0]],
                                 grupos_precargados=[g[0] for g in grupos if g[0]])
        except Exception as e:
            logger_db.error(f"Error precargando datos: {str(e)}")
            return render_template('reportes.html')
    
    # Si es AJAX, retornar JSON
    try:
        import time
        inicio = time.time()
        
        # Obtener parámetros
        usuario = request.args.get('usuario', '').strip()
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        grupo = request.args.get('grupo', '').strip()
        status = request.args.get('status', '').strip()
        tipo = request.args.get('tipo', '').strip()
        page = request.args.get('page', 1, type=int)
        search = request.args.get('search', '').strip()
        
        # Obtener items por página del cliente, o usar por defecto
        try:
            per_page = int(request.args.get('per_page', Config.ITEMS_PER_PAGE))
            # Validar que esté en rango sensato
            if per_page < 5 or per_page > 500:
                per_page = Config.ITEMS_PER_PAGE
        except:
            per_page = Config.ITEMS_PER_PAGE
        
        # Construir query base (optimizado: solo traer columnas necesarias)
        query = Reporte.query
        
        # Aplicar filtros
        if usuario:
            query = query.filter_by(usuario_asignado=usuario)
        elif search:
            # Búsqueda parcial, case insensitive
            query = query.filter(
                Reporte.usuario_asignado.ilike(f'%{search}%')
            )
        
        if fecha_inicio:
            try:
                fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
                query = query.filter(Reporte.fecha >= fecha_inicio)
            except:
                pass
        
        if fecha_fin:
            try:
                fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
                query = query.filter(Reporte.fecha <= fecha_fin)
            except:
                pass
        
        if grupo:
            query = query.filter_by(grupo=grupo)
        
        if status:
            query = query.filter_by(status=status)
        
        if tipo:
            query = query.filter_by(tipo=tipo)
        
        # Contar total antes de paginar
        total_registros = query.count()
        
        # Calcular totales de TODOS los registros (no solo de la página)
        try:
            resultado = query.with_entities(
                func.sum(Reporte.horas_aprobadas).label('total_aprobadas'),
                func.sum(Reporte.horas_reales).label('total_reales'),
                func.count(Reporte.wo).label('total_wo')
            ).first()
        except:
            resultado = None
        
        if resultado:
            totales = {
                'total_aprobadas': float(resultado.total_aprobadas) if resultado.total_aprobadas else 0,
                'total_reales': float(resultado.total_reales) if resultado.total_reales else 0,
                'total_wo': resultado.total_wo if resultado.total_wo else 0,
                'diferencia': round(
                    (float(resultado.total_reales) if resultado.total_reales else 0) - 
                    (float(resultado.total_aprobadas) if resultado.total_aprobadas else 0),
                    2
                )
            }
        else:
            totales = {
                'total_aprobadas': 0,
                'total_reales': 0,
                'total_wo': 0,
                'diferencia': 0
            }
        
        # Paginar resultados DESPUÉS de calcular totales
        reportes_pagina = query.order_by(
            Reporte.usuario_asignado,
            Reporte.fecha.desc()
        ).paginate(page=page, per_page=per_page)
        
        return jsonify({
            'success': True,
            'reportes': [reporte.to_dict() for reporte in reportes_pagina.items],
            'totales': totales,
            'paginacion': {
                'total_registros': reportes_pagina.total,
                'total_paginas': reportes_pagina.pages,
                'pagina_actual': page,
                'items_por_pagina': per_page
            },
            'filtros_aplicados': {
                'usuario': usuario,
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
                'grupo': grupo,
                'status': status,
                'busqueda': search
            },
            'tiempo_ejecucion': f"{(time.time() - inicio):.2f}s"
        }), 200
        
    except Exception as e:
        logger_db.error(f"Error obteniendo reportes: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@main_bp.route('/usuarios', methods=['GET'])
def get_usuarios():
    """
    Endpoint para obtener lista de usuarios únicos
    """
    try:
        usuarios = db.session.query(
            Reporte.usuario_asignado
        ).distinct().order_by(
            Reporte.usuario_asignado
        ).limit(500).all()
        
        lista_usuarios = [usuario[0] for usuario in usuarios if usuario[0]]
        
        return jsonify({
            'success': True,
            'usuarios': lista_usuarios,
            'total': len(lista_usuarios)
        }), 200
        
    except Exception as e:
        logger_db.error(f"Error obteniendo usuarios: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@main_bp.route('/filtros-combinados', methods=['GET'])
def get_filtros_combinados():
    """
    Endpoint para obtener usuarios, grupos, status y tipos de una sola vez
    """
    try:
        usuarios = db.session.query(
            Reporte.usuario_asignado
        ).distinct().order_by(
            Reporte.usuario_asignado
        ).limit(500).all()
        
        grupos = db.session.query(
            Reporte.grupo
        ).distinct().order_by(
            Reporte.grupo
        ).limit(200).all()
        
        status_list = db.session.query(
            Reporte.status
        ).distinct().order_by(
            Reporte.status
        ).limit(50).all()
        
        tipos_list = db.session.query(
            Reporte.tipo
        ).distinct().order_by(
            Reporte.tipo
        ).limit(50).all()
        
        lista_usuarios = [usuario[0] for usuario in usuarios if usuario[0]]
        lista_grupos = [grupo[0] for grupo in grupos if grupo[0]]
        lista_status = [status[0] for status in status_list if status[0]]
        lista_tipos = [tipo[0] for tipo in tipos_list if tipo[0]]
        
        return jsonify({
            'success': True,
            'usuarios': lista_usuarios,
            'grupos': lista_grupos,
            'status': lista_status,
            'tipos': lista_tipos,
            'total': {
                'usuarios': len(lista_usuarios),
                'grupos': len(lista_grupos),
                'status': len(lista_status),
                'tipos': len(lista_tipos)
            }
        }), 200
        
    except Exception as e:
        logger_db.error(f"Error obteniendo filtros combinados: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@main_bp.route('/grupos', methods=['GET'])
def get_grupos():
    """
    Endpoint para obtener lista de grupos únicos
    """
    try:
        grupos = db.session.query(
            Reporte.grupo
        ).distinct().order_by(
            Reporte.grupo
        ).limit(200).all()
        
        lista_grupos = [grupo[0] for grupo in grupos if grupo[0]]
        
        return jsonify({
            'success': True,
            'grupos': lista_grupos,
            'total': len(lista_grupos)
        }), 200
        
    except Exception as e:
        logger_db.error(f"Error obteniendo grupos: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@main_bp.route('/status', methods=['GET'])
def get_status():
    """
    Endpoint para obtener lista de status únicos
    """
    try:
        status_list = db.session.query(
            Reporte.status
        ).distinct().order_by(
            Reporte.status
        ).limit(50).all()
        
        lista_status = [status[0] for status in status_list if status[0]]
        
        return jsonify({
            'success': True,
            'status': lista_status,
            'total': len(lista_status)
        }), 200
        
    except Exception as e:
        logger_db.error(f"Error obteniendo status: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@main_bp.route('/estadisticas', methods=['GET'])
def estadisticas():
    """
    Endpoint para obtener estadísticas generales
    """
    try:
        # Totales generales
        resultado = Reporte.query.with_entities(
            func.count(Reporte.id).label('total_registros'),
            func.count(func.distinct(Reporte.usuario_asignado)).label('usuarios'),
            func.count(func.distinct(Reporte.grupo)).label('grupos'),
            func.sum(Reporte.horas_aprobadas).label('total_aprobadas'),
            func.sum(Reporte.horas_reales).label('total_reales')
        ).first()
        
        return jsonify({
            'success': True,
            'estadisticas': {
                'total_registros': resultado.total_registros or 0,
                'usuarios_unicos': resultado.usuarios or 0,
                'grupos_unicos': resultado.grupos or 0,
                'total_horas_aprobadas': float(resultado.total_aprobadas) if resultado.total_aprobadas else 0,
                'total_horas_reales': float(resultado.total_reales) if resultado.total_reales else 0
            }
        }), 200
        
    except Exception as e:
        logger_db.error(f"Error obteniendo estadísticas: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@main_bp.route('/email/reporte-usuario', methods=['POST', 'OPTIONS'])
def email_reporte_usuario():
    """
    Envía el reporte de un usuario por correo
    """
    # Manejar CORS preflight requests
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        from app.services.email_service import EmailService
        from app.services.export_service import ExportService
        
        # Debug: Log para ver qué recibe el servidor
        logger_db.info(f"[DEBUG] Content-Type: {request.content_type}")
        logger_db.info(f"[DEBUG] request.form: {dict(request.form)}")
        logger_db.info(f"[DEBUG] request.data: {request.data}")
        
        # Aceptar FormData
        usuario = request.form.get('usuario', '').strip()
        email_destino = request.form.get('email', '').strip()
        fecha_inicio = request.form.get('fecha_inicio')
        fecha_fin = request.form.get('fecha_fin')
        grupo = request.form.get('grupo', '').strip()
        status = request.form.get('status', '').strip()
        tipo = request.form.get('tipo', '').strip()
        
        logger_db.info(f"[EMAIL] Usuario: {usuario}, Email: {email_destino}")
        
        if not usuario:
            logger_db.warning("❌ Error: Usuario no proporcionado")
            return jsonify({'success': False, 'message': 'Usuario requerido'}), 400
        
        if not email_destino:
            logger_db.warning("❌ Error: Email no proporcionado")
            return jsonify({'success': False, 'message': 'Correo requerido'}), 400
        
        # Construir query con los mismos filtros que en /reportes
        query = Reporte.query.filter_by(usuario_asignado=usuario)
        
        if fecha_inicio:
            try:
                fecha_inicio_obj = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
                query = query.filter(Reporte.fecha >= fecha_inicio_obj)
            except Exception as e:
                logger_db.warning(f"Error parseando fecha_inicio: {e}")
                pass
        
        if fecha_fin:
            try:
                fecha_fin_obj = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
                query = query.filter(Reporte.fecha <= fecha_fin_obj)
            except Exception as e:
                logger_db.warning(f"Error parseando fecha_fin: {e}")
                pass
        
        if grupo:
            query = query.filter_by(grupo=grupo)
        
        if status:
            query = query.filter_by(status=status)
        
        if tipo:
            query = query.filter_by(tipo=tipo)
        
        # Obtener los datos
        reportes = query.order_by(Reporte.fecha.desc()).all()
        logger_db.info(f"[REPORTES] Reportes encontrados para {usuario}: {len(reportes)}")
        
        if not reportes:
            logger_db.warning(f"No hay reportes para el usuario: {usuario}")
            return jsonify({'success': False, 'message': 'No hay reportes para este usuario'}), 404
        
        # Generar Excel
        logger_db.info(f"[EXCEL] Generando Excel para {len(reportes)} reportes...")
        excel_data = ExportService.generar_excel_reporte(reportes, usuario)
        logger_db.info(f"[OK] Excel generado correctamente")
        
        # Sanitizar usuario para HTML (remover caracteres especiales para el nombre de archivo)
        usuario_sanitizado = usuario.encode('ascii', errors='ignore').decode('ascii').replace('/', '_').replace('\\', '_')
        
        # Enviar correo con adjunto - HTML profesional
        fecha_generacion = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    margin: 0;
                    padding: 0;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    background-color: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    overflow: hidden;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 28px;
                    font-weight: 600;
                }}
                .header p {{
                    margin: 10px 0 0 0;
                    opacity: 0.9;
                    font-size: 14px;
                }}
                .content {{
                    padding: 30px;
                }}
                .user-info {{
                    background-color: #f8f9fa;
                    border-left: 4px solid #667eea;
                    padding: 15px;
                    margin-bottom: 20px;
                    border-radius: 4px;
                }}
                .user-info strong {{
                    color: #667eea;
                    display: block;
                    font-size: 12px;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    margin-bottom: 5px;
                }}
                .user-info p {{
                    margin: 0;
                    font-size: 16px;
                    color: #333;
                }}
                .stats {{
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 15px;
                    margin: 20px 0;
                }}
                .stat-box {{
                    background-color: #f8f9fa;
                    padding: 15px;
                    border-radius: 6px;
                    text-align: center;
                }}
                .stat-box .number {{
                    font-size: 24px;
                    font-weight: 700;
                    color: #667eea;
                    margin-bottom: 5px;
                }}
                .stat-box .label {{
                    font-size: 12px;
                    color: #666;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }}
                .message {{
                    background-color: #e8f4f8;
                    border-left: 4px solid #17a2b8;
                    padding: 15px;
                    border-radius: 4px;
                    margin: 20px 0;
                    color: #0c5460;
                }}
                .footer {{
                    background-color: #f8f9fa;
                    padding: 20px;
                    text-align: center;
                    border-top: 1px solid #dee2e6;
                    font-size: 12px;
                    color: #666;
                }}
                .footer p {{
                    margin: 5px 0;
                }}
                .attachment-notice {{
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    margin: 15px 0;
                    padding: 10px;
                    background-color: #d4edda;
                    border-left: 4px solid #28a745;
                    border-radius: 4px;
                    color: #155724;
                    font-size: 14px;
                }}
                .attachment-notice::before {{
                    content: "📎";
                    font-size: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📊 Reporte de Horas</h1>
                    <p>Sistema REDEMI de Reportes</p>
                </div>
                
                <div class="content">
                    <div class="user-info">
                        <strong>👤 Reporte de Usuario</strong>
                        <p>{usuario}</p>
                    </div>
                    
                    <p>Tu reporte ha sido generado exitosamente. Se adjunta el archivo Excel con todos los datos solicitados.</p>
                    
                    <div class="message">
                        <strong>✓ Información del reporte:</strong>
                        <p style="margin: 10px 0 0 0;">Se incluyen todos los registros con los filtros aplicados ordenados por fecha.</p>
                    </div>
                    
                    <div class="stats">
                        <div class="stat-box">
                            <div class="number">{len(reportes)}</div>
                            <div class="label">Registros</div>
                        </div>
                        <div class="stat-box">
                            <div class="number">✓</div>
                            <div class="label">Completado</div>
                        </div>
                    </div>
                    
                    <div class="attachment-notice">
                        Archivo adjunto: reporte_usuario.xlsx
                    </div>
                    
                    <p style="margin-top: 20px; color: #666; font-size: 13px;">
                        <strong>Fecha de generación:</strong> {fecha_generacion}
                    </p>
                </div>
                
                <div class="footer">
                    <p><strong>Sistema REDEMI de Reportes</strong></p>
                    <p>Este es un correo automático. Por favor no responder a esta dirección.</p>
                    <p>© 2026 - Todos los derechos reservados</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        email_enviado = EmailService.send_email(
            subject="Reporte de Horas",
            body=html_body,
            recipients=[email_destino],
            attachment_filename=f"reporte_usuario.xlsx",
            attachment_data=excel_data
        )
        
        if email_enviado:
            logger_db.info(f"[SUCCESS] Correo enviado exitosamente a {email_destino} para usuario {usuario}")
            return jsonify({
                'success': True,
                'message': f'Reporte enviado exitosamente a {email_destino}'
            }), 200
        else:
            logger_db.error(f"[ERROR] No se pudo enviar correo a {email_destino} para usuario {usuario}")
            return jsonify({
                'success': False,
                'message': f'No se pudo enviar el correo a {email_destino}. Verifica que el correo sea válido.'
            }), 400
        
    except Exception as e:
        logger_db.error(f"❌ Error enviando reporte por correo: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@main_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """
    Renderiza la página del dashboard
    """
    return render_template('dashboard.html')
