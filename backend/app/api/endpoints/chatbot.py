"""
Endpoints para la API del chatbot.
"""
from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import uuid
import re

from ...chatbot import ChatMessage, ComputerChatbot
from ...ai_engine import get_ai_engine
from sqlalchemy.orm import Session
from ...database import get_db
from ...models import User
from ...auth import get_current_user

# Instancia global del chatbot
chatbot = ComputerChatbot()

router = APIRouter()

class ChatRequest(BaseModel):
    """Modelo para las solicitudes de chat."""
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    """Modelo para las respuestas de chat."""
    message: str
    session_id: str

class ChatHistoryResponse(BaseModel):
    """Modelo para las respuestas de historial de chat."""
    messages: List[ChatMessage]
    session_id: str

@router.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
) -> Dict:
    """
    Endpoint para enviar un mensaje al chatbot y recibir una respuesta.
    """
    # Crear un ID de sesión si no se proporciona
    session_id = request.session_id or str(uuid.uuid4())
    
    # Configurar el motor de IA si es necesario
    if chatbot.ai_engine is None:
        chatbot.set_ai_engine(get_ai_engine(db))
    
    # Procesar el mensaje y obtener respuesta
    response = chatbot.process_message(session_id, request.message)
    
    # Verificar si el mensaje contiene palabras clave para buscar componentes
    keywords = ["recomienda", "busca", "encuentra", "mejor", "componente", "cpu", "gpu", "ram", "placa", "motherboard", "fuente", "psu", "almacenamiento", "ssd", "hdd"]
    
    if any(keyword in request.message.lower() for keyword in keywords):
        # Intentar obtener componentes de la base de datos
        try:
            from ...scraper import ComponentScraper
            from ... import crud
            
            # Inicializar el scraper
            component_scraper = ComponentScraper()
            
            # Determinar qué tipo de componente buscar
            component_type = None
            if "cpu" in request.message.lower():
                component_type = "CPU"
            elif "gpu" in request.message.lower() or "tarjeta" in request.message.lower():
                component_type = "GPU"
            elif "ram" in request.message.lower() or "memoria" in request.message.lower():
                component_type = "RAM"
            elif "placa" in request.message.lower() or "motherboard" in request.message.lower():
                component_type = "Motherboard"
            elif "fuente" in request.message.lower() or "psu" in request.message.lower():
                component_type = "PSU"
            elif "almacenamiento" in request.message.lower() or "ssd" in request.message.lower() or "hdd" in request.message.lower():
                component_type = "Storage"
            
            if component_type:
                # Buscar componentes en la base de datos
                components = crud.get_components_by_type(db, component_type, limit=3)
                
                # Si no hay componentes, intentar hacer scraping
                if not components:
                    # Hacer scraping y guardar en la base de datos
                    scraped_components = component_scraper.scrape_newegg_components(component_type, max_pages=1)
                    for comp_data in scraped_components[:5]:  # Limitar a 5 componentes
                        component = crud.create_component(
                            db,
                            name=comp_data.name,
                            type=comp_data.type,
                            brand=comp_data.brand,
                            model=comp_data.model,
                            price=comp_data.price,
                            description=comp_data.description,
                            image_url=comp_data.image_url
                        )
                    
                    # Obtener los componentes recién añadidos
                    components = crud.get_components_by_type(db, component_type, limit=3)
                
                # Añadir información de componentes a la respuesta
                if components:
                    component_info = "\n\nAquí tienes algunas recomendaciones de nuestra base de datos:\n"
                    for i, comp in enumerate(components, 1):
                        component_info += f"{i}. {comp.name} - {comp.price}€\n"
                    
                    # Añadir la información al final de la respuesta
                    response += component_info
        except Exception as e:
            print(f"Error al buscar componentes: {e}")
            # No modificar la respuesta si hay error
    
    # No hay usuario autenticado en este endpoint público
    return {
        "message": response,
        "session_id": session_id
    }

@router.get("/history/{session_id}", response_model=ChatHistoryResponse)
def get_chat_history(
    session_id: str,
    current_user: Optional[User] = Depends(get_current_user)
) -> Dict:
    """
    Obtiene el historial de mensajes de una sesión de chat.
    """
    # Verificar si la sesión existe
    if session_id not in chatbot.sessions:
        raise HTTPException(status_code=404, detail="Sesión de chat no encontrada")
    
    session = chatbot.sessions[session_id]
    
    # Verificar si el usuario tiene acceso a esta sesión
    if current_user and session.user_id and session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a esta sesión de chat")
    
    return {
        "messages": session.messages,
        "session_id": session_id
    }

@router.delete("/history/{session_id}")
def delete_chat_history(
    session_id: str,
    current_user: Optional[User] = Depends(get_current_user)
) -> Dict:
    """
    Elimina el historial de mensajes de una sesión de chat.
    """
    # Verificar si la sesión existe
    if session_id not in chatbot.sessions:
        raise HTTPException(status_code=404, detail="Sesión de chat no encontrada")
    
    session = chatbot.sessions[session_id]
    
    # Verificar si el usuario tiene acceso a esta sesión
    if current_user and session.user_id and session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar esta sesión de chat")
    
    # Eliminar la sesión
    del chatbot.sessions[session_id]
    
    return {"message": "Historial de chat eliminado correctamente"}