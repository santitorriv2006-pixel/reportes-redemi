import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    """Configuración base de la aplicación"""
    
    # Flask
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Base de Datos
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///reportes.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv(
        'SQLALCHEMY_TRACK_MODIFICATIONS',
        False
    )
    
    # Carga de Archivos
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 50000000))  # 50MB
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads/')
    ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_EXTENSIONS', 'xlsx').split(','))
    
    # Correo
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', True)
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@empresa.com')
    MAIL_RECIPIENTS = os.getenv(
        'MAIL_RECIPIENTS',
        'admin@empresa.com'
    ).split(',')
    MAIL_SUPPRESS_SEND = False  # Permitir envío en producción
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')
    
    # Paginación
    ITEMS_PER_PAGE = 20


class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    TESTING = False
    DEBUG = True
    MAIL_SUPPRESS_SEND = False  # Enviar correos reales en desarrollo


class ProductionConfig(Config):
    """Configuración para producción"""
    TESTING = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://user:password@localhost/reportes'
    )


class TestingConfig(Config):
    """Configuración para testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
