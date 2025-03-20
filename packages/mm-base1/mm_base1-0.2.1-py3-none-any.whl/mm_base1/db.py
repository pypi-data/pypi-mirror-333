from bson import ObjectId
from mm_mongo import DatabaseAny, MongoCollection

from mm_base1.models import DConfig, DLog, DValue


class BaseDB:
    def __init__(self, database: DatabaseAny) -> None:
        self.dconfig: MongoCollection[str, DConfig] = MongoCollection(database, DConfig)
        self.dvalue: MongoCollection[str, DValue] = MongoCollection(database, DValue)
        self.dlog: MongoCollection[ObjectId, DLog] = MongoCollection(database, DLog)
