"""
Módulo de chatbot para el sistema ComPuter.
Proporciona funcionalidades de asistente virtual para ayudar a los usuarios
en la selección de componentes y responder preguntas técnicas.
"""
from typing import Dict, List, Optional, Any
import re
import json
import os
from pydantic import BaseModel

# Modelos de datos para el chatbot
class ChatMessage(BaseModel):
    """Modelo para los mensajes del chat."""
    role: str  # 'user' o 'assistant'
    content: str
    timestamp: Optional[str] = None

class ChatSession(BaseModel):
    """Modelo para una sesión de chat."""
    session_id: str
    messages: List[ChatMessage] = []
    user_id: Optional[int] = None
    context: Dict[str, Any] = {}

# Base de conocimiento simple para el chatbot
KNOWLEDGE_BASE = {
    "cpu": {
        "description": "La Unidad Central de Procesamiento (CPU) es el cerebro de la computadora, responsable de ejecutar instrucciones y procesar datos.",
        "important_specs": ["núcleos", "hilos", "frecuencia", "caché", "socket"],
        "usage_types": {
            "gaming": "Para gaming, busca CPUs con alta frecuencia y buen rendimiento por núcleo.",
            "workstation": "Para estaciones de trabajo, prioriza CPUs con muchos núcleos e hilos.",
            "office": "Para uso de oficina, CPUs de gama media son suficientes."
        }
    },
    "gpu": {
        "description": "La Unidad de Procesamiento Gráfico (GPU) se encarga de renderizar gráficos y puede acelerar ciertas cargas de trabajo.",
        "important_specs": ["memoria VRAM", "núcleos CUDA/Stream Processors", "frecuencia", "ancho de bus"],
        "usage_types": {
            "gaming": "Para gaming, busca GPUs con buen rendimiento en juegos a tu resolución objetivo.",
            "workstation": "Para estaciones de trabajo, prioriza GPUs con mucha VRAM y soporte para APIs profesionales.",
            "office": "Para uso de oficina, GPUs integradas o de gama baja son suficientes."
        }
    },
    "ram": {
        "description": "La Memoria de Acceso Aleatorio (RAM) almacena datos temporales para acceso rápido por el CPU.",
        "important_specs": ["capacidad", "frecuencia", "latencia", "tipo (DDR4, DDR5)"],
        "usage_types": {
            "gaming": "Para gaming, 16GB a 32GB de RAM rápida es recomendable.",
            "workstation": "Para estaciones de trabajo, 32GB o más dependiendo de las aplicaciones.",
            "office": "Para uso de oficina, 8GB a 16GB es suficiente."
        }
    },
    "storage": {
        "description": "El almacenamiento guarda datos permanentemente, con opciones como SSD (más rápido) o HDD (más capacidad por precio).",
        "important_specs": ["tipo (SSD/HDD)", "capacidad", "velocidad de lectura/escritura", "interfaz"],
        "usage_types": {
            "gaming": "Para gaming, un SSD para el sistema y juegos, con HDD opcional para almacenamiento masivo.",
            "workstation": "Para estaciones de trabajo, SSDs NVMe rápidos y capacidad según necesidades.",
            "office": "Para uso de oficina, un SSD para el sistema es recomendable."
        }
    },
    "motherboard": {
        "description": "La placa base conecta todos los componentes y determina compatibilidad y capacidad de expansión.",
        "important_specs": ["socket CPU", "chipset", "formato", "slots de expansión", "puertos"],
        "usage_types": {
            "gaming": "Para gaming, busca placas con buen soporte para overclocking y múltiples GPUs si es necesario.",
            "workstation": "Para estaciones de trabajo, prioriza placas con muchos puertos y opciones de expansión.",
            "office": "Para uso de oficina, placas básicas son suficientes."
        }
    },
    "psu": {
        "description": "La fuente de alimentación proporciona energía a todos los componentes.",
        "important_specs": ["potencia (W)", "certificación (80+ Bronze/Gold/Platinum)", "modularidad"],
        "usage_types": {
            "gaming": "Para gaming de alta gama, 650W-850W con buena certificación.",
            "workstation": "Para estaciones de trabajo potentes, 850W+ con alta certificación.",
            "office": "Para uso de oficina, 450W-550W es generalmente suficiente."
        }
    }
}

