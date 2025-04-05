from typing import Annotated

from fastapi import Depends

from app.core.depends import Asession, CacheService, QueueService
from app.secret.repositories.log import LogRepository
from app.secret.services.secret import SecretService as SecretServiceCls
from app.secret.repositories.secret import SecretRepository


secret_repository = SecretRepository()
log_repository = LogRepository()

def get_secret_service(
    session: Asession,
    cache_service: CacheService,
    queue_service: QueueService,
) -> SecretServiceCls:
    return SecretServiceCls(
        session=session,
        log_repository=log_repository,
        cache_service=cache_service,
        secret_repository=secret_repository,
        queue_service=queue_service,
    )


SecretService = Annotated[SecretServiceCls, Depends(get_secret_service)]