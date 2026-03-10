# Documentación Técnica - Sistema de Reportes Empresariales

## Arquitectura de la Aplicación

### Patrón MVC Modificado

La aplicación sigue un patrón modificado de MVC con separación clara de responsabilidades:

```
Solicitud HTTP
    ↓
[Routes/Blueprints] → Punto de entrada
    ↓
[Services] → Lógica de negocio
    ↓
[Models] → Acceso a datos
    ↓
[Base de Datos]
    ↓
[Respuesta JSON/HTML]
```

## Componentes Principales

### 1. Factory Pattern (app/__init__.py)

Implementa el patrón Factory para crear instancias de Flask:

```python
def create_app(config_name=None):
    app = Flask(__name__)
    db.init_app(app)
    # Registrar blueprints
    # Registrar error handlers
    return app
```

**Ventajas**:
- Testing simplificado
- Múltiples instancias de la app
- Configuración flexible

### 2. Blueprints (app/routes/)

Los blueprints organizan las rutas por funcionalidad:

- **main_routes.py**: Rutas principales (reportes, búsqueda)
- **upload_routes.py**: Carga y validación de archivos
- **export_routes.py**: Endpoints de descarga
- **api_routes.py**: Endpoints de la API (dashboard)

### 3. Services (app/services/)

Encapsulan la lógica de negocio:

#### ExcelProcessingService
- Validación de archivos
- Conversión de tipos de datos
- Preparación para BD

#### ExportService
- Generación de Excel
- Formateo de datos
- Cálculo de totales

#### EmailService
- Inicialización de correo
- Envío de reportes
- Construcción de HTML

### 4. Models (app/models/)

Define la estructura de datos:

```python
class Reporte(db.Model):
    # Campos y relaciones
    # Índices optimizados
    # Métodos auxiliares

class HistorialCarga(db.Model):
    # Registro de cargas
    # Estado y errores
```

## Flujos de Proceso

### 1. Carga de Archivo

```
1. Usuario sube archivo Excel
   ↓
2. Validar extensión (.xlsx)
   ↓
3. Guardar temporalmente
   ↓
4. Leer con pandas
   ↓
5. Validar columnas obligatorias
   ↓
6. Validar tipos de datos
   ↓
7. Limpiar datos (trim, strings)
   ↓
8. Insertar en BD con transacción
   ↓
9. Registrar en historial
   ↓
10. Eliminar archivo temporal
   ↓
11. Retornar estadísticas
```

**Manejo de Errores**:
- Validación fallida → mostrar mensaje específico
- Inserción fallida → rollback de transacción
- Archivo corrupto → error de formato

### 2. Búsqueda y Filtros

```
1. Usuario aplica filtros
   ↓
2. Construir query base
   ↓
3. Aplicar filtros dinámicamente:
   - Usuario (búsqueda parcial, case-insensitive)
   - Fecha inicio/fin
   - Grupo
   ↓
4. Contar total de registros
   ↓
5. Paginar resultados
   ↓
6. Calcular totales de la página
   ↓
7. Retornar datos + paginación
```

**Índices Utilizados**:
- `usuario_asignado` - búsqueda por usuario
- `fecha` - filtros de rango
- `grupo` - filtro por grupo
- Índices compuestos para queries complejas

### 3. Exportación a Excel

```
1. Consultar reportes según filtros
   ↓
2. Crear DataFrame con pandas
   ↓
3. Agregar fila de totales
   ↓
4. Formatear columnas (ancho, número)
   ↓
5. Crear hojas adicionales (resumen)
   ↓
6. Escribir en BytesIO (en memoria)
   ↓
7. Enviar como descarga
   ↓
8. Registrar en logs
```

### 4. Automatización de Reportes

```
APScheduler
    ↓
Trigger CronTrigger (08:00, 14:00, 17:30)
    ↓
Ejecutar enviar_resumen_reportes()
    ↓
1. Crear aplicación context
2. Consultar datos resumidos por usuario
3. Generar archivo Excel global
4. Construir HTML del reporte
5. Enviar correo con adjunto
6. Registrar en logs
```

## Validación de Datos

### En Carga

```python
# 1. Validar columnas
if columnas_faltantes:
    return error

# 2. Validar tipos
df['Fecha'] = pd.to_datetime(df['Fecha'])
df['Horas'] = pd.to_numeric(df['Horas'])

# 3. Limpiar espacios
df['Usuario'] = df['Usuario'].str.strip()

# 4. Eliminar nulos
df = df.dropna(subset=['Usuario', 'Grupo'])
```

### En Búsqueda

```python
# Case-insensitive
query.filter(Reporte.usuario_asignado.ilike(f'%{search}%'))

# Conversión de fechas
fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()

# Validación de tipo
page = request.args.get('page', 1, type=int)
```

## Rendimiento y Optimización

### Índices de Base de Datos

```sql
-- Índices simples
CREATE INDEX idx_usuario ON reportes(usuario_asignado)
CREATE INDEX idx_fecha ON reportes(fecha)
CREATE INDEX idx_grupo ON reportes(grupo)

-- Índices compuestos
CREATE INDEX idx_usuario_fecha ON reportes(usuario_asignado, fecha)
CREATE INDEX idx_usuario_grupo ON reportes(usuario_asignado, grupo)
CREATE INDEX idx_grupo_fecha ON reportes(grupo, fecha)
```

