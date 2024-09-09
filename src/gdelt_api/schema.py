from pydantic import BaseModel
from datetime import date


class RelationsSchema(BaseModel):
    date: date
    country_a: str
    country_b: str
    relations_score: float
