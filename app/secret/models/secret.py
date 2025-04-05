from sqlalchemy import Column, String, DateTime, Boolean, func


from app.core.db.base_model import BaseModel


class Secret(BaseModel):
    __tablename__ = "secrets"

    encrypted_data = Column(String, nullable=False)
    key_hash = Column(String, primary_key=True, unique=True, nullable=False)
    passphrase_hash = Column(String, nullable=True, default=None)
    created_at = Column(DateTime, default=func.now())
    expires_at = Column(DateTime, nullable=True)
    is_used = Column(Boolean, default=False)

