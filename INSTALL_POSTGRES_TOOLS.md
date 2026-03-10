# 🔧 Instalación de PostgreSQL para Export/Restore

Si necesitas usar `pg_dump` o `psql` desde la línea de comandos (para PostgreSQL):

## Windows

### Opción 1: PostgreSQL Completo (Recomendado)
1. Descarga desde: https://www.postgresql.org/download/windows/
2. Ejecuta el installer
3. Durante instalación, marca "Command Line Tools"
4. Al terminar, abre PowerShell y verifica:
   ```bash
   pg_dump --version
   psql --version
   ```

### Opción 2: Solo Herramientas Standalone
```powershell
# Con chocolatey (si lo tienes instalado)
choco install postgresql

# O con scoop
scoop install postgresql
```

---

## Mac

```bash
brew install postgresql
pg_dump --version
psql --version
```

---

## Linux

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install postgresql-client

# Fedora/RHEL
sudo dnf install postgresql

# Verificar
pg_dump --version
psql --version
```

---

## Verificar Instalación

```bash
# Esto debería mostrar la versión
pg_dump --version
psql --version

# Y esto debería funcionar (en el caso de PostgreSQL en Render)
psql -h dpg-xxxxx.render.internal -U postgres -d reportes -c "SELECT 1;"
```

---

## Uso en Scripts

Una vez instalado:

```bash
# Exportar desde PostgreSQL
python export_db.py
# Detecta automáticamente si es SQLite o PostgreSQL

# Restaurar a PostgreSQL
python restore_db.py database_backup_postgres_*.sql
```

Los scripts `export_db.py` y `restore_db.py` ya incluyen los comandos necesarios.

---

**Nota**: Si solo usas SQLite, no necesitas PostgreSQL client tools. Pero si despliegas en Render con PostgreSQL, es útil tener estas herramientas para debugging.
