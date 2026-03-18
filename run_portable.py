#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Versión portable de run.py - Abre navegador automáticamente
"""

import os
import sys
import webbrowser
import threading
import time
from dotenv import load_dotenv
from logger_config import setup_logging
from app import create_app, db

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logger = setup_logging()

# Crear aplicación
app = create_app()

# Crear base de datos automáticamente
with app.app_context():
    db.create_all()


def abrir_navegador(host, port):
    """Abre el navegador después de que el servidor esté listo"""
    time.sleep(2)  # Esperar 2 segundos para que Flask inicie
    url = f"http://{host if host != '0.0.0.0' else 'localhost'}:{port}"
    webbrowser.open(url)
    logger.info(f"Navegador abierto en {url}")


def main():
    """Función principal"""
    
    # Obtener configuración
    host = os.getenv('FLASK_HOST', '127.0.0.1')  # localhost por defecto
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'

    logger.info(f"🚀 Iniciando Sistema de Reportes en {host}:{port}")
    logger.info(f"Modo debug: {debug}")

    # Crear directorios necesarios
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    os.makedirs('archivos', exist_ok=True)

    try:
        # Iniciar navegador en un thread separado
        thread = threading.Thread(target=abrir_navegador, args=(host, port), daemon=True)
        thread.start()
        
        print("\n" + "="*60)
        print(" 📊 SISTEMA DE GESTIÓN DE REPORTES")
        print("="*60)
        print(f"✅ Servidor iniciado")
        print(f"🌐 Accede a: http://localhost:{port}")
        print(f"❌ Presiona Ctrl+C para salir")
        print("="*60 + "\n")
        
        app.run(host=host, port=port, debug=debug)
        
    except KeyboardInterrupt:
        logger.info("Aplicación cerrada por usuario")
        print("\n✅ Aplicación cerrada")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error al ejecutar aplicación: {str(e)}")
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
