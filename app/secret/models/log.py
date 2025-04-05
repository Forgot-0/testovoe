from sqlalchemy import UUID, Column, DateTime, String, func, text
from sqlalchemy.dialects.postgresql import JSONB, INET

from app.core.db.base_model import BaseModel


class Log(BaseModel):
    __tablename__ = "logs"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    event_type = Column(String(20), nullable=False)
    ip_address = Column(INET, nullable=False)
    secret_key_hash = Column(String, nullable=False)
    data = Column(JSONB, nullable=False)
    created_at = Column(DateTime, default=func.now())