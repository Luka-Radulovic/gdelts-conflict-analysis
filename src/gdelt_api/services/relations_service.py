from gdelt_api.database.models import RelationsModel
from gdelt_api.repository import relations_repository
from gdelt_api.schema import RelationsSchema


def add_relations(relations: RelationsSchema) -> RelationsSchema:
    model = RelationsModel(**relations.model_dump())
    result = relations_repository.add_relations(model)
    return RelationsSchema.model_construct(**result.__dict__)
