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
    current_user: Optional[User] = None,
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
    
    # Asociar la sesión con el usuario si está autenticado
    if current_user:
        session = chatbot.get_or_create_session(session_id)
        session.user_id = current_user.id
    
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