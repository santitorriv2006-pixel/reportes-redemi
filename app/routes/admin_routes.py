from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models import Usuario, Reporte
from logger_config import logger_db
from datetime import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def require_admin(f):
    """Decorador para verificar que el usuario es administrador"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.rol != 'admin':
            flash('No tienes permiso para acceder a esta sección', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/', methods=['GET'])
@login_required
@require_admin
def dashboard():
    """Panel principal de administración"""
    try:
        # Estadísticas generales
        total_usuarios = Usuario.query.count()
        usuarios_activos = Usuario.query.filter_by(activo=True).count()
        total_reportes = Reporte.query.count()
        
        # Últimos usuarios registrados
        ultimos_usuarios = Usuario.query.order_by(Usuario.fecha_registro.desc()).limit(5).all()
        
        # Últimos reportes cargados
        ultimos_reportes = Reporte.query.order_by(Reporte.fecha_carga.desc()).limit(5).all()
        
        # Reportes por estado
        reportes_por_estado = db.session.query(
            Reporte.status,
            db.func.count(Reporte.id).label('cantidad')
        ).group_by(Reporte.status).all()
        
        stats = {
            'total_usuarios': total_usuarios,
            'usuarios_activos': usuarios_activos,
            'total_reportes': total_reportes,
            'reportes_por_estado': {estado or 'Sin estado': cantidad for estado, cantidad in reportes_por_estado}
        }
        
        logger_db.info(f"Usuario admin {current_user.email} accedió al panel de administración")
        
        return render_template('admin/dashboard.html',
                             stats=stats,
                             ultimos_usuarios=ultimos_usuarios,
                             ultimos_reportes=ultimos_reportes)
    except Exception as e:
        logger_db.error(f"Error en admin dashboard: {str(e)}")
        flash('Error al cargar el panel de administración', 'error')
        return redirect(url_for('main.index'))


@admin_bp.route('/usuarios', methods=['GET'])
@login_required
@require_admin
def usuarios():
    """Listado de usuarios"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '').strip()
        
        query = Usuario.query
        
        # Búsqueda
        if search:
            query = query.filter(
                db.or_(
                    Usuario.nombre.ilike(f'%{search}%'),
                    Usuario.email.ilike(f'%{search}%')
                )
            )
        
        # Orden
        query = query.order_by(Usuario.fecha_registro.desc())
        
        # Paginación
        paginate = query.paginate(page=page, per_page=per_page, error_out=False)
        
        logger_db.info(f"Usuario admin {current_user.email} listó usuarios")
        
        return render_template('admin/usuarios.html',
                             usuarios=paginate.items,
                             paginate=paginate,
                             search=search,
                             per_page=per_page)
    except Exception as e:
        logger_db.error(f"Error al listar usuarios: {str(e)}")
        flash('Error al cargar el listado de usuarios', 'error')
        return redirect(url_for('admin.dashboard'))


@admin_bp.route('/usuarios/<int:usuario_id>/editar', methods=['GET', 'POST'])
@login_required
@require_admin
def editar_usuario(usuario_id):
    """Editar usuario"""
    try:
        usuario = Usuario.query.get_or_404(usuario_id)
        
        if request.method == 'POST':
            nombre = request.form.get('nombre', '').strip()
            rol = request.form.get('rol', 'usuario')
            activo = request.form.get('activo') == 'on'
            
            # Validaciones
            if not nombre:
                flash('El nombre es requerido', 'error')
                return render_template('admin/editar_usuario.html', usuario=usuario)
            
            if rol not in ['usuario', 'admin']:
                flash('Rol inválido', 'error')
                return render_template('admin/editar_usuario.html', usuario=usuario)
            
            usuario.nombre = nombre
            usuario.rol = rol
            usuario.activo = activo
            
            db.session.commit()
            
            logger_db.info(f"Usuario admin {current_user.email} editó a {usuario.email}")
            flash('Usuario actualizado correctamente', 'success')
            return redirect(url_for('admin.usuarios'))
        
        return render_template('admin/editar_usuario.html', usuario=usuario)
    
    except Exception as e:
        db.session.rollback()
        logger_db.error(f"Error al editar usuario {usuario_id}: {str(e)}")
        flash('Error al editar el usuario', 'error')
        return redirect(url_for('admin.usuarios'))


@admin_bp.route('/usuarios/<int:usuario_id>/eliminar', methods=['POST'])
@login_required
@require_admin
def eliminar_usuario(usuario_id):
    """Eliminar usuario"""
    try:
        # No permitir que se elimine a sí mismo
        if usuario_id == current_user.id:
            flash('No puedes eliminar tu propia cuenta', 'error')
            return redirect(url_for('admin.usuarios'))
        
        usuario = Usuario.query.get_or_404(usuario_id)
        
        # Eliminar reportes del usuario
        Reporte.query.filter_by(usuario_asignado=usuario.nombre).delete()
        
        db.session.delete(usuario)
        db.session.commit()
        
        logger_db.info(f"Usuario admin {current_user.email} eliminó a {usuario.email}")
        flash(f'Usuario {usuario.email} eliminado correctamente', 'success')
    
    except Exception as e:
        db.session.rollback()
        logger_db.error(f"Error al eliminar usuario {usuario_id}: {str(e)}")
        flash('Error al eliminar el usuario', 'error')
    
    return redirect(url_for('admin.usuarios'))


