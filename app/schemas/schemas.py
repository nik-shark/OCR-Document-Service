from pydantic import BaseModel, ConfigDict
from datetime import date

class Documents(BaseModel):
    path: str
    date: date

    model_config = ConfigDict(
        from_attributes=True
    )


class DocumentsText(BaseModel):
    id_doc: int
    text: str

    model_config = ConfigDict(
        from_attributes=True
    )
