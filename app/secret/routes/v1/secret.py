# app/secret/routes/v1/secret.py
from fastapi import APIRouter, HTTPException, Request, status

from app.secret.deps import SecretService
from app.secret.schemas.secret import SecretCreateRequest, SecretDeleteRequest, SecretDeleteResponse, SecretResponse

router = APIRouter()


@router.post(
    "/secret",
    status_code=status.HTTP_201_CREATED,
    response_model=SecretResponse,
    summary="Create a secret",
    description="Create a secret with an optional passphrase and TTL",
)
async def create_secret(
    request: Request,
    secret_request: SecretCreateRequest,
    secret_service: SecretService,
) -> SecretResponse:
    key = await secret_service.create_secret(secret_request, ip_address=request.client.host)
    return SecretResponse(secret_key=key)

@router.get(
    "/secret/{key}",
    status_code=status.HTTP_200_OK,
    summary="Get a secret",
    description="Get a secret by its key",
)
async def get_secret(
    key: str,
    request: Request,
    secret_service: SecretService,
) -> str:
    secret = await secret_service.get_secret(key, ip_address=request.client.host)
    if not secret:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Secret not found")
    return secret

@router.delete(
    "/secret/{key}",
    status_code=status.HTTP_200_OK,
    response_model=SecretDeleteResponse,
    summary="Delete a secret",
    description="Delete a secret by its key",
)
async def delete_secret(
    key: str,
    request: Request,
    delete_request: SecretDeleteRequest,
    secret_service: SecretService,
) -> SecretDeleteResponse:
    await secret_service.delete_secret_request(key, delete_request, ip_address=request.client.host)
    return SecretDeleteResponse(status="secret_deleted")

