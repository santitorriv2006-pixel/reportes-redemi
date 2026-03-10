#!/usr/bin/env python
"""
Archivo principal para ejecutar la aplicación Flask
"""

import os
import sys
from dotenv import load_dotenv
from logger_config import setup_logging
from app import create_app, db

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logger = setup_logging()

# Crear aplicación
app = create_app()

# 🔹 Crear base de datos automáticamente
with app.app_context():
    db.create_all()


def main():
    """Función principal"""

    # Obtener configuración
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'

    logger.info(f"Iniciando aplicación en {host}:{port}")
    logger.info(f"Modo debug: {debug}")

    # Crear directorios necesarios
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('logs', exist_ok=True)

    try:
        app.run(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        logger.info("Aplicación cerrada por usuario")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error al ejecutar aplicación: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()