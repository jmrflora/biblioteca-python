from fastapi import APIRouter

from projetoBiblio.app.pessoas.api import router as pessoas_router

api_router = APIRouter()

include_api = api_router.include_router

routers = (
    (pessoas_router, "pessoas", "pessoas"),
)

for router_item in routers:
    router, prefix, tag = router_item

    if tag:
        include_api(router, prefix=f"/{prefix}", tags=[tag])
    else:
        include_api(router, prefix=f"/{prefix}")