from typing import Optional
from dataclasses import dataclass



@dataclass

class Product:
    id: int
    name: str
    description: Optional[str]
    quantity: int
    price: float
