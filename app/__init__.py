from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from config import config_by_name
import os

# Importar db del módulo de modelos para evitar imports circulares
from app.models import db

def create_app(config_name=None):
    """Factory function para crear la aplicación Flask"""
    
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config_by_name.get(config_name, config_by_name['default']))
    
    # Inicializar extensiones con la app
    db.init_app(app)
    
    # Inicializar Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import Usuario
        # Expirar cache antes de cargar - esto fuerza recarga desde BD
        db.session.expire_all()
        user = Usuario.query.get(int(user_id))
        return user
    
    # Invalidar sesión SQLAlchemy antes de cada request
    @app.before_request
    def clear_sqlalchemy_cache():
        """Limpiar caché de SQLAlchemy para evitar datos antiguos"""
        if current_user.is_authenticated:
            # Expulsar TODOS los objetos en caché
            db.session.expunge_all()
    
    # Importar servicios DESPUÉS de db
    from app.services import EmailService
    EmailService.init_mail(app)
    
    # Registrar blueprints
    from app.routes import main_bp, upload_bp, export_bp, api_bp, auth_bp, admin_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(export_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(admin_bp)
    
    # Registrar error handlers
    register_error_handlers(app)
    
    # Crear tablas
    with app.app_context():
        db.create_all()
    
    # Inicializar scheduler (tanto en desarrollo como producción)
    from scheduler import init_scheduler
    init_scheduler(app)
    
    return app


def register_error_handlers(app):
    """Registra manejadores de errores globales"""
    from flask import render_template
    from logger_config import setup_logging
    
    logger = setup_logging()
    
    @app.errorhandler(404)
    def not_found_error(error):
        logger.warning(f"Error 404: {error}")
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Error 500: {error}")
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(413)
    def request_entity_too_large(error):
        logger.warning(f"Error 413: Archivo demasiado grande")
        return render_template('errors/413.html'), 413
    
    return app
