from ninja import Schema
from pydantic import BaseModel
from bson.objectid import ObjectId


# SCHEMA
class RateSerializer(BaseModel):
    rate: float
    count: int


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
