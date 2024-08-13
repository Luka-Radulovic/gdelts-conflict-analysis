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


def get_relations_by_two_countries_and_date_range(
    country_code_a: str, country_code_b: str, date_from: date, date_to: date
) -> list[RelationsSchema]:
    if country_code_a > country_code_b:
        country_code_a, country_code_b = country_code_b, country_code_a
    return [
        RelationsSchema.model_construct(**relations.__dict__)
        for relations in relations_repository.get_relations_by_two_countries_and_date_range(
            country_code_a, country_code_b, date_from, date_to
        )
    ]


def get_relations_by_country(country_code: str) -> list[RelationsSchema]:
    return [
        RelationsSchema.model_construct(**relations.__dict__)
        for relations in relations_repository.get_relations_by_country(country_code)
    ]


def get_relations_by_date_range(date_from: date, date_to: date) -> list[RelationsSchema]:
    return [
        RelationsSchema.model_construct(**relations.__dict__)
        for relations in relations_repository.get_relations_by_date_range(date_from, date_to)
    ]
