from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TransactionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date: str
    description: str
    category: Optional[str]
    amount: float
    currency: Optional[str]
    created_at: datetime


class UploadResponse(BaseModel):
    status: str
    created: int
