"""
Datos de muestra para poblar la base de datos con componentes de PC.
"""
from sqlalchemy.orm import Session
from app.models import Component
from app.database import get_db

def create_sample_components(db: Session):
    """Crea componentes de muestra en la base de datos."""
    
    # CPUs
    cpus = [
        {
            "name": "AMD Ryzen 5 5600X",
            "type": "cpu",
            "brand": "AMD",
            "price": 299.99,
            "specifications": {
                "cores": 6,
                "threads": 12,
                "base_clock": "3.7 GHz",
                "boost_clock": "4.6 GHz",
                "socket": "AM4",
                "tdp": "65W"
            },
            "performance_score": 85,
            "compatibility_info": {"socket": "AM4", "memory_support": "DDR4"}
        },
        {
            "name": "Intel Core i5-12600K",
            "type": "cpu",
            "brand": "Intel",
            "price": 329.99,
            "specifications": {
                "cores": 10,
                "threads": 16,
                "base_clock": "3.7 GHz",
                "boost_clock": "4.9 GHz",
                "socket": "LGA1700",
                "tdp": "125W"
            },
            "performance_score": 88,
            "compatibility_info": {"socket": "LGA1700", "memory_support": "DDR4/DDR5"}
        },
        {
            "name": "AMD Ryzen 7 5800X3D",
            "type": "cpu",
            "brand": "AMD",
            "price": 449.99,
            "specifications": {
                "cores": 8,
                "threads": 16,
                "base_clock": "3.4 GHz",
                "boost_clock": "4.5 GHz",
                "socket": "AM4",
                "tdp": "105W"
            },
            "performance_score": 92,
            "compatibility_info": {"socket": "AM4", "memory_support": "DDR4"}
        }
    ]
    
    # GPUs
    gpus = [
        {
            "name": "NVIDIA RTX 4060 Ti",
            "type": "gpu",
            "brand": "NVIDIA",
            "price": 399.99,
            "specifications": {
                "memory": "8GB GDDR6",
                "memory_bus": "128-bit",
                "base_clock": "2310 MHz",
                "boost_clock": "2535 MHz",
                "cuda_cores": 4352
            },
            "performance_score": 80,
            "compatibility_info": {"pcie": "PCIe 4.0 x16", "power_requirement": "165W"}
        },
        {
            "name": "AMD Radeon RX 7600",
            "type": "gpu",
            "brand": "AMD",
            "price": 269.99,
            "specifications": {
                "memory": "8GB GDDR6",
                "memory_bus": "128-bit",
                "base_clock": "1720 MHz",
                "boost_clock": "2625 MHz",
                "stream_processors": 2048
            },
            "performance_score": 75,
            "compatibility_info": {"pcie": "PCIe 4.0 x16", "power_requirement": "165W"}
        },
        {
            "name": "NVIDIA RTX 4070",
            "type": "gpu",
            "brand": "NVIDIA",
            "price": 599.99,
            "specifications": {
                "memory": "12GB GDDR6X",
                "memory_bus": "192-bit",
                "base_clock": "1920 MHz",
                "boost_clock": "2475 MHz",
                "cuda_cores": 5888
            },
            "performance_score": 87,
            "compatibility_info": {"pcie": "PCIe 4.0 x16", "power_requirement": "200W"}
        }
    ]
    
    # RAM
    ram_modules = [
        {
            "name": "Corsair Vengeance LPX 16GB (2x8GB) DDR4-3200",
            "type": "ram",
            "brand": "Corsair",
            "price": 79.99,
            "specifications": {
                "capacity": "16GB",
                "type": "DDR4",
                "speed": "3200 MHz",
                "latency": "CL16",
                "voltage": "1.35V"
            },
            "performance_score": 78,
            "compatibility_info": {"type": "DDR4", "form_factor": "DIMM"}
        },
        {
            "name": "G.Skill Trident Z5 32GB (2x16GB) DDR5-5600",
            "type": "ram",
            "brand": "G.Skill",
            "price": 199.99,
            "specifications": {
                "capacity": "32GB",
                "type": "DDR5",
                "speed": "5600 MHz",
                "latency": "CL36",
                "voltage": "1.25V"
            },
            "performance_score": 90,
            "compatibility_info": {"type": "DDR5", "form_factor": "DIMM"}
        }
    ]
    
    # Storage
    storage_devices = [
        {
            "name": "Samsung 980 PRO 1TB NVMe SSD",
            "type": "storage",
            "brand": "Samsung",
            "price": 129.99,
            "specifications": {
                "capacity": "1TB",
                "type": "NVMe SSD",
                "interface": "PCIe 4.0 x4",
                "read_speed": "7000 MB/s",
                "write_speed": "5000 MB/s"
            },
            "performance_score": 95,
            "compatibility_info": {"interface": "M.2 2280", "protocol": "NVMe"}
        },
        {
            "name": "Western Digital Blue 2TB HDD",
            "type": "storage",
            "brand": "Western Digital",
            "price": 59.99,
            "specifications": {
                "capacity": "2TB",
                "type": "HDD",
                "interface": "SATA III",
                "rpm": "5400 RPM",
                "cache": "256MB"
            },
            "performance_score": 60,
            "compatibility_info": {"interface": "SATA III", "form_factor": "3.5\""}
        }
    ]
    
    # Motherboards
    motherboards = [
        {
            "name": "MSI B550 TOMAHAWK",
            "type": "motherboard",
            "brand": "MSI",
            "price": 179.99,
            "specifications": {
                "socket": "AM4",
                "chipset": "B550",
                "form_factor": "ATX",
                "memory_slots": 4,
                "max_memory": "128GB"
            },
            "performance_score": 82,
            "compatibility_info": {"socket": "AM4", "memory_support": "DDR4", "pcie_slots": "PCIe 4.0"}
        },
        {
            "name": "ASUS ROG STRIX Z690-E",
            "type": "motherboard",
            "brand": "ASUS",
            "price": 399.99,
            "specifications": {
                "socket": "LGA1700",
                "chipset": "Z690",
                "form_factor": "ATX",
                "memory_slots": 4,
                "max_memory": "128GB"
            },
            "performance_score": 90,
            "compatibility_info": {"socket": "LGA1700", "memory_support": "DDR4/DDR5", "pcie_slots": "PCIe 5.0"}
        }
    ]
    
    # PSUs
    psus = [
        {
            "name": "Corsair RM750x 750W 80+ Gold",
            "type": "psu",
            "brand": "Corsair",
            "price": 129.99,
            "specifications": {
                "wattage": "750W",
                "efficiency": "80+ Gold",
                "modular": "Fully Modular",
                "form_factor": "ATX"
            },
            "performance_score": 85,
            "compatibility_info": {"form_factor": "ATX", "connectors": "PCIe, SATA, CPU"}
        },
        {
            "name": "EVGA SuperNOVA 850 G5 850W 80+ Gold",
            "type": "psu",
            "brand": "EVGA",
            "price": 149.99,
            "specifications": {
                "wattage": "850W",
                "efficiency": "80+ Gold",
                "modular": "Fully Modular",
                "form_factor": "ATX"
            },
            "performance_score": 87,
            "compatibility_info": {"form_factor": "ATX", "connectors": "PCIe, SATA, CPU"}
        }
    ]
    
    # Combinar todos los componentes
    all_components = cpus + gpus + ram_modules + storage_devices + motherboards + psus
    
    # Crear componentes en la base de datos
    for comp_data in all_components:
        # Verificar si el componente ya existe
        existing = db.query(Component).filter(Component.name == comp_data["name"]).first()
        if not existing:
            component = Component(**comp_data)
            db.add(component)
    
    db.commit()
    print(f"Se han creado {len(all_components)} componentes de muestra en la base de datos.")

if __name__ == "__main__":
    # Ejecutar solo si se llama directamente
    db = next(get_db())
    create_sample_components(db)
    db.close()