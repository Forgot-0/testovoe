from datetime import datetime
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.secret.models.secret import Secret
from app.secret.schemas.secret import SecretCreate


class SecretRepository:
    async def create(self, session: AsyncSession, secret: SecretCreate) -> None:
        secret = Secret(**secret.model_dump())
        session.add(secret)

    async def get_by_key(self, session: AsyncSession, key_hash: str) -> Secret | None:
        result = await session.execute(select(Secret).where(Secret.key_hash == key_hash))
        secret = result.scalars().first()
        return secret

    async def delete_by_key(self, session: AsyncSession, key: str) -> None:
        stmt = delete(Secret).where(Secret.key_hash == key)
        await session.execute(stmt)

    async def delete_expired(self, session: AsyncSession) -> None:
        stmt = delete(Secret).where(Secret.expires_at < datetime.now())
        await session.execute(stmt)