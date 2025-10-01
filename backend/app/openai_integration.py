"""
Módulo para integración con OpenAI.
Proporciona funcionalidades para conectar con la API de OpenAI
y generar respuestas para el chatbot.
"""
import os
from typing import List, Dict, Any, Optional

# Configurar la API key de OpenAI
# En producción, esto debería venir de variables de entorno
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "tu-api-key-aqui")

class OpenAIHandler:
    """Clase para manejar la integración con OpenAI."""
    
    def __init__(self):
        """Inicializa el manejador de OpenAI."""
        self.model = "gpt-3.5-turbo"
        self.system_prompt = """
        Eres un asistente especializado en componentes de computadoras y tecnología.
        Tu objetivo es ayudar a los usuarios a elegir los mejores componentes para sus necesidades,
        responder preguntas técnicas sobre hardware y software, y proporcionar recomendaciones personalizadas.
        Tienes conocimiento sobre CPUs, GPUs, placas base, memoria RAM, almacenamiento, fuentes de alimentación,
        y otros componentes de PC. También puedes ayudar con preguntas sobre compatibilidad, rendimiento y relación calidad-precio.
        
        Debes responder directamente a las preguntas del usuario sin mencionar que eres una IA.
        Proporciona información técnica precisa y recomendaciones basadas en las necesidades específicas del usuario.
        """
    
    def generate_response(self, user_message: str, chat_history: Optional[List[Dict[str, str]]] = None) -> str:
        """
        Genera una respuesta utilizando lógica mejorada basada en el mensaje del usuario.
        
        Args:
            user_message: El mensaje del usuario.
            chat_history: Historial de mensajes previos (opcional).
            
        Returns:
            La respuesta generada.
        """
        message_lower = user_message.lower()
        
        # Respuestas más dinámicas basadas en el contexto
        if any(word in message_lower for word in ["hola", "buenos", "buenas", "saludos"]):
            return "¡Hola! Soy tu asistente especializado en componentes de PC. ¿En qué puedo ayudarte hoy? Puedo recomendarte CPUs, GPUs, RAM, placas base y más según tu presupuesto y necesidades."
        
        elif any(word in message_lower for word in ["cpu", "procesador", "microprocesador"]):
            if "gaming" in message_lower or "juegos" in message_lower:
                return "Para gaming, te recomiendo los AMD Ryzen 7 7800X3D o Intel Core i5-13600K. El 7800X3D es excelente para juegos gracias a su cache 3D, mientras que el i5-13600K ofrece gran rendimiento por precio. ¿Tienes algún presupuesto en mente?"
            elif "trabajo" in message_lower or "productividad" in message_lower:
                return "Para trabajo y productividad, los AMD Ryzen 9 7900X o Intel Core i7-13700K son ideales. Ofrecen muchos núcleos para multitarea, renderizado y aplicaciones profesionales. ¿Qué tipo de trabajo realizas principalmente?"
            else:
                return "Los procesadores más recomendados actualmente son los AMD Ryzen 7000 y los Intel Core de 13ª generación. Para gaming, el Ryzen 7 7800X3D es excelente. Para productividad, el Intel i9-13900K destaca. ¿Para qué uso principal necesitas el procesador?"
        
        elif any(word in message_lower for word in ["gpu", "tarjeta", "gráfica", "video"]):
            if "4k" in message_lower:
                return "Para gaming en 4K, necesitas una GPU potente como la RTX 4080, RTX 4090 o RX 7900 XTX. La RTX 4090 es la más potente pero costosa. La RTX 4080 ofrece excelente rendimiento 4K con mejor precio. ¿Cuál es tu presupuesto aproximado?"
            elif "1440p" in message_lower:
                return "Para 1440p, la RTX 4070, RTX 4070 Ti o RX 7800 XT son perfectas. La RTX 4070 ofrece gran relación calidad-precio, mientras que la RX 7800 XT compite muy bien en rendimiento puro. ¿Prefieres NVIDIA o AMD?"
            else:
                return "Las mejores tarjetas gráficas actuales incluyen la RTX 4070 para 1440p, RTX 4080 para 4K, y RX 7800 XT como alternativa AMD. ¿A qué resolución planeas jugar y cuál es tu presupuesto?"
        
        elif any(word in message_lower for word in ["ram", "memoria"]):
            if "gaming" in message_lower:
                return "Para gaming, 16GB de RAM DDR4-3600 o DDR5-5200 es el estándar actual. 32GB es recomendable si también haces streaming o edición. Las marcas Corsair, G.Skill y Kingston son confiables. ¿Qué plataforma usarás (Intel o AMD)?"
            else:
                return "La cantidad de RAM depende del uso: 16GB para gaming y uso general, 32GB para edición de video y trabajo profesional, 64GB+ para estaciones de trabajo intensivas. ¿Para qué la necesitas principalmente?"
        
        elif any(word in message_lower for word in ["placa", "motherboard", "tarjeta madre"]):
            if "amd" in message_lower or "ryzen" in message_lower:
                return "Para AMD Ryzen, los chipsets B650 y X670 son los más actuales. B650 es perfecto para la mayoría de usuarios, mientras que X670 ofrece más conectividad. Marcas como ASUS, MSI y Gigabyte son confiables. ¿Qué procesador Ryzen planeas usar?"
            elif "intel" in message_lower:
                return "Para Intel, los chipsets Z790 y B760 son los actuales. Z790 permite overclocking y tiene más funciones, B760 es más económico. ¿Qué procesador Intel tienes en mente?"
            else:
                return "La elección de placa base depende de tu CPU. Para AMD Ryzen: B650/X670. Para Intel: B760/Z790. Considera puertos USB, slots PCIe y capacidad de expansión según tus necesidades. ¿Qué procesador usarás?"
        
        elif any(word in message_lower for word in ["fuente", "psu", "alimentación"]):
            return "Para fuentes de alimentación, recomiendo 650W-750W para sistemas gaming, 850W+ para configuraciones high-end. Busca certificación 80+ Gold mínimo. Marcas confiables: Corsair, Seasonic, EVGA. ¿Qué GPU planeas usar?"
        
        elif any(word in message_lower for word in ["presupuesto", "precio", "costo", "dinero"]):
            return "Puedo ayudarte según tu presupuesto:\n• 600-800€: PC básico para gaming 1080p\n• 800-1200€: Gaming 1440p sólido\n• 1200-1800€: High-end gaming/trabajo\n• 1800€+: Enthusiast/4K gaming\n¿Cuál es tu rango de presupuesto?"
        
        elif any(word in message_lower for word in ["compatibilidad", "compatible"]):
            return "La compatibilidad es clave: CPU y placa base deben tener el mismo socket, RAM debe ser compatible con la placa, GPU necesita slot PCIe x16, y la fuente debe tener suficiente potencia. ¿Tienes componentes específicos en mente?"
        
        elif any(word in message_lower for word in ["recomendación", "recomienda", "mejor", "bueno"]):
            return "Para darte la mejor recomendación necesito saber: ¿Para qué usarás la PC principalmente? ¿Gaming, trabajo, diseño gráfico? ¿Cuál es tu presupuesto aproximado? ¿Tienes preferencia por alguna marca?"
        
        else:
            return "Puedo ayudarte con recomendaciones de componentes para tu PC. ¿Qué tipo de uso le darás principalmente? ¿Gaming, trabajo, diseño gráfico? Así podré darte recomendaciones más precisas."

# Instancia global del manejador de OpenAI
openai_handler = OpenAIHandler()