from fastapi import APIRouter

from app.secret.routes.v1.secret import router as secret_router

router_v1 = APIRouter()

router_v1.include_router(secret_router, tags=["secret"])
