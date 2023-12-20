from ..crud.crud import MySQLCRUD
from fastapi import APIRouter, HTTPException


router = APIRouter()
db = MySQLCRUD('host', 'user', 'password', 'database')




@router.post("/create")
async def create_admin_endpoint(email: str, password: str):
    admin_id = db.create_admin(email, password)
    if admin_id:
        return {"message": "Admin created successfully", "admin_id": admin_id}
    else:
        raise HTTPException(status_code=400, detail="Error creating admin")