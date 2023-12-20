from fastapi import APIRouter, HTTPException
from typing import List
from ..crud.crud import MySQLCRUD
from ..schemas.schemas import ServiceCreate, ServiceUpdate, Service

router = APIRouter()
db = MySQLCRUD('host', 'user', 'password', 'database')

@router.post("/", response_model=Service)
async def create_service(service: ServiceCreate):
    service_id = db.create('Services', list(service.dict().keys()), list(service.dict().values()))
    created_service = db.read('Services', conditions=f"WHERE serviceid = {service_id}")[0]
    return {
        "serviceid": created_service[0],
        "description": created_service[1],
        "price": created_service[2],
        "service_name": created_service[3]
    }


@router.get("/", response_model=List[Service])
async def read_services():
    services_data = db.read('Services')
    return [{"serviceid": service[0], "description": service[1], "price": service[2],"service_name":service[3]} for service in services_data]


@router.get("/{service_id}", response_model=Service)
async def read_service(service_id: int):
    service = db.read('Services', conditions=f"WHERE serviceid = {service_id}")
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return {
        "serviceid": service[0][0],
        "description": service[0][1],
        "price": service[0][2],
        "service_name": service[0][3]
    }


@router.put("/{service_id}", response_model=Service)
async def update_service(service_id: int, service: ServiceUpdate):
    db.update('Services', service.dict(), f"serviceid = {service_id}")
    updated_service = db.read('Services', conditions=f"WHERE serviceid = {service_id}")[0]
    return {
        "serviceid": updated_service[0],
        "description": updated_service[1],
        "price": updated_service[2],
        "service_name": updated_service[3]
    }

@router.delete("/{service_id}")
async def delete_service(service_id: int):
    db.delete('Services', f"serviceid = {service_id}")
    return {"message": "Service deleted successfully."}
