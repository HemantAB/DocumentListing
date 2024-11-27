# app/api/endpoints/documents.py
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, asc
from ...core.logging import setup_logging
from ...models.document import Document
from ...schemas.document import DocumentCreate, Document as DocumentSchema, DocumentResponse
from ..deps import get_db
from datetime import datetime, timezone

router = APIRouter()
logger = setup_logging()

@router.get("", response_model=DocumentResponse)
async def list_documents(
    db: Session = Depends(get_db),
    search: Optional[str] = None,
    sort_by: Optional[str] = Query(None, regex="^(name|created_at)$"),
    sort_order: Optional[str] = Query("asc", regex="^(asc|desc)$"),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100)
):
    try:
        query = db.query(Document)
        
        # Apply search filter
        if search:
            query = query.filter(Document.name.like(f"%{search}%"))
        
        # Get total count
        total = query.count()
        
        # Apply sorting
        if sort_by:
            order_column = getattr(Document, sort_by)
            if sort_order == "desc":
                order_column = desc(order_column)
            else:
                order_column = asc(order_column)
            query = query.order_by(order_column)
        
        # Apply pagination
        query = query.offset((page - 1) * per_page).limit(per_page)
        
        # Execute query
        documents = query.all()
        
        # Calculate size for each document
        result_documents = []
        for doc in documents:
            doc_dict = {
                "id": doc.id,
                "name": doc.name,
                "content": doc.content,
                "created_at": doc.created_at.replace(tzinfo=timezone.utc),
                "updated_at": doc.updated_at.replace(tzinfo=timezone.utc),
                "size": len(doc.content.encode('utf-8'))
            }
            result_documents.append(DocumentSchema(**doc_dict))
        
        return DocumentResponse(documents=result_documents, total=total)
        
    except Exception as e:
        logger.error(f"Error listing documents: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving documents")

@router.get("/{document_id}", response_model=DocumentSchema)
async def get_document(document_id: int, db: Session = Depends(get_db)):
    try:
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
            
        # Prepare document with UTC timezone
        document_dict = {
            "id": document.id,
            "name": document.name,
            "content": document.content,
            "created_at": document.created_at.replace(tzinfo=timezone.utc),
            "updated_at": document.updated_at.replace(tzinfo=timezone.utc),
            "size": len(document.content.encode('utf-8'))
        }
        
        return DocumentSchema(**document_dict)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving document {document_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving document")

@router.post("", response_model=DocumentSchema, status_code=201)
async def create_document(document: DocumentCreate, db: Session = Depends(get_db)):
    try:
        now = datetime.now(timezone.utc)
        db_document = Document(
            name=document.name,
            content=document.content,
            created_at=now,
            updated_at=now
        )
        db.add(db_document)
        db.commit()
        db.refresh(db_document)
        
        document_dict = {
            "id": db_document.id,
            "name": db_document.name,
            "content": db_document.content,
            "created_at": db_document.created_at.replace(tzinfo=timezone.utc),
            "updated_at": db_document.updated_at.replace(tzinfo=timezone.utc),
            "size": len(db_document.content.encode('utf-8'))
        }
        
        return DocumentSchema(**document_dict)
        
    except Exception as e:
        logger.error(f"Error creating document: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error creating document")

@router.delete("/{document_id}")
async def delete_document(document_id: int, db: Session = Depends(get_db)):
    try:
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
            
        db.delete(document)
        db.commit()
        
        return {"message": "Document deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting document {document_id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error deleting document")
