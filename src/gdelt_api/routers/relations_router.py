from datetime import date
from fastapi import APIRouter

from gdelt_api.schema import RelationsSchema
from gdelt_api.services import relations_service


router: APIRouter = APIRouter(prefix="/relations")


@router.post("/")
async def add_relations(relations: RelationsSchema) -> RelationsSchema:
    return relations_service.add_relations(relations)


@router.get("")
async def get_relations_country_date(country_code: str, date: date) -> list[RelationsSchema]:
    return relations_service.get_relations_country_date(country_code, date)
