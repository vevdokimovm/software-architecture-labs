from fastapi import APIRouter, HTTPException
from app.schemas import BalanceViewResponse, BalanceHistoryEntryResponse
from app.models import BalanceViewModel, BalanceHistoryModel
from app.event_store import SessionLocal
from uuid import UUID

router = APIRouter(prefix="/queries", tags=["queries"])

@router.get("/balance/{user_id}", response_model=BalanceViewResponse)
def get_balance(user_id: UUID):
    db = SessionLocal()
    view = db.query(BalanceViewModel).get(str(user_id))
    db.close()
    if not view:
        raise HTTPException(status_code=404, detail="Not found")
    return {"user_id": user_id, "balance": view.balance}

@router.get("/history/{user_id}", response_model=list[BalanceHistoryEntryResponse])
def get_history(user_id: UUID):
    db = SessionLocal()
    entries = (
        db.query(BalanceHistoryModel)
          .filter(BalanceHistoryModel.user_id == str(user_id))
          .order_by(BalanceHistoryModel.timestamp.desc())
          .all()
    )
    db.close()
    return [
        {
            "event_type": e.event_type,
            "amount": e.amount,
            "timestamp": e.timestamp
        } for e in entries
    ]
