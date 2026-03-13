from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import Usuario, CodigoVerificacion
from app.services import EmailService
from datetime import datetime, timedelta
from logger_config import logger_db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    """Página de registro de nuevos usuarios"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validaciones
        if not nombre or not email or not password:
            flash('Todos los campos son requeridos', 'error')
            return render_template('auth/registro.html')
        
        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres', 'error')
            return render_template('auth/registro.html')
        
        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'error')
            return render_template('auth/registro.html')
        
        # Verificar si el email ya existe
        if Usuario.query.filter_by(email=email).first():
            flash('El email ya está registrado', 'error')
            return render_template('auth/registro.html')
        
        try:
            # Crear nuevo usuario
            usuario = Usuario(nombre=nombre, email=email)
            usuario.set_password(password)
            
            db.session.add(usuario)
            db.session.commit()
            
            logger_db.info(f'Nuevo usuario registrado: {email}')
            flash('¡Registro exitoso! Por favor inicia sesión', 'success')
            return redirect(url_for('auth.login'))
        
        except Exception as e:
            db.session.rollback()
            logger_db.error(f'Error al registrar usuario: {str(e)}')
            flash('Error al registrar. Intenta de nuevo', 'error')
            return render_template('auth/registro.html')
    
    return render_template('auth/registro.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de inicio de sesión - Envía código de verificación"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Email y contraseña son requeridos', 'error')
            return render_template('auth/login.html')
        
        try:
            # Buscar usuario
            usuario = Usuario.query.filter_by(email=email).first()
            
            if not usuario or not usuario.check_password(password):
                logger_db.warning(f'Intento de login fallido para: {email}')
                flash('Email o contraseña incorrectos', 'error')
                return render_template('auth/login.html')
            
            if not usuario.activo:
                flash('La cuenta ha sido desactivada', 'error')
                logger_db.warning(f'Intento de login con cuenta inactiva: {email}')
                return render_template('auth/login.html')
            
            # Generar código de verificación
            codigo = CodigoVerificacion.generar_codigo()
            fecha_expiracion = datetime.utcnow() + timedelta(minutes=10)
            
            # Limpiar códigos anteriores no usados
            CodigoVerificacion.query.filter_by(email=email, usado=False).delete()
            
            # Crear nuevo código
            cod_verificacion = CodigoVerificacion(
                email=email,
                codigo=codigo,
                fecha_expiracion=fecha_expiracion
            )
            
            db.session.add(cod_verificacion)
            db.session.commit()
            
            # Enviar código por email
            asunto = 'Código de Verificación - Sistema de Reportes REDEMI'
            cuerpo = f"""
            <h2>Código de Verificación</h2>
            <p>Hola {usuario.nombre},</p>
            <p>Tu código de verificación es:</p>
            <h1 style="color: #0284c7; font-size: 48px; letter-spacing: 5px;">{codigo}</h1>
            <p>Este código caduca en 10 minutos.</p>
            <p>Si no solicitaste este código, ignora este mensaje.</p>
            <hr>
            <p style="color: #666; font-size: 12px;">© 2026 Sistema de Reportes REDEMI</p>
            """
            
            EmailService.send_email(asunto, cuerpo, [email])
            
            # Guardar email en sesión para verificación
            session['email_verificacion'] = email
            session['usuario_id'] = usuario.id
            
            logger_db.info(f'Código de verificación enviado a: {email}')
            flash('Se ha enviado un código de verificación a tu email', 'info')
            return redirect(url_for('auth.verificar'))
        
        except Exception as e:
            db.session.rollback()
            logger_db.error(f'Error en login: {str(e)}')
            flash('Error al iniciar sesión. Intenta de nuevo', 'error')
            return render_template('auth/login.html')
    
    return render_template('auth/login.html')


@auth_bp.route('/verificar', methods=['GET', 'POST'])
def verificar():
    """Página para verificar el código"""
    email = session.get('email_verificacion')
    usuario_id = session.get('usuario_id')
    
    if not email or not usuario_id:
        flash('Debes iniciar sesión primero', 'error')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        codigo = request.form.get('codigo', '').strip()
        
        if not codigo:
            flash('Por favor ingresa el código', 'error')
            return render_template('auth/verificar.html', email=email)
        
        try:
            # Buscar código válido
            cod_verificacion = CodigoVerificacion.query.filter_by(
                email=email,
                codigo=codigo,
                usado=False
            ).first()
            
            if not cod_verificacion:
                cod_verificacion = CodigoVerificacion.query.filter_by(
                    email=email
                ).order_by(CodigoVerificacion.fecha_creacion.desc()).first()
                
                if cod_verificacion:
                    cod_verificacion.intentos += 1
                    db.session.commit()
                    
                    if cod_verificacion.intentos >= 3:
                        flash('Demasiados intentos fallidos. Intenta iniciar sesión de nuevo', 'error')
                        logger_db.warning(f'Demasiados intentos fallidos para: {email}')
                        session.clear()
                        return redirect(url_for('auth.login'))
                
                flash('Código inválido o expirado', 'error')
                return render_template('auth/verificar.html', email=email)
            
            if cod_verificacion.est_expirado():
                flash('El código ha expirado. Intenta iniciar sesión de nuevo', 'error')
                logger_db.warning(f'Código expirado para: {email}')
                session.clear()
                return redirect(url_for('auth.login'))
            
            # Marcar código como usado
            cod_verificacion.usado = True
            
            # Obtener usuario y actualizar último login
            usuario = Usuario.query.get(usuario_id)
            usuario.ultimo_login = datetime.utcnow()
            
            db.session.commit()
            
            # Iniciar sesión
            login_user(usuario)
            logger_db.info(f'Usuario verificado e inició sesión: {email}')
            
            # Limpiar sesión
            session.pop('email_verificacion', None)
            session.pop('usuario_id', None)
            
            flash(f'¡Bienvenido, {usuario.nombre}!', 'success')
            return redirect(url_for('main.index'))
        
        except Exception as e:
            db.session.rollback()
            logger_db.error(f'Error en verificación: {str(e)}')
            flash('Error al verificar código. Intenta de nuevo', 'error')
            return render_template('auth/verificar.html', email=email)
    
    return render_template('auth/verificar.html', email=email)


@auth_bp.route('/logout')
@login_required
def logout():
    """Cerrar sesión"""
    usuario_email = current_user.email
    logout_user()
    logger_db.info(f'Usuario cerró sesión: {usuario_email}')
    flash('Sesión cerrada correctamente', 'success')
    return redirect(url_for('auth.login'))


@auth_bp.route('/perfil')
@login_required
def perfil():
    """Página del perfil del usuario"""
    # Limpiar caché de SQLAlchemy completamente
    db.session.expunge_all()
    db.session.close()
    
    # Cargar usuario FRESH sin caché - query nueva
    usuario = Usuario.query.filter_by(id=current_user.id).first()
    if not usuario:
        logout_user()
        return redirect(url_for('auth.login'))
    
    # Debug: mostrar en logs qué rol tiene
    logger_db.info(f"Perfil accedido por {usuario.email}, rol={usuario.rol}")
    
    return render_template('auth/perfil.html', usuario=usuario)

@auth_bp.route('/actualizar-perfil', methods=['POST'])
@login_required
def actualizar_perfil():
    """Actualizar información del perfil"""
    try:
        data = request.get_json()
        nombre = data.get('nombre', '').strip()
        email = data.get('email', '').strip().lower()
        
        # Validaciones
        if not nombre:
            return jsonify({'success': False, 'message': 'El nombre es requerido'}), 400
        
        if not email:
            return jsonify({'success': False, 'message': 'El email es requerido'}), 400
        
        # Verificar si el email ya está usado por otro usuario
        usuario_existente = Usuario.query.filter(
            Usuario.email == email,
            Usuario.id != current_user.id
        ).first()
        
        if usuario_existente:
            return jsonify({'success': False, 'message': 'Este email ya está en uso'}), 400
        
        # Actualizar usuario
        current_user.nombre = nombre
        current_user.email = email
        db.session.commit()
        
        logger_db.info(f'Usuario {current_user.id} actualizó su perfil')
        
        return jsonify({'success': True, 'message': 'Perfil actualizado correctamente'})
    
    except Exception as e:
        logger_db.error(f'Error al actualizar perfil: {str(e)}')
        return jsonify({'success': False, 'message': 'Error al actualizar el perfil'}), 500


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Página para solicitar recuperación de contraseña"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        
        if not email:
            flash('Por favor ingresa tu email', 'error')
            return render_template('auth/forgot_password.html')
        
        try:
            # Buscar usuario
            usuario = Usuario.query.filter_by(email=email).first()
            
            if not usuario:
                # No revelar si el email existe o no por seguridad
                flash('Si el email existe en nuestra base de datos, recibirás un correo de recuperación', 'info')
                return render_template('auth/forgot_password.html')
            
            # Generar código de recuperación
            codigo = CodigoVerificacion.generar_codigo()
            fecha_expiracion = datetime.utcnow() + timedelta(minutes=30)
            
            # Limpiar códigos anteriores no usados
            CodigoVerificacion.query.filter_by(email=email, usado=False).delete()
            
            # Crear nuevo código para recuperación
            cod_recuperacion = CodigoVerificacion(
                email=email,
                codigo=codigo,
                fecha_expiracion=fecha_expiracion
            )
            
            db.session.add(cod_recuperacion)
            db.session.commit()
            
            # Enviar código por email
            asunto = 'Recuperar Contraseña - Sistema de Reportes REDEMI'
            cuerpo = f"""
            <h2>Recuperación de Contraseña</h2>
            <p>Hola {usuario.nombre},</p>
            <p>Hemos recibido una solicitud para recuperar tu contraseña.</p>
            <p>Tu código de recuperación es:</p>
            <h1 style="color: #0284c7; font-size: 48px; letter-spacing: 5px;">{codigo}</h1>
            <p>Este código caduca en 30 minutos.</p>
            <p><strong>Si no solicitaste esto, ignora este mensaje y tu contraseña permanecerá sin cambios.</strong></p>
            <hr>
            <p style="color: #666; font-size: 12px;">© 2026 Sistema de Reportes REDEMI</p>
            """
            
            EmailService.send_email(asunto, cuerpo, [email])
            
            # Guardar email en sesión
            session['email_recuperacion'] = email
            
            logger_db.info(f'Código de recuperación enviado a: {email}')
            flash('Se ha enviado un código de recuperación a tu email', 'info')
            return redirect(url_for('auth.reset_password'))
        
        except Exception as e:
            db.session.rollback()
            logger_db.error(f'Error en recuperación de contraseña: {str(e)}')
            flash('Error al procesar la solicitud. Intenta de nuevo', 'error')
            return render_template('auth/forgot_password.html')
    
    return render_template('auth/forgot_password.html')


@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    """Página para restablecer la contraseña"""
    email = session.get('email_recuperacion')
    
    if not email:
        flash('Debes solicitar la recuperación de contraseña primero', 'error')
        return redirect(url_for('auth.forgot_password'))
    
    if request.method == 'POST':
        codigo = request.form.get('codigo', '').strip()
        nueva_password = request.form.get('nueva_password', '')
        confirmar_password = request.form.get('confirmar_password', '')
        
        if not codigo:
            flash('Por favor ingresa el código de recuperación', 'error')
            return render_template('auth/reset_password.html', email=email)
        
        if not nueva_password or not confirmar_password:
            flash('Por favor completa todos los campos', 'error')
            return render_template('auth/reset_password.html', email=email)
        
        if len(nueva_password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres', 'error')
            return render_template('auth/reset_password.html', email=email)
        
        if nueva_password != confirmar_password:
            flash('Las contraseñas no coinciden', 'error')
            return render_template('auth/reset_password.html', email=email)
        
        try:
            # Buscar código válido
            cod_verificacion = CodigoVerificacion.query.filter_by(
                email=email,
                codigo=codigo,
                usado=False
            ).first()
            
            if not cod_verificacion:
                cod_verificacion = CodigoVerificacion.query.filter_by(
                    email=email
                ).order_by(CodigoVerificacion.fecha_creacion.desc()).first()
                
                if cod_verificacion:
                    cod_verificacion.intentos += 1
                    db.session.commit()
                    
                    if cod_verificacion.intentos >= 5:
                        flash('Demasiados intentos fallidos. Solicita un nuevo código', 'error')
                        logger_db.warning(f'Demasiados intentos fallidos para recuperación: {email}')
                        session.clear()
                        return redirect(url_for('auth.forgot_password'))
                
                flash('Código inválido o expirado', 'error')
                return render_template('auth/reset_password.html', email=email)
            
            if cod_verificacion.est_expirado():
                flash('El código ha expirado. Solicita un nuevo código', 'error')
                logger_db.warning(f'Código expirado para recuperación: {email}')
                session.clear()
                return redirect(url_for('auth.forgot_password'))
            
            # Buscar usuario y actualizar contraseña
            usuario = Usuario.query.filter_by(email=email).first()
            if not usuario:
                flash('Usuario no encontrado', 'error')
                session.clear()
                return redirect(url_for('auth.login'))
            
            # Actualizar contraseña
            usuario.set_password(nueva_password)
            cod_verificacion.usado = True
            
            db.session.commit()
            
            logger_db.info(f'Usuario {email} restableció su contraseña')
            
            # Limpiar sesión
            session.pop('email_recuperacion', None)
            
            flash('¡Contraseña actualizada correctamente! Por favor inicia sesión', 'success')
            return redirect(url_for('auth.login'))
        
        except Exception as e:
            db.session.rollback()
            logger_db.error(f'Error al restablecer contraseña: {str(e)}')
            flash('Error al restablecer la contraseña. Intenta de nuevo', 'error')
            return render_template('auth/reset_password.html', email=email)
    
    return render_template('auth/reset_password.html', email=email)