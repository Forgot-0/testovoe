from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import uuid4

from sqlalchemy.orm import Session

from app.core.services.cache.base import CacheServiceInterface
from app.core.services.queue.service import QueueServiceInterface
from app.secret.repositories.log import LogRepository
from app.secret.repositories.secret import SecretRepository
from app.secret.schemas.log import LogCreate
from app.secret.schemas.secret import SecretCreate, SecretCreateRequest, SecretDeleteRequest
from app.secret.security import decrypt_data, encrypt_data, hash_key, hash_passphrase



@dataclass
class SecretService:
    session: Session
    log_repository: LogRepository
    secret_repository: SecretRepository
    cache_service: CacheServiceInterface
    queue_service: QueueServiceInterface

    async def create_secret(self, secret_request: SecretCreateRequest, ip_address: str) -> str:
        encrypted_data = encrypt_data(secret_request.secret)
        secret_key = str(uuid4())
        key_hash = hash_key(secret_key)
        passphrase_hash = hash_passphrase(secret_request.passphrase) if secret_request.passphrase else None
        expires_at = (
            datetime.now() + timedelta(seconds=secret_request.ttl_seconds) 
            if secret_request.ttl_seconds else None
        )

        secret = SecretCreate(
            encrypted_data=encrypted_data,
            key_hash=key_hash,
            passphrase_hash=passphrase_hash,
            expires_at=expires_at,
        )
        ttl_seconds = secret_request.ttl_seconds if secret_request.ttl_seconds else 5*60
        await self.secret_repository.create(self.session, secret)
        await self.cache_service.set(
            secret.key_hash, secret.encrypted_data,
            ttl=max(ttl_seconds, 5*60)
        )
        log = LogCreate(
            event_type="secret_created",
            ip_address=ip_address,
            secret_key_hash=key_hash,
            data={
                "ttl_seconds": secret_request.ttl_seconds,
                "passphrase": passphrase_hash,
            },
        )
        await self.log_repository.create(self.session, log)

        await self.session.commit()

        return secret_key

    async def get_secret(self, key: str, ip_address: str) -> str | None:
        key_hash = hash_key(key)
        cached_secret = await self.cache_service.get(key_hash)

        secret_data = cached_secret

        if not secret_data:
            secret = await self.secret_repository.get_by_key(self.session, key_hash)
            if secret:
                if secret.expires_at and secret.expires_at < datetime.now():
                    await self.delete_secret(key)
                    return None

                secret_data = secret.encrypted_data if secret else None


        if secret_data:
            log = LogCreate(
                event_type="secret_retrieved",
                ip_address=ip_address,
                secret_key_hash=key_hash,
                data={},
            )
            await self.log_repository.create(self.session, log)
            await self.delete_secret(key)
            return decrypt_data(secret_data)

    async def delete_secret(self, key: str) -> None:
        key_hash = hash_key(key)
        await self.secret_repository.delete_by_key(self.session, key_hash)
        await self.cache_service.delete(key_hash)
        await self.session.commit()
    
    async def delete_secret_request(self, key: str, delete_request: SecretDeleteRequest, ip_address: str) -> None:
        key_hash = hash_key(key)
        secrets = await self.secret_repository.get_by_key(self.session, key_hash)

        if not secrets:
            raise ...

        if secrets.passphrase_hash:
            if secrets.passphrase_hash != hash_passphrase(delete_request.passphrase):
                raise ...

        await self.secret_repository.delete_by_key(self.session, key_hash)
        await self.cache_service.delete(key_hash)
        if secrets:
            log = LogCreate(
                event_type="secret_deleted",
                ip_address=ip_address,
                secret_key_hash=key_hash,
                data={
                    "key_hash": key_hash,
                    "passphrase": secrets.passphrase_hash,
                },
            )
            await self.log_repository.create(self.session, log)

        await self.session.commit()

