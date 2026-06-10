from pydantic import BaseModel, ConfigDict
from datetime import datetime

class DocumentsResponse(BaseModel):
    id: int
    path: str
    date: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class DocumentsTextResponse(BaseModel):
    id_doc: int
    text: str

    model_config = ConfigDict(
        from_attributes=True
    )

class UploadResponse(BaseModel):
    status: str
    document_id: int
    path: str

    model_config = ConfigDict(
        from_attributes=True
    )