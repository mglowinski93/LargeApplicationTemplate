from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column

from .....common.database import Base


# an example mapping using the base
class Template(Base):
    __tablename__ = "templates"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    value_data: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime)
