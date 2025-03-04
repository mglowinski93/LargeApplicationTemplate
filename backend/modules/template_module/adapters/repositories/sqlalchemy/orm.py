from datetime import datetime
from uuid import UUID

from sqlalchemy import JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from modules.common.database import Base


class Template(Base):
    __tablename__ = "templates"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    value_data: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    version: Mapped[int] = mapped_column(nullable=False)
