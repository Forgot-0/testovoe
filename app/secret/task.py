from taskiq import TaskiqDepends
from sqlalchemy.ext.asyncio import AsyncSession


from app.core.db.session import get_session
from app.core.services.queue.task import BaseTask
from app.core.depends import queued
from app.secret.repositories.secret import SecretRepository


@queued
class DeleteExpiredSecret(BaseTask):
    __task_name__ = 'delete_expired_secret'
    __schedule__ = "* * * * *"

    async def run(self, session: AsyncSession = TaskiqDepends(get_session)) -> None:
        secret_repository = SecretRepository()
        await secret_repository.delete_expired(session)
        await session.commit()
        await session.close()
