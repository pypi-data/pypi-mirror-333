from bson import ObjectId
from fastapi import APIRouter
from mm_mongo import MongoDeleteResult

from mm_base5.core.db import DLog
from mm_base5.server.deps import BaseCoreDep

router: APIRouter = APIRouter(prefix="/api/system/dlogs", tags=["system"])


@router.get("/{id}")
def get_dlog(core: BaseCoreDep, id: ObjectId) -> DLog:
    return core.db.dlog.get(id)


@router.delete("/{id}")
def delete_dlog(core: BaseCoreDep, id: ObjectId) -> MongoDeleteResult:
    return core.db.dlog.delete(id)


@router.delete("/category/{category}")
def delete_by_category(core: BaseCoreDep, category: str) -> MongoDeleteResult:
    return core.db.dlog.delete_many({"category": category})


@router.delete("")
def delete_all_dlogs(core: BaseCoreDep) -> MongoDeleteResult:
    core.logger.debug("delete_all_dlogs called")
    return core.db.dlog.delete_many({})
