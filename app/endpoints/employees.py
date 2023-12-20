# Assuming you have these imports
from fastapi import APIRouter, HTTPException
from typing import List
from ..crud.crud import MySQLCRUD
from ..schemas.schemas import EmployeeCreate, EmployeeUpdate, Employee

router = APIRouter()
db = MySQLCRUD('host', 'user', 'password', 'database')

@router.post("/", response_model=Employee)
async def create_employee(employee: EmployeeCreate):
    employee_id = db.create('Employees', list(employee.dict().keys()), list(employee.dict().values()))
    created_employee = db.read('Employees', conditions=f"WHERE employeeid = {employee_id}")[0]
    return {
        "employeeid": created_employee[0],
        "emp_name": created_employee[1],
        "serviceid": created_employee[2],
        "description": created_employee[3]
    }

@router.get("/", response_model=List[Employee])
async def read_employees():
    employees_data = db.read('Employees')
    return [{"employeeid": emp[0], "emp_name": emp[1], "serviceid": emp[2], "description": emp[3]} for emp in employees_data]

@router.get("/{employee_id}", response_model=Employee)
async def read_employee(employee_id: int):
    employee = db.read('Employees', conditions=f"WHERE employeeid = {employee_id}")
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {
        "employeeid": employee[0][0],
        "emp_name": employee[0][1],
        "serviceid": employee[0][2],
        "description": employee[0][3]
    }

@router.put("/{employee_id}", response_model=Employee)
async def update_employee(employee_id: int, employee: EmployeeUpdate):
    db.update('Employees', employee.dict(), f"employeeid = {employee_id}")
    updated_employee = db.read('Employees', conditions=f"WHERE employeeid = {employee_id}")[0]
    return {
        "employeeid": updated_employee[0],
        "emp_name": updated_employee[1],
        "serviceid": updated_employee[2],
        "description": updated_employee[3]
    }

@router.delete("/{employee_id}")
async def delete_employee(employee_id: int):
    db.delete('Employees', f"employeeid = {employee_id}")
    return {"message": "Employee deleted successfully."}
