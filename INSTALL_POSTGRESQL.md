# 📥 INSTALAR POSTGRESQL EN WINDOWS 11/10

## Paso 1: Descargar PostgreSQL

1. Ve a: **https://www.postgresql.org/download/windows/**
2. Click en la versión más reciente (ej: PostgreSQL 16)
3. Desconfigura el instalador `.exe`

## Paso 2: Instalar

1. Ejecuta el instalador que descargaste
2. En pantalla "License Agreement" → Acepta → Next
3. Installation Directory (dejar default) → Next
4. **IMPORTANTE en "Select Components":**
   - ✅ PostgreSQL Server (DEBE estar)
   - ✅ pgAdmin (útil para ver BD)
   - ✅ Command Line Tools (IMPORTANTE para scripts)
   - ✅ Development Libraries
   - Click Next
5. Data Directory (dejar default) → Next
6. **IMPORTANTE - Contraseña para superuser "postgres":**
   ```
   postgres
   ```
   (anota la contraseña que uses, la necesitarás)
   - Click Next
7. Port: **5432** (default)
   - Click Next
8. Locale: Tu idioma
   - Click Next
9. Review → Click Install
10. ⏳ Espera a que termine (1-5 minutos)
11. Finish

## Paso 3: Verificar Instalación

Abre **PowerShell** (NUEVA TERMINAL) y ejecuta:

```powershell
psql --version
```

Debería mostrar algo como: `psql (PostgreSQL) 16.0`

Si dice "No encontrado", cierra PowerShell y abre una nueva.

## Paso 4: Configurar en tu Proyecto

Una vez instalado, ejecuta en tu directorio del proyecto:

```powershell
# En la terminal de VS Code o nueva PowerShell
cd "c:\Users\TORRESHS\OneDrive - HITSS\Documentos\reportes redemi"

# Ejecutar setup
.\setup_postgres.ps1
```

El script te pedirá:
- Contraseña del superuser de PostgreSQL (aquella que configuraste)
- Luego crea la BD y restaura los datos automáticamente

## Si algo falla:

### "psql: No encontrado"
- Cierra y abre una NUEVA PowerShell
- Verifica: `Get-Command psql`

### "FATAL: password authentication failed for user "postgres""
- Verifica la contraseña que usaste en la instalación
- Si olvidaste, reinstala PostgreSQL

### Puerto 5432 ya en uso
- Durante instalación, cambia a 5433
- En .env: cámbia a `localhost:5433`

## Pasos después de instalar:

```powershell
# 1. Verificar
psql --version

# 2. Setup automático
.\setup_postgres.ps1

# 3. Probar la app
python run.py
# Debería conectar a PostgreSQL

# 4. Subir a GitHub
git add -A
git commit -m "Migrate to PostgreSQL"
git push origin main
```

---

## ❌ Si NO quieres instalar PostgreSQL localmente:

Puedes saltar esto e ir directamente a **Render**:

1. Olvida esta guía
2. Lee `RENDER_DEPLOYMENT.md`
3. Crea PostgreSQL en Render directamente
4. Los datos ya están listos en `migration_postgres_*.sql`

---

**Creado**: 2026-03-10
**Tiempo estimado**: 15 minutos (incluye descarga e instalación)
