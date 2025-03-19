from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP, TEXT, DOUBLE_PRECISION
from sqlalchemy.orm import relationship, Mapped
from .base import Base, HumanIDMixin


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
    areas: Mapped[list["Area"]] = relationship(
        back_populates="announcements",
        cascade="all, delete",
        secondary="gopacs.announcement_areas",
    )
    problem_profile_items: Mapped[list["ProblemProfileItem"]] = relationship(
        back_populates="announcement",
        cascade="all, delete",
    )


class Area(Base):
    __tablename__ = "areas"
    __table_args__ = {"schema": "gopacs"}

    id = Column(TEXT, primary_key=True)

    # Relationships
    announcements: Mapped[list["Announcement"]] = relationship(
        back_populates="areas",
        cascade="all, delete",
        secondary="gopacs.announcement_areas    ",
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


class ProblemProfileItem(Base, HumanIDMixin):
    __tablename__ = "problem_profile_items"
    __table_args__ = {"schema": "gopacs"}

    id = Column(TEXT, primary_key=True)
    start_time = Column(TIMESTAMP(timezone=True), nullable=False)
    end_time = Column(TIMESTAMP(timezone=True), nullable=False)
    required = Column(DOUBLE_PRECISION, nullable=False)
    remaining = Column(DOUBLE_PRECISION, nullable=False)

    announcement_id = Column(
        UUID(as_uuid=True),
        ForeignKey("gopacs.announcements.id"),
        nullable=False,
    )

    # Relationships
    announcement: Mapped["Announcement"] = relationship(
        back_populates="problem_profile_items",
    )