# Patrones de preguntas comunes
PATTERNS = [
    (r"(?i)qu[eé] es (un |una |el |la )?(\w+)", "component_info"),
    (r"(?i)recomienda (un |una |)(\w+)", "component_recommendation"),
    (r"(?i)cu[aá]l es (la |el |)(mejor|buena|bueno) (\w+)", "best_component"),
    (r"(?i)compatib(le|ilidad)", "compatibility"),
    (r"(?i)presupuesto", "budget"),
    (r"(?i)(gaming|juegos|videojuegos)", "gaming_usage"),
    (r"(?i)(trabajo|profesional|workstation)", "work_usage"),
    (r"(?i)(oficina|básico|básica)", "office_usage"),
]

class ComputerChatbot:
    """Clase principal del chatbot para ComPuter."""
    
    def __init__(self):
        """Inicializa el chatbot."""
        self.sessions: Dict[str, ChatSession] = {}
        self.ai_engine = None
        self.nlp_trainer = None
        self._load_nlp_model()
        
    def _load_nlp_model(self):
        """Carga el modelo NLP entrenado."""
        try:
            from .nlp_training import NLPTrainer
            self.nlp_trainer = NLPTrainer()
            
            # Verificar si existe el modelo entrenado
            model_path = "backend/app/models/nlp_model.joblib"
            if os.path.exists(model_path):
                # El modelo se carga automáticamente en predict_intent
                pass
            else:
                print("Modelo NLP no encontrado. Usando detección de intención básica.")
        except ImportError:
            print("NLPTrainer no disponible. Usando detección de intención básica.")
            self.nlp_trainer = None
        
    def set_ai_engine(self, ai_engine):
        """Establece el motor de IA para recomendaciones."""
        self.ai_engine = ai_engine
    
    def get_or_create_session(self, session_id: str, user_id: Optional[int] = None) -> ChatSession:
        """Obtiene una sesión existente o crea una nueva."""
        if session_id not in self.sessions:
            self.sessions[session_id] = ChatSession(session_id=session_id, user_id=user_id)
        return self.sessions[session_id]
    
    def add_message(self, session_id: str, message: ChatMessage) -> None:
        """Añade un mensaje a la sesión."""
        session = self.get_or_create_session(session_id)
        session.messages.append(message)
    
    def process_message(self, session_id: str, message: str) -> str:
        """Procesa un mensaje del usuario y genera una respuesta."""
        # Añadir mensaje del usuario
        user_message = ChatMessage(role="user", content=message)
        self.add_message(session_id, user_message)
        
        # Generar respuesta
        response = self._generate_response(session_id, message)
        
        # Añadir respuesta del chatbot
        bot_message = ChatMessage(role="assistant", content=response)
        self.add_message(session_id, bot_message)
        
        return response
    
    def _generate_response(self, session_id: str, message: str) -> str:
        """Genera una respuesta basada en el mensaje del usuario."""
        session = self.get_or_create_session(session_id)
        
        # Detectar intención del mensaje
        intent = self._detect_intent(message)
        
        if intent == "component_info":
            component = self._extract_component(message)
            return self._get_component_info(component)
        
        elif intent == "component_recommendation":
            component = self._extract_component(message)
            usage_type = self._extract_usage_type(session)
            return self._recommend_component(component, usage_type)
        
        elif intent == "best_component":
            component = self._extract_component(message)
            usage_type = self._extract_usage_type(session)
            return self._best_component(component, usage_type)
        
        elif intent == "compatibility":
            return self._compatibility_info()
        
        elif intent == "budget":
            return self._budget_info()
        
        elif intent == "gaming_usage" or intent == "work_usage" or intent == "office_usage":
            usage = "gaming" if intent == "gaming_usage" else "workstation" if intent == "work_usage" else "office"
            session.context["usage_type"] = usage
            return self._usage_type_info(usage)
        
        else:
            return "Puedo ayudarte a elegir componentes para tu PC. Pregúntame sobre CPUs, GPUs, RAM, almacenamiento, placas base o fuentes de alimentación. También puedo darte recomendaciones según tu presupuesto y tipo de uso."
    
    def _detect_intent(self, message: str) -> str:
        """Detecta la intención del mensaje del usuario usando NLP o patrones básicos."""
        # Intentar usar el modelo NLP entrenado
        if self.nlp_trainer:
            try:
                result = self.nlp_trainer.predict_intent(message)
                # Solo usar la predicción si la confianza es alta
                if result['confidence'] > 0.6:
                    return result['intent']
            except Exception as e:
                print(f"Error en predicción NLP: {e}")
        
        # Fallback a detección por patrones
        for pattern, intent in PATTERNS:
            if re.search(pattern, message):
                return intent
        return "unknown"
    
    def _extract_component(self, message: str) -> str:
        """Extrae el tipo de componente mencionado en el mensaje."""
        # Mapeo de términos comunes a componentes en la base de conocimiento
        component_mapping = {
            "procesador": "cpu", "cpu": "cpu", "microprocesador": "cpu",
            "tarjeta gráfica": "gpu", "gpu": "gpu", "gráfica": "gpu", "video": "gpu",
            "memoria": "ram", "ram": "ram",
            "disco": "storage", "almacenamiento": "storage", "ssd": "storage", "hdd": "storage",
            "placa": "motherboard", "placa base": "motherboard", "motherboard": "motherboard", "tarjeta madre": "motherboard",
            "fuente": "psu", "fuente de poder": "psu", "psu": "psu", "alimentación": "psu"
        }
        
        message = message.lower()
        for term, component in component_mapping.items():
            if term in message:
                return component
        
        # Buscar componentes directamente
        for component in KNOWLEDGE_BASE.keys():
            if component in message:
                return component
        
        return "general"
    
    def _extract_usage_type(self, session: ChatSession) -> str:
        """Extrae el tipo de uso del contexto de la sesión o asume un valor predeterminado."""
        return session.context.get("usage_type", "general")
    
    def _get_component_info(self, component: str) -> str:
        """Obtiene información sobre un componente específico."""
        if component in KNOWLEDGE_BASE:
            info = KNOWLEDGE_BASE[component]
            response = f"{info['description']}\n\nEspecificaciones importantes: {', '.join(info['important_specs'])}."
            return response
        else:
            return "No tengo información específica sobre ese componente. Puedo ayudarte con CPU, GPU, RAM, almacenamiento, placas base y fuentes de alimentación."
    
    def _recommend_component(self, component: str, usage_type: str) -> str:
        """Genera una recomendación para un tipo de componente según el uso."""
        if component in KNOWLEDGE_BASE:
            info = KNOWLEDGE_BASE[component]
            if usage_type in info["usage_types"]:
                return info["usage_types"][usage_type]
            else:
                return f"Para recomendarte un {component}, necesito saber si lo usarás para gaming, trabajo profesional u oficina."
        else:
            return "No puedo recomendar ese tipo de componente. Puedo ayudarte con CPU, GPU, RAM, almacenamiento, placas base y fuentes de alimentación."
    
    def _best_component(self, component: str, usage_type: str) -> str:
        """Informa sobre el mejor componente según el tipo de uso."""
        if component in KNOWLEDGE_BASE:
            if usage_type == "general":
                return f"El mejor {component} depende de tu uso. ¿Lo usarás para gaming, trabajo profesional u oficina?"
            else:
                return self._recommend_component(component, usage_type)
        else:
            return "No tengo información sobre ese tipo de componente. Puedo ayudarte con CPU, GPU, RAM, almacenamiento, placas base y fuentes de alimentación."
    
    def _compatibility_info(self) -> str:
        """Proporciona información sobre compatibilidad de componentes."""
        return ("La compatibilidad entre componentes es crucial. Algunos puntos importantes:\n\n"
                "- El socket de la CPU debe ser compatible con la placa base\n"
                "- La RAM debe ser del tipo soportado por la placa base (DDR4, DDR5, etc.)\n"
                "- La fuente de alimentación debe tener suficiente potencia para todos los componentes\n"
                "- La caja debe tener espacio para todos los componentes\n\n"
                "Nuestro sistema verifica automáticamente la compatibilidad entre los componentes que selecciones.")
    
    def _budget_info(self) -> str:
        """Proporciona información sobre presupuestos."""
        return ("El presupuesto es un factor importante. Aquí hay algunas guías generales:\n\n"
                "- Gama baja (500-700€): Ideal para tareas básicas y algo de gaming casual\n"
                "- Gama media (700-1200€): Buen rendimiento en gaming 1080p y tareas productivas\n"
                "- Gama alta (1200-2000€): Excelente para gaming 1440p y trabajo profesional\n"
                "- Gama entusiasta (2000€+): Máximo rendimiento para gaming 4K y cargas de trabajo intensivas\n\n"
                "¿Cuál es tu presupuesto aproximado? Puedo ayudarte a distribuirlo entre componentes.")
                
    def generate_recommendation(self, budget: float, usage_type: str, preferences: Dict[str, bool] = None) -> str:
        """Genera una recomendación utilizando el motor de IA."""
        if not self.ai_engine:
            return "Lo siento, el motor de recomendaciones no está disponible en este momento."
            
        try:
            # Calcular distribución del presupuesto
            budget_distribution = self.ai_engine._calculate_budget_distribution(budget, usage_type)
            
            # Ajustar según preferencias
            if preferences:
                budget_distribution = self.ai_engine._adjust_budget_for_preferences(budget_distribution, preferences)
            
            # Seleccionar componentes
            selected_components = self.ai_engine._select_components_by_budget(budget_distribution)
            
            # Formatear respuesta
            response = f"Basado en tu presupuesto de {budget}€ para un uso de tipo {usage_type}, te recomiendo:\n\n"
            
            for component_type, component in selected_components.items():
                response += f"- {component_type.upper()}: {component.name} - {component.price}€\n"
            
            total_price = sum(component.price for component in selected_components.values())
            response += f"\nPrecio total estimado: {total_price}€"
            
            return response
        except Exception as e:
            return f"Lo siento, ha ocurrido un error al generar la recomendación: {str(e)}"
    
    def _usage_type_info(self, usage_type: str) -> str:
        """Proporciona información sobre un tipo de uso específico."""
        if usage_type == "gaming":
            return ("Para un PC de gaming, deberías priorizar:\n\n"
                    "1. GPU potente (30-40% del presupuesto)\n"
                    "2. CPU con buen rendimiento por núcleo (20-25% del presupuesto)\n"
                    "3. 16GB+ de RAM rápida (10-15% del presupuesto)\n"
                    "4. SSD para sistema y juegos (10-15% del presupuesto)\n"
                    "5. Placa base y fuente de calidad (resto del presupuesto)\n\n"
                    "¿Tienes algún presupuesto en mente o algún componente específico sobre el que quieras saber más?")
        elif usage_type == "workstation":
            return ("Para una estación de trabajo profesional, deberías priorizar:\n\n"
                    "1. CPU con muchos núcleos e hilos (30-40% del presupuesto)\n"
                    "2. GPU profesional o potente según tus aplicaciones (20-30% del presupuesto)\n"
                    "3. 32GB+ de RAM (15-20% del presupuesto)\n"
                    "4. SSD NVMe rápido y capacidad según necesidades (10-15% del presupuesto)\n"
                    "5. Placa base y fuente de alta calidad (resto del presupuesto)\n\n"
                    "¿Tienes algún presupuesto en mente o algún componente específico sobre el que quieras saber más?")
        else:  # office
            return ("Para un PC de oficina, deberías priorizar:\n\n"
                    "1. CPU de gama media (25-30% del presupuesto)\n"
                    "2. 8-16GB de RAM (15-20% del presupuesto)\n"
                    "3. SSD para el sistema (15-20% del presupuesto)\n"
                    "4. Placa base confiable (15-20% del presupuesto)\n"
                    "5. Fuente de calidad (10-15% del presupuesto)\n\n"
                    "¿Tienes algún presupuesto en mente o algún componente específico sobre el que quieras saber más?")

# Instancia global del chatbot
chatbot = ComputerChatbot()