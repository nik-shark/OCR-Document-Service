from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class DocumentBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int


class UploadResponse(DocumentBase):
    path: str = Field(max_length=256)
    date: datetime


class DocumentsResponse(DocumentBase):
    doc_id: int
    text: str