from datetime import date

from gdelt_api.database.models import RelationsModel
from gdelt_api.repository import relations_repository
from gdelt_api.schema import RelationsSchema


def add_relations(relations: RelationsSchema) -> RelationsSchema:
    if relations.country_code_a > relations.country_code_b:
        relations.country_code_a, relations.country_code_b = (
            relations.country_code_b,
            relations.country_code_a,
        )
    model = RelationsModel(**relations.model_dump())
    result = relations_repository.add_relations(model)
    return RelationsSchema.model_construct(**result.__dict__)


def get_relations_by_country_and_date(country_code: str, date: date) -> list[RelationsSchema]:
    return [
        RelationsSchema.model_construct(**relations.__dict__)
        for relations in relations_repository.get_relations_by_country_and_date(country_code, date)
    ]


def get_relations_by_two_countries(
    country_code_a: str, country_code_b: str
) -> list[RelationsSchema]:
    if country_code_a > country_code_b:
        country_code_a, country_code_b = country_code_b, country_code_a
    return [
        RelationsSchema.model_construct(**relations.__dict__)
        for relations in relations_repository.get_relations_by_two_countries(
            country_code_a, country_code_b
        )
    ]


def get_relations_by_composite_id(
    country_code_a: str, country_code_b: str, date: date
) -> RelationsSchema:
    if country_code_a > country_code_b:
        country_code_a, country_code_b = country_code_b, country_code_a
    return RelationsSchema.model_construct(
        **relations_repository.get_relations_by_composite_id(
            country_code_a, country_code_b, date
        ).__dict__
    )