**Impacto**:
- Búsquedas por usuario: ~100x más rápido
- Filtros de fecha: ~50x más rápido
- Queries complejas: indexación inteligente

### Paginación

```python
# Evita cargar todos los registros
reportes = query.paginate(page=page, per_page=20)

# Límite configurable en config.py
ITEMS_PER_PAGE = 20
```

### Queries Optimizadas

```python
# ✓ BIEN: Agregación en BD
resultado = db.session.query(
    func.sum(Reporte.horas),
    func.count(Reporte.id)
).first()

# ✗ MALO: Cargar todo en memoria
total = sum(r.horas for r in reportes)
```

## Manejo de Errores

### Niveles de Error

1. **Validación** → 400 Bad Request
2. **No encontrado** → 404 Not Found
3. **Error del servidor** → 500 Internal Server Error
4. **Archivo grande** → 413 Payload Too Large

### Error Handlers

```python
@app.errorhandler(404)
def not_found_error(error):
    logger.warning(f"Error 404: {error}")
    return render_template('errors/404.html'), 404
```

### Try-Catch Específico

```python
try:
    # Lógica
except ValueError as e:
    logger.warning(f"Valor inválido: {e}")
    return jsonify({'error': 'Valor inválido'}), 400
except Exception as e:
    logger.error(f"Error inesperado: {e}")
    db.session.rollback()
    return jsonify({'error': 'Error interno'}), 500
```

## Logging

### Niveles

```
DEBUG   - Información de desarrollo
INFO    - Eventos normales
WARNING - Situaciones inusuales (errores recuperables)
ERROR   - Errores graves
CRITICAL- Fallos del sistema
```

### Loggers por Módulo

```python
logger_excel      = logging.getLogger('reportes_app.excel')
logger_db         = logging.getLogger('reportes_app.db')
logger_email      = logging.getLogger('reportes_app.email')
logger_scheduler  = logging.getLogger('reportes_app.scheduler')
```

### Formato

```
2026-02-26 15:30:45 - reportes_app.excel - INFO - Archivo validado exitosamente
```

## Seguridad

### CSRF Protection (WTForms)

```python
@app.route('/form', methods=['POST'])
def form_handler():
    form = MyForm()
    if form.validate_on_submit():
        # Procesar forma segura
```

### SQL Injection Prevention

```python
# ✓ SEGURO: Parámetros enlazados
query = Reporte.query.filter_by(usuario_asignado=usuario)

# ✗ INSEGURO: String formatting
query = f"SELECT * FROM reportes WHERE usuario = '{usuario}'"
```

### File Upload Security

```python
# Validar extensión
if not ExcelProcessingService.allowed_file(filename):
    return error

# Tamaño máximo
MAX_CONTENT_LENGTH = 50000000

# Guardar con nombre seguro
filename = secure_filename(filename)
```

## Testing

### Estructura de Tests

```
tests/
├── test_excel_service.py    # Validación Excel
├── test_export_service.py   # Exportación
├── test_routes.py           # Endpoints
└── test_models.py           # Modelos
```

### Ejemplo de Test

```python
def test_validar_archivo(client):
    with open('test_file.xlsx', 'rb') as f:
        response = client.post(
            '/upload/archivo',
            data={'file': f}
        )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
```

## Deployment

### Variables de Entorno Críticas

```env
# Producción
FLASK_ENV=production
DEBUG=False
SECRET_KEY=clave_muy_larga_y_segura
DATABASE_URL=postgresql://...
```

### Gunicorn Configuration

```bash
gunicorn \
    --workers 4 \
    --worker-class sync \
    --bind 0.0.0.0:5000 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    run:app
```

### Nginx Configuration

```nginx
upstream app {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Monitoreo y Mantenimiento

### Métricas a Monitorear

- Tiempo de respuesta de endpoints
- Errores por tipo (404, 500, etc.)
- Carga de archivos (cantidad, tamaño, tiempo)
- Uso de BD (queries lentas, conexiones)
- Errores de correo

### Limpieza de Datos

```python
# Limpiar archivos temporales
def cleanup_uploads():
    for file in os.listdir('uploads/'):
        if os.path.getmtime(file) < now - timedelta(hours=24):
            os.remove(file)

# Ejecutar diariamente con scheduler
scheduler.add_job(cleanup_uploads, 'cron', hour=2)
```

## Escalabilidad

### Para Muchos Usuarios

1. **Caching**:
   ```python
   from flask_caching import Cache
   cache = Cache(app, config={'CACHE_TYPE': 'redis'})
   ```

2. **Session Sticky** en Nginx/Load Balancer

3. **Base de datos** → PostgreSQL en producción

### Para Muchos Datos

1. **Paginación** (ya implementada)

2. **Índices compuestos** (ya implementados)

3. **Particionamiento** de tabla por fecha:
   ```sql
   CREATE TABLE reportes_2026_01 PARTITION OF reportes
   FOR VALUES FROM ('2026-01-01') TO ('2026-02-01')
   ```

4. **Archivado** de datos antiguos

---

**Versión**: 1.0.0  
**Última actualización**: Febrero 2026
