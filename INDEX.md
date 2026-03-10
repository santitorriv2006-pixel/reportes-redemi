📑 ÍNDICE COMPLETO - Sistema de Reportes Empresariales

═══════════════════════════════════════════════════════════════════════════════

🚀 DOCUMENTACIÓN DISPONIBLE

═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│ PARA EMPEZAR (LEER PRIMERO)                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│ ⚡ QUICK_START.txt                                                           │
│    → Instalación en 5 minutos                                               │
│    → Primeros pasos básicos                                                 │
│    → Solución rápida de problemas                                           │
│    📍 EMPIEZA AQUÍ SI TIENES PRISA                                          │
│                                                                              │
│ 📖 README.md                                                                │
│    → Guía general completa                                                  │
│    → Requisitos del sistema                                                 │
│    → Estructura del proyecto                                                │
│    → Endpoints API                                                          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│ PARA USUARIOS FINALES                                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│ 👤 GUIA_DE_USO.md                                                           │
│    → Cómo cargar archivos                                                   │
│    → Búsqueda y filtros                                                     │
│    → Descarga de reportes                                                   │
│    → Interpretación del Dashboard                                           │
│    → Troubleshooting de usuario                                             │
│                                                                              │
│ 📊 EJEMPLO_EXCEL.md                                                         │
│    → Formato exacto del archivo Excel                                       │
│    → Columnas requeridas                                                    │
│    → Validaciones                                                           │
│    → Ejemplos correctos e incorrectos                                       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│ PARA DESARROLLADORES                                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│ 💻 TECHNICAL_DOCS.md                                                        │
│    → Arquitectura de la aplicación                                          │
│    → Patrón MVC y Factory Pattern                                           │
│    → Flujos de proceso detallados                                           │
│    → Optimización y rendimiento                                             │
│    → Seguridad y validaciones                                               │
│    → Testing                                                                │
│                                                                              │
│ 🚀 DEPLOYMENT.md                                                            │
│    → Windows (Gunicorn, servicio)                                           │
│    → Linux/Ubuntu (Systemd, Nginx, PostgreSQL)                              │
│    → Docker (Dockerfile, Docker Compose)                                    │
│    → Heroku                                                                 │
│    → DigitalOcean                                                           │
│    → Configuración de producción                                            │
│    → Backup y monitoreo                                                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│ INFORMES EJECUTIVOS                                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│ 📊 RESUMEN_EJECUTIVO.md                                                     │
│    → Descripción general del proyecto                                       │
│    → Funcionalidades principales                                            │
│    → Especificaciones técnicas                                              │
│    → Métricas de rendimiento                                                │
│    → Análisis de ROI                                                        │
│    → Plan de implementación                                                 │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════

📂 ESTRUCTURA DEL CÓDIGO

═══════════════════════════════════════════════════════════════════════════════

reportes_redemi/
│
├── 🎯 ARCHIVOS PRINCIPALES
│   ├── run.py                  ← Punto de entrada (ejecutar esto)
│   ├── config.py               ← Configuración de la aplicación
│   ├── logger_config.py        ← Sistema de logging
│   ├── scheduler.py            ← Tareas automáticas (correos)
│   ├── requirements.txt        ← Dependencias Python
│   └── .env                    ← Variables de entorno (secretos)
│
├── 📁 app/ (Código principal)
│   ├── __init__.py             ← Factory de Flask
│   │
│   ├── 📁 models/
│   │   └── __init__.py         ← Modelos SQLAlchemy (Reporte, HistorialCarga)
│   │
│   ├── 📁 routes/
│   │   ├── __init__.py
│   │   ├── main_routes.py      ← /reportes, /usuarios, /grupos, /estadisticas
│   │   ├── upload_routes.py    ← /upload/archivo, /upload/historial
│   │   ├── export_routes.py    ← /export/usuario/<usuario>, /export/global
│   │   └── api_routes.py       ← /api/dashboard/usuario, /api/dashboard/global
│   │
│   ├── 📁 services/
│   │   ├── __init__.py
│   │   ├── excel_service.py    ← Validación y procesamiento Excel
│   │   ├── export_service.py   ← Generación de archivos Excel
│   │   └── email_service.py    ← Envío de correos
│   │
│   ├── 📁 templates/
│   │   ├── base.html           ← Template base
│   │   ├── index.html          ← Página principal
│   │   ├── upload.html         ← Carga de archivos
│   │   ├── reportes.html       ← Vista de reportes
│   │   ├── dashboard.html      ← Dashboard con gráficos
│   │   └── errors/
│   │       ├── 404.html        ← Página no encontrada
│   │       ├── 500.html        ← Error del servidor
│   │       └── 413.html        ← Archivo demasiado grande
│   │
│   └── 📁 static/
│       ├── 📁 css/
│       │   └── style.css       ← Estilos personalizados
│       └── 📁 js/
│           └── main.js         ← Funciones JavaScript globales
│
├── 📁 logs/                    ← Archivos de registro (se crean automáticamente)
│   └── app.log                 ← Logs de la aplicación
│
├── 📁 uploads/                 ← Archivos temporales de carga
│
├── 📁 reportes.db              ← Base de datos SQLite (se crea automáticamente)
│
├── 🔧 INSTALACIÓN & SETUP
│   ├── setup.bat               ← Instalación automática (Windows)
│   ├── setup.py                ← Instalación automática (multiplataforma)
│   └── init_db.py              ← Cargar datos de ejemplo
│
├── .gitignore                  ← Archivos ignorados por Git
│
└── 📚 DOCUMENTACIÓN
    ├── README.md               ← Guía general completa
    ├── QUICK_START.txt         ← Inicio rápido (5 min)
    ├── GUIA_DE_USO.md          ← Cómo usar la aplicación
    ├── EJEMPLO_EXCEL.md        ← Formato de archivo Excel
    ├── TECHNICAL_DOCS.md       ← Documentación técnica
    ├── DEPLOYMENT.md           ← Guía de deployment
    ├── RESUMEN_EJECUTIVO.md    ← Resumen ejecutivo
    └── INDEX.md                ← Este archivo


