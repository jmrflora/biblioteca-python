from fastapi import APIRouter

from backend.app.api.livro import router as livros_router
from backend.app.api.usuario import router as usuarios_router
from backend.app.api.admin import router as admins_router
from backend.app.api.emprestimo import router as emprestimos_router
from backend.app.api.reserva import router as reservas_router
from backend.app.api.devolucao import router as devolucoes_router
from backend.app.api.notaDePagamento import router as notas_router
from backend.app.api.auth import router as auth_router
from backend.app.api.exemplar import router as exemplar_router



"""""
from backend.app.api.usuario import router as usuarios_router
from backend.app.api.admin import router as admins_router
from backend.app.api.emprestimo import router as emprestimos_router
from backend.app.api.reserva import router as reservas_router
from backend.app.api.devolucao import router as devolucoes_router
from backend.app.api.notaDePagamento import router as notas_router
"""

api_router = APIRouter()

include_api = api_router.include_router


routers = (
    (livros_router, "livros", "livros"),
    (usuarios_router, "usuarios", "usuarios"),
    (admins_router, "admins", "admins"),
    (emprestimos_router, "emprestimos", "emprestimos"),
    (reservas_router, "reservas", "reservas"),
    (devolucoes_router, "devolucoes", "devolucoes"),
    (notas_router, "notas", "notas"),
    (auth_router, "auth", "auth"),
    (exemplar_router, "exemplar", "exemplar"),
)

for router_item in routers:
    router, prefix, tag = router_item

    if tag:
        include_api(router, prefix=f"/{prefix}", tags=[tag])
    else:
        include_api(router, prefix=f"/{prefix}")
