from decimal import Decimal
from pydantic import BaseModel
from datetime import date
from typing import Optional

class RoomBase(BaseModel):
    room_type: str
    floor: int
    view_type: str
    room_price: float
    room_desc: str
    is_available: bool = True  # New field, defaulting to True

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
    description: str
    price: float
    service_name:str

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(ServiceBase):
    pass

class Service(ServiceBase):
    serviceid: int

#schemas for employees
class EmployeeBase(BaseModel):
    emp_name: str
    serviceid: int  # Assuming this is a foreign key to a Service
    description: str

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    employeeid: int

#schemas for transactions
class TransactionBase(BaseModel):
    bookingid: int  # Assuming this is a foreign key to a Booking
    customerid: int  # Assuming this is a foreign key to a Customer
    total_amount: float
    payment_type: str

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(TransactionBase):
    pass

class Transaction(TransactionBase):
    transactionid: int
