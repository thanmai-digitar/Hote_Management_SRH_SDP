from fastapi import APIRouter, HTTPException
from typing import List
from ..crud.crud import MySQLCRUD
from ..schemas.schemas import RoomCreate, RoomUpdate, Room

router = APIRouter()
db = MySQLCRUD('host', 'user', 'password', 'database')

@router.post("/", response_model=Room)
def create_room(room: RoomCreate):
    room_id = db.create('Rooms', room.dict().keys(), room.dict().values())
    return db.read('Rooms', conditions=f"WHERE RoomID = {room_id}")[0]

@router.get("/", response_model=List[Room])
def read_rooms():
    return db.read('Rooms')

@router.get("/{room_id}", response_model=Room)
def read_room(room_id: int):
    room = db.read('Rooms', conditions=f"WHERE RoomID = {room_id}")
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room[0]

@router.put("/{room_id}", response_model=Room)
def update_room(room_id: int, room: RoomUpdate):
    db.update('Rooms', room.dict(), f"RoomID = {room_id}")
    return db.read('Rooms', conditions=f"WHERE RoomID = {room_id}")[0]

@router.delete("/{room_id}")
def delete_room(room_id: int):
    db.delete('Rooms', f"RoomID = {room_id}")
    return {"message": "Room deleted successfully."}
