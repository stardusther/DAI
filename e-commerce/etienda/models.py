# Create your models here.
from pydantic import BaseModel, AnyUrl, FilePath, Field, EmailStr, validator
from datetime import datetime
from typing import Any

# Database schema
# https://docs.pydantic.dev/latest/
# con anotaciones de tipo https://docs.python.org/3/library/typing.html
# https://docs.pydantic.dev/latest/usage/fields/


class Rating(BaseModel):
    """Model to store the score and number of ratings a product has"""
    rate: float = Field(ge=0., lt=5.)
    count: int = Field(ge=0)


class Product(BaseModel):
    """Model to store products"""
    _id: Any
    title: str
    price: float
    description: str
    category: str
    image: str | None
    rating: Rating

    @validator('title')
    @classmethod
    def title_must_start_capital(cls, obj: str) -> str:
        if not obj[0].isupper():  #Check wether the first letter is a capital letter or not
            raise ValueError('Title must start with a capital letter')
        return obj.title()


class Purchase(BaseModel):
    """Model to store purchases"""
    _id: Any
    user: EmailStr
    date: datetime
    products: list