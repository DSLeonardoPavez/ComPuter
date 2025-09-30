from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import timedelta

from .database import get_db
from .models import Base
from .database import engine
from .schemas import ComponentCreate, Component, CompatibilityCheck, CompatibilityRequest, RecommendationRequest, RecommendationResult, UserCreate, User, UserProfileCreate, UserProfile, Token
from .crud import get_components, get_component, get_components_by_type, create_component, update_component, delete_component, check_compatibility, generate_recommendations, create_user, get_user_by_email, create_user_profile, get_user_profile
from .ai_engine import get_ai_engine
from .auth import authenticate_user, create_access_token, get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES
from .api.endpoints import chatbot as chatbot_endpoints

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ComPuter API",
    description="API para el sistema de recomendación de componentes de PC",
    version="0.1.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de ComPuter"}

# Endpoints para componentes
@app.get("/components/", response_model=List[Component])
def read_components(
    skip: int = 0, 
    limit: int = 100, 
    type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    if type:
        components = get_components_by_type(db, type=type, skip=skip, limit=limit)
    else:
        components = get_components(db, skip=skip, limit=limit)
    return components

@app.get("/components/{component_id}", response_model=Component)
def read_component(component_id: int, db: Session = Depends(get_db)):
    component = get_component(db, component_id=component_id)
    if component is None:
        raise HTTPException(status_code=404, detail="Componente no encontrado")
    return component

@app.post("/components/", response_model=Component)
def add_component(component: ComponentCreate, db: Session = Depends(get_db)):
    return create_component(db=db, component=component)

@app.put("/components/{component_id}", response_model=Component)
def update_component_endpoint(component_id: int, component: ComponentCreate, db: Session = Depends(get_db)):
    updated_component = update_component(db, component_id=component_id, component=component)
    if updated_component is None:
        raise HTTPException(status_code=404, detail="Componente no encontrado")
    return updated_component

@app.delete("/components/{component_id}")
def delete_component_endpoint(component_id: int, db: Session = Depends(get_db)):
    success = delete_component(db, component_id=component_id)
    if not success:
        raise HTTPException(status_code=404, detail="Componente no encontrado")
    return {"message": "Componente eliminado correctamente"}

# Endpoints para verificación de compatibilidad
@app.post("/compatibility/check/", response_model=CompatibilityCheck)
def check_components_compatibility(request: CompatibilityRequest, db: Session = Depends(get_db)):
    result = check_compatibility(db, request.components)
    return result

# Endpoints para recomendaciones
@app.post("/recommendations/", response_model=RecommendationResult)
def get_recommendations(request: RecommendationRequest, db: Session = Depends(get_db)):
    recommendations = generate_recommendations(
        db, 
        budget=request.budget, 
        usage_type=request.usage_type, 
        preferences=request.preferences
    )
    return recommendations

# Endpoints para usuarios
@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=User)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    return create_user(db=db, user=user)

@app.post("/users/profile/", response_model=UserProfile)
def create_profile(profile: UserProfileCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    # Verificar que el usuario solo pueda crear su propio perfil
    if profile.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="No tienes permiso para crear este perfil")
    return create_user_profile(db=db, profile=profile)

@app.get("/users/{user_id}/profile/", response_model=UserProfile)
def read_user_profile(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    # Verificar que el usuario solo pueda ver su propio perfil
    if user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver este perfil")
    profile = get_user_profile(db, user_id=user_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    return profile

@app.get("/users/me/", response_model=User)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

# Incluir los endpoints del chatbot
app.include_router(chatbot_endpoints.router, prefix="/api/chatbot", tags=["chatbot"])