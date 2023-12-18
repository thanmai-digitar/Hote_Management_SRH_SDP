from decimal import Decimal
from pydantic import BaseModel
from datetime import date
from typing import Optional

class RoomBase(BaseModel):
    room_type: str
    floor: int
    view_type: str
    room_price: float

class RoomCreate(RoomBase):
    pass

class RoomUpdate(RoomBase):
    pass

class Room(RoomBase):
    roomid: int
# Schemas for Customers
class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str  # Assuming phone is stored as a string in the database
    customerid:int

class CustomerCreate(CustomerBase):
    Password: str  # Added Password field for creating a new customer

class CustomerUpdate(CustomerBase):
    pass

class Customer(CustomerBase):
    customerid: int

# Schemas for Bookings
class BookingBase(BaseModel):
    customerid: int
    serviceid: Optional[int] = None  # Optional because not all bookings may include a service
    roomid: int
    checkin_date: date
    checkout_date: date
    total_amount: float

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BookingBase):
    pass

class Booking(BookingBase):
    bookingid: int

# Schemas for Services
class ServiceBase(BaseModel):
    Description: str
    Price: float

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(ServiceBase):
    pass

class Service(ServiceBase):
    ServiceID: int
