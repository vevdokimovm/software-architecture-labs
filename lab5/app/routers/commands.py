from fastapi import APIRouter, HTTPException
from app.schemas import CreateBalanceRequest, AdjustBalanceRequest, MessageResponse
from app.event_store import EventStore
from app.aggregate import BalanceAggregate
from app.projections import ProjectionHandler

router = APIRouter(prefix="/commands", tags=["commands"])
store = EventStore()
proj = ProjectionHandler()

@router.post("/create", response_model=MessageResponse)
def create(req: CreateBalanceRequest):
    aid = str(req.user_id)
    agg = BalanceAggregate(aid)
    history = store.load(aid)
    agg.load_from_history(history)
    try:
        changes = agg.handle_create()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    for ev in changes:
        rec = store.append(aid, ev["type"], ev["data"])
        proj.project({
            "type": rec.event_type,
            "data": rec.event_data,
            "aggregate_id": aid,
            "timestamp": rec.timestamp
        })
    return {"detail": "Balance created"}

@router.post("/credit", response_model=MessageResponse)
def credit(req: AdjustBalanceRequest):
    aid = str(req.user_id)
    agg = BalanceAggregate(aid)
    history = store.load(aid)
    agg.load_from_history(history)
    try:
        changes = agg.handle_credit(req.amount)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    for ev in changes:
        rec = store.append(aid, ev["type"], ev["data"])
        proj.project({
            "type": rec.event_type,
            "data": rec.event_data,
            "aggregate_id": aid,
            "timestamp": rec.timestamp
        })
    return {"detail": "Balance credited"}

@router.post("/debit", response_model=MessageResponse)
def debit(req: AdjustBalanceRequest):
    aid = str(req.user_id)
    agg = BalanceAggregate(aid)
    history = store.load(aid)
    agg.load_from_history(history)
    try:
        changes = agg.handle_debit(req.amount)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    for ev in changes:
        rec = store.append(aid, ev["type"], ev["data"])
        proj.project({
            "type": rec.event_type,
            "data": rec.event_data,
            "aggregate_id": aid,
            "timestamp": rec.timestamp
        })
    return {"detail": "Balance debited"}
