# Sistema de Gestión y Análisis de Reportes Empresariales

Aplicación web profesional con Flask para la carga, análisis y exportación de reportes empresariales desde archivos Excel.

## 🚀 Características Principales

- ✅ **Carga de Archivos Excel** - Validación automática de columnas obligatorias
- ✅ **Base de Datos SQLite/PostgreSQL** - Almacenamiento seguro con índices optimizados
- ✅ **Búsqueda Avanzada** - Filtros por usuario, fecha y grupo
- ✅ **Exportación Flexible** - Descargas individuales y globales en Excel
- ✅ **Dashboard Dinámico** - Gráficos interactivos con Chart.js
- ✅ **Automatización** - Envío de reportes por correo (08:00, 14:00, 17:30)
- ✅ **Logging Completo** - Registro de todas las operaciones
- ✅ **Arquitectura Modular** - Código escalable y mantenible

## 📋 Requisitos del Sistema

- Python 3.8+
- pip (gestor de paquetes Python)
- Base de datos (SQLite o PostgreSQL)

## 🔧 Instalación

### 1. Clonar o descargar el proyecto

```bash
cd "c:\Users\TORRESHS\OneDrive - HITSS\Documentos\reportes redemi"
```

### 2. Crear entorno virtual

```bash
python -m venv venv
venv\Scripts\activate  # En Windows
# source venv/bin/activate  # En Linux/Mac
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Editar el archivo `.env`:

```env
# Base de Datos
DATABASE_URL=sqlite:///reportes.db
SQLALCHEMY_TRACK_MODIFICATIONS=False

# Flask
FLASK_ENV=development
SECRET_KEY=tu_clave_secreta_aqui

# Carga de Archivos
MAX_CONTENT_LENGTH=50000000
UPLOAD_FOLDER=uploads/

