from ninja import Schema
from pydantic import BaseModel, validator
from bson.objectid import ObjectId


# SCHEMA
class RateSerializer(BaseModel):
    rate: float
    count: int
    # user_rate: int

    # @validator('user_rate', pre=True, always=True)
    # def set_default_user_rate(cls, v):
    #     return v if v is not None else 0


class ProductSerializer(BaseModel):  # sirve para validar y para documentación
    _id: str
    title: str
    price: float
    description: str
    category: str
    image: str = None
    rating: RateSerializer

    class Config:
        # Configuración para la compatibilidad con MongoDB
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str  # Convertir ObjectId a str para la serialización
        }


class CreateProductSerializer(BaseModel):
    title: str
    price: float
    description: str
    category: str
    rating: RateSerializer


class MessageSerializer(Schema):
    message: str


class ProductResultSerializer(Schema):
    _id: str
    title: str
    description: str
    category: str