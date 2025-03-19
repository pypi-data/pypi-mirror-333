from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP, TEXT
from sqlalchemy.orm import relationship
from .base import Base


class Announcement(Base):
    __tablename__ = "announcements"
    __table_args__ = {"schema": "gopacs"}

    id = Column(UUID(as_uuid=True), primary_key=True)
    problem_id = Column(UUID(as_uuid=True), nullable=False)
    message = Column(TEXT, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False)
    last_updated_at = Column(TIMESTAMP(timezone=True), nullable=False)
    type = Column(TEXT, nullable=False)

    # Relationships
    areas = relationship(
        "AnnouncementArea",
        back_populates="announcement",
        cascade="all, delete",
        secondary="announcement_areas",
    )


class Area(Base):
    __tablename__ = "areas"
    __table_args__ = {"schema": "gopacs"}

    id = Column(TEXT, primary_key=True)

    # Relationships
    areas = relationship(
        "AnnouncementArea",
        back_populates="area",
        cascade="all, delete",
        secondary="announcement_areas",
    )


class AnnouncementArea(Base):
    __tablename__ = "announcement_areas"
    __table_args__ = {"schema": "gopacs"}

    announcement_id = Column(
        UUID(as_uuid=True),
        ForeignKey("gopacs.announcements.id"),
        primary_key=True,
    )
    area_id = Column(
        TEXT,
        ForeignKey("gopacs.areas.id"),
        primary_key=True,
    )
