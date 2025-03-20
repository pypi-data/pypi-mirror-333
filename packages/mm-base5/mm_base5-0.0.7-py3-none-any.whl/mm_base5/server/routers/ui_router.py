from typing import Annotated, cast

from fastapi import APIRouter, Form, Query
from starlette.responses import HTMLResponse, RedirectResponse

from mm_base5.server.deps import BaseCoreDep, FormDep, RenderDep
from mm_base5.server.utils import redirect

router: APIRouter = APIRouter(prefix="/system", include_in_schema=False)

# PAGES


@router.get("/")
def system_page(render: RenderDep, core: BaseCoreDep) -> HTMLResponse:
    has_telegram_settings = core.system_service.has_telegram_settings()
    return render.html("system.j2", stats=core.system_service.get_stats(), has_telegram_settings=has_telegram_settings)


@router.get("/dconfigs")
def dconfigs_page(render: RenderDep, core: BaseCoreDep) -> HTMLResponse:
    return render.html("dconfigs.j2", info=core.system_service.get_dconfig_info())


@router.get("/dconfigs/toml")
def dconfigs_toml_page(render: RenderDep, core: BaseCoreDep) -> HTMLResponse:
    return render.html("dconfigs_toml.j2", toml_str=core.system_service.export_dconfig_as_toml())


@router.get("/dconfigs/multiline/{key:str}")
def dconfigs_multiline_page(render: RenderDep, core: BaseCoreDep, key: str) -> HTMLResponse:
    return render.html("dconfigs_multiline.j2", dconfig=core.dconfig, key=key)


@router.get("/dvalues")
def dvalues_page(render: RenderDep, core: BaseCoreDep) -> HTMLResponse:
    return render.html("dvalues.j2", info=core.system_service.get_dvalue_info())


@router.get("/dvalues/{key:str}")
def update_dvalue_page(render: RenderDep, core: BaseCoreDep, key: str) -> HTMLResponse:
    return render.html("dvalues_update.j2", value=core.system_service.export_dvalue_field_as_toml(key), key=key)


@router.get("/dlogs")
def dlogs_page(
    render: RenderDep, core: BaseCoreDep, category: Annotated[str | None, Query()] = None, limit: Annotated[int, Query()] = 100
) -> HTMLResponse:
    category_stats = core.system_service.get_dlog_category_stats()
    query = {"category": category} if category else {}
    dlogs = core.db.dlog.find(query, "-created_at", limit)
    form = {"category": category, "limit": limit}
    all_count = core.db.dlog.count({})
    return render.html("dlogs.j2", dlogs=dlogs, category_stats=category_stats, form=form, all_count=all_count)


# ACTIONS


@router.post("/dconfigs")
def update_dconfig(render: RenderDep, core: BaseCoreDep, form: FormDep) -> RedirectResponse:
    data = cast(dict[str, str], form)
    core.system_service.update_dconfig(data)
    render.flash("dconfigs updated successfully")
    return redirect("/system/dconfigs")


@router.post("/dconfigs/multiline/{key:str}")
def update_dconfig_multiline(render: RenderDep, core: BaseCoreDep, key: str, value: Annotated[str, Form()]) -> RedirectResponse:
    core.system_service.update_dconfig({key: value})
    render.flash("dconfig updated successfully")
    return redirect("/system/dconfigs")


@router.post("/dconfigs/toml")
def update_dconfig_from_toml(render: RenderDep, core: BaseCoreDep, value: Annotated[str, Form()]) -> RedirectResponse:
    core.system_service.update_dconfig_from_toml(value)
    render.flash("dconfigs updated successfully")
    return redirect("/system/dconfigs")


@router.post("/dvalues/{key:str}")
def update_dvalue(render: RenderDep, core: BaseCoreDep, key: str, value: Annotated[str, Form()]) -> RedirectResponse:
    core.system_service.update_dvalue_field(key, value)
    render.flash("dvalue updated successfully")
    return redirect("/system/dvalues")