═══════════════════════════════════════════════════════════════════════════════

🎯 FLUJOS PRINCIPALES

═══════════════════════════════════════════════════════════════════════════════

1️⃣ CARGA DE ARCHIVO

   Usuario
      ↓
   POST /upload/archivo
      ↓
   ExcelProcessingService.validate_file()
      ↓
   ExcelProcessingService.prepare_for_database()
      ↓
   Insertar en Reporte (BD)
      ↓
   Registrar en HistorialCarga
      ↓
   Retornar estadísticas (JSON)


2️⃣ BÚSQUEDA Y FILTROS

   Usuario aplica filtros
      ↓
   GET /reportes?usuario=&fecha_inicio=&fecha_fin=&grupo=
      ↓
   Construir query dinámicamente
      ↓
   Contar totales
      ↓
   Paginar resultados
      ↓
   Calcular sumas
      ↓
   Retornar JSON


3️⃣ EXPORTACIÓN

   Usuario click "Descargar"
      ↓
   GET /export/usuario/<usuario> o /export/global
      ↓
   ExportService.export_usuario_excel() o export_global_excel()
      ↓
   Generar DataFrame (pandas)
      ↓
   Agregar totales
      ↓
   Crear Excel en memoria
      ↓
   Enviar como descarga


4️⃣ DASHBOARD

   Usuario selecciona modo
      ↓
   GET /api/dashboard/usuario/<usuario> o /api/dashboard/global
      ↓
   Procesar datos para gráficos
      ↓
   Retornar datos (JSON)
      ↓
   Chart.js renderiza gráficos


5️⃣ AUTOMATIZACIÓN

   APScheduler (cada día)
      ↓
   08:00 / 14:00 / 17:30
      ↓
   enviar_resumen_reportes()
      ↓
   Consultar datos
      ↓
   Generar Excel
      ↓
   Construir HTML
      ↓
   EmailService.send_email()
      ↓
   Correo enviado


═══════════════════════════════════════════════════════════════════════════════

⚙️ CONFIGURACIÓN

═══════════════════════════════════════════════════════════════════════════════

Archivo: .env

[Base de Datos]
DATABASE_URL=sqlite:///reportes.db
SQLALCHEMY_TRACK_MODIFICATIONS=False

[Flask]
FLASK_ENV=development
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
SECRET_KEY=tu_clave_secreta

[Archivos]
MAX_CONTENT_LENGTH=50000000
UPLOAD_FOLDER=uploads/
ALLOWED_EXTENSIONS=xlsx

[Correo]
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_contraseña_app
MAIL_RECIPIENTS=email1@empresa.com

[Logging]
LOG_LEVEL=INFO
LOG_FILE=logs/app.log


═══════════════════════════════════════════════════════════════════════════════

📊 MODELOS DE BASE DE DATOS

═══════════════════════════════════════════════════════════════════════════════

