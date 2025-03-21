"""Database models for RAG."""

import os
from datetime import datetime
from datetime import timezone as tz
from typing import List, Optional

import os
from pgvector.sqlalchemy import Vector  # type: ignore
from sqlalchemy import (BigInteger, Column, DateTime, ForeignKey, Integer,
                        String, Text, UniqueConstraint)

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class DbBase(DeclarativeBase):
    """Base class for all models."""

    pass


def utc_now() -> datetime:
    """Get current UTC datetime."""
    return datetime.now(tz.utc)


class ProjectDB(DbBase):
    """Project model."""

    __tablename__ = "projects"
    __table_args__ = (UniqueConstraint("name", name="uix_project_name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now
    )

    files: Mapped[List["FileDB"]] = relationship(
        "FileDB", back_populates="project", cascade="all, delete-orphan"
    )


class FileDB(DbBase):
    """File model."""

    __tablename__ = "files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.id", ondelete="CASCADE")
    )
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    crc: Mapped[str] = mapped_column(String(128), nullable=False)
    file_size: Mapped[int] = mapped_column(BigInteger, nullable=False)
    last_updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now
    )
    last_ingested: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now
    )

    project: Mapped["ProjectDB"] = relationship("ProjectDB", back_populates="files")
    chunks: Mapped[List["ChunkDB"]] = relationship(
        "ChunkDB", back_populates="file", cascade="all, delete-orphan"
    )


class ChunkDB(DbBase):
    """Chunk model with vector embedding."""

    __tablename__ = "chunks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    file_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("files.id", ondelete="CASCADE")
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[List[float]] = mapped_column(Vector(None))  # Dimension will be set during initialization

    @classmethod
    def set_embedding_dimension(cls, dimension: int):
        """Set the embedding dimension for the chunks table.
        
        Args:
            dimension: The dimension size for the vector column
        """
        if dimension <= 0:
            raise ValueError("Embedding dimension must be positive")
        cls.embedding.type.dimension = dimension
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    chunk_metadata: Mapped[dict] = mapped_column(JSONB, default={})
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now
    )

    file: Mapped["FileDB"] = relationship("FileDB", back_populates="chunks")
