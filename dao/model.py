from pydantic import BaseModel

class Ingredeint(BaseModel):
     ingredient: str
     allergy: str
     description: str 

class Product(BaseModel):
    product: str
    report: list[Ingredeint]
    