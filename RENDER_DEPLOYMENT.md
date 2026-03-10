# Guía: Desplegar en Render con PostgreSQL

## ⚠️ IMPORTANTE - Seguridad

**NUNCA** hagas commit del `.env` con datos sensibles. Ya está en `.gitignore`:

```bash
git status  # Verificar que .env no aparece
git ls-files | grep "\.env"  # No debería devolver nada
```

---

## 🗄️ ¿SQLite o PostgreSQL?

| Característica | SQLite | PostgreSQL |
|---|---|---|
| **Facilidad** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Producción** | ❌ No recomendado | ✅ Recomendado |
| **Múltiples usuarios** | ❌ Lento | ✅ Optimizado |
| **Escalabilidad** | ❌ Limitado | ✅ Excelente |
| **Costo en Render** | Gratis | Desde $15/mes (o gratis si tienes créditos) |

👉 **Para una app en línea: USA POSTGRESQL**

---

## 📋 Pasos para Render con PostgreSQL

### 1️⃣ Exportar Base de Datos Actual

Si tienes datos en SQLite:

```bash
# Activar venv (si no está)
./venv/Scripts/Activate.ps1

# Exportar como SQL
python export_db.py

# Crea: database_backup_sqlite_YYYYMMDD_HHMMSS.sql
```

### 2️⃣ Subir a GitHub

```bash
git add database_backup_*.sql .env.example export_db.py restore_db.py
git commit -m "Add database backup for Render PostgreSQL deployment"
git push origin main
```

### 3️⃣ Crear PostgreSQL en Render

1. Ve a [dashboard.render.com](https://dashboard.render.com)
2. Click en **"New +" → PostgreSQL**
3. Completa:
   - **Name**: `reportes-db` (o el que prefieras)
   - **Database**: `reportes`
   - **User**: `postgres`
   - **Region**: Elige la más cercana
   - Click **"Create Database"**

4. **COPIA** la URL interna:
   ```
   postgresql://reportes_user:xxxxx@dpg-xxxxx.render.internal:5432/reportes_db
   ```

### 4️⃣ Crear Web Service en Render

1. Click en **"New +" → Web Service**
2. Conecta tu repositorio GitHub
3. Completa:
   - **Name**: `reportes-api`
   - **Environment**: `Python 3`
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command**:
     ```bash
     gunicorn app:app
     ```

4. Debajo en **Environment**:
   - Agrega todas las variables (ver sección 5️⃣)

5. Click **"Create Web Service"** y espera el deploy

### 5️⃣ Configurar Variables de Entorno en Render

**En Web Service → Settings → Environment**, agrega:

```
DATABASE_URL=postgresql://reportes_user:PASSWORD@dpg-xxxxx.render.internal:5432/reportes_db
FLASK_ENV=production
SECRET_KEY=genera_una_clave_fuerte_aqui_min_32_caracteres
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=contraseña_de_app_de_google
MAIL_DEFAULT_SENDER=noreply@empresa.com
MAIL_RECIPIENTS=admin@empresa.com
LOG_LEVEL=INFO
```

**Generar SECRET_KEY fuerte**:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 6️⃣ Restaurar Base de Datos

Después de que el deploy termine:

```bash
# En la terminal de Render (Web Service → Shell)
python restore_db.py database_backup_sqlite_*.sql
```

O hacer dump desde PostgreSQL local:
```bash
pg_dump -h localhost -U postgres -d reportes > database_backup_postgres_local.sql
# Subir a GitHub y restaurar en Render
```

---

## ✅ Verificar que Funciona

```bash
# Visita tu URL de Render (ej: https://reportes-api.onrender.com)
# Deberías ver tu aplicación corriendo
```

---

## 🔄 Actualizar Datos en el Futuro

Cuando hagas cambios en tu BD local:

**Opción A: SQLite → PostgreSQL en Render**
```bash
python export_db.py              # Exporta SQLite actual
git add database_backup_*.sql
git commit -m "Update database"
git push

# En Render shell:
python restore_db.py database_backup_sqlite_*.sql
```

**Opción B: PostgreSQL local → PostgreSQL Render**
```bash
# Exportar local
pg_dump -h localhost -U postgres -d reportes > backup.sql
git add backup.sql && git push

# En Render shell
python restore_db.py backup.sql
```

---

## 🆘 Troubleshooting

### Error: "connection refused" a la BD

```bash
# Verificar DATABASE_URL en Render Settings → Environment
# Debe ser la URL interna (render.internal, no public)
```

### Error: "pg_dump: command not found"

**Windows**: Instala [PostgreSQL](https://www.postgresql.org/download/windows/)
**Linux**: `sudo apt-get install postgresql-client`
**Mac**: `brew install postgresql`

### Error: "psql: FATAL: remaining connection slots are reserved"

```bash
# Render free tier tiene límite de conexiones
# Solución: Usar sqlalchemy connection pooling
# Ya está configurado en config.py
```

### La aplicación está lenta

PostgreSQL en Render free tier tiene limitaciones. Opciones:
- Subir a plan pagado ($15/mes)
- Optimizar queries en `app/routes/*.py`
- Agregar índices en modelos

---

## 📊 Estructura Final en Render

```
Render Dashboard
├── Web Service: reportes-api
│   ├── DATABASE_URL → PostgreSQL
│   ├── SECRET_KEY → tu_clave_fuerte
│   └── MAIL_* → credenciales gmail
│
├── PostgreSQL: reportes-db
│   ├── Host: dpg-xxxxx.render.internal
│   ├── Port: 5432
│   └── Database: reportes
│
└── GitHub (conectado)
    ├── database_backup_*.sql
    ├── export_db.py
    ├── restore_db.py
    └── código de la app
```

---

## 🔐 Checklist Final

- [ ] `.env` con datos sensibles NO está en git
- [ ] `.env.example` tiene la plantilla
- [ ] PostgreSQL creada en Render
- [ ] Web Service configurada
- [ ] Todas las variables de entorno en Render
- [ ] `SECRET_KEY` es fuerte (32+ caracteres)
- [ ] Gmail usa contraseña de app, no la real
- [ ] Base de datos restaurada en Render
- [ ] Aplicación responde en URL de Render

---

## 📝 Próximas Veces

```bash
# Cambios locales → Render
python export_db.py
git add -A && git commit -m "Update data"
git push

# En Render shell después del auto-deploy
python restore_db.py database_backup_*.sql
```

---

**Creado:** 2026-03-10  
**Última actualización:** PostgreSQL + Render production setup
