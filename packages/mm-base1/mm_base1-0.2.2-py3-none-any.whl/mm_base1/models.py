from datetime import datetime
from enum import Enum, unique
from typing import ClassVar

from bson import ObjectId
from mm_mongo import MongoModel
from mm_std import utc_now
from pydantic import Field


@unique
class DConfigType(str, Enum):
    STRING = "STRING"
    MULTILINE = "MULTILINE"
    DATETIME = "DATETIME"
    BOOLEAN = "BOOLEAN"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    DECIMAL = "DECIMAL"


class DConfig(MongoModel[str]):
    type: DConfigType
    value: str
    updated_at: datetime | None = None
    created_at: datetime = Field(default_factory=utc_now)

    __collection__: str = "dconfig"
    __validator__: ClassVar[dict[str, object]] = {
        "$jsonSchema": {
            "required": ["type", "value", "updated_at", "created_at"],
            "additionalProperties": False,
            "properties": {
                "_id": {"bsonType": "string"},
                "type": {"enum": ["STRING", "MULTILINE", "DATETIME", "BOOLEAN", "INTEGER", "FLOAT", "DECIMAL"]},
                "value": {"bsonType": "string"},
                "updated_at": {"bsonType": ["date", "null"]},
                "created_at": {"bsonType": "date"},
            },
        },
    }


class DValue(MongoModel[str]):
    value: str
    updated_at: datetime | None = None
    created_at: datetime = Field(default_factory=utc_now)

    __collection__ = "dvalue"
    __validator__: ClassVar[dict[str, object]] = {
        "$jsonSchema": {
            "required": ["value", "updated_at", "created_at"],
            "additionalProperties": False,
            "properties": {
                "_id": {"bsonType": "string"},
                "value": {"bsonType": "string"},
                "updated_at": {"bsonType": ["date", "null"]},
                "created_at": {"bsonType": "date"},
            },
        },
    }


class DLog(MongoModel[ObjectId]):
    category: str
    data: object
    created_at: datetime = Field(default_factory=utc_now)

    __collection__: str = "dlog"
    __indexes__ = "category, created_at"
    __validator__: ClassVar[dict[str, object]] = {
        "$jsonSchema": {
            "required": ["category", "data", "created_at"],
            "additionalProperties": False,
            "properties": {
                "_id": {"bsonType": "objectId"},
                "category": {"bsonType": "string"},
                "data": {},
                "created_at": {"bsonType": "date"},
            },
        },
    }
