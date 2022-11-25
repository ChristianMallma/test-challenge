from pydantic import BaseModel, Field
from typing import Optional


class RegisterProductSchema(BaseModel):
    name: Optional[str] = Field(None, alias="Nombre")
    status: Optional[bool] = Field(True, alias="Estado")
    stock: Optional[int] = Field(0, alias="Cantidad")
    description: Optional[str] = Field(None, alias="Descripción")
    price: Optional[float] = Field(0.0, alias="Precio")


class UpdateProductSchema(BaseModel):
    name: Optional[str] = Field(None)
    status: Optional[bool] = Field(None)
    stock: Optional[int] = Field(None)
    description: Optional[str] = Field(None)
    price: Optional[float] = Field(None)
