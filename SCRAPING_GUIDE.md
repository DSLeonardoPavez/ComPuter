# Guía de Web Scraping - ComPuter

Esta guía explica cómo funciona el sistema de web scraping para obtener datos de componentes de PC de manera ética y eficiente.

## Descripción General

El sistema de scraping de ComPuter está diseñado para:
- Obtener información actualizada de componentes de PC
- Respetar las políticas de robots.txt de los sitios web
- Implementar rate limiting para evitar sobrecargar los servidores
- Procesar y normalizar datos de múltiples fuentes
- Almacenar información estructurada en la base de datos

## Arquitectura del Sistema

### Componentes Principales

1. **ComponentScraper** (`backend/app/scraper.py`)
   - Clase principal para el scraping
   - Manejo de sesiones HTTP
   - Rate limiting y retry logic

2. **Parsers Específicos**
   - `parse_newegg_product()`: Parser para Newegg
   - `parse_amazon_product()`: Parser para Amazon
   - `estimate_performance_score()`: Estimación de rendimiento

3. **Base de Datos**
   - Almacenamiento en PostgreSQL
   - Normalización de datos
   - Prevención de duplicados

## Configuración

### Variables de Entorno
```env
# En .env
SCRAPING_ENABLED=true
SCRAPING_INTERVAL_HOURS=24
USER_AGENT=ComPuter-Bot/1.0
REQUEST_DELAY_SECONDS=2
NEWEGG_API_KEY=tu-api-key-opcional
AMAZON_API_KEY=tu-api-key-opcional
```

### Dependencias Requeridas
```python
# En requirements.txt
requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
fake-useragent>=1.4.0
selenium>=4.15.0  # Para sitios con JavaScript
```

## Fuentes de Datos Configuradas

### 1. Newegg
```python
NEWEGG_URLS = {
    'processors': 'https://www.newegg.com/Processors-Desktops/Category/ID-343',
    'graphics_cards': 'https://www.newegg.com/Video-Cards-Video-Devices/Category/ID-38',
    'memory': 'https://www.newegg.com/Desktop-Memory/Category/ID-147',
    'motherboards': 'https://www.newegg.com/Motherboards/Category/ID-20',
    'storage': 'https://www.newegg.com/Hard-Drives/Category/ID-15'
}
```

**Datos extraídos:**
- Nombre del producto
- Precio actual y descuentos
- Especificaciones técnicas
- Imágenes del producto
- Ratings y reviews
- Disponibilidad

### 2. Amazon
```python
AMAZON_URLS = {
    'computers': 'https://www.amazon.com/s?k=computer+components',
    'processors': 'https://www.amazon.com/s?k=cpu+processor',
    'graphics': 'https://www.amazon.com/s?k=graphics+card'
}
```

**Datos extraídos:**
- Información básica del producto
- Precios y ofertas
- Especificaciones cuando están disponibles
- Imágenes
- Ratings de usuarios

## Uso del Sistema

### Ejecutar Scraping Manualmente

#### Desde Docker
```bash
# Entrar al contenedor del backend
docker-compose exec backend bash

# Ejecutar scraping completo
python -c "
from app.scraper import scrape_and_populate_database
scrape_and_populate_database()
"

# Scraping de una fuente específica
python -c "
from app.scraper import ComponentScraper
scraper = ComponentScraper()
scraper.scrape_newegg_components()
"
```

#### Desde Python directamente
```python
from app.scraper import ComponentScraper, scrape_and_populate_database

# Crear instancia del scraper
scraper = ComponentScraper()

# Scraping específico por tipo
processors = scraper.scrape_newegg_components('processors')
graphics_cards = scraper.scrape_amazon_components('graphics')

# Scraping completo y guardado en BD
scrape_and_populate_database()
```

### Programar Scraping Automático

#### Con Cron (Linux/macOS)
```bash
# Editar crontab
crontab -e

# Ejecutar cada 6 horas
0 /6  cd /path/to/ComPuter && docker-compose exec -T backend python -c "from app.scraper import scrape_and_populate_database; scrape_and_populate_database()"
```

