from decimal import Decimal
from app.models import BalanceViewModel, BalanceHistoryModel
from app.event_store import SessionLocal

class ProjectionHandler:
    def __init__(self):
        self.Session = SessionLocal

    def project(self, event):
        db = self.Session()
        et = event["type"]
        aid = event["aggregate_id"]
        data = event["data"]

        # История
        if et in ("BalanceCredited", "BalanceDebited"):
            entry = BalanceHistoryModel(
                user_id=aid,
                event_type=et,
                amount=Decimal(str(data["amount"])),
                timestamp=event.get("timestamp")
            )
            db.add(entry)

        # Проекция баланса
        if et == "BalanceCreated":
            view = BalanceViewModel(user_id=aid, balance=Decimal("0.00"))
            db.add(view)
        elif et == "BalanceCredited":
            view = db.query(BalanceViewModel).get(aid)
            view.balance += Decimal(str(data["amount"]))
        elif et == "BalanceDebited":
            view = db.query(BalanceViewModel).get(aid)
            view.balance -= Decimal(str(data["amount"]))

        db.commit()
        db.close()
