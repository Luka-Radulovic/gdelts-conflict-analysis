from datetime import date

from fastapi import HTTPException
import sqlalchemy

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
    try:
        result = relations_repository.add_relations(model)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(400, "Relations already exist for this composite key.")
    return RelationsSchema.model_construct(**result.__dict__)


def get_relations_by_country_and_date(country_code: str, date: date) -> list[RelationsSchema]:
    return [
        RelationsSchema.model_construct_cc(country_code, relations.__dict__)
        for relations in relations_repository.get_relations_by_country_and_date(country_code, date)
    ]


def get_relations_by_two_countries(
    country_code_a: str, country_code_b: str
) -> list[RelationsSchema]:
    cca, ccb = country_code_a, country_code_b
    if cca > ccb:
        cca, ccb = ccb, cca
    return [
        RelationsSchema.model_construct_cc(country_code_a, relations.__dict__)
        for relations in relations_repository.get_relations_by_two_countries(
            cca, ccb
        )
    ]


def get_relations_by_composite_id(
    country_code_a: str, country_code_b: str, date: date
) -> RelationsSchema:
    cca, ccb = country_code_a, country_code_b
    if cca > ccb:
        cca, ccb = ccb, cca
    return RelationsSchema.model_construct_cc(
        country_code_a,
        relations_repository.get_relations_by_composite_id(
            cca, ccb, date
        ).__dict__,
    )


def get_relations_by_two_countries_and_date_range(
    country_code_a: str, country_code_b: str, date_from: date, date_to: date
) -> list[RelationsSchema]:
    cca, ccb = country_code_a, country_code_b
    if cca > ccb:
        cca, ccb = ccb, cca
    return [
        RelationsSchema.model_construct_cc(cca, **relations.__dict__)
        for relations in relations_repository.get_relations_by_two_countries_and_date_range(
            cca, ccb, date_from, date_to
        )
    ]


def get_relations_by_country(country_code: str) -> list[RelationsSchema]:
    return [
        RelationsSchema.model_construct_cc(country_code, relations.__dict__)
        for relations in relations_repository.get_relations_by_country(country_code)
    ]


def get_relations_by_date_range(date_from: date, date_to: date) -> list[RelationsSchema]:
    return [
        RelationsSchema.model_construct(**relations.__dict__)
        for relations in relations_repository.get_relations_by_date_range(date_from, date_to)
    ]