# Correo (para automatización)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_contraseña_app
MAIL_RECIPIENTS=email1@empresa.com,email2@empresa.com
```

### 5. Ejecutar aplicación

```bash
python run.py
```

La aplicación estará disponible en: **http://localhost:5000**

## 📁 Estructura del Proyecto

```
reportes_redemi/
├── app/
│   ├── __init__.py           # Factory Flask
│   ├── models/
│   │   └── __init__.py       # Modelos SQLAlchemy
│   ├── routes/
│   │   ├── main_routes.py    # Rutas principales
│   │   ├── upload_routes.py  # Carga de archivos
│   │   ├── export_routes.py  # Exportación
│   │   └── api_routes.py     # Endpoints API
│   ├── services/
│   │   ├── excel_service.py  # Procesamiento Excel
│   │   ├── export_service.py # Exportación
│   │   └── email_service.py  # Envío de correos
│   ├── templates/
│   │   ├── base.html         # Template base
│   │   ├── index.html        # Página inicio
│   │   ├── upload.html       # Carga de archivos
│   │   ├── reportes.html     # Vista de reportes
│   │   ├── dashboard.html    # Dashboard
│   │   └── errors/           # Páginas de error
│   └── static/
│       ├── css/style.css     # Estilos personalizados
│       └── js/main.js        # Scripts globales
├── config.py                  # Configuración
├── logger_config.py           # Sistema de logging
├── scheduler.py               # Tareas automáticas
├── run.py                     # Archivo principal
├── .env                       # Variables de entorno
└── requirements.txt           # Dependencias Python
```

## 🗄️ Modelo de Base de Datos

### Tabla: Reportes

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer (PK) | Identificador único |
| wo | String | Número de orden |
| usuario_asignado | String | Usuario responsable (indexado) |
| fecha | Date | Fecha del reporte (indexada) |
| horas_aprobadas | Float | Horas aprobadas |
| horas_reales | Float | Horas trabajadas |
| grupo | String | Grupo de trabajo (indexado) |
| fecha_carga | DateTime | Fecha de carga |

**Índices**: usuario_asignado, fecha, grupo y combinaciones

### Tabla: HistorialCarga

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer (PK) | Identificador único |
| nombre_archivo | String | Nombre del archivo cargado |
| cantidad_registros | Integer | Total de registros |
| registros_procesados | Integer | Registros insertados |
| registros_error | Integer | Registros con error |
| fecha_carga | DateTime | Fecha de carga (indexada) |
| estado | String | exitoso/parcial/error |
| mensaje_error | Text | Detalle de errores |

## 🎯 Endpoints API

### Carga de Archivos

```
POST /upload/archivo
GET  /upload/historial?page=1
```

### Reportes y Búsqueda

```
GET /reportes?usuario=&fecha_inicio=&fecha_fin=&grupo=&page=1
GET /usuarios
GET /grupos
GET /estadisticas
```

### Exportación

```
GET /export/usuario/<usuario>?fecha_inicio=&fecha_fin=&grupo=
GET /export/global?fecha_inicio=&fecha_fin=&grupo=
```

### Dashboard API

```
GET /api/dashboard/usuario/<usuario>?fecha_inicio=&fecha_fin=
GET /api/dashboard/global?fecha_inicio=&fecha_fin=&grupo=
```

## 📊 Validación de Archivos Excel

El sistema valida automáticamente:

✅ **Columnas obligatorias**:
- WO
- Usuario Asignado
- Fecha
- Horas Aprobadas
- Horas Reales
- Grupo

✅ **Tipos de datos**:
- Fecha: formato YYYY-MM-DD
- Horas Aprobadas: numérico
- Horas Reales: numérico

✅ **Tamaño máximo**: 50MB

## ⏰ Automatización de Reportes

El sistema envía reportes automáticamente:

| Hora | Descripción |
|------|-------------|
| 08:00 | Resumen matutino |
| 14:00 | Resumen vespertino |
| 17:30 | Consolidado final |

Los reportes incluyen:
- Tabla de totales por usuario
- Archivo Excel global adjunto
- HTML formateado

## 🔒 Configuración de Correo (Gmail)

1. Habilitar **autenticación de dos factores** en tu cuenta Google
2. Generar **contraseña de aplicación**:
   - Ir a myaccount.google.com
   - Seguridad → Contraseña de aplicación
   - Seleccionar "Mail" y "Windows"
3. Usar esa contraseña en `.env`

```env
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_contraseña_app_generada
```

## 📈 Características del Dashboard

### Modo Usuario
- Horas aprobadas por mes
- Horas por grupo
- Comparación horas aprobadas vs reales

### Modo Global
- Top 10 usuarios por horas aprobadas
- Horas totales por grupo
- Total horas por mes

## 🛠️ Herramientas y Tecnologías

- **Flask** - Framework web
- **SQLAlchemy** - ORM para base de datos
- **Pandas** - Procesamiento de datos
- **Chart.js** - Gráficos interactivos
- **Bootstrap 5** - Framework CSS
- **APScheduler** - Tareas programadas
- **WTForms** - Validación de formularios

## 📝 Logging

Archivos de log en `logs/app.log`:
- Carga de archivos (excel_service)
- Operaciones de BD (db)
- Envío de correos (email)
- Tareas programadas (scheduler)

Rotación automática cada 10MB

## 🚀 Deployment

### En Producción

```env
FLASK_ENV=production
DEBUG=False
DATABASE_URL=postgresql://user:password@localhost/reportes
SECRET_KEY=clave_segura_muy_larga
```

Usar **Gunicorn**:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

O **Waitress**:
```bash
pip install waitress
waitress-serve --port=5000 run:app
```

## 🐛 Solución de Problemas

### Error: "No module named 'app'"
```bash
# Asegúrate de estar en el directorio correcto
cd "ruta\a\reportes redemi"
# Activa el entorno virtual
venv\Scripts\activate
```

### Error de Base de Datos
```bash
# Eliminar base de datos e inicializar
rm reportes.db
python run.py
```

### Error de Correo
- Verificar credenciales en `.env`
- Habilitar "aplicaciones menos seguras" en Gmail
- Comprobar conexión a internet

## 📧 Contacto y Soporte

Para reportar problemas o sugerencias, contacta al equipo de desarrollo.

## 📄 Licencia

Este proyecto es de uso interno de HITSS.

---

**Última actualización**: Febrero 2026
**Versión**: 1.0.0
