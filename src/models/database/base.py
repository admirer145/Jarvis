from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, UTC
from sqlalchemy import Column, DateTime

Base = declarative_base()

class TimestampMixin:
    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC), nullable=False) 