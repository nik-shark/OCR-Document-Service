from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from core.engine import Base


class DocumentsModel(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String)
    date = Column(DateTime)


class DocumentsTextModel(Base):
    __tablename__ = 'documents_text'

    id = Column(Integer, primary_key=True, index=True)
    id_doc = Column(Integer, ForeignKey('documents.id'))
    text = Column(String)

    doc = relationship('DocumentsModel')