#### Con Task Scheduler (Windows)
1. Abrir Task Scheduler
2. Crear tarea básica
3. Configurar trigger (cada 6 horas)
4. Acción: Ejecutar programa
5. Programa: `docker-compose`
6. Argumentos: `exec -T backend python -c "from app.scraper import scrape_and_populate_database; scrape_and_populate_database()"`

## Estructura de Datos

### Modelo de Componente
```python
class Component:
    id: int
    name: str
    type: ComponentType  # CPU, GPU, RAM, etc.
    brand: str
    model: str
    price: float
    specifications: dict  # JSON con specs técnicas
    performance_score: float  # 0-100
    power_consumption: int  # Watts
    image_url: str
    source_url: str
    last_updated: datetime
    availability: bool
```

### Especificaciones por Tipo

#### Procesadores (CPU)
```json
{
    "cores": 8,
    "threads": 16,
    "base_clock": "3.2 GHz",
    "boost_clock": "4.6 GHz",
    "socket": "AM4",
    "tdp": "65W",
    "cache_l3": "32MB",
    "architecture": "Zen 3"
}
```

#### Tarjetas Gráficas (GPU)
```json
{
    "memory": "8GB GDDR6",
    "memory_bus": "256-bit",
    "base_clock": "1605 MHz",
    "boost_clock": "1770 MHz",
    "cuda_cores": 2944,
    "rt_cores": 46,
    "power_connectors": "8-pin + 6-pin"
}
```

#### Memoria RAM
```json
{
    "capacity": "16GB",
    "type": "DDR4",
    "speed": "3200 MHz",
    "cas_latency": "CL16",
    "voltage": "1.35V",
    "form_factor": "DIMM"
}
```

## Consideraciones Éticas y Legales

### Buenas Prácticas Implementadas

1. **Respeto a robots.txt**
```python
def check_robots_txt(self, url):
    """Verificar si el scraping está permitido"""
    try:
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(f"{url}/robots.txt")
        rp.read()
        return rp.can_fetch(self.user_agent, url)
    except:
        return False
```

2. **Rate Limiting**
```python
def make_request(self, url):
    """Realizar request con rate limiting"""
    time.sleep(self.request_delay)  # 2 segundos por defecto
    response = self.session.get(url, timeout=30)
    return response
```

3. **User-Agent Identificable**
```python
headers = {
    'User-Agent': 'ComPuter-Bot/1.0 (Educational Project)',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
}
```

### Limitaciones y Restricciones

- **Frecuencia**: Máximo una vez cada 2 segundos por request
- **Volumen**: Máximo 1000 productos por sesión
- **Horarios**: Evitar horas pico (configurar en cron)
- **Contenido**: Solo información pública disponible

## 🔍 Procesamiento de Datos

### Limpieza y Normalización

```python
def clean_price(self, price_text):
    """Limpiar y convertir precios"""
    # Remover símbolos y espacios
    price = re.sub(r'[^\d.,]', '', price_text)
    # Convertir a float
    return float(price.replace(',', ''))

def normalize_specifications(self, specs):
    """Normalizar especificaciones"""
    normalized = {}
    for key, value in specs.items():
        # Convertir unidades a formato estándar
        if 'ghz' in key.lower():
            normalized[key] = self.convert_to_mhz(value)
        elif 'gb' in key.lower():
            normalized[key] = self.convert_to_mb(value)
    return normalized
```

### Estimación de Rendimiento

```python
def estimate_performance_score(self, component_type, specs):
    """Estimar score de rendimiento 0-100"""
    if component_type == 'CPU':
        # Basado en cores, frecuencia, arquitectura
        base_score = specs.get('cores', 4) * 10
        freq_bonus = specs.get('base_clock_mhz', 3000) / 100
        return min(100, base_score + freq_bonus)
    
    elif component_type == 'GPU':
        # Basado en CUDA cores, memoria, frecuencia
        cuda_score = specs.get('cuda_cores', 1000) / 50
        memory_score = specs.get('memory_gb', 4) * 5
        return min(100, cuda_score + memory_score)
```

