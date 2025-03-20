from fastapi import APIRouter
from starlette.responses import PlainTextResponse

from mm_base5.core.db import DValue
from mm_base5.server.deps import BaseCoreDep

router: APIRouter = APIRouter(prefix="/api/system/dvalues", tags=["system"])


@router.get("/toml", response_class=PlainTextResponse)
def get_dvalues_as_toml(core: BaseCoreDep) -> str:
    return core.system_service.export_dvalue_as_toml()


@router.get("/{key}/toml", response_class=PlainTextResponse)
def get_dvalue_field_as_toml(core: BaseCoreDep, key: str) -> str:
    return core.system_service.export_dvalue_field_as_toml(key)


@router.get("/{key}/value")
def get_dvalue_value(core: BaseCoreDep, key: str) -> object:
    return core.system_service.get_dvalue_value(key)


@router.get("/{key}")
def get_dvalue_key(core: BaseCoreDep, key: str) -> DValue:
    return core.db.dvalue.get(key)
