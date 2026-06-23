from sqlalchemy import String, ForeignKey, DateTime, func, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
import datetime

from db.engine import Base


class DocumentsModel(Base):
    __tablename__ = 'documents'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    path: Mapped[str] = mapped_column(String(256))
    date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    text: Mapped['DocumentsTextModel'] = relationship(
        back_populates='doc',
        uselist=False,
        cascade='all, delete-orphan'
    )


class DocumentsTextModel(Base):
    __tablename__ = 'documents_text'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    doc_id: Mapped[int] = mapped_column(
        ForeignKey('documents.id', ondelete='CASCADE'),
        nullable=False
    )

    text: Mapped[str] = mapped_column(Text, nullable=False)

    doc: Mapped['DocumentsModel'] = relationship(back_populates='text')