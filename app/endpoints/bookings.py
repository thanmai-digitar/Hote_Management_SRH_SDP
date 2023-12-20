from fastapi import APIRouter, HTTPException
from typing import List, Optional
from ..crud.crud import MySQLCRUD
from ..schemas.schemas import BookingCreate, BookingUpdate, Booking
from datetime import date, datetime



router = APIRouter()
db = MySQLCRUD('host', 'user', 'password', 'database')


def get_service_ids():
    services = db.read('Services')
    return [service[0] for service in services]  # Assuming service ID is the first column

def get_room_ids():
    rooms = db.read('Rooms')
    return [room[0] for room in rooms]  # Assuming room ID is the first column


def calculate_duration(checkin_date: date, checkout_date: date) -> int:
    duration = (checkout_date - checkin_date).days
    return duration if duration > 0 else 0


def calculate_total_amount(room_id: int, service_id: Optional[int], checkin_date: date, checkout_date: date) -> float:
    # Calculate duration of stay
    duration = calculate_duration(checkin_date, checkout_date)

    # Fetch room price per day
    room_price_per_day = db.read('Rooms', conditions=f"WHERE roomid = {room_id}")[0][4]  # Assuming price is the 5th column

    # Initialize total amount with room cost
    total_amount = room_price_per_day * duration

    # Add service price if a service is selected
    if service_id:
        service_price = db.read('Services', conditions=f"WHERE serviceid = {service_id}")[0][2]  # Assuming price is the 3rd column
        total_amount += service_price

    return total_amount


@router.post("/", response_model=Booking)
async def create_booking(booking: BookingCreate):
    # Fetch IDs for validation
    service_ids = get_service_ids()
    room_ids = get_room_ids()

    if booking.roomid not in room_ids:
        raise HTTPException(status_code=400, detail="Invalid RoomID")

    # Check if service ID is provided and valid
    if booking.serviceid is not None and booking.serviceid not in service_ids:
        raise HTTPException(status_code=400, detail="Invalid ServiceID")

    # Calculate total amount
    total_amount = calculate_total_amount(booking.roomid, booking.serviceid, booking.checkin_date, booking.checkout_date)

    # Create booking with calculated total amount
    booking_data = booking.dict()
    booking_data['total_amount'] = total_amount
    booking_id = db.create('Bookings', list(booking_data.keys()), list(booking_data.values()))
    db.update('Rooms', {'is_available': False}, f"roomid = {booking.roomid}")
    created_booking = db.read('Bookings', conditions=f"WHERE bookingid = {booking_id}")[0]
    return {
        "bookingid": created_booking[0],
        "customerid": created_booking[1],
        "serviceid": created_booking[2],
        "roomid": created_booking[3],
        "checkin_date": created_booking[4],
        "checkout_date": created_booking[5],
        "total_amount": created_booking[6]
    }

@router.get("/", response_model=List[Booking])
async def read_bookings():
    bookings_data = db.read('Bookings')
    return [{
        "bookingid": booking[0],
        "customerid": booking[1],
        "serviceid": booking[2],
        "roomid": booking[3],
        "checkin_date": booking[4],
        "checkout_date": booking[5],
        "total_amount": booking[6]
    } for booking in bookings_data]


@router.get("/{booking_id}/", response_model=Booking)
async def read_booking(booking_id: int):
    print(f"Fetching booking with ID: {booking_id}")  # Debugging print statement
    booking = db.read('Bookings', conditions=f"WHERE bookingid = {booking_id}")

    if not booking:
        print("No booking found with this ID.")  # Debugging print statement
        raise HTTPException(status_code=404, detail="Booking not found")

    booking_details = booking[0]
    print(f"Booking details: {booking_details}")  # Debugging print statement

    return {
        "bookingid": booking_details[0],
        "customerid": booking_details[1],
        "serviceid": booking_details[2],
        "roomid": booking_details[3],
        "checkin_date": booking_details[4],
        "checkout_date": booking_details[5],
        "total_amount": booking_details[6]
    }


@router.get('/{customerid}', response_model=List[Booking])
async def get_user_bookings(customerid: int):
    bookings_data = db.read('Bookings', conditions=f"WHERE customerid = {customerid}")
    return [{
        "bookingid": booking[0],
        "customerid": booking[1],
        "serviceid": booking[2],
        "roomid": booking[3],
        "checkin_date": booking[4],
        "checkout_date": booking[5],
        "total_amount": booking[6]
    } for booking in bookings_data]



@router.put("/{booking_id}", response_model=Booking)
async def update_booking(booking_id: int, booking: BookingUpdate):
    total_amount = calculate_total_amount(booking.roomid, booking.serviceid, booking.checkin_date, booking.checkout_date)
    booking_data = booking.dict()
    booking_data['total_amount'] = total_amount
    db.update('Bookings', booking.dict(), f"bookingid = {booking_id}")
    updated_booking = db.read('Bookings', conditions=f"WHERE bookingid = {booking_id}")[0]
    return {
        "bookingid": updated_booking[0],
        "customerid": updated_booking[1],
        "serviceid": updated_booking[2],
        "roomid": updated_booking[3],
        "checkin_date": updated_booking[4],
        "checkout_date": updated_booking[5],
        "total_amount": updated_booking[6]
    }

@router.delete("/{booking_id}/{roomid}")
async def delete_booking(booking_id: int, roomid: int):
    db.update('Rooms', {'is_available': True}, f"roomid = {roomid}")
    db.delete('Bookings', f"bookingid = {booking_id}")
    return {"message": "Booking deleted successfully."}


