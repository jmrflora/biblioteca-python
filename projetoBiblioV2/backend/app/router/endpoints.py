from fastapi import APIRouter

from backend.app.api.livro import router as livros_router


api_router = APIRouter()

include_api = api_router.include_router


routers = (
    (livros_router, "livros", "livros"),
)


for router_item in routers:
    router, prefix, tag = router_item

    if tag:
        include_api(router, prefix=f"/{prefix}", tags=[tag])
    else:
        include_api(router, prefix=f"/{prefix}")