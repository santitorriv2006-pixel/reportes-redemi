"""
Módulo de rutas de la aplicación
"""

from .main_routes import main_bp
from .upload_routes import upload_bp
from .export_routes import export_bp
from .api_routes import api_bp
from .auth_routes import auth_bp
from .admin_routes import admin_bp

__all__ = [
    'main_bp',
    'upload_bp',
    'export_bp',
    'api_bp',
    'auth_bp',
    'admin_bp'
]
