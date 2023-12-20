from fastapi import APIRouter, HTTPException,Form
from typing import List
from ..crud.crud import MySQLCRUD
from ..schemas.schemas import CustomerBase, CustomerCreate, CustomerUpdate, Customer
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


router = APIRouter()
db = MySQLCRUD('host', 'user', 'password', 'database')

# @router.post("/", response_model=Customer)
# def create_customer(customer: CustomerCreate):
#     customer_id = db.create('Customers', list(customer.dict().keys()), list(customer.dict().values()))
#     return db.read('Customers', conditions=f"WHERE CustomerID = {customer_id}")[0]

@router.post("/", response_model=CustomerBase)
async def create_customer(
    first_name: str = Form(...),
    last_name: str = Form(...),
    phone: str = Form(...), 
    email: str = Form(...),  
    password: str = Form(...)
):
    hashed_password = pwd_context.hash(password)
    customer_data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone": phone,
        "password": hashed_password  
    }
    customer_id = db.create('customers', list(customer_data.keys()), list(customer_data.values()))
    customer = db.read('customers', conditions=f"WHERE customerid = {customer_id}")[0]

    
    customer_dict = {
       
        "customerid": customer[4],
        "first_name": customer[0],
        "last_name": customer[1],
        "email": str(customer[2]), 
        "phone": str(customer[3]),  
        "password": customer[5]  
    }

    return customer_dict



@router.get("/", response_model=List[Customer])
async def read_customers():
    customers_data = db.read('Customers')
    customers_list = []

    for customer in customers_data:
        customer_dict = {
            "customerid": customer[4],
            "first_name": customer[0],
            "last_name": customer[1],
            "email": str(customer[2]),
            "phone": str(customer[3]),
          
        }
        customers_list.append(customer_dict)

    return customers_list

@router.get("/{customer_id}", response_model=CustomerBase)
async def read_customer(customer_id: int):
    customer = db.read('Customers', conditions=f"WHERE CustomerID = {customer_id}")
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    customer_dict = {
    "first_name": customer[0][0],
    "last_name": customer[0][1],
    "email": str(customer[0][2]),
    "phone": str(customer[0][3]),
    "customerid": customer[0][4]

    
}
    return customer_dict

@router.put("/{customer_id}", response_model=Customer)
async def update_customer(
    customer_id: int,
    first_name: str = Form(...),
    last_name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    customer_data = {
        "first_name": first_name,
        "last_name": last_name,
        "phone": phone,
        "email": email,
        "password": password 
    }

   
    db.update('Customers', customer_data, f"customerid = {customer_id}")

   
    updated_customer = db.read('Customers', conditions=f"WHERE customerid = {customer_id}")[0]

    
    updated_customer_dict = {
        "customerid": updated_customer[4],
        "first_name": updated_customer[0],
        "last_name": updated_customer[1],
        "email": str(updated_customer[2]),
        "phone": str(updated_customer[3]),
       
    }

    return updated_customer_dict

@router.delete("/{customer_id}")
async def delete_customer(customer_id: int):
    db.delete('Customers', f"CustomerID = {customer_id}")
    return {"message": "Customer deleted successfully."}
