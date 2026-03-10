import logging
import logging.handlers
import os
from config import Config

def setup_logging():
    """Configura el sistema de logging de la aplicación"""
    
    # Crear directorio de logs si no existe
    if not os.path.exists(Config.LOG_FILE.rsplit('/', 1)[0]):
        os.makedirs(Config.LOG_FILE.rsplit('/', 1)[0])
    
    # Configurar logger principal
    logger = logging.getLogger('reportes_app')
    logger.setLevel(getattr(logging, Config.LOG_LEVEL))
    
    # Formato de logs
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler de archivo (con rotación)
    file_handler = logging.handlers.RotatingFileHandler(
        Config.LOG_FILE,
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setLevel(getattr(logging, Config.LOG_LEVEL))
    file_handler.setFormatter(formatter)
    
    # Handler de consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, Config.LOG_LEVEL))
    console_handler.setFormatter(formatter)
    
    # Agregar handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Loggers específicos para módulos
logger_db = logging.getLogger('reportes_app.db')
logger_excel = logging.getLogger('reportes_app.excel')
logger_email = logging.getLogger('reportes_app.email')
logger_scheduler = logging.getLogger('reportes_app.scheduler')
