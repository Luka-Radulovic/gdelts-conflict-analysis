from datetime import date
from typing import Callable

from fastapi import APIRouter, HTTPException

from gdelt_api.schema import RelationsSchema
from gdelt_api.services import relations_service

router: APIRouter = APIRouter(prefix="/relations")


@router.post("/")
async def add_relations(relations: RelationsSchema) -> RelationsSchema:
    return relations_service.add_relations(relations)


@router.get("/")
async def get_relations(
    country_code: str | None = None,
    country_code_a: str | None = None,
    country_code_b: str | None = None,
    date: date | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
) -> list[RelationsSchema] | RelationsSchema:
    qargs_qmethods: dict[tuple, Callable] = {
        (country_code_a, country_code_b, date): relations_service.get_relations_by_composite_id,
        (country_code_a, country_code_b, date_from, date_to): relations_service.get_relations_by_two_countries_and_date_range,
        (country_code_a, country_code_b): relations_service.get_relations_by_two_countries,
        (country_code, date): relations_service.get_relations_by_country_and_date,
        (country_code,): relations_service.get_relations_by_country,
        (date_from, date_to): relations_service.get_relations_by_date_range,
    }
    for qargs, qmethod in qargs_qmethods.items():
        if any(arg is None for arg in qargs):
            continue
        return qmethod(*qargs)
    names = ", ".join([name[14:].replace('_', ' ') for name in dir(relations_service) if name.startswith("get_")])
    raise HTTPException(
        status_code=400,
        detail=f"Missing query parameters. These are the standard ways of querying relations: {names}",
    )
