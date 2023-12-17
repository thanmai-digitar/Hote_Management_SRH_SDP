from fastapi import APIRouter, HTTPException
from typing import List
from ..crud.crud import MySQLCRUD
from ..schemas.schemas import CustomerCreate, CustomerUpdate, Customer

router = APIRouter()
db = MySQLCRUD('host', 'user', 'password', 'database')

# @router.post("/", response_model=Customer)
# def create_customer(customer: CustomerCreate):
#     customer_id = db.create('Customers', list(customer.dict().keys()), list(customer.dict().values()))
#     return db.read('Customers', conditions=f"WHERE CustomerID = {customer_id}")[0]

@router.post("/", response_model=Customer)
def create_customer(customer: CustomerCreate):
    customer_id = db.create('Customers', list(customer.dict().keys()), list(customer.dict().values()))
    customer_data = db.read('Customers', conditions=f"WHERE CustomerID = {customer_id}")[0]

    # Convert customer_data (tuple) to a dictionary
    customer_dict = {
        "CustomerID": customer_data[0],
        "Name": customer_data[1],
        "Email": customer_data[2],
        "Phone": customer_data[3],
        "Password": customer_data[4]  # Note: Returning passwords is a security risk!
    }

    return customer_dict


@router.get("/", response_model=List[Customer])
def read_customers():
    return db.read('Customers')

@router.get("/{customer_id}", response_model=Customer)
def read_customer(customer_id: int):
    customer = db.read('Customers', conditions=f"WHERE CustomerID = {customer_id}")
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer[0]

@router.put("/{customer_id}", response_model=Customer)
def update_customer(customer_id: int, customer: CustomerUpdate):
    db.update('Customers', customer.dict(), f"CustomerID = {customer_id}")
    return db.read('Customers', conditions=f"WHERE CustomerID = {customer_id}")[0]

@router.delete("/{customer_id}")
def delete_customer(customer_id: int):
    db.delete('Customers', f"CustomerID = {customer_id}")
    return {"message": "Customer deleted successfully."}
