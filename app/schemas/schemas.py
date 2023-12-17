from pydantic import BaseModel
from datetime import date
from typing import Optional

# Schemas for Rooms
class RoomBase(BaseModel):
    Room_Type: str
    Floor: int
    View_Type: str
    Price: float

class RoomCreate(RoomBase):
    pass

class RoomUpdate(RoomBase):
    pass

class Room(RoomBase):
    RoomID: int

# Schemas for Customers
class CustomerBase(BaseModel):
    Name: str
    Email: str
    Phone: str

class CustomerCreate(CustomerBase):
    Password: str  # Note: In a real application, ensure this is hashed!

class CustomerUpdate(CustomerBase):
    pass

class Customer(CustomerBase):
    CustomerID: int

# Schemas for Bookings
class BookingBase(BaseModel):
    CustomerID: int
    ServiceID: Optional[int] = None  # Optional because not all bookings may include a service
    RoomID: int
    Checkin_date: date
    Checkout_date: date
    Total_Amount: float

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BookingBase):
    pass

class Booking(BookingBase):
    BookingID: int

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
