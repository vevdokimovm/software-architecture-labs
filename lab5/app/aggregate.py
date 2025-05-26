from decimal import Decimal
from app.event_store import EventStore

class BalanceAggregate:
    def __init__(self, aggregate_id: str):
        self.user_id = aggregate_id
        self.balance = Decimal("0.00")
        self.changes = []

    def apply(self, event):
        et = event["type"]
        d = event["data"]
        if et == "BalanceCreated":
            self.balance = Decimal("0.00")
        elif et == "BalanceCredited":
            self.balance += Decimal(str(d["amount"]))
        elif et == "BalanceDebited":
            self.balance -= Decimal(str(d["amount"]))

    def load_from_history(self, events):
        for ev in events:
            self.apply({"type": ev.event_type, "data": ev.event_data})

    def handle_create(self):
        if self.changes:
            raise ValueError("Already created")
        self.changes.append({"type": "BalanceCreated", "data": {}})
        return self.changes

    def handle_credit(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be > 0")
        self.changes.append({"type": "BalanceCredited", "data": {"amount": amount}})
        return self.changes

    def handle_debit(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be > 0")
        if self.balance < amount:
            raise ValueError("Insufficient funds")
        self.changes.append({"type": "BalanceDebited", "data": {"amount": amount}})
        return self.changes
