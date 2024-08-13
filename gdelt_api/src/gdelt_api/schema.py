from datetime import date

from pydantic import BaseModel


class RelationsSchema(BaseModel):
    date: date
    country_code_a: str
    country_code_b: str
    relations_score: float
    num_verbal_coop: int
    num_material_coop: int
    num_verbal_conf: int
    num_material_conf: int
