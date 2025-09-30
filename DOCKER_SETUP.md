# 🐳 Guía de Configuración Docker - ComPuter

Esta guía te ayudará a configurar y ejecutar el proyecto ComPuter usando Docker de manera profesional.

## 📋 Prerrequisitos

### Instalación de Docker
1. **Windows**: Descargar Docker Desktop desde [docker.com](https://www.docker.com/products/docker-desktop)
2. **Linux**: 
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   ```
3. **macOS**: Descargar Docker Desktop desde [docker.com](https://www.docker.com/products/docker-desktop)

### Verificar Instalación
```bash
docker --version
docker-compose --version
```

## 🚀 Configuración Inicial

### 1. Clonar y Configurar Variables de Entorno
```bash
# Clonar el repositorio
git clone <tu-repositorio>
cd ComPuter

# Copiar archivo de configuración
cp .env.example .env

# Editar variables de entorno (opcional para desarrollo)
# Los valores por defecto funcionan para desarrollo local
```

### 2. Estructura de Archivos Docker
```
ComPuter/
├── docker-compose.yml          # Configuración principal de servicios
├── docker-init.sql            # Script de inicialización de PostgreSQL
├── nginx.conf                 # Configuración del proxy reverso
├── .env.example              # Plantilla de variables de entorno
├── backend/
│   └── Dockerfile            # Imagen del backend FastAPI
└── frontend/
    └── Dockerfile            # Imagen del frontend React
```

## 🏗️ Comandos de Docker

### Desarrollo (Recomendado)
```bash
# Construir y levantar todos los servicios
docker-compose up --build

# Ejecutar en segundo plano
docker-compose up -d --build

# Ver logs en tiempo real
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### Producción
```bash
# Usar configuración de producción con Nginx
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

### Comandos Útiles
```bash
# Detener todos los servicios
docker-compose down

# Detener y eliminar volúmenes (⚠️ Elimina datos de la BD)
docker-compose down -v

# Reconstruir solo un servicio
docker-compose build backend
docker-compose up -d backend

# Ejecutar comandos dentro de un contenedor
docker-compose exec backend bash
docker-compose exec postgres psql -U computer_user -d computer_db

# Ver estado de los servicios
docker-compose ps

# Ver uso de recursos
docker stats
```

## 🗄️ Configuración de Base de Datos

### Acceso a PostgreSQL
```bash
# Conectar a la base de datos
docker-compose exec postgres psql -U computer_user -d computer_db

# Desde fuera del contenedor
psql -h localhost -p 5432 -U computer_user -d computer_db
```

### Comandos SQL Útiles
```sql
-- Ver tablas creadas
\dt

-- Ver estructura de una tabla
\d components

-- Ver datos de ejemplo
SELECT * FROM components LIMIT 5;

-- Verificar datos de entrenamiento NLP
SELECT * FROM nlp_training_data LIMIT 10;
```

### Backup y Restore
```bash
# Crear backup
docker-compose exec postgres pg_dump -U computer_user computer_db > backup.sql

# Restaurar backup
docker-compose exec -T postgres psql -U computer_user computer_db < backup.sql
```

## 🕷️ Sistema de Web Scraping

### Configuración
El sistema de scraping está integrado en el backend y se ejecuta automáticamente:

```python
# En backend/app/scraper.py
class ComponentScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'ComPuter-Bot/1.0'
        })
```

### Ejecutar Scraping Manualmente
```bash
# Entrar al contenedor del backend
docker-compose exec backend bash