## 📈 Monitoreo y Logs

### Configuración de Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraping.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('ComponentScraper')
```

### Métricas Importantes
- Productos procesados por minuto
- Tasa de éxito de requests
- Errores de parsing
- Tiempo de respuesta promedio
- Productos nuevos vs actualizados

### Dashboard de Monitoreo
```python
def get_scraping_stats():
    """Obtener estadísticas de scraping"""
    return {
        'total_components': db.query(Component).count(),
        'last_update': db.query(Component).order_by(Component.last_updated.desc()).first().last_updated,
        'components_by_type': db.query(Component.type, func.count()).group_by(Component.type).all(),
        'average_price_by_type': db.query(Component.type, func.avg(Component.price)).group_by(Component.type).all()
    }
```

## Manejo de Errores

### Errores Comunes y Soluciones

#### 1. Rate Limiting (429)
```python
def handle_rate_limit(self, response):
    if response.status_code == 429:
        retry_after = int(response.headers.get('Retry-After', 60))
        logger.warning(f"Rate limited. Waiting {retry_after} seconds")
        time.sleep(retry_after)
        return True
    return False
```

#### 2. Cambios en la Estructura HTML
```python
def robust_parse(self, soup, selectors):
    """Parser robusto con múltiples selectores"""
    for selector in selectors:
        try:
            element = soup.select_one(selector)
            if element:
                return element.get_text().strip()
        except Exception as e:
            logger.debug(f"Selector {selector} failed: {e}")
    return None
```

#### 3. Productos Duplicados
```python
def avoid_duplicates(self, product_data):
    """Evitar duplicados basado en nombre y modelo"""
    existing = db.query(Component).filter(
        Component.name == product_data['name'],
        Component.model == product_data['model']
    ).first()
    
    if existing:
        # Actualizar precio si es diferente
        if existing.price != product_data['price']:
            existing.price = product_data['price']
            existing.last_updated = datetime.utcnow()
        return existing
    else:
        return Component(**product_data)
```

## Actualización y Mantenimiento

### Actualizar Parsers
```python
# Crear nuevos parsers para sitios adicionales
def parse_bestbuy_product(self, soup):
    """Parser para Best Buy"""
    return {
        'name': soup.select_one('.sr-product-title').get_text(),
        'price': self.clean_price(soup.select_one('.sr-price').get_text()),
        'image_url': soup.select_one('.product-image img')['src']
    }
```

### Testing de Parsers
```python
import unittest

class TestScrapers(unittest.TestCase):
    def setUp(self):
        self.scraper = ComponentScraper()
    
    def test_newegg_parser(self):
        # Test con HTML de ejemplo
        html = """<div class="item-title">Test CPU</div>"""
        soup = BeautifulSoup(html, 'html.parser')
        result = self.scraper.parse_newegg_product(soup)
        self.assertEqual(result['name'], 'Test CPU')
```

## Soporte y Troubleshooting

### Comandos de Diagnóstico
```bash
# Ver logs de scraping
docker-compose logs backend | grep -i scraping

# Verificar conectividad
docker-compose exec backend python -c "
import requests
response = requests.get('https://www.newegg.com')
print(f'Status: {response.status_code}')
"

# Probar parser específico
docker-compose exec backend python -c "
from app.scraper import ComponentScraper
scraper = ComponentScraper()
print('Scraper initialized successfully')
"
```

### Problemas Frecuentes

1. **Timeout en requests**: Aumentar timeout en configuración
2. **Cambios en HTML**: Actualizar selectores CSS
3. **Bloqueo por IP**: Usar proxies rotativos
4. **Memoria insuficiente**: Procesar en lotes más pequeños

---

**¡El sistema de scraping está listo para obtener datos actualizados de componentes!** 🎉