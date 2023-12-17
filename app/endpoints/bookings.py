from fastapi import APIRouter, HTTPException
from typing import List
from ..crud.crud import MySQLCRUD
from ..schemas.schemas import BookingCreate, BookingUpdate, Booking

router = APIRouter()
db = MySQLCRUD('host', 'user', 'password', 'database')

@router.post("/", response_model=Booking)
def create_booking(booking: BookingCreate):
    booking_id = db.create('Bookings', booking.dict().keys(), booking.dict().values())
    return db.read('Bookings', conditions=f"WHERE BookingID = {booking_id}")[0]

@router.get("/", response_model=List[Booking])
def read_bookings():
    return db.read('Bookings')

@router.get("/{booking_id}", response_model=Booking)
def read_booking(booking_id: int):
    booking = db.read('Bookings', conditions=f"WHERE BookingID = {booking_id}")
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking[0]

@router.put("/{booking_id}", response_model=Booking)
def update_booking(booking_id: int, booking: BookingUpdate):
    db.update('Bookings', booking.dict(), f"BookingID = {booking_id}")
    return db.read('Bookings', conditions=f"WHERE BookingID = {booking_id}")[0]

@router.delete("/{booking_id}")
def delete_booking(booking_id: int):
    db.delete('Bookings', f"BookingID = {booking_id}")
    return {"message": "Booking deleted successfully."}
