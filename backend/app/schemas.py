from pydantic import BaseModel, EmailStr
from typing import List, Dict, Optional, Any

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class SpecificationBase(BaseModel):
    name: str
    value: str

class SpecificationCreate(SpecificationBase):
    pass

class Specification(SpecificationBase):
    id: int
    component_id: int

    class Config:
        orm_mode = True

class ComponentBase(BaseModel):
    name: str
    type: str
    brand: str
    model: str
    price: float
    description: Optional[str] = None
    image_url: Optional[str] = None
    performance_score: Optional[float] = None
    power_consumption: Optional[int] = None

class ComponentCreate(ComponentBase):
    specifications: List[SpecificationCreate] = []

class Component(ComponentBase):
    id: int
    specifications: List[Specification] = []

    class Config:
        orm_mode = True

class CompatibilityRequest(BaseModel):
    components: List[int]

class CompatibilityCheck(BaseModel):
    compatible: bool
    message: str
    issues: List[str] = []
    compatibility_score: Optional[float] = None

class RecommendationRequest(BaseModel):
    budget: float
    usage_type: str
    preferences: Optional[Dict[str, bool]] = None

class RecommendationResult(BaseModel):
    components: List[Component]
    total_price: float
    performance_score: float
    compatibility_score: float

class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool = True
    is_admin: bool = False

    class Config:
        orm_mode = True

class UserProfileBase(BaseModel):
    user_id: int
    usage_type: str
    budget: float
    preferences: Optional[Dict[str, bool]] = None

class UserProfileCreate(UserProfileBase):
    pass

class UserProfile(UserProfileBase):
    id: int

    class Config:
        orm_mode = True
    budget: float
    preferences: Dict[str, Any]

class UserProfileCreate(UserProfileBase):
    pass

class UserProfile(UserProfileBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True