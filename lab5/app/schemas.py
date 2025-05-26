from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal
import datetime

class CreateBalanceRequest(BaseModel):
    user_id: UUID

class AdjustBalanceRequest(BaseModel):
    user_id: UUID
    amount: Decimal

class BalanceViewResponse(BaseModel):
    user_id: UUID
    balance: Decimal

class BalanceHistoryEntryResponse(BaseModel):
    event_type: str
    amount: Decimal
    timestamp: datetime.datetime

class MessageResponse(BaseModel):
    detail: str
