from bson import ObjectId
from fastapi.encoders import ENCODERS_BY_TYPE
from pymongo.results import (
    DeleteResult,
    InsertManyResult,
    InsertOneResult,
    UpdateResult,
)


def add_custom_encodings() -> None:
    ENCODERS_BY_TYPE[ObjectId] = str
    ENCODERS_BY_TYPE[InsertOneResult] = str
    ENCODERS_BY_TYPE[DeleteResult] = lambda obj: obj.raw_result
    ENCODERS_BY_TYPE[UpdateResult] = lambda obj: obj.raw_result
    ENCODERS_BY_TYPE[InsertOneResult] = lambda o: str(o.inserted_id) if isinstance(o.inserted_id, ObjectId) else o.inserted_id
    ENCODERS_BY_TYPE[InsertManyResult] = lambda obj: [str(o) if isinstance(o, ObjectId) else o for o in obj.inserted_ids]
