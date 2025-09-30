"""
Módulo de entrenamiento NLP para el chatbot de ComPuter.
Entrena el modelo con datos específicos de componentes de PC.
"""
import json
import re
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

class NLPTrainer:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.pipeline = None
        self.intent_labels = [
            'recommendation',
            'component_info',
            'compatibility',
            'budget',
            'usage_type',
            'comparison',
            'greeting',
            'goodbye'
        ]
        
    def get_training_data(self) -> List[Dict[str, str]]:
        """Genera datos de entrenamiento específicos para componentes de PC."""
        training_data = [
            # Recomendaciones
            {"text": "necesito una recomendación de PC", "intent": "recommendation"},
            {"text": "qué PC me recomiendas", "intent": "recommendation"},
            {"text": "ayúdame a elegir componentes", "intent": "recommendation"},
            {"text": "quiero armar una PC", "intent": "recommendation"},
            {"text": "recomiéndame una configuración", "intent": "recommendation"},
            {"text": "necesito ayuda para elegir componentes", "intent": "recommendation"},
            {"text": "qué configuración me sugieres", "intent": "recommendation"},
            {"text": "ayúdame a armar mi PC", "intent": "recommendation"},
            
            # Información de componentes
            {"text": "qué es un procesador", "intent": "component_info"},
            {"text": "cuáles son las especificaciones del RTX 4070", "intent": "component_info"},
            {"text": "información sobre tarjetas gráficas", "intent": "component_info"},
            {"text": "qué diferencia hay entre DDR4 y DDR5", "intent": "component_info"},
            {"text": "cuánta RAM necesito", "intent": "component_info"},
            {"text": "qué es mejor SSD o HDD", "intent": "component_info"},
            {"text": "explícame qué hace la placa madre", "intent": "component_info"},
            {"text": "cuántos watts necesita mi fuente", "intent": "component_info"},
            {"text": "qué significa TDP en procesadores", "intent": "component_info"},
            {"text": "diferencias entre AMD e Intel", "intent": "component_info"},
            
            # Compatibilidad
            {"text": "es compatible este procesador con esta placa", "intent": "compatibility"},
            {"text": "funciona esta RAM con mi motherboard", "intent": "compatibility"},
            {"text": "puedo usar esta GPU con mi fuente", "intent": "compatibility"},
            {"text": "verificar compatibilidad", "intent": "compatibility"},
            {"text": "estos componentes son compatibles", "intent": "compatibility"},
            {"text": "mi placa soporta este procesador", "intent": "compatibility"},
            {"text": "check compatibility", "intent": "compatibility"},
            
            # Presupuesto
            {"text": "tengo un presupuesto de 1000 dólares", "intent": "budget"},
            {"text": "mi presupuesto es limitado", "intent": "budget"},
            {"text": "qué puedo comprar con 500 dólares", "intent": "budget"},
            {"text": "opciones económicas", "intent": "budget"},
            {"text": "PC barata", "intent": "budget"},
            {"text": "configuración de bajo costo", "intent": "budget"},
            {"text": "presupuesto máximo 800", "intent": "budget"},
            
            # Tipo de uso
            {"text": "para gaming", "intent": "usage_type"},
            {"text": "uso profesional", "intent": "usage_type"},
            {"text": "para juegos", "intent": "usage_type"},
            {"text": "trabajo de oficina", "intent": "usage_type"},
            {"text": "edición de video", "intent": "usage_type"},
            {"text": "streaming", "intent": "usage_type"},
            {"text": "programación", "intent": "usage_type"},
            {"text": "diseño gráfico", "intent": "usage_type"},
            {"text": "uso básico", "intent": "usage_type"},
            {"text": "workstation", "intent": "usage_type"},
            
            # Comparaciones
            {"text": "compara estos procesadores", "intent": "comparison"},
            {"text": "qué es mejor entre estas opciones", "intent": "comparison"},
            {"text": "diferencias entre estos componentes", "intent": "comparison"},
            {"text": "cuál me conviene más", "intent": "comparison"},
            {"text": "versus", "intent": "comparison"},
            {"text": "comparación", "intent": "comparison"},
            
            # Saludos
            {"text": "hola", "intent": "greeting"},
            {"text": "buenos días", "intent": "greeting"},
            {"text": "hi", "intent": "greeting"},
            {"text": "hey", "intent": "greeting"},
            {"text": "buenas", "intent": "greeting"},
            
            # Despedidas
            {"text": "adiós", "intent": "goodbye"},
            {"text": "gracias", "intent": "goodbye"},
            {"text": "bye", "intent": "goodbye"},
            {"text": "hasta luego", "intent": "goodbye"},
            {"text": "nos vemos", "intent": "goodbye"}
        ]
        
        return training_data
    
    def preprocess_text(self, text: str) -> str:
        """Preprocesa el texto para el entrenamiento."""
        # Convertir a minúsculas
        text = text.lower()
        
        # Remover caracteres especiales pero mantener espacios
        text = re.sub(r'[^\w\s]', '', text)
        
        # Remover espacios extra
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def train_model(self) -> Dict[str, Any]:
        """Entrena el modelo NLP con los datos de componentes."""
        print("Iniciando entrenamiento del modelo NLP...")
        
        # Obtener datos de entrenamiento
        training_data = self.get_training_data()
        
        # Preparar datos
        texts = [self.preprocess_text(item["text"]) for item in training_data]
        labels = [item["intent"] for item in training_data]
        
        # Dividir datos
        X_train, X_test, y_train, y_test = train_test_split(
            texts, labels, test_size=0.2, random_state=42, stratify=labels
        )
        
        # Crear pipeline
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(
                ngram_range=(1, 2),
                max_features=1000,
                stop_words=None  # No usar stop words en español
            )),
            ('classifier', MultinomialNB(alpha=0.1))
        ])
        
        # Entrenar modelo
        self.pipeline.fit(X_train, y_train)
        
        # Evaluar modelo
        y_pred = self.pipeline.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Precisión del modelo: {accuracy:.2f}")
        print("\nReporte de clasificación:")
        print(classification_report(y_test, y_pred))
        
        # Guardar modelo
        model_path = "backend/app/models/nlp_model.joblib"
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        joblib.dump(self.pipeline, model_path)
        
        print(f"Modelo guardado en: {model_path}")
        
        return {
            "accuracy": accuracy,
            "model_path": model_path,
            "training_samples": len(training_data),
            "test_samples": len(X_test)
        }
    
    def predict_intent(self, text: str) -> Dict[str, Any]:
        """Predice la intención de un texto."""
        if not self.pipeline:
            # Cargar modelo si no está cargado
            model_path = "backend/app/models/nlp_model.joblib"
            if os.path.exists(model_path):
                self.pipeline = joblib.load(model_path)
            else:
                raise ValueError("Modelo no encontrado. Ejecuta el entrenamiento primero.")
        
        processed_text = self.preprocess_text(text)
        predicted_intent = self.pipeline.predict([processed_text])[0]
        confidence_scores = self.pipeline.predict_proba([processed_text])[0]
        
        # Obtener confianza de la predicción
        max_confidence = max(confidence_scores)
        
        return {
            "intent": predicted_intent,
            "confidence": max_confidence,
            "all_scores": dict(zip(self.intent_labels, confidence_scores))
        }
    
    def test_predictions(self):
        """Prueba el modelo con algunos ejemplos."""
        test_texts = [
            "necesito una PC para gaming",
            "qué procesador me recomiendas",
            "es compatible esta RAM",
            "tengo 800 dólares de presupuesto",
            "hola, necesito ayuda"
        ]
        
        print("\nPruebas del modelo:")
        print("-" * 50)
        
        for text in test_texts:
            result = self.predict_intent(text)
            print(f"Texto: '{text}'")
            print(f"Intención: {result['intent']} (confianza: {result['confidence']:.2f})")
            print()

def main():
    """Función principal para entrenar el modelo."""
    trainer = NLPTrainer()
    
    # Entrenar modelo
    results = trainer.train_model()
    
    print("\nResultados del entrenamiento:")
    print(f"- Precisión: {results['accuracy']:.2f}")
    print(f"- Muestras de entrenamiento: {results['training_samples']}")
    print(f"- Muestras de prueba: {results['test_samples']}")
    
    # Probar predicciones
    trainer.test_predictions()

if __name__ == "__main__":
    main()