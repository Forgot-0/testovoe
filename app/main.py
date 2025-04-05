from contextlib import asynccontextmanager

from fastapi import FastAPI
import redis.asyncio as redis
from starlette.middleware.cors import CORSMiddleware

from app.secret.routers import router_v1 as secret_router_v1
from app.core.configs.app import app_config
from app.core.middlewares import LoggingMiddleware, NoCacheMiddleware


@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    redis_client = redis.from_url(app_config.redis_url)
    yield
    await redis_client.aclose()


app = FastAPI(
    openapi_url=f'{app_config.API_V1_STR}/openapi.json' if app_config.ENVIRONMENT in ['local', 'staging'] else None,
    lifespan=lifespan,
)

app.add_middleware(LoggingMiddleware)
app.add_middleware(NoCacheMiddleware)

if app_config.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin).strip('/') for origin in app_config.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

app.include_router(secret_router_v1, prefix=app_config.API_V1_STR)

