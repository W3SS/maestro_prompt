"""
SQLAlchemy 2.0 Database Models for Maestro AI.

Defines the core entities for persistence:
- User: System users with authentication
- Album: Generated albums with metadata
- Track: Individual tracks belonging to albums
- Batch: Processing batches for Suno generation
- BatchItem: Individual items within a batch
"""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Integer, Text, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import enum


class Base(DeclarativeBase):
    """Base class for all models."""
    pass


class BatchStatus(str, enum.Enum):
    """Batch processing status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ItemStatus(str, enum.Enum):
    """Individual item status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class User(Base):
    """User entity for authentication."""
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    albums: Mapped[List["Album"]] = relationship(back_populates="owner", cascade="all, delete-orphan")
    batches: Mapped[List["Batch"]] = relationship(back_populates="owner", cascade="all, delete-orphan")


class Album(Base):
    """Album entity representing a generated album."""
    __tablename__ = "albums"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    archetype: Mapped[str] = mapped_column(String(100), nullable=False)
    genres: Mapped[str] = mapped_column(Text, nullable=False)  # JSON serialized list
    theme: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Foreign keys
    owner_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    
    # Relationships
    owner: Mapped[Optional["User"]] = relationship(back_populates="albums")
    tracks: Mapped[List["Track"]] = relationship(back_populates="album", cascade="all, delete-orphan")


class Track(Base):
    """Track entity representing an individual track in an album."""
    __tablename__ = "tracks"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    track_number: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    lyrics: Mapped[str] = mapped_column(Text, nullable=False)
    style_tags: Mapped[str] = mapped_column(Text, nullable=False)  # JSON serialized list
    duration_estimate: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    
    # Foreign keys
    album_id: Mapped[int] = mapped_column(ForeignKey("albums.id"), nullable=False)
    
    # Relationships
    album: Mapped["Album"] = relationship(back_populates="tracks")


class Batch(Base):
    """Batch entity for Suno generation processing."""
    __tablename__ = "batches"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)  # UUID
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[BatchStatus] = mapped_column(
        SQLEnum(BatchStatus), 
        default=BatchStatus.PENDING,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Foreign keys
    owner_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    
    # Relationships
    owner: Mapped[Optional["User"]] = relationship(back_populates="batches")
    items: Mapped[List["BatchItem"]] = relationship(back_populates="batch", cascade="all, delete-orphan")


class BatchItem(Base):
    """Individual item within a batch."""
    __tablename__ = "batch_items"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    style_tags: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[ItemStatus] = mapped_column(
        SQLEnum(ItemStatus),
        default=ItemStatus.PENDING,
        nullable=False
    )
    suno_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # Suno's track ID
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Foreign keys
    batch_id: Mapped[str] = mapped_column(ForeignKey("batches.id"), nullable=False)
    
    # Relationships
    batch: Mapped["Batch"] = relationship(back_populates="items")
