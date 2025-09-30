"""
Script de prueba manual para el motor de IA de recomendaciones
"""
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Component, Specification, User, UserProfile
from crud import create_component, check_compatibility, generate_recommendations
from ai_engine import distribute_budget, adjust_budget_by_preferences

# Configuración de la base de datos de prueba
DATABASE_URL = "sqlite:///./test_manual.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

def crear_componentes_prueba():
    """Crear componentes de prueba para el motor de IA"""
    print("Creando componentes de prueba...")
    
    # CPU
    cpu1 = create_component(
        db=db,
        type="CPU",
        name="Intel Core i5-12600K",
        price=280.0,
        brand="Intel",
        performance_score=85,
        power_consumption=125,
        description="Procesador de gama media-alta con buen rendimiento",
        image_url="https://example.com/i5-12600k.jpg",
        specifications=[
            {"name": "cores", "value": "10"},
            {"name": "threads", "value": "16"},
            {"name": "base_clock", "value": "3.7 GHz"},
            {"name": "socket", "value": "LGA1700"}
        ]
    )
    
    cpu2 = create_component(
        db=db,
        type="CPU",
        name="AMD Ryzen 7 5800X",
        price=320.0,
        brand="AMD",
        performance_score=90,
        power_consumption=105,
        description="Procesador de alto rendimiento para gaming y productividad",
        image_url="https://example.com/ryzen7-5800x.jpg",
        specifications=[
            {"name": "cores", "value": "8"},
            {"name": "threads", "value": "16"},
            {"name": "base_clock", "value": "3.8 GHz"},
            {"name": "socket", "value": "AM4"}
        ]
    )
    
    # GPU
    gpu1 = create_component(
        db=db,
        type="GPU",
        name="NVIDIA RTX 3070",
        price=500.0,
        brand="NVIDIA",
        performance_score=88,
        power_consumption=220,
        description="Tarjeta gráfica de alto rendimiento para gaming en 1440p",
        image_url="https://example.com/rtx3070.jpg",
        specifications=[
            {"name": "memory", "value": "8GB GDDR6"},
            {"name": "cuda_cores", "value": "5888"},
            {"name": "power_connector", "value": "8-pin"}
        ]
    )
    
    gpu2 = create_component(
        db=db,
        type="GPU",
        name="AMD Radeon RX 6700 XT",
        price=450.0,
        brand="AMD",
        performance_score=82,
        power_consumption=230,
        description="Tarjeta gráfica con buen rendimiento para gaming en 1440p",
        image_url="https://example.com/rx6700xt.jpg",
        specifications=[
            {"name": "memory", "value": "12GB GDDR6"},
            {"name": "stream_processors", "value": "2560"},
            {"name": "power_connector", "value": "8-pin + 6-pin"}
        ]
    )
    
    # RAM
    ram1 = create_component(
        db=db,
        type="RAM",
        name="Corsair Vengeance LPX 16GB",
        price=75.0,
        brand="Corsair",
        performance_score=75,
        power_consumption=10,
        description="Memoria RAM DDR4 de buena calidad y rendimiento",
        image_url="https://example.com/corsair-vengeance.jpg",
        specifications=[
            {"name": "capacity", "value": "16GB"},
            {"name": "type", "value": "DDR4"},
            {"name": "speed", "value": "3200MHz"}
        ]
    )
    
    # Storage
    storage1 = create_component(
        db=db,
        type="Storage",
        name="Samsung 970 EVO Plus 1TB",
        price=120.0,
        brand="Samsung",
        performance_score=92,
        power_consumption=8,
        description="SSD NVMe de alta velocidad y fiabilidad",
        image_url="https://example.com/samsung-970evo.jpg",
        specifications=[
            {"name": "capacity", "value": "1TB"},
            {"name": "type", "value": "NVMe SSD"},
            {"name": "interface", "value": "PCIe 3.0 x4"}
        ]
    )
    
    # Motherboard
    motherboard1 = create_component(
        db=db,
        type="Motherboard",
        name="ASUS ROG Strix Z690-A",
        price=280.0,
        brand="ASUS",
        performance_score=85,
        power_consumption=15,
        description="Placa base de gama alta para procesadores Intel de 12ª generación",
        image_url="https://example.com/asus-z690.jpg",
        specifications=[
            {"name": "socket", "value": "LGA1700"},
            {"name": "chipset", "value": "Z690"},
            {"name": "memory_slots", "value": "4"},
            {"name": "max_memory", "value": "128GB"}
        ]
    )
    
    motherboard2 = create_component(
        db=db,
        type="Motherboard",
        name="MSI MAG B550 TOMAHAWK",
        price=180.0,
        brand="MSI",
        performance_score=80,
        power_consumption=12,
        description="Placa base de gama media para procesadores AMD Ryzen",
        image_url="https://example.com/msi-b550.jpg",
        specifications=[
            {"name": "socket", "value": "AM4"},
            {"name": "chipset", "value": "B550"},
            {"name": "memory_slots", "value": "4"},
            {"name": "max_memory", "value": "128GB"}
        ]
    )
    
    # PSU
    psu1 = create_component(
        db=db,
        type="PSU",
        name="Corsair RM750x",
        price=120.0,
        brand="Corsair",
        performance_score=88,
        power_consumption=0,
        description="Fuente de alimentación modular de 750W con certificación 80+ Gold",
        image_url="https://example.com/corsair-rm750x.jpg",
        specifications=[
            {"name": "wattage", "value": "750W"},
            {"name": "certification", "value": "80+ Gold"},
            {"name": "modular", "value": "Full"}
        ]
    )
    
    print("Componentes de prueba creados exitosamente.")
    return {
        "cpus": [cpu1, cpu2],
        "gpus": [gpu1, gpu2],
        "ram": [ram1],
        "storage": [storage1],
        "motherboards": [motherboard1, motherboard2],
        "psu": [psu1]
    }

