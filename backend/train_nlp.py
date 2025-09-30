#!/usr/bin/env python3
"""
Script para entrenar el modelo NLP del chatbot ComPuter.
Ejecutar desde el directorio backend: python train_nlp.py
"""
import sys
import os

# Agregar el directorio actual al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.nlp_training import main

if __name__ == "__main__":
    print("=== Entrenamiento del Modelo NLP para ComPuter ===")
    print("Iniciando proceso de entrenamiento...")
    print()
    
    try:
        main()
        print("\n Entrenamiento completado exitosamente!")
        print("El modelo está listo para usar en el chatbot.")
    except Exception as e:
        print(f"\n Error durante el entrenamiento: {e}")
        sys.exit(1)