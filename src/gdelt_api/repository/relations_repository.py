from gdelt_api.database.models import RelationsModel
from gdelt_api.database.session import session_scope


def add_relations(relations: RelationsModel) -> RelationsModel:
    with session_scope() as session:
        session.add(relations)
    return relations