def probar_distribucion_presupuesto():
    """Probar la distribución del presupuesto"""
    print("\n--- Prueba de distribución de presupuesto ---")
    budget = 1500
    usage_type = "gaming"
    
    distribution = distribute_budget(budget, usage_type)
    print(f"Presupuesto total: ${budget}")
    print(f"Tipo de uso: {usage_type}")
    print("Distribución:")
    for component_type, amount in distribution.items():
        print(f"  {component_type}: ${amount}")
    
    # Probar ajuste por preferencias
    print("\n--- Prueba de ajuste por preferencias ---")
    preferences = {"GPU": "high", "CPU": "medium", "Storage": "low"}
    adjusted = adjust_budget_by_preferences(distribution, preferences)
    print("Preferencias:", preferences)
    print("Distribución ajustada:")
    for component_type, amount in adjusted.items():
        print(f"  {component_type}: ${amount}")
    
    return distribution, adjusted

def probar_recomendaciones():
    """Probar la generación de recomendaciones"""
    print("\n--- Prueba de generación de recomendaciones ---")
    budget = 1500
    usage_type = "gaming"
    preferences = {"GPU": "high", "CPU": "medium"}
    
    recommendations = generate_recommendations(db, budget, usage_type, preferences)
    print(f"Recomendaciones para presupuesto ${budget}, uso {usage_type}, preferencias {preferences}:")
    for component_type, component in recommendations.items():
        print(f"  {component_type}: {component.name} (${component.price})")
    
    # Calcular presupuesto total utilizado
    total_spent = sum(component.price for component in recommendations.values())
    print(f"Presupuesto total utilizado: ${total_spent} de ${budget}")
    
    return recommendations

def probar_compatibilidad(components):
    """Probar la verificación de compatibilidad"""
    print("\n--- Prueba de verificación de compatibilidad ---")
    
    # Probar compatibilidad entre CPU Intel y placa base Intel
    cpu_intel = components["cpus"][0]  # Intel
    motherboard_intel = components["motherboards"][0]  # Socket LGA1700
    
    compatible = check_compatibility(db, cpu_intel.id, motherboard_intel.id)
    print(f"Compatibilidad entre {cpu_intel.name} y {motherboard_intel.name}: {compatible}")
    
    # Probar compatibilidad entre CPU AMD y placa base AMD
    cpu_amd = components["cpus"][1]  # AMD
    motherboard_amd = components["motherboards"][1]  # Socket AM4
    
    compatible = check_compatibility(db, cpu_amd.id, motherboard_amd.id)
    print(f"Compatibilidad entre {cpu_amd.name} y {motherboard_amd.name}: {compatible}")
    
    # Probar incompatibilidad entre CPU Intel y placa base AMD
    compatible = check_compatibility(db, cpu_intel.id, motherboard_amd.id)
    print(f"Compatibilidad entre {cpu_intel.name} y {motherboard_amd.name}: {compatible}")
    
    # Probar incompatibilidad entre CPU AMD y placa base Intel
    compatible = check_compatibility(db, cpu_amd.id, motherboard_intel.id)
    print(f"Compatibilidad entre {cpu_amd.name} y {motherboard_intel.name}: {compatible}")

def main():
    """Función principal para ejecutar todas las pruebas"""
    print("=== PRUEBA MANUAL DEL MOTOR DE IA DE RECOMENDACIONES ===\n")
    
    # Crear componentes de prueba
    components = crear_componentes_prueba()
    
    # Probar distribución de presupuesto
    distribution, adjusted = probar_distribucion_presupuesto()
    
    # Probar generación de recomendaciones
    recommendations = probar_recomendaciones()
    
    # Probar verificación de compatibilidad
    probar_compatibilidad(components)
    
    print("\n=== PRUEBAS COMPLETADAS ===")

if __name__ == "__main__":
    main()