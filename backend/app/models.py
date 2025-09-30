from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

# Tabla de asociación para relaciones muchos a muchos
compatibility = Table(
    'compatibility',
    Base.metadata,
    Column('component_id', Integer, ForeignKey('components.id'), primary_key=True),
    Column('compatible_with_id', Integer, ForeignKey('components.id'), primary_key=True)
)

class Component(Base):
    __tablename__ = "components"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String, index=True)  # CPU, GPU, RAM, etc.
    brand = Column(String, index=True)
    model = Column(String, index=True)
    price = Column(Float)
    description = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    performance_score = Column(Float, nullable=True)
    power_consumption = Column(Integer, nullable=True)  # en watts
    specifications = relationship("Specification", back_populates="component")
    
    # Relación muchos a muchos para compatibilidad
    compatible_with = relationship(
        "Component",
        secondary=compatibility,
        primaryjoin=id==compatibility.c.component_id,
        secondaryjoin=id==compatibility.c.compatible_with_id,
        backref="compatible_components"
    )

class Specification(Base):
    __tablename__ = "specifications"

    id = Column(Integer, primary_key=True, index=True)
    component_id = Column(Integer, ForeignKey("components.id"))
    name = Column(String, index=True)
    value = Column(String)
    component = relationship("Component", back_populates="specifications")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    profile = relationship("UserProfile", back_populates="user", uselist=False)

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    usage_type = Column(String)  # gaming, office, design, etc.
    budget = Column(Float)
    preferences = Column(String)  # JSON string con preferencias
    user = relationship("User", back_populates="profile")