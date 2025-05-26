from sqlalchemy import (
    Column, String, Integer, DateTime, JSON, Numeric
)
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class EventModel(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, autoincrement=True)
    aggregate_id = Column(String, index=True)
    event_type = Column(String, nullable=False)
    event_data = Column(JSON, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class BalanceViewModel(Base):
    __tablename__ = "balance_view"
    user_id = Column(String, primary_key=True)
    balance = Column(Numeric(18, 2), nullable=False)

class BalanceHistoryModel(Base):
    __tablename__ = "balance_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, index=True)
    event_type = Column(String, nullable=False)
    amount = Column(Numeric(18,2), nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
