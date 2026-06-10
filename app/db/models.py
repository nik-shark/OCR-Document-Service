from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from core.engine import Base
from datetime import datetime


class DocumentsModel(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String(256))
    date = Column(
        DateTime,
        default=datetime.now
    )

    text = relationship(
        'DocumentsTextModel',
        back_populates='doc'
    )


class DocumentsTextModel(Base):
    __tablename__ = 'documents_text'

    id = Column(Integer, primary_key=True, index=True)
    id_doc = Column(Integer, ForeignKey('documents.id'))
    text = Column(Text)

    doc = relationship(
        'DocumentsModel',
        back_populates='text'
    )
