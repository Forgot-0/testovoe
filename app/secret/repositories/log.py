from sqlalchemy.ext.asyncio import AsyncSession

from app.secret.models.log import Log
from app.secret.schemas.log import LogCreate


class LogRepository:
    async def create(self, session: AsyncSession, log_create: LogCreate) -> Log:
        log = Log(**log_create.model_dump())
        session.add(log)
