import os
import sys
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import Component, Specification
from app.ai_engine import AIRecommendationEngine, get_ai_engine

# Configuración de la base de datos de prueba
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class TestAIEngine(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Crear tablas en la base de datos de prueba
        Base.metadata.create_all(bind=engine)
        
        # Crear una sesión de prueba
        db = TestingSessionLocal()
        
        # Crear componentes de prueba
        components = [
            # CPUs
            Component(
                name="Intel Core i5-12400F",
                type="CPU",
                brand="Intel",
                model="i5-12400F",
                price=180.0,
                performance_score=75.0,
                power_consumption=65
            ),
            Component(
                name="AMD Ryzen 5 5600X",
                type="CPU",
                brand="AMD",
                model="Ryzen 5 5600X",
                price=200.0,
                performance_score=80.0,
                power_consumption=65
            ),
            Component(
                name="Intel Core i9-13900K",
                type="CPU",
                brand="Intel",
                model="i9-13900K",
                price=590.0,
                performance_score=100.0,
                power_consumption=125
            ),
            
            # GPUs
            Component(
                name="NVIDIA GeForce RTX 3060",
                type="GPU",
                brand="NVIDIA",
                model="RTX 3060",
                price=300.0,
                performance_score=70.0,
                power_consumption=170
            ),
            Component(
                name="AMD Radeon RX 6700 XT",
                type="GPU",
                brand="AMD",
                model="RX 6700 XT",
                price=350.0,
                performance_score=75.0,
                power_consumption=230
            ),
            Component(
                name="NVIDIA GeForce RTX 4090",
                type="GPU",
                brand="NVIDIA",
                model="RTX 4090",
                price=1600.0,
                performance_score=100.0,
                power_consumption=450
            ),
            
            # RAM
            Component(
                name="Corsair Vengeance 16GB DDR4",
                type="RAM",
                brand="Corsair",
                model="Vengeance",
                price=60.0,
                performance_score=70.0,
                power_consumption=10
            ),
            Component(
                name="G.Skill Trident Z 32GB DDR4",
                type="RAM",
                brand="G.Skill",
                model="Trident Z",
                price=120.0,
                performance_score=85.0,
                power_consumption=15
            ),
            
            # Almacenamiento
            Component(
                name="Samsung 970 EVO 1TB",
                type="Storage",
                brand="Samsung",
                model="970 EVO",
                price=100.0,
                performance_score=85.0,
                power_consumption=6
            ),
            Component(
                name="WD Blue 2TB HDD",
                type="Storage",
                brand="Western Digital",
                model="Blue",
                price=50.0,
                performance_score=40.0,
                power_consumption=8
            ),
            
            # Placas base
            Component(
                name="ASUS ROG Strix B550-F",
                type="Motherboard",
                brand="ASUS",
                model="ROG Strix B550-F",
                price=180.0,
                performance_score=80.0,
                power_consumption=15
            ),
            Component(
                name="MSI MAG B660 Tomahawk",
                type="Motherboard",
                brand="MSI",
                model="MAG B660 Tomahawk",
                price=190.0,
                performance_score=75.0,
                power_consumption=15
            ),
            
            # Fuentes de alimentación
            Component(
                name="EVGA 650W 80+ Gold",
                type="PSU",
                brand="EVGA",
                model="650W Gold",
                price=80.0,
                performance_score=75.0,
                power_consumption=0
            ),
            Component(
                name="Corsair RM850x",
                type="PSU",
                brand="Corsair",
                model="RM850x",
                price=140.0,
                performance_score=90.0,
                power_consumption=0
            ),
        ]
        
        # Añadir especificaciones a los componentes
        specifications = [
            # CPU Intel
            Specification(component_id=1, name="socket", value="LGA1700"),
            Specification(component_id=1, name="cores", value="6"),
            Specification(component_id=1, name="threads", value="12"),
            
            # CPU AMD
            Specification(component_id=2, name="socket", value="AM4"),
            Specification(component_id=2, name="cores", value="6"),
            Specification(component_id=2, name="threads", value="12"),
            
            # CPU Intel high-end
            Specification(component_id=3, name="socket", value="LGA1700"),
            Specification(component_id=3, name="cores", value="24"),
            Specification(component_id=3, name="threads", value="32"),
            
            # Placas base
            Specification(component_id=11, name="socket", value="AM4"),
            Specification(component_id=12, name="socket", value="LGA1700"),
        ]
        
        # Guardar en la base de datos
        for component in components:
            db.add(component)
        db.commit()
        
        # Refrescar para obtener IDs
        for component in components:
            db.refresh(component)
        
        # Añadir especificaciones
        for spec in specifications:
            db.add(spec)
        
        db.commit()
        db.close()
    
    @classmethod
    def tearDownClass(cls):
        # Eliminar la base de datos de prueba
        os.remove("./test.db")
    
    def setUp(self):
        # Crear una sesión para cada prueba
        self.db = TestingSessionLocal()
        self.ai_engine = get_ai_engine(self.db)
    
    def tearDown(self):
        self.db.close()
    
    def test_budget_distribution(self):
        """Prueba la distribución del presupuesto según el tipo de uso"""
        # Caso de gaming
        budget = 1000
        usage_type = "gaming"
        distribution = self.ai_engine._calculate_budget_distribution(budget, usage_type)
        
        # Verificar que la GPU recibe la mayor parte del presupuesto en gaming
        self.assertGreater(distribution["GPU"], distribution["CPU"])
        self.assertGreater(distribution["GPU"], distribution["RAM"])
        
        # Caso de workstation
        usage_type = "workstation"
        distribution = self.ai_engine._calculate_budget_distribution(budget, usage_type)
        
        # Verificar que la CPU recibe una parte importante del presupuesto en workstation
        self.assertGreater(distribution["CPU"], distribution["RAM"])
    
    def test_adjust_budget_for_preferences(self):
        """Prueba el ajuste del presupuesto según preferencias"""
        budget = 1000
        usage_type = "gaming"
        distribution = self.ai_engine._calculate_budget_distribution(budget, usage_type)
        
        # Preferencia por GPU de alta gama
        preferences = {"high_end_gpu": True}
        adjusted = self.ai_engine._adjust_budget_for_preferences(distribution, preferences)
        
        # Verificar que el presupuesto para GPU aumenta
        self.assertGreater(adjusted["GPU"], distribution["GPU"])
    
    def test_generate_recommendation(self):
        """Prueba la generación de recomendaciones completas"""
        budget = 1200
        usage_type = "gaming"
        
        # Generar recomendación
        recommendation = self.ai_engine.generate_recommendation(budget, usage_type)
        
        # Verificar que la recomendación contiene todos los tipos de componentes necesarios
        component_types = [comp.type for comp in recommendation["components"]]
        self.assertIn("CPU", component_types)
        self.assertIn("GPU", component_types)
        self.assertIn("RAM", component_types)
        self.assertIn("Storage", component_types)
        self.assertIn("Motherboard", component_types)
        self.assertIn("PSU", component_types)
        
        # Verificar que el precio total no excede el presupuesto
        self.assertLessEqual(recommendation["total_price"], budget * 1.05)  # 5% de margen
    
    def test_compatibility_check(self):
        """Prueba la verificación de compatibilidad entre componentes"""
        # Obtener componentes para la prueba
        cpu_intel = self.db.query(Component).filter(Component.name == "Intel Core i5-12400F").first()
        cpu_amd = self.db.query(Component).filter(Component.name == "AMD Ryzen 5 5600X").first()
        motherboard_amd = self.db.query(Component).filter(Component.name == "ASUS ROG Strix B550-F").first()
        
        # Verificar compatibilidad entre CPU AMD y placa base AMD
        components = {
            "CPU": cpu_amd,
            "Motherboard": motherboard_amd
        }
        result = self.ai_engine._check_compatibility(components)
        self.assertTrue(result["compatible"])
        
        # Verificar incompatibilidad entre CPU Intel y placa base AMD
        components = {
            "CPU": cpu_intel,
            "Motherboard": motherboard_amd
        }
        result = self.ai_engine._check_compatibility(components)
        self.assertFalse(result["compatible"])

if __name__ == "__main__":
    unittest.main()