from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import ContactMessage
from app.schemas import ContactMessageCreate, ContactMessageResponse, MessageResponse

router = APIRouter(prefix="/contact", tags=["Contact"])


@router.post(
    "/",
    response_model=ContactMessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Send Contact Message",
    description="Submits a contact form message from a visitor. Returns the saved message with its ID.",
)
def send_message(payload: ContactMessageCreate, db: Session = Depends(get_db)):
    message = ContactMessage(**payload.model_dump())
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


@router.get(
    "/messages",
    response_model=List[ContactMessageResponse],
    summary="Get All Contact Messages",
    description="Returns all contact messages. Optionally filter by read status.",
)
def get_all_messages(
    is_read: Optional[bool] = Query(None, description="Filter by read/unread status"),
    db: Session = Depends(get_db),
):
    query = db.query(ContactMessage)
    if is_read is not None:
        query = query.filter(ContactMessage.is_read == is_read)
    return query.order_by(ContactMessage.created_at.desc()).all()


@router.get(
    "/messages/{message_id}",
    response_model=ContactMessageResponse,
    summary="Get Single Contact Message",
    description="Returns a single contact message by its ID.",
)
def get_message(message_id: int, db: Session = Depends(get_db)):
    message = db.query(ContactMessage).filter(ContactMessage.id == message_id).first()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Message with ID {message_id} not found.",
        )
    return message


@router.patch(
    "/messages/{message_id}/read",
    response_model=ContactMessageResponse,
    summary="Mark Message as Read",
    description="Marks a contact message as read by its ID.",
)
def mark_message_read(message_id: int, db: Session = Depends(get_db)):
    message = db.query(ContactMessage).filter(ContactMessage.id == message_id).first()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Message with ID {message_id} not found.",
        )
    message.is_read = True
    db.commit()
    db.refresh(message)
    return message


@router.delete(
    "/messages/{message_id}",
    response_model=MessageResponse,
    summary="Delete Contact Message",
    description="Permanently deletes a contact message by its ID.",
)
def delete_message(message_id: int, db: Session = Depends(get_db)):
    message = db.query(ContactMessage).filter(ContactMessage.id == message_id).first()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Message with ID {message_id} not found.",
        )
    db.delete(message)
    db.commit()
    return MessageResponse(message=f"Message {message_id} deleted successfully.")
