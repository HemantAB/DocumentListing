# app/schemas/document.py
from pydantic import BaseModel, constr
from datetime import datetime
from typing import Optional

class DocumentBase(BaseModel):
    name: constr(min_length=1, max_length=255) # type: ignore
    content: str

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    size: int

    class Config:
        from_attributes = True

class DocumentResponse(BaseModel):
    documents: list[Document]
    total: int