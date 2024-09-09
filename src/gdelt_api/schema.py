from pydantic import BaseModel
from datetime import date


class RelationsSchema(BaseModel):
    date: date
    country_code_a: str
    country_code_b: str
    relations_score: float