Tabla: reportes
┌─────────────────────────────────────────────┐
│ id (PK)                                     │
│ wo (string)                                 │
│ usuario_asignado (string) [INDEXADO]        │
│ fecha (date) [INDEXADO]                     │
│ horas_aprobadas (float)                     │
│ horas_reales (float)                        │
│ grupo (string) [INDEXADO]                   │
│ fecha_carga (datetime)                      │
│                                             │
│ Índices compuestos:                         │
│ - (usuario_asignado, fecha)                 │
│ - (usuario_asignado, grupo)                 │
│ - (grupo, fecha)                            │
└─────────────────────────────────────────────┘

Tabla: historial_carga
┌─────────────────────────────────────────────┐
│ id (PK)                                     │
│ nombre_archivo (string)                     │
│ cantidad_registros (int)                    │
│ registros_procesados (int)                  │
│ registros_error (int)                       │
│ fecha_carga (datetime) [INDEXADO]           │
│ estado (string)                             │
│ mensaje_error (text)                        │
│ usuario_carga (string)                      │
└─────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════

🔑 ENDPOINTS API

═══════════════════════════════════════════════════════════════════════════════

CARGA
  POST   /upload/archivo              Cargar archivo Excel
  GET    /upload/historial            Ver historial de cargas

REPORTES
  GET    /reportes                    Obtener reportes (con filtros)
  GET    /usuarios                    Lista de usuarios únicos
  GET    /grupos                      Lista de grupos únicos
  GET    /estadisticas                Estadísticas generales

EXPORTACIÓN
  GET    /export/usuario/<usuario>    Descargar Excel del usuario
  GET    /export/global               Descargar Excel global

DASHBOARD
  GET    /api/dashboard/usuario/<usuario>   Datos para dashboard usuario
  GET    /api/dashboard/global               Datos para dashboard global


═══════════════════════════════════════════════════════════════════════════════

✅ CHECKLIST DE FUNCIONALIDADES

═══════════════════════════════════════════════════════════════════════════════

CARGA
  ✅ Validar extensión (.xlsx)
  ✅ Validar columnas obligatorias
  ✅ Validar tipos de datos
  ✅ Procesar automáticamente
  ✅ Historial de cargas
  ✅ Mensajes de error claros

BÚSQUEDA
  ✅ Búsqueda por usuario (parcial)
  ✅ Filtro por rango de fechas
  ✅ Filtro por grupo
  ✅ Paginación (20 items/página)
  ✅ Totales en tiempo real

EXPORTACIÓN
  ✅ Descarga individual por usuario
  ✅ Descarga global consolidada
  ✅ Formato Excel profesional
  ✅ Múltiples hojas
  ✅ Filas de totales

DASHBOARD
  ✅ Gráficos de líneas (horas por mes)
  ✅ Gráficos de barras (horas por grupo)
  ✅ Gráfico donut (comparación)
  ✅ Top usuarios
  ✅ Filtros dinámicos
  ✅ Actualización en tiempo real

AUTOMATIZACIÓN
  ✅ Envío a las 08:00 AM
  ✅ Envío a las 02:00 PM
  ✅ Envío a las 05:30 PM
  ✅ Correos con HTML
  ✅ Excel adjunto
  ✅ Resumen por usuario

ARQUITECTURA
  ✅ Código modular
  ✅ Separación de responsabilidades
  ✅ Logging completo
  ✅ Manejo de errores global
  ✅ Validación robusta
  ✅ Consultas optimizadas


═══════════════════════════════════════════════════════════════════════════════

📞 SOPORTE Y AYUDA

═══════════════════════════════════════════════════════════════════════════════

¿No sabes cómo empezar?
  → Abre QUICK_START.txt (5 minutos)

¿Cómo uso la aplicación?
  → Abre GUIA_DE_USO.md

¿Cuál es el formato del Excel?
  → Abre EJEMPLO_EXCEL.md

¿Necesito información técnica?
  → Abre TECHNICAL_DOCS.md

¿Cómo desplego en producción?
  → Abre DEPLOYMENT.md

¿Quiero un resumen general?
  → Abre RESUMEN_EJECUTIVO.md


═══════════════════════════════════════════════════════════════════════════════

🎉 ESTADO DEL PROYECTO

═══════════════════════════════════════════════════════════════════════════════

✅ COMPLETADO
  • Estructura del proyecto
  • Modelos de base de datos
  • Todas las rutas/endpoints
  • Servicios de procesamiento
  • Interfaz web completa
  • Dashboard con gráficos
  • Sistema de automatización
  • Logging y manejo de errores
  • Documentación exhaustiva
  • Scripts de instalación

ESTADO: ✅ LISTO PARA PRODUCCIÓN

═══════════════════════════════════════════════════════════════════════════════

Sistema de Reportes Empresariales v1.0.0
Desarrollado: Febrero 2026
Desarrollador: Equipo técnico HITSS

═══════════════════════════════════════════════════════════════════════════════
