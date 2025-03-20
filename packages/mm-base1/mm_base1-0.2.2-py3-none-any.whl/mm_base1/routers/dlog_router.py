from bson import ObjectId
from fastapi import APIRouter
from mm_mongo import MongoDeleteResult, mongo_query

from mm_base1.app import BaseApp
from mm_base1.models import DLog


def init(app: BaseApp) -> APIRouter:
    router = APIRouter()

    @router.get("")
    def get_dlogs(category: str | None = None, limit: int = 100) -> list[DLog]:
        return app.dlog_collection.find(mongo_query(category=category), "-created_at", limit=limit)

    @router.delete("", response_model=None)
    def delete_all_dlogs() -> MongoDeleteResult:
        return app.dlog_collection.delete_many({})

    @router.get("/{pk}")
    def get_dlog(pk: ObjectId) -> DLog:
        return app.dlog_collection.get(pk)

    @router.delete("/{pk}", response_model=None)
    def delete_dlog(pk: ObjectId) -> MongoDeleteResult:
        return app.dlog_collection.delete(pk)

    @router.delete("/category/{category}", response_model=None)
    def delete_by_category(category: str) -> MongoDeleteResult:
        return app.dlog_collection.delete_many({"category": category})

    return router
