from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_session
from app.core.services.cache.base import CacheServiceInterface
from app.core.services.cache.deps import get_cache_service, get_cached_decorator
from app.core.services.log.depends import get_log_service
from app.core.services.queue.depends import get_queue_service, get_queued_decorator
from app.core.services.queue.service import QueueServiceInterface
from app.core.services.queue.taskiq.init import broker

logger = get_log_service()


Asession = Annotated[AsyncSession, Depends(get_session)]
QueueService = Annotated[QueueServiceInterface, Depends(get_queue_service)]
CacheService = Annotated[CacheServiceInterface, Depends(get_cache_service)]
 
cached = get_cached_decorator()
queued = get_queued_decorator()


# @broker.depends
# async def get_session_task_iq() -> AsyncGenerator[AsyncSession, None]:
#     async for session in get_session():
#         yield session
