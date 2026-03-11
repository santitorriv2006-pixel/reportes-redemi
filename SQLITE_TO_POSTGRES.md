# 🐘 MIGRACIÓN SQLite → PostgreSQL

## ✅ Estado Actual

- **BD original**: SQLite (`instance/reportes.db`)
- **Archivos generados**:
  - `migration_sqlite_20260310_*.sql` - Dump SQLite
  - `migration_postgres_20260310_*.sql` - Script PostgreSQL

---

## 📋 Opción 1: PostgreSQL en Render (⭐ SIN instalar localmente)

### Paso 1: Subir a GitHub

```powershell
./push_postgres_migration.ps1
```

O manualmente:
```bash
git add migration_postgres_*.sql
git add migrate_to_postgres.py
git add quick_migrate_to_postgres.py
git commit -m "Migrate to PostgreSQL"
git push origin main
```

### Paso 2: Crear PostgreSQL en Render

1. Ve a [dashboard.render.com](https://dashboard.render.com)
2. Click en **New** → **PostgreSQL**
3. Completa:
   - **Name**: `reportes-db`
   - **Database**: `reportes`
   - **Region**: Más cercana a ti
4. Click **Create**
5. **COPIA** la URL interna:
   ```
   postgresql://reportes_user:xxxxx@dpg-xxxxx.render.internal:5432/reportes_db
   ```

### Paso 3: Crear Web Service

1. Click en **New** → **Web Service**
2. Conecta tu repositorio GitHub
3. Configuración:
   - **Name**: `reportes-api`
   - **Environment**: Python 3
   - **Build**: `pip install -r requirements.txt`
   - **Start**: `gunicorn app:app`
4. En **Environment**, agrega todas las variables (ver abajo)
5. Click **Create Web Service**

### Paso 4: Variables de Entorno en Render

En **Web Service → Settings → Environment**, agrega:

```
DATABASE_URL=postgresql://reportes_user:PASSWORD@dpg-xxxxx.render.internal:5432/reportes_db
FLASK_ENV=production
SECRET_KEY=genera_con_secrets.token_hex(32)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=contraseña_app_google
MAIL_DEFAULT_SENDER=noreply@empresa.com
MAIL_RECIPIENTS=admin@empresa.com
LOG_LEVEL=INFO
```

**Para generar SECRET_KEY fuerte**:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Paso 5: Restaurar Datos

Después de que el deploy termine:

1. En Render: **Web Service → Shell**
2. Ejecuta:
   ```bash
   psql -U reportes_user -d reportes_db < migration_postgres_20260310_*.sql
   ```

   O más simple (si psql está en tu PATH):
   ```bash
   cat migration_postgres_20260310_*.sql | psql $DATABASE_URL
   ```

Listo! ✅

---

## 📋 Opción 2: PostgreSQL Local (si quieres testing)

### Instalar PostgreSQL

```powershell
# Necesita admin
./install_postgres.ps1
```

O manualmente:
- **Windows**: https://www.postgresql.org/download/windows/
- **Mac**: `brew install postgresql`
- **Linux**: `sudo apt-get install postgresql`

### Crear BD

```bash
# Conectar a PostgreSQL
psql -U postgres

# En la consola psql:
CREATE DATABASE reportes;
CREATE USER reportes_user WITH PASSWORD 'tu_contraseña';
ALTER ROLE reportes_user CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE reportes TO reportes_user;
\q
```

### Restaurar Datos

```bash
psql -U reportes_user -d reportes -f migration_postgres_20260310_*.sql
```

### Actualizar .env

```
DATABASE_URL=postgresql://reportes_user:tu_contraseña@localhost:5432/reportes
FLASK_ENV=development
```

### Probar Localmente

```bash
python run.py
# Debería conectar a PostgreSQL local
```

---

## 🔄 Cambiar de BD Después

**Si quieres volver a SQLite**:
```env
DATABASE_URL=sqlite:///instance/reportes.db
```

**Si quieres cambiar a PostgreSQL**:
```env
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

La app auto-adapta el tipo de BD 🎉

---

## 🆘 Troubleshooting

### "ERROR: role "reportes_user" does not exist"
```bash
# En Render, el usuario ya debe existir
# Usa el usuario que genera Render (ej: postgres)
```

### "permission denied for schema public"
```bash
# En PostgreSQL local, da permisos:
GRANT USAGE ON SCHEMA public TO reportes_user;
GRANT CREATE ON SCHEMA public TO reportes_user;
```

### "connection refused"
- Verifica que PostgreSQL está corriendo
- Verify DATABASE_URL es correcta
- En Render: use la URL **internal** (no public)

### Tablas vacías después de restore
```bash
# Verifica el dump
head migration_postgres_*.sql
# Debería mostrar CREATE TABLE y INSERT statements
```

---

## ✅ Checklist Final

- [ ] Archivos `migration_*.sql` creados ✅
- [ ] Subidos a GitHub
- [ ] PostgreSQL creada en Render (o local)
- [ ] Web Service configurada con variables
- [ ] Datos restaurados en PostgreSQL
- [ ] Aplicación responde en URL de Render
- [ ] `.env` actualizado con DATABASE_URL de PostgreSQL
- [ ] `.env` con datos sensibles NO en git (en `.gitignore`)

---

## 📝 Referencias

- [PostgreSQL en Render](https://render.com/docs/databases)
- [Render Deployment](https://render.com/docs/deploy-web-servers)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

**Creado**: 2026-03-10
**Estado**: Migración completada, listo para Render
