from datetime import datetime

from pydantic import BaseModel, Field


class SecretCreate(BaseModel):
    encrypted_data: str
    key_hash: str
    passphrase_hash: str | None = Field(default=None)
    expires_at: datetime | None = Field(default=None)


class SecretCreateRequest(BaseModel):
    secret: str
    passphrase: str | None = Field(default=None)
    ttl_seconds: int | None = Field(default=None)

class SecretDeleteRequest(BaseModel):
    passphrase: str | None = Field(default=None)

class SecretDeleteResponse(BaseModel):
    status: str = Field(default="secret_deleted")

class SecretResponse(BaseModel):
    secret_key: str

