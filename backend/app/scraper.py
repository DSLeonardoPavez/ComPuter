import requests
from bs4 import BeautifulSoup
import json
import time
import logging
from typing import List, Dict, Optional
from dataclasses import dataclass
import re
from urllib.parse import urljoin, urlparse
from sqlalchemy.orm import Session
import random

from . import models, schemas, crud

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ComponentData:
    name: str
    type: str
    brand: str
    model: str
    price: float
    description: str = ""
    image_url: str = ""
    specifications: Dict[str, str] = None
    performance_score: float = 0.0
    power_consumption: int = 0

class ComponentScraper:
    """Scraper mejorado para obtener datos de componentes de PC de diferentes sitios web."""
    
    def __init__(self):
        self.session = requests.Session()
        # Rotar User-Agents para evitar detección
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]
        self.session.headers.update({
            'User-Agent': random.choice(self.user_agents)
        })
        self.delay = random.uniform(1, 3)  # Delay aleatorio entre requests
    
    def scrape_newegg_components(self, component_type: str, max_pages: int = 5) -> List[ComponentData]:
        """Scraper mejorado para Newegg."""
        components = []
        
        # URLs base para diferentes tipos de componentes
        base_urls = {
            'CPU': 'https://www.newegg.com/Processors-Desktops/Category/ID-34',
            'GPU': 'https://www.newegg.com/Video-Cards-Video-Devices/Category/ID-38',
            'RAM': 'https://www.newegg.com/Desktop-Memory/Category/ID-147',
            'Motherboard': 'https://www.newegg.com/Motherboards/Category/ID-20',
            'Storage': 'https://www.newegg.com/Internal-SSDs/Category/ID-636',
            'PSU': 'https://www.newegg.com/Power-Supplies/Category/ID-58',
            'Case': 'https://www.newegg.com/Cases/Category/ID-7',
            'Cooler': 'https://www.newegg.com/Fans-PC-Cooling/Category/ID-35'
        }
        
        if component_type not in base_urls:
            logger.warning(f"Tipo de componente no soportado: {component_type}")
            return components
        
        try:
            for page in range(1, max_pages + 1):
                # Rotar User-Agent para cada página
                self.session.headers.update({
                    'User-Agent': random.choice(self.user_agents)
                })
                
                url = f"{base_urls[component_type]}?Page={page}"
                logger.info(f"Scraping página {page} de {component_type} en Newegg")
                
                response = self.session.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Buscar elementos de productos con múltiples selectores
                product_items = (soup.find_all('div', class_='item-container') or 
                               soup.find_all('div', class_='item-cell') or
                               soup.find_all('div', {'data-testid': 'product-item'}))
                
                for item in product_items:
                    try:
                        component = self._parse_newegg_item(item, component_type)
                        if component:
                            components.append(component)
                    except Exception as e:
                        logger.error(f"Error parsing item: {e}")
                        continue
                
                # Delay aleatorio entre páginas
                time.sleep(random.uniform(1, 3))
                
        except Exception as e:
            logger.error(f"Error scraping Newegg: {e}")
        
        return components
    
    def _parse_newegg_item(self, item, component_type: str) -> Optional[ComponentData]:
        """Parsea un elemento de producto de Newegg con mejor extracción."""
        try:
            # Extraer nombre del producto con múltiples selectores
            name_elem = (item.find('a', class_='item-title') or 
                        item.find('h3') or 
                        item.find('a', {'data-testid': 'product-title'}))
            if not name_elem:
                return None
            name = name_elem.get_text(strip=True)
            
            # Extraer precio con múltiples selectores
            price_elem = (item.find('li', class_='price-current') or 
                         item.find('span', class_='price-current') or
                         item.find('div', class_='price'))
            price = 0.0
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                price_match = re.search(r'\$?([\d,]+\.?\d*)', price_text)
                if price_match:
                    price = float(price_match.group(1).replace(',', ''))
            
            # Extraer imagen
            img_elem = item.find('img')
            image_url = ''
            if img_elem:
                image_url = img_elem.get('src') or img_elem.get('data-src', '')
            
            # Extraer descripción
            desc_elem = item.find('p', class_='item-promo')
            description = desc_elem.get_text(strip=True) if desc_elem else ""
            
            # Extraer marca y modelo del nombre
            brand, model = self._extract_brand_model(name, component_type)
            
            # Crear especificaciones mejoradas
            specs = self._extract_specifications_enhanced(item, component_type, name)
            
            return ComponentData(
                name=name,
                type=component_type,
                brand=brand,
                model=model,
                price=price,
                description=description,
                image_url=image_url,
                specifications=specs,
                performance_score=self._estimate_performance_score_enhanced(name, component_type, price, specs),
                power_consumption=self._estimate_power_consumption_enhanced(component_type, specs, name)
            )
            
        except Exception as e:
            logger.error(f"Error parsing Newegg item: {e}")
            return None
    
    def scrape_amazon_components(self, component_type: str, search_term: str, max_pages: int = 3) -> List[ComponentData]:
        """Scraper para Amazon (ejemplo básico)."""
        components = []
        
        try:
            for page in range(1, max_pages + 1):
                url = f"https://www.amazon.com/s?k={search_term}&page={page}"
                logger.info(f"Scraping página {page} de Amazon para: {search_term}")
                
                response = self.session.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Buscar productos
                product_items = soup.find_all('div', {'data-component-type': 's-search-result'})
                
                for item in product_items:
                    try:
                        component = self._parse_amazon_item(item, component_type)
                        if component:
                            components.append(component)
                    except Exception as e:
                        logger.error(f"Error parsing Amazon item: {e}")
                        continue
                
                time.sleep(self.delay)
                
        except Exception as e:
            logger.error(f"Error scraping Amazon: {e}")
        
        return components
    
    def _parse_amazon_item(self, item, component_type: str) -> Optional[ComponentData]:
        """Parsea un elemento de producto de Amazon."""
        try:
            # Extraer nombre
            name_elem = item.find('h2', class_='a-size-mini')
            if not name_elem:
                name_elem = item.find('span', class_='a-size-medium')
            if not name_elem:
                return None
            
            name = name_elem.get_text(strip=True)
            
            # Extraer precio
            price_elem = item.find('span', class_='a-price-whole')
            price = 0.0
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                price_match = re.search(r'([\d,]+)', price_text)
                if price_match:
                    price = float(price_match.group(1).replace(',', ''))
            
            # Extraer imagen
            img_elem = item.find('img', class_='s-image')
            image_url = img_elem.get('src', '') if img_elem else ''
            
            # Extraer marca y modelo
            brand, model = self._extract_brand_model(name, component_type)
            
            return ComponentData(
                name=name,
                type=component_type,
                brand=brand,
                model=model,
                price=price,
                image_url=image_url,
                specifications={},
                performance_score=self._estimate_performance_score(name, component_type, price),
                power_consumption=self._estimate_power_consumption(component_type, {})
            )
            
        except Exception as e:
            logger.error(f"Error parsing Amazon item: {e}")
            return None
    
    def _extract_brand_model(self, name: str, component_type: str) -> tuple:
        """Extrae marca y modelo del nombre del producto."""
        # Marcas conocidas por tipo de componente
        brands = {
            'CPU': ['Intel', 'AMD', 'Ryzen', 'Core'],
            'GPU': ['NVIDIA', 'AMD', 'GeForce', 'Radeon', 'RTX', 'GTX', 'RX'],
            'RAM': ['Corsair', 'G.Skill', 'Kingston', 'Crucial', 'Patriot'],
            'Motherboard': ['ASUS', 'MSI', 'Gigabyte', 'ASRock', 'EVGA'],
            'Storage': ['Samsung', 'Western Digital', 'Seagate', 'Crucial', 'Kingston']
        }
        
        brand = "Unknown"
        model = name
        
        if component_type in brands:
            for b in brands[component_type]:
                if b.lower() in name.lower():
                    brand = b
                    break
        
        # Limpiar el modelo removiendo la marca
        if brand != "Unknown":
            model = name.replace(brand, '').strip()
        
        return brand, model
    
    def _extract_specifications(self, item, component_type: str) -> Dict[str, str]:
        """Extrae especificaciones del elemento HTML."""
        specs = {}
        
        # Buscar especificaciones en el HTML
        spec_elements = item.find_all('span', class_='item-features')
        for spec_elem in spec_elements:
            spec_text = spec_elem.get_text(strip=True)
            # Parsear especificaciones básicas
            if 'GHz' in spec_text:
                specs['frequency'] = spec_text
            elif 'GB' in spec_text and component_type == 'RAM':
                specs['capacity'] = spec_text
            elif 'Socket' in spec_text:
                specs['socket'] = spec_text
        
        return specs
    
    def _estimate_performance_score(self, name: str, component_type: str, price: float) -> float:
        """Estima un score de rendimiento basado en el nombre y precio."""
        base_score = min(price / 100, 10.0)  # Score base basado en precio
        
        # Ajustes por palabras clave en el nombre
        performance_keywords = {
            'CPU': ['i9', 'i7', 'Ryzen 9', 'Ryzen 7', 'Ultra', 'Extreme'],
            'GPU': ['RTX 4090', 'RTX 4080', 'RTX 3080', 'RX 7900', 'Ti', 'Super'],
            'RAM': ['3200', '3600', '4000', 'RGB', 'Gaming'],
            'Storage': ['NVMe', 'M.2', 'Pro', 'Evo']
        }
        
        if component_type in performance_keywords:
            for keyword in performance_keywords[component_type]:
                if keyword.lower() in name.lower():
                    base_score += 1.0
        
        return min(base_score, 10.0)
    
    def _estimate_power_consumption(self, component_type: str, specs: Dict[str, str]) -> int:
        """Estima el consumo de energía del componente."""
        base_consumption = {
            'CPU': 65,
            'GPU': 200,
            'RAM': 5,
            'Motherboard': 20,
            'Storage': 5,
            'PSU': 0
        }
        
        return base_consumption.get(component_type, 10)

    def scrape_pcpartpicker_components(self, component_type: str, max_pages: int = 3) -> List[ComponentData]:
        """Nuevo scraper para PCPartPicker."""
        components = []
        
        # URLs para PCPartPicker
        base_urls = {
            'CPU': 'https://pcpartpicker.com/products/cpu/',
            'GPU': 'https://pcpartpicker.com/products/video-card/',
            'RAM': 'https://pcpartpicker.com/products/memory/',
            'Motherboard': 'https://pcpartpicker.com/products/motherboard/',
            'Storage': 'https://pcpartpicker.com/products/internal-hard-drive/',
            'PSU': 'https://pcpartpicker.com/products/power-supply/',
            'Case': 'https://pcpartpicker.com/products/case/',
            'Cooler': 'https://pcpartpicker.com/products/cpu-cooler/'
        }
        
        if component_type not in base_urls:
            return components
        
        try:
            for page in range(1, max_pages + 1):
                self.session.headers.update({
                    'User-Agent': random.choice(self.user_agents)
                })
                
                url = f"{base_urls[component_type]}#page={page}"
                logger.info(f"Scraping página {page} de {component_type} en PCPartPicker")
                
                response = self.session.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Buscar productos en PCPartPicker
                product_rows = soup.find_all('tr', class_='tr__product')
                
                for row in product_rows:
                    try:
                        component = self._parse_pcpartpicker_item(row, component_type)
                        if component:
                            components.append(component)
                    except Exception as e:
                        logger.error(f"Error parsing PCPartPicker item: {e}")
                        continue
                
                time.sleep(random.uniform(2, 4))
                
        except Exception as e:
            logger.error(f"Error scraping PCPartPicker: {e}")
        
        return components
    
    def _parse_pcpartpicker_item(self, row, component_type: str) -> Optional[ComponentData]:
        """Parsea un elemento de PCPartPicker."""
        try:
            # Extraer nombre
            name_elem = row.find('td', class_='td__name')
            if not name_elem:
                return None
            name_link = name_elem.find('a')
            name = name_link.get_text(strip=True) if name_link else ""
            
            # Extraer precio
            price_elem = row.find('td', class_='td__price')
            price = 0.0
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                price_match = re.search(r'\$?([\d,]+\.?\d*)', price_text)
                if price_match:
                    price = float(price_match.group(1).replace(',', ''))
            
            # Extraer especificaciones de las columnas
            spec_cells = row.find_all('td')
            specs = {}
            for cell in spec_cells:
                cell_text = cell.get_text(strip=True)
                if 'GHz' in cell_text:
                    specs['frequency'] = cell_text
                elif 'GB' in cell_text and component_type == 'RAM':
                    specs['capacity'] = cell_text
                elif 'W' in cell_text and component_type == 'PSU':
                    specs['wattage'] = cell_text
            
            brand, model = self._extract_brand_model(name, component_type)
            
            return ComponentData(
                name=name,
                type=component_type,
                brand=brand,
                model=model,
                price=price,
                specifications=specs,
                performance_score=self._estimate_performance_score_enhanced(name, component_type, price, specs),
                power_consumption=self._estimate_power_consumption_enhanced(component_type, specs, name)
            )
            
        except Exception as e:
            logger.error(f"Error parsing PCPartPicker item: {e}")
            return None

    def _extract_specifications_enhanced(self, item, component_type: str, name: str) -> Dict[str, str]:
        """Extrae especificaciones mejoradas del elemento HTML."""
        specs = {}
        
        # Buscar especificaciones en el HTML
        spec_elements = item.find_all(['span', 'div', 'li'], class_=re.compile(r'(spec|feature|detail)'))
        
        for spec_elem in spec_elements:
            spec_text = spec_elem.get_text(strip=True)
            
            # Parsear especificaciones por tipo de componente
            if component_type == 'CPU':
                if re.search(r'(\d+\.?\d*)\s*GHz', spec_text):
                    specs['base_clock'] = spec_text
                if re.search(r'(\d+)\s*cores?', spec_text, re.IGNORECASE):
                    specs['cores'] = spec_text
                if 'Socket' in spec_text:
                    specs['socket'] = spec_text
                if re.search(r'(\d+)nm', spec_text):
                    specs['process'] = spec_text
                    
            elif component_type == 'GPU':
                if re.search(r'(\d+)\s*GB', spec_text):
                    specs['memory'] = spec_text
                if 'GDDR' in spec_text:
                    specs['memory_type'] = spec_text
                if re.search(r'(\d+)\s*MHz', spec_text):
                    specs['memory_clock'] = spec_text
                    
            elif component_type == 'RAM':
                if re.search(r'(\d+)\s*GB', spec_text):
                    specs['capacity'] = spec_text
                if 'DDR' in spec_text:
                    specs['type'] = spec_text
                if re.search(r'(\d+)\s*MHz', spec_text):
                    specs['speed'] = spec_text
                    
            elif component_type == 'Storage':
                if re.search(r'(\d+)\s*(GB|TB)', spec_text):
                    specs['capacity'] = spec_text
                if 'NVMe' in spec_text or 'M.2' in spec_text:
                    specs['interface'] = spec_text
                if re.search(r'(\d+)\s*MB/s', spec_text):
                    specs['read_speed'] = spec_text
        
        # Extraer especificaciones adicionales del nombre del producto
        if component_type == 'CPU':
            if 'i9' in name or 'Ryzen 9' in name:
                specs['tier'] = 'High-end'
            elif 'i7' in name or 'Ryzen 7' in name:
                specs['tier'] = 'Performance'
            elif 'i5' in name or 'Ryzen 5' in name:
                specs['tier'] = 'Mainstream'
                
        elif component_type == 'GPU':
            if any(x in name for x in ['4090', '4080', '7900']):
                specs['tier'] = 'Flagship'
            elif any(x in name for x in ['4070', '4060', '7800', '7700']):
                specs['tier'] = 'High-end'
            elif any(x in name for x in ['3060', '6600', '6500']):
                specs['tier'] = 'Mainstream'
        
        return specs
    
    def _estimate_performance_score_enhanced(self, name: str, component_type: str, price: float, specs: Dict[str, str]) -> float:
        """Estima un score de rendimiento mejorado."""
        base_score = min(price / 200, 8.0)  # Score base más conservador
        
        # Ajustes específicos por tipo de componente
        if component_type == 'CPU':
            if any(x in name.upper() for x in ['I9', 'RYZEN 9']):
                base_score += 2.0
            elif any(x in name.upper() for x in ['I7', 'RYZEN 7']):
                base_score += 1.5
            elif any(x in name.upper() for x in ['I5', 'RYZEN 5']):
                base_score += 1.0
                
            # Bonus por especificaciones
            if 'cores' in specs:
                core_match = re.search(r'(\d+)', specs['cores'])
                if core_match and int(core_match.group(1)) >= 8:
                    base_score += 0.5
                    
        elif component_type == 'GPU':
            gpu_tiers = {
                '4090': 3.0, '4080': 2.5, '4070': 2.0, '4060': 1.5,
                '7900': 2.8, '7800': 2.2, '7700': 1.8, '6600': 1.2
            }
            for tier, bonus in gpu_tiers.items():
                if tier in name:
                    base_score += bonus
                    break
                    
        elif component_type == 'RAM':
            if 'DDR5' in name:
                base_score += 1.0
            elif 'DDR4' in name:
                base_score += 0.5
                
            # Bonus por velocidad
            speed_match = re.search(r'(\d+)', specs.get('speed', ''))
            if speed_match and int(speed_match.group(1)) >= 3200:
                base_score += 0.5
        
        return min(base_score, 10.0)
    
    def _estimate_power_consumption_enhanced(self, component_type: str, specs: Dict[str, str], name: str) -> int:
        """Estima el consumo de energía mejorado."""
        base_consumption = {
            'CPU': 65,
            'GPU': 200,
            'RAM': 5,
            'Motherboard': 20,
            'Storage': 5,
            'PSU': 0,
            'Case': 0,
            'Cooler': 10
        }
        
        consumption = base_consumption.get(component_type, 10)
        
        # Ajustes específicos
        if component_type == 'CPU':
            if any(x in name.upper() for x in ['I9', 'RYZEN 9']):
                consumption = 125
            elif any(x in name.upper() for x in ['I7', 'RYZEN 7']):
                consumption = 95
            elif 'T' in name:  # Versiones de bajo consumo
                consumption = 35
                
        elif component_type == 'GPU':
            gpu_power = {
                '4090': 450, '4080': 320, '4070': 200, '4060': 115,
                '7900': 355, '7800': 263, '7700': 245, '6600': 132
            }
            for model, power in gpu_power.items():
                if model in name:
                    consumption = power
                    break
        
        return consumption

