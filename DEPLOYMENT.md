# 🚀 Guía de Deployment - Sistema de Reportes Empresariales

## 📋 Tabla de Contenidos

1. [Deployment en Windows](#windows)
2. [Deployment en Linux/Ubuntu](#linux)
3. [Deployment en Docker](#docker)
4. [Deployment en Heroku](#heroku)
5. [Deployment en DigitalOcean](#digitalocean)

---

## <a name="windows"></a>🪟 Deployment en Windows

### Opción 1: Local Development Server

Perfecta para testing y desarrollo.

```batch
# 1. Instalar
python setup.py
# o
setup.bat

# 2. Ejecutar
python run.py

# 3. Acceder
# http://localhost:5000
```

### Opción 2: Producción con Gunicorn

```bash
# 1. Instalar Gunicorn
pip install gunicorn

# 2. Ejecutar
gunicorn -w 4 -b 0.0.0.0:5000 run:app

# 3. Para hacerlo persistente, crear servicio Windows

# Crear archivo start_service.bat:
@echo off
cd C:\ruta\a\proyecto
venv\Scripts\gunicorn -w 4 -b 0.0.0.0:5000 run:app

# Crear servicio con NSSM (descargar de https://nssm.cc/download)
nssm install ReportesApp "C:\ruta\start_service.bat"
nssm start ReportesApp
```

### Configuración de Firewall

```powershell
# Permitir puerto 5000
netsh advfirewall firewall add rule name="Reportes" dir=in action=allow protocol=tcp localport=5000
```

---

## <a name="linux"></a>🐧 Deployment en Linux/Ubuntu

### Opción 1: Systemd Service

```bash
# 1. Instalar dependencias
sudo apt-get update
sudo apt-get install python3 python3-venv python3-pip nginx

# 2. Crear usuario para la app
sudo useradd -m reportes
sudo su - reportes

# 3. Clonar/copiar proyecto
git clone <repo> reportes
cd reportes

# 4. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. Crear archivo .env
cp .env.example .env
# Editar .env con valores correctos

# 6. Crear servicio systemd
sudo cat > /etc/systemd/system/reportes.service << EOF
[Unit]
Description=Sistema de Reportes Empresariales
After=network.target

[Service]
User=reportes
WorkingDirectory=/home/reportes/reportes
ExecStart=/home/reportes/reportes/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 run:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 7. Habilitar y ejecutar
sudo systemctl daemon-reload
sudo systemctl enable reportes
sudo systemctl start reportes
sudo systemctl status reportes
```

### Opción 2: Nginx como Reverse Proxy

```bash
# 1. Instalar Nginx
sudo apt-get install nginx

# 2. Crear configuración
sudo cat > /etc/nginx/sites-available/reportes << 'EOF'
server {
    listen 80;
    server_name example.com www.example.com;

    # Redirigir HTTP a HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com www.example.com;

    # Certificados SSL (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    # Configuración SSL
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Proxy a Flask
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Archivos estáticos
    location /static {
        alias /home/reportes/reportes/app/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Límite de tamaño de carga
    client_max_body_size 50M;
}
EOF

# 3. Habilitar sitio
sudo ln -s /etc/nginx/sites-available/reportes /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# 4. SSL con Let's Encrypt
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d example.com -d www.example.com
```

### Opción 3: PostgreSQL en Producción

```bash
# 1. Instalar PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# 2. Crear base de datos
sudo -u postgres psql << EOF
CREATE DATABASE reportes;
CREATE USER reportes_user WITH PASSWORD 'contraseña_segura';
ALTER ROLE reportes_user SET client_encoding TO 'utf8';
ALTER ROLE reportes_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE reportes_user SET default_transaction_deferrable TO ON;
GRANT ALL PRIVILEGES ON DATABASE reportes TO reportes_user;
EOF

# 3. Actualizar .env
# DATABASE_URL=postgresql://reportes_user:contraseña_segura@localhost/reportes

# 4. Instalar driver Python
pip install psycopg2-binary

# 5. Inicializar BD
python3 -c "from app import create_app, db; app = create_app(); db.create_all()"
```

---

## <a name="docker"></a>🐳 Deployment con Docker

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos
COPY requirements.txt .
COPY . .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Crear directorios
RUN mkdir -p logs uploads

# Exponer puerto
EXPOSE 5000

# Variables de entorno
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# Comando de inicio
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://reportes_user:password@db:5432/reportes
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db
    volumes:
      - ./uploads:/app/uploads
      - ./logs:/app/logs
    restart: always

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=reportes
      - POSTGRES_USER=reportes_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always

volumes:
  postgres_data:
```

### Comandos Docker

```bash
# Construir
docker build -t reportes-app .

# Ejecutar
docker run -p 5000:5000 reportes-app

# Con compose
docker-compose up -d

# Ver logs
docker-compose logs -f web

# Parar
docker-compose down
```

---

## <a name="heroku"></a>📦 Deployment en Heroku

### Procfile

```
web: gunicorn run:app
```

### runtime.txt

```
python-3.11.0
```

### Configuración

```bash
# 1. Instalar Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# 2. Login
heroku login

# 3. Crear app
heroku create tu-app-name

# 4. Agregar PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# 5. Variables de entorno
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=tu_clave_muy_larga

# 6. Deploy
git push heroku main

# 7. Inicializar BD
heroku run python -c "from app import create_app, db; app = create_app(); db.create_all()"

# 8. Ver logs
heroku logs --tail
```

---

## <a name="digitalocean"></a>⚙️ Deployment en DigitalOcean

### Paso a Paso

```bash
# 1. Crear Droplet (Ubuntu 22.04, 1GB RAM, $6/mes)

# 2. SSH al servidor
ssh root@tu_ip

# 3. Actualizar sistema
apt-get update && apt-get upgrade -y

# 4. Instalar dependencias
apt-get install -y python3 python3-venv python3-pip postgresql postgresql-contrib nginx git

# 5. Crear usuario
adduser reportes
sudo -su reportes

# 6. Clonar proyecto
git clone <tu_repo> ~/reportes
cd ~/reportes

# 7. Setup (seguir pasos Linux anteriores)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 8. Configurar como servicio systemd (ver sección Linux)

# 9. Configurar DNS
# En DigitalOcean, crear A record apuntando a tu IP

# 10. Certificado SSL gratuito
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d example.com
```

---

## 🔒 Configuración de Producción

### Variables de Entorno Críticas

```env
# Flask
FLASK_ENV=production
DEBUG=False
SECRET_KEY=generar_con: python -c "import secrets; print(secrets.token_urlsafe(32))"

# Base de Datos
DATABASE_URL=postgresql://user:password@host:5432/reportes

# Correo
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_contraseña_app

# Seguridad
MAX_CONTENT_LENGTH=50000000
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
REMEMBER_COOKIE_SECURE=True
```

### Backup Automático

```bash
# Script de backup diario
#!/bin/bash
BACKUP_DIR="/backups"
DB_NAME="reportes"

# Crear carpeta de backup
mkdir -p $BACKUP_DIR

# Backup de BD
pg_dump -U reportes_user $DB_NAME | gzip > $BACKUP_DIR/reportes_$(date +%Y%m%d_%H%M%S).sql.gz

# Eliminar backups antiguos (más de 30 días)
find $BACKUP_DIR -name "reportes_*.sql.gz" -mtime +30 -delete

# Agregar a crontab (cron tab -e)
# 0 2 * * * /home/reportes/backup.sh
```

### Monitoreo

```bash
# Instalación de Monitoring
apt-get install prometheus node-exporter

# Alertas con Alertmanager
# (Configuración avanzada - consultar documentación)
```

---

## 🛠️ Troubleshooting

### Puerto Already in Use

```bash
# Ver qué usa el puerto
lsof -i :5000

# Matar proceso
kill -9 <PID>
```

### Permission Denied

```bash
# Cambiar permisos
chmod +x run.py
sudo chown -R reportes:reportes /app
```

### Database Connection Error

```bash
# Verificar conexión
psql -U reportes_user -d reportes -h localhost

# Reiniciar servicio
sudo systemctl restart postgresql
```

### Gunicorn Worker Timeout

```bash
# Aumentar timeout en gunicorn
gunicorn --timeout 120 run:app
```

---

## ✅ Checklist de Deployment

- [ ] Base de datos configurada
- [ ] Variables de entorno establecidas
- [ ] SSL/TLS certificado instalado
- [ ] Firewall configurado
- [ ] Backup automático activo
- [ ] Logging funcionando
- [ ] Monitoreo en lugar
- [ ] Correos configurados
- [ ] Dominio apuntando
- [ ] Pruebas de carga exitosas

---

## 📞 Soporte en Producción

Monitorear:
- Disk space
- Memory usage
- CPU usage
- Database size
- Error logs

Mantener:
- Dependencias actualizadas
- Backups regulares
- Certificados SSL renovados
- Logs archivados

---

**Última actualización**: Febrero 2026  
**Versión**: 1.0.0
