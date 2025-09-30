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
    """Scraper para obtener datos de componentes de PC de diferentes sitios web."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.delay = 1  # Delay entre requests para ser respetuoso
    
    def scrape_newegg_components(self, component_type: str, max_pages: int = 5) -> List[ComponentData]:
        """Scraper para Newegg (ejemplo)."""
        components = []
        
        # URLs base para diferentes tipos de componentes
        base_urls = {
            'CPU': 'https://www.newegg.com/Processors-Desktops/Category/ID-34',
            'GPU': 'https://www.newegg.com/Video-Cards-Video-Devices/Category/ID-38',
            'RAM': 'https://www.newegg.com/Desktop-Memory/Category/ID-147',
            'Motherboard': 'https://www.newegg.com/Motherboards/Category/ID-20',
            'Storage': 'https://www.newegg.com/Internal-SSDs/Category/ID-636'
        }
        
        if component_type not in base_urls:
            logger.warning(f"Tipo de componente no soportado: {component_type}")
            return components
        
        try:
            for page in range(1, max_pages + 1):
                url = f"{base_urls[component_type]}?Page={page}"
                logger.info(f"Scraping página {page} de {component_type} en Newegg")
                
                response = self.session.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Buscar elementos de productos (esto es un ejemplo, los selectores reales pueden variar)
                product_items = soup.find_all('div', class_='item-container')
                
                for item in product_items:
                    try:
                        component = self._parse_newegg_item(item, component_type)
                        if component:
                            components.append(component)
                    except Exception as e:
                        logger.error(f"Error parsing item: {e}")
                        continue
                
                time.sleep(self.delay)
                
        except Exception as e:
            logger.error(f"Error scraping Newegg: {e}")
        
        return components
    
    def _parse_newegg_item(self, item, component_type: str) -> Optional[ComponentData]:
        """Parsea un elemento de producto de Newegg."""
        try:
            # Extraer nombre del producto
            name_elem = item.find('a', class_='item-title')
            if not name_elem:
                return None
            name = name_elem.get_text(strip=True)
            
            # Extraer precio
            price_elem = item.find('li', class_='price-current')
            price = 0.0
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                price_match = re.search(r'\$?([\d,]+\.?\d*)', price_text)
                if price_match:
                    price = float(price_match.group(1).replace(',', ''))
            
            # Extraer imagen
            img_elem = item.find('img')
            image_url = img_elem.get('src', '') if img_elem else ''
            
            # Extraer marca y modelo del nombre
            brand, model = self._extract_brand_model(name, component_type)
            
            # Crear especificaciones básicas
            specs = self._extract_specifications(item, component_type)
            
            return ComponentData(
                name=name,
                type=component_type,
                brand=brand,
                model=model,
                price=price,
                image_url=image_url,
                specifications=specs,
                performance_score=self._estimate_performance_score(name, component_type, price),
                power_consumption=self._estimate_power_consumption(component_type, specs)
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

def scrape_and_populate_database(db: Session, component_types: List[str] = None):
    """Función principal para hacer scraping y poblar la base de datos."""
    if component_types is None:
        component_types = ['CPU', 'GPU', 'RAM', 'Motherboard', 'Storage']
    
    scraper = ComponentScraper()
    
    for component_type in component_types:
        logger.info(f"Iniciando scraping para {component_type}")
        
        # Scraping de múltiples fuentes
        components = []
        
        # Newegg
        try:
            newegg_components = scraper.scrape_newegg_components(component_type, max_pages=2)
            components.extend(newegg_components)
            logger.info(f"Obtenidos {len(newegg_components)} componentes de Newegg")
        except Exception as e:
            logger.error(f"Error scraping Newegg: {e}")
        
        # Amazon (con términos de búsqueda específicos)
        search_terms = {
            'CPU': 'processor intel amd',
            'GPU': 'graphics card nvidia amd',
            'RAM': 'memory ddr4 ddr5',
            'Motherboard': 'motherboard gaming',
            'Storage': 'ssd nvme'
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
        
        # Guardar en base de datos
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
                
                # Verificar si ya existe un componente similar
                existing = db.query(models.Component).filter(
                    models.Component.name == component_data.name,
                    models.Component.brand == component_data.brand
                ).first()
                
                if not existing:
                    created_component = crud.create_component(db, component_create)
                    if created_component:
                        saved_count += 1
                
            except Exception as e:
                logger.error(f"Error guardando componente {component_data.name}: {e}")
        
        logger.info(f"Guardados {saved_count} componentes de tipo {component_type}")
        
        # Delay entre tipos de componentes
        time.sleep(2)
    
    logger.info("Scraping completado")

if __name__ == "__main__":
    # Ejemplo de uso
    from .database import SessionLocal
    
    db = SessionLocal()
    try:
        scrape_and_populate_database(db, ['CPU', 'GPU'])
    finally:
        db.close()