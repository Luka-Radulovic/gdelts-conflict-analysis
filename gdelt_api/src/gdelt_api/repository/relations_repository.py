from datetime import date

from gdelt_api.database.models import RelationsModel
from gdelt_api.database.session import session_scope


def add_relations(relations: RelationsModel) -> RelationsModel:
    with session_scope() as session:
        session.add(relations)
    return relations


def add_all_relations(relations: list[RelationsModel]) -> list[RelationsModel]:
    with session_scope() as session:
        session.add_all(relations)
    return relations


def get_relations_by_country_and_date(country_code: str, date: date) -> list[RelationsModel]:
    with session_scope() as session:
        result_a = (
            session.query(RelationsModel)
            .filter(RelationsModel.country_code_a == country_code, RelationsModel.date == date)
            .all()
        )
        result_b = (
            session.query(RelationsModel)
            .filter(RelationsModel.country_code_b == country_code, RelationsModel.date == date)
            .all()
        )

    return result_a + result_b


def get_relations_by_two_countries(
    country_code_a: str, country_code_b: str
) -> list[RelationsModel]:
    with session_scope() as session:
        result = (
            session.query(RelationsModel)
            .filter(
                RelationsModel.country_code_a == country_code_a,
                RelationsModel.country_code_b == country_code_b,
            )
            .all()
        )
    return result


def get_relations_by_composite_id(
    country_code_a: str, country_code_b: str, date: date
) -> RelationsModel | None:
    with session_scope() as session:
        result = (
            session.query(RelationsModel)
            .filter(
                RelationsModel.country_code_a == country_code_a,
                RelationsModel.country_code_b == country_code_b,
                RelationsModel.date == date,
            )
            .first()
        )
    return result


def get_relations_by_two_countries_and_date_range(
    country_code_a: str, country_code_b: str, date_from: date, date_to: date
) -> list[RelationsModel]:
    with session_scope() as session:
        result = (
            session.query(RelationsModel)
            .filter(
                RelationsModel.country_code_a == country_code_a,
                RelationsModel.country_code_b == country_code_b,
                RelationsModel.date >= date_from,
                RelationsModel.date <= date_to,
            )
            .all()
        )
    return result


def get_relations_by_country(country_code: str) -> list[RelationsModel]:
    with session_scope() as session:
        result_a = (
            session.query(RelationsModel)
            .filter(RelationsModel.country_code_a == country_code)
            .all()
        )
        result_b = (
            session.query(RelationsModel)
            .filter(RelationsModel.country_code_b == country_code)
            .all()
        )
    return result_a + result_b


def get_relations_by_date_range(date_from: date, date_to: date) -> list[RelationsModel]:
    with session_scope() as session:
        result = (
            session.query(RelationsModel)
            .filter(RelationsModel.date >= date_from, RelationsModel.date <= date_to)
            .all()
        )
    return result
