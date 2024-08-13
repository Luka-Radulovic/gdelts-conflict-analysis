from datetime import date

from fastapi import APIRouter, HTTPException

from gdelt_api.schema import RelationsSchema
from gdelt_api.services import relations_service

router: APIRouter = APIRouter(prefix="/relations")


@router.post("/")
async def add_relations(relations: RelationsSchema) -> RelationsSchema:
    return relations_service.add_relations(relations)


@router.get("/")
async def get_relations(
    country_code: str = "",
    country_code_a: str = "",
    country_code_b: str = "",
    date: date | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
) -> list[RelationsSchema] | RelationsSchema:
    if country_code_a and country_code_b and date:
        return relations_service.get_relations_by_composite_id(country_code_a, country_code_b, date)
    elif country_code_a and country_code_b and date_from and date_to:
        return relations_service.get_relations_by_two_countries_and_date_range(
            country_code_a, country_code_b, date_from, date_to
        )
    elif country_code_a and country_code_b:
        return relations_service.get_relations_by_two_countries(country_code_a, country_code_b)
    elif country_code and date:
        return relations_service.get_relations_by_country_and_date(country_code, date)
    elif country_code:
        return relations_service.get_relations_by_country(country_code)
    elif date_from and date_to:
        return relations_service.get_relations_by_date_range(date_from, date_to)
    else:
        raise HTTPException(
            status_code=400,
            detail="Relations can be queried by supplying either: both country codes, one country code and a date, or both country codes and a date.",
        )
