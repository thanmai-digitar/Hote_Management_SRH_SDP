from fastapi import APIRouter, HTTPException
from typing import List
from ..crud.crud import MySQLCRUD
from ..schemas.schemas import ServiceCreate, ServiceUpdate, Service

router = APIRouter()
db = MySQLCRUD('host', 'user', 'password', 'database')

@router.post("/", response_model=Service)
def create_service(service: ServiceCreate):
    service_id = db.create('Services', service.dict().keys(), service.dict().values())
    return db.read('Services', conditions=f"WHERE ServiceID = {service_id}")[0]

@router.get("/", response_model=List[Service])
def read_services():
    return db.read('Services')

@router.get("/{service_id}", response_model=Service)
def read_service(service_id: int):
    service = db.read('Services', conditions=f"WHERE ServiceID = {service_id}")
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service[0]

@router.put("/{service_id}", response_model=Service)
def update_service(service_id: int, service: ServiceUpdate):
    db.update('Services', service.dict(), f"ServiceID = {service_id}")
    return db.read('Services', conditions=f"WHERE ServiceID = {service_id}")[0]

@router.delete("/{service_id}")
def delete_service(service_id: int):
    db.delete('Services', f"ServiceID = {service_id}")
    return {"message": "Service deleted successfully."}
