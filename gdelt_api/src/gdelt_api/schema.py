from datetime import date
from typing import Any

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

    @classmethod
    def model_construct_cc(cls, country_code: str, raw: dict[str, Any]) -> "RelationsSchema":
        if raw["country_code_b"] == country_code:
            raw["country_code_a"], raw["country_code_b"] = (
                raw["country_code_b"],
                raw["country_code_a"],
            )
        return RelationsSchema.model_construct(**raw)
