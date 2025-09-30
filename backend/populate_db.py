#!/usr/bin/env python3
"""
Script para poblar la base de datos con componentes de muestra.
Ejecutar desde el directorio backend: python populate_db.py
"""
import sys
import os

# Agregar el directorio actual al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, SessionLocal
from app.models import Base
from app.sample_data import create_sample_components

def init_database():
    """Inicializa la base de datos y crea las tablas."""
    print("Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas exitosamente.")

def populate_database():
    """Puebla la base de datos con componentes de muestra."""
    print("Poblando la base de datos con componentes de muestra...")
    
    db = SessionLocal()
    try:
        create_sample_components(db)
        print(" Base de datos poblada exitosamente.")
    except Exception as e:
        print(f" Error al poblar la base de datos: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def main():
    """Función principal."""
    print("=== Inicialización de la Base de Datos ComPuter ===")
    print()
    
    try:
        # Inicializar base de datos
        init_database()
        
        # Poblar con datos de muestra
        populate_database()
        
        print("\n🎉 Base de datos inicializada y poblada correctamente!")
        print("El sistema está listo para usar.")
        
    except Exception as e:
        print(f"\n❌ Error durante la inicialización: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()