@admin_bp.route('/reportes', methods=['GET'])
@login_required
@require_admin
def reportes():
    """Listado de reportes"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '').strip()
        estado = request.args.get('estado', '').strip()
        
        query = Reporte.query
        
        # Búsqueda
        if search:
            query = query.filter(
                db.or_(
                    Reporte.wo.ilike(f'%{search}%'),
                    Reporte.usuario_asignado.ilike(f'%{search}%'),
                    Reporte.grupo.ilike(f'%{search}%')
                )
            )
        
        # Filtrar por estado
        if estado:
            query = query.filter_by(status=estado)
        
        # Orden
        query = query.order_by(Reporte.fecha_carga.desc())
        
        # Paginación
        paginate = query.paginate(page=page, per_page=per_page, error_out=False)
        
        # Estados únicos
        estados = db.session.query(Reporte.status).distinct().filter(Reporte.status.isnot(None)).all()
        estados = [e[0] for e in estados if e[0]]
        
        logger_db.info(f"Usuario admin {current_user.email} listó reportes")
        
        return render_template('admin/reportes.html',
                             reportes=paginate.items,
                             paginate=paginate,
                             search=search,
                             estado=estado,
                             estados=estados,
                             per_page=per_page)
    except Exception as e:
        logger_db.error(f"Error al listar reportes: {str(e)}")
        flash('Error al cargar el listado de reportes', 'error')
        return redirect(url_for('admin.dashboard'))


@admin_bp.route('/reportes/<int:reporte_id>/editar', methods=['GET', 'POST'])
@login_required
@require_admin
def editar_reporte(reporte_id):
    """Editar reporte"""
    try:
        reporte = Reporte.query.get_or_404(reporte_id)
        
        if request.method == 'POST':
            status = request.form.get('status', '').strip()
            
            if not status:
                flash('El estado es requerido', 'error')
                return render_template('admin/editar_reporte.html', reporte=reporte)
            
            reporte.status = status
            db.session.commit()
            
            logger_db.info(f"Usuario admin {current_user.email} editó reporte {reporte.id}")
            flash('Reporte actualizado correctamente', 'success')
            return redirect(url_for('admin.reportes'))
        
        return render_template('admin/editar_reporte.html', reporte=reporte)
    
    except Exception as e:
        db.session.rollback()
        logger_db.error(f"Error al editar reporte {reporte_id}: {str(e)}")
        flash('Error al editar el reporte', 'error')
        return redirect(url_for('admin.reportes'))


@admin_bp.route('/reportes/<int:reporte_id>/eliminar', methods=['POST'])
@login_required
@require_admin
def eliminar_reporte(reporte_id):
    """Eliminar reporte"""
    try:
        reporte = Reporte.query.get_or_404(reporte_id)
        
        db.session.delete(reporte)
        db.session.commit()
        
        logger_db.info(f"Usuario admin {current_user.email} eliminó reporte {reporte_id}")
        flash('Reporte eliminado correctamente', 'success')
    
    except Exception as e:
        db.session.rollback()
        logger_db.error(f"Error al eliminar reporte {reporte_id}: {str(e)}")
        flash('Error al eliminar el reporte', 'error')
    
    return redirect(url_for('admin.reportes'))


@admin_bp.route('/api/usuarios', methods=['GET'])
@login_required
@require_admin
def api_usuarios():
    """API para obtener usuarios en formato JSON"""
    try:
        usuarios = Usuario.query.all()
        return jsonify([usuario.to_dict() for usuario in usuarios])
    except Exception as e:
        logger_db.error(f"Error en API usuarios: {str(e)}")
        return jsonify({'error': 'Error al obtener usuarios'}), 500


@admin_bp.route('/api/estadisticas', methods=['GET'])
@login_required
@require_admin
def api_estadisticas():
    """API para obtener estadísticas en tiempo real"""
    try:
        total_usuarios = Usuario.query.count()
        usuarios_activos = Usuario.query.filter_by(activo=True).count()
        total_reportes = Reporte.query.count()
        
        reportes_por_tipo = db.session.query(
            Reporte.tipo,
            db.func.count(Reporte.id).label('cantidad')
        ).group_by(Reporte.tipo).all()
        
        return jsonify({
            'total_usuarios': total_usuarios,
            'usuarios_activos': usuarios_activos,
            'total_reportes': total_reportes,
            'reportes_por_tipo': {tipo or 'Sin tipo': cantidad for tipo, cantidad in reportes_por_tipo}
        })
    except Exception as e:
        logger_db.error(f"Error en API estadísticas: {str(e)}")
        return jsonify({'error': 'Error al obtener estadísticas'}), 500
