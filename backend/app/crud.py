from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict, Any, Optional
import random
import logging

from . import models, schemas
from .ai_engine import get_ai_engine

# Configurar logging
logger = logging.getLogger(__name__)

# Funciones mejoradas para componentes
def get_component(db: Session, component_id: int) -> Optional[models.Component]:
    """Obtiene un componente por ID con manejo de errores."""
    try:
        return db.query(models.Component).filter(models.Component.id == component_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener componente {component_id}: {e}")
        return None

def get_components(db: Session, skip: int = 0, limit: int = 100) -> List[models.Component]:
    """Obtiene lista de componentes con paginación."""
    try:
        return db.query(models.Component).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener componentes: {e}")
        return []

def get_components_by_type(db: Session, type: str, skip: int = 0, limit: int = 100) -> List[models.Component]:
    """Obtiene componentes filtrados por tipo."""
    try:
        return db.query(models.Component).filter(models.Component.type == type).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener componentes por tipo {type}: {e}")
        return []

def search_components(db: Session, query: str, component_type: Optional[str] = None, 
                     min_price: Optional[float] = None, max_price: Optional[float] = None,
                     skip: int = 0, limit: int = 100) -> List[models.Component]:
    """Búsqueda avanzada de componentes."""
    try:
        db_query = db.query(models.Component)
        
        # Filtro por texto
        if query:
            db_query = db_query.filter(
                models.Component.name.ilike(f"%{query}%") |
                models.Component.brand.ilike(f"%{query}%") |
                models.Component.model.ilike(f"%{query}%")
            )
        
        # Filtro por tipo
        if component_type:
            db_query = db_query.filter(models.Component.type == component_type)
        
        # Filtro por precio
        if min_price is not None:
            db_query = db_query.filter(models.Component.price >= min_price)
        if max_price is not None:
            db_query = db_query.filter(models.Component.price <= max_price)
        
        return db_query.offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        logger.error(f"Error en búsqueda de componentes: {e}")
        return []

def create_component(db: Session, component: schemas.ComponentCreate) -> Optional[models.Component]:
    """Crea un nuevo componente con manejo de errores mejorado."""
    try:
        db_component = models.Component(
            name=component.name,
            type=component.type,
            brand=component.brand,
            model=component.model,
            price=component.price,
            description=component.description,
            image_url=component.image_url,
            performance_score=component.performance_score,
            power_consumption=component.power_consumption
        )
        db.add(db_component)
        db.commit()
        db.refresh(db_component)
        
        # Crear especificaciones
        if component.specifications:
            for spec in component.specifications:
                db_spec = models.Specification(
                    component_id=db_component.id,
                    name=spec.name,
                    value=spec.value
                )
                db.add(db_spec)
        
        db.commit()
        db.refresh(db_component)
        logger.info(f"Componente creado exitosamente: {db_component.id}")
        return db_component
    except SQLAlchemyError as e:
        logger.error(f"Error al crear componente: {e}")
        db.rollback()
        return None

def update_component(db: Session, component_id: int, component: schemas.ComponentCreate):
    db_component = get_component(db, component_id)
    if not db_component:
        return None
        
    # Actualizar campos del componente
    db_component.name = component.name
    db_component.type = component.type
    db_component.brand = component.brand
    db_component.model = component.model
    db_component.price = component.price
    db_component.description = component.description
    db_component.image_url = component.image_url
    db_component.performance_score = component.performance_score
    db_component.power_consumption = component.power_consumption
    
    # Eliminar especificaciones existentes
    db.query(models.Specification).filter(models.Specification.component_id == component_id).delete()
    
    # Crear nuevas especificaciones
    for spec in component.specifications:
        db_spec = models.Specification(
            component_id=db_component.id,
            name=spec.name,
            value=spec.value
        )
        db.add(db_spec)
    
    db.commit()
    db.refresh(db_component)
    return db_component

def delete_component(db: Session, component_id: int):
    db_component = get_component(db, component_id)
    if not db_component:
        return False
        
    # Eliminar especificaciones
    db.query(models.Specification).filter(models.Specification.component_id == component_id).delete()
    
    # Eliminar componente
    db.delete(db_component)
    db.commit()
    return True

def check_compatibility(db: Session, component_ids: List[int]) -> Dict:
    """
    Verifica la compatibilidad entre componentes utilizando el motor de IA.
    """
    components = {}
    
    # Obtener todos los componentes y organizarlos por tipo
    for component_id in component_ids:
        component = get_component(db, component_id)
        if component:
            components[component.type] = component
    
    # Utilizar el motor de IA para verificar compatibilidad
    ai_engine = get_ai_engine(db)
    compatibility_result = ai_engine._check_compatibility(components)
    
    return compatibility_result

def generate_recommendations(db: Session, budget: float, usage_type: str, preferences: Dict[str, bool] = None) -> Dict:
    """
    Genera recomendaciones de componentes utilizando el motor de IA.
    """
    # Utilizar el motor de IA para generar recomendaciones
    ai_engine = get_ai_engine(db)
    recommendation_result = ai_engine.generate_recommendation(budget, usage_type, preferences)
    
    return recommendation_result

def create_user(db: Session, user: schemas.UserCreate):
    """
    Crea un nuevo usuario en el sistema.
    """
    # Hashear la contraseña antes de guardarla
    from .auth import get_password_hash
    
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        name=user.name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    """
    Obtiene un usuario por su email.
    """
    return db.query(models.User).filter(models.User.email == email).first()

def create_user_profile(db: Session, profile: schemas.UserProfileCreate):
    """
    Crea un perfil de usuario con preferencias.
    """
    db_profile = models.UserProfile(
        user_id=profile.user_id,
        usage_type=profile.usage_type,
        budget=profile.budget,
        preferences=profile.preferences
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def get_user_profile(db: Session, user_id: int):
    """
    Obtiene el perfil de un usuario.
    """
    return db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id).first()

def check_compatibility_detailed(db: Session, component_ids: List[int]) -> schemas.CompatibilityCheck:
    """
    Verifica la compatibilidad detallada entre componentes.
    Esta función complementa la verificación básica del motor de IA.
    """
    components = []
    issues = []
    
    # Obtener componentes
    for component_id in component_ids:
        component = get_component(db, component_id)
        if component:
            components.append(component)
        else:
            issues.append(f"Componente con ID {component_id} no encontrado")
    
    # Verificar si hay suficientes componentes para comparar
    if len(components) < 2:
        return schemas.CompatibilityCheck(
            compatible=False,
            issues=["Se necesitan al menos dos componentes para verificar compatibilidad"],
            compatibility_score=0.0
        )
    
    # Ejemplo de regla: verificar compatibilidad entre CPU y placa madre
    cpu = next((c for c in components if c.type == "CPU"), None)
    motherboard = next((c for c in components if c.type == "Motherboard"), None)
    
    if cpu and motherboard:
        # Obtener socket de CPU
        cpu_socket = next((spec.value for spec in cpu.specifications if spec.name == "socket"), None)
        # Obtener socket de placa madre
        mb_socket = next((spec.value for spec in motherboard.specifications if spec.name == "socket"), None)
        
        if cpu_socket and mb_socket and cpu_socket != mb_socket:
            issues.append(f"Socket de CPU ({cpu_socket}) no compatible con placa madre ({mb_socket})")
    
    # Calcular puntuación de compatibilidad
    compatibility_score = 1.0 if not issues else max(0.0, 1.0 - (len(issues) * 0.2))
    
    return schemas.CompatibilityCheck(
        compatible=len(issues) == 0,
        issues=issues,
        compatibility_score=compatibility_score
    )

def generate_recommendations(db: Session, user_requirements: Dict[str, Any]) -> List[schemas.RecommendationResult]:
    """
    Genera recomendaciones de componentes basadas en los requisitos del usuario.
    Esta es una implementación básica que se debe expandir con algoritmos de IA.
    """
    # Extraer requisitos del usuario
    budget = user_requirements.get("budget", 1000.0)
    usage_type = user_requirements.get("usage_type", "gaming")
    
    # Obtener todos los componentes
    all_components = get_components(db)
    
    # Filtrar componentes por tipo
    components_by_type = {}
    for component in all_components:
        if component.type not in components_by_type:
            components_by_type[component.type] = []
        components_by_type[component.type].append(component)
    
    # Crear recomendaciones (simulación básica)
    recommendations = []
    
    # Para una configuración básica, necesitamos CPU, GPU, RAM, Motherboard, Storage
    essential_types = ["CPU", "GPU", "RAM", "Motherboard", "Storage", "PSU"]
    
    # Crear 3 recomendaciones diferentes
    for _ in range(3):
        selected_components = []
        total_price = 0.0
        total_performance = 0.0
        
        # Seleccionar un componente de cada tipo esencial
        for component_type in essential_types:
            if component_type in components_by_type and components_by_type[component_type]:
                # En una implementación real, aquí se usaría un algoritmo de IA
                # Por ahora, seleccionamos aleatoriamente
                component = random.choice(components_by_type[component_type])
                selected_components.append(component)
                total_price += component.price
                total_performance += component.performance_score
        
        # Verificar compatibilidad
        component_ids = [c.id for c in selected_components]
        compatibility_result = check_compatibility(db, component_ids)
        
        # Solo agregar si está dentro del presupuesto
        if total_price <= budget:
            recommendations.append(
                schemas.Recommendation(
                    components=selected_components,
                    total_price=total_price,
                    performance_score=total_performance / len(selected_components) if selected_components else 0,
                    compatibility_score=compatibility_result.compatibility_score
                )
            )
    
    # Ordenar por puntuación de rendimiento
    recommendations.sort(key=lambda x: x.performance_score, reverse=True)
    
    return recommendations

def create_user(db: Session, user: schemas.UserCreate):
    # En una implementación real, se debe hashear la contraseña
    hashed_password = user.password + "_hashed"  # Esto es solo un ejemplo
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_user_profile(db: Session, profile: schemas.UserProfileCreate, user_id: int):
    db_profile = models.UserProfile(
        user_id=user_id,
        usage_type=profile.usage_type,
        budget=profile.budget,
        preferences=str(profile.preferences)  # Convertir a string para almacenar
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile