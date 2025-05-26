from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, EventModel
import json
from decimal import Decimal

# Создаём движок SQLite
engine = create_engine(
    "sqlite:///laba5.db",
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

def init_db():
    Base.metadata.create_all(bind=engine)

class EventStore:
    def __init__(self):
        self.Session = SessionLocal

    def append(self, aggregate_id: str, event_type: str, data: dict):
        db = self.Session()

        # сериализуем Decimal -> str (иначе SQLite JSON сломается)
        def convert(o):
            if isinstance(o, Decimal):
                return str(o)
            return o

        clean_data = json.loads(json.dumps(data, default=convert))

        ev = EventModel(
            aggregate_id=aggregate_id,
            event_type=event_type,
            event_data=clean_data
        )
        db.add(ev)
        db.commit()
        db.close()
        return ev

    def load(self, aggregate_id: str):
        db = self.Session()
        evs = (
            db.query(EventModel)
              .filter_by(aggregate_id=aggregate_id)
              .order_by(EventModel.id)
              .all()
        )
        db.close()
        return evs
