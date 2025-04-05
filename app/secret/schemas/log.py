
from typing import Any

from pydantic import BaseModel


class LogCreate(BaseModel):
    event_type: str
    ip_address: str
    secret_key_hash: str
    data: dict[str, Any]