def scrape_and_populate_database(db: Session, component_types: List[str] = None):
    """Función principal mejorada para hacer scraping y poblar la base de datos."""
    if component_types is None:
        component_types = ['CPU', 'GPU', 'RAM', 'Motherboard', 'Storage', 'PSU', 'Case', 'Cooler']
    
    scraper = ComponentScraper()
    
    for component_type in component_types:
        logger.info(f"Iniciando scraping para {component_type}")
        
        # Scraping de múltiples fuentes mejorado
        components = []
        
        # Newegg
        try:
            newegg_components = scraper.scrape_newegg_components(component_type, max_pages=3)
            components.extend(newegg_components)
            logger.info(f"Obtenidos {len(newegg_components)} componentes de Newegg")
        except Exception as e:
            logger.error(f"Error scraping Newegg: {e}")
        
        # PCPartPicker
        try:
            pcpp_components = scraper.scrape_pcpartpicker_components(component_type, max_pages=2)
            components.extend(pcpp_components)
            logger.info(f"Obtenidos {len(pcpp_components)} componentes de PCPartPicker")
        except Exception as e:
            logger.error(f"Error scraping PCPartPicker: {e}")
        
        # Amazon (con términos de búsqueda específicos)
        search_terms = {
            'CPU': 'processor intel amd ryzen core',
            'GPU': 'graphics card nvidia amd geforce radeon',
            'RAM': 'memory ddr4 ddr5 gaming',
            'Motherboard': 'motherboard gaming asus msi',
            'Storage': 'ssd nvme m.2 samsung crucial',
            'PSU': 'power supply modular 80+ gold',
            'Case': 'pc case gaming mid tower',
            'Cooler': 'cpu cooler air liquid aio'
        }
        
        if component_type in search_terms:
            try:
                amazon_components = scraper.scrape_amazon_components(
                    component_type, 
                    search_terms[component_type], 
                    max_pages=2
                )
                components.extend(amazon_components)
                logger.info(f"Obtenidos {len(amazon_components)} componentes de Amazon")
            except Exception as e:
                logger.error(f"Error scraping Amazon: {e}")
        
        # Guardar en base de datos con mejor manejo de duplicados
        saved_count = 0
        for component_data in components:
            try:
                # Convertir a schema de Pydantic
                specifications = [
                    schemas.SpecificationCreate(name=k, value=v)
                    for k, v in (component_data.specifications or {}).items()
                ]
                
                component_create = schemas.ComponentCreate(
                    name=component_data.name,
                    type=component_data.type,
                    brand=component_data.brand,
                    model=component_data.model,
                    price=component_data.price,
                    description=component_data.description,
                    image_url=component_data.image_url,
                    performance_score=component_data.performance_score,
                    power_consumption=component_data.power_consumption,
                    specifications=specifications
                )
                
                # Verificar duplicados más inteligente
                existing = db.query(models.Component).filter(
                    models.Component.name.ilike(f"%{component_data.name[:50]}%"),
                    models.Component.brand == component_data.brand,
                    models.Component.type == component_data.type
                ).first()
                
                if not existing:
                    created_component = crud.create_component(db, component_create)
                    if created_component:
                        saved_count += 1
                else:
                    # Actualizar precio si es diferente
                    if existing.price != component_data.price and component_data.price > 0:
                        existing.price = component_data.price
                        db.commit()
                
            except Exception as e:
                logger.error(f"Error guardando componente {component_data.name}: {e}")
        
        logger.info(f"Guardados {saved_count} componentes nuevos de tipo {component_type}")
        
        # Delay entre tipos de componentes
        time.sleep(random.uniform(3, 5))
    
    logger.info("Scraping completado")

if __name__ == "__main__":
    # Ejemplo de uso
    from .database import SessionLocal
    
    db = SessionLocal()
    try:
        scrape_and_populate_database(db)
    finally:
        db.close()