# Ejecutar script de scraping
python -c "
from app.scraper import scrape_and_populate_database
scrape_and_populate_database()
"
```

### Configurar Scraping Automático
En el archivo `.env`:
```env
SCRAPING_ENABLED=true
SCRAPING_INTERVAL_HOURS=24
REQUEST_DELAY_SECONDS=2
```

### Fuentes de Datos Configuradas
1. **Newegg**: Procesadores, tarjetas gráficas, memorias RAM
2. **Amazon**: Componentes diversos con precios competitivos
3. **Datos sintéticos**: Para desarrollo y testing

## 🌐 Acceso a la Aplicación

### URLs de Desarrollo
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432
- **Redis** (opcional): localhost:6379

### URLs de Producción (con Nginx)
- **Aplicación**: http://localhost
- **API**: http://localhost/api
- **Documentación**: http://localhost/docs

## 🔧 Solución de Problemas

### Problemas Comunes

#### 1. Puerto ya en uso
```bash
# Ver qué proceso usa el puerto
netstat -tulpn | grep :3000
netstat -tulpn | grep :8000

# Cambiar puertos en docker-compose.yml si es necesario
```

#### 2. Error de conexión a la base de datos
```bash
# Verificar que PostgreSQL esté corriendo
docker-compose ps postgres

# Ver logs de PostgreSQL
docker-compose logs postgres

# Reiniciar solo PostgreSQL
docker-compose restart postgres
```

#### 3. Problemas de permisos (Linux/macOS)
```bash
# Dar permisos al directorio
sudo chown -R $USER:$USER .

# O ejecutar Docker con sudo (no recomendado)
sudo docker-compose up
```

#### 4. Error "No space left on device"
```bash
# Limpiar imágenes no utilizadas
docker system prune -a

# Limpiar volúmenes no utilizados
docker volume prune
```

### Logs y Debugging

#### Ver logs detallados
```bash
# Todos los servicios
docker-compose logs --tail=100 -f

# Solo errores
docker-compose logs --tail=100 | grep -i error

# Servicio específico con timestamps
docker-compose logs -t backend
```

#### Debugging del backend
```bash
# Entrar al contenedor
docker-compose exec backend bash

# Verificar variables de entorno
env | grep -E "(DATABASE|JWT|SECRET)"

# Probar conexión a la BD
python -c "
from app.database import engine
from sqlalchemy import text
with engine.connect() as conn:
    result = conn.execute(text('SELECT version()'))
    print(result.fetchone())
"
```

## 🚀 Despliegue en Producción

### 1. Configuración de Producción
```bash
# Crear archivo .env.prod
cp .env.example .env.prod

# Editar variables críticas
SECRET_KEY=tu-clave-super-secreta-de-produccion
JWT_SECRET_KEY=tu-jwt-secreto-de-produccion
DATABASE_URL=postgresql://user:pass@prod-db:5432/computer_db
DEBUG=false
ENVIRONMENT=production
```

### 2. Docker Compose para Producción
```bash
# Usar configuración de producción
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### 3. Configuración SSL (Opcional)
```bash
# Generar certificados SSL
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ssl/computer.key -out ssl/computer.crt

# Descomentar configuración HTTPS en nginx.conf
```

## 📊 Monitoreo y Mantenimiento

### Verificar Estado de Servicios
```bash
# Estado general
docker-compose ps

# Uso de recursos
docker stats

# Espacio en disco
docker system df
```

### Actualizaciones
```bash
# Actualizar imágenes
docker-compose pull

# Reconstruir con cambios
docker-compose up --build -d

# Actualización sin downtime (rolling update)
docker-compose up -d --no-deps backend
docker-compose up -d --no-deps frontend
```

### Backup Automatizado
```bash
# Script de backup (crear como backup.sh)
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec postgres pg_dump -U computer_user computer_db > "backup_${DATE}.sql"
```

## 🎯 Próximos Pasos

1. **Configurar CI/CD** con GitHub Actions
2. **Implementar monitoreo** con Prometheus/Grafana
3. **Configurar alertas** para errores críticos
4. **Optimizar imágenes Docker** para reducir tamaño
5. **Implementar health checks** más robustos

## 📞 Soporte

Si encuentras problemas:
1. Revisa los logs: `docker-compose logs`
2. Verifica la configuración: `docker-compose config`
3. Consulta la documentación de la API: http://localhost:8000/docs
4. Crea un issue en el repositorio del proyecto

---

**¡Listo!** Tu aplicación ComPuter debería estar corriendo en Docker. 🎉