from fastapi import APIRouter, HTTPException
from typing import List
from ..crud.crud import MySQLCRUD
from ..schemas.schemas import RoomCreate, RoomUpdate, Room

router = APIRouter()
db = MySQLCRUD('host', 'user', 'password', 'database')

@router.post("/", response_model=Room)
def create_room(room: RoomCreate):
    room_id = db.create('Rooms', list(room.dict().keys()), list(room.dict().values()))
    created_room = db.read('Rooms', conditions=f"WHERE roomid = {room_id}")[0]
    return {
        "roomid": created_room[0],
        "room_type": created_room[1],
        "floor": created_room[2],
        "view_type": created_room[3],
        "room_price": created_room[4]
    }

@router.get("/", response_model=List[Room])
def read_rooms():
    rooms_data = db.read('Rooms')
    return [{"roomid": room[0], "room_type": room[1], "floor": room[2], "view_type": room[3], "room_price": room[4]} for room in rooms_data]

@router.get("/{room_id}", response_model=Room)
def read_room(room_id: int):
    room = db.read('Rooms', conditions=f"WHERE roomid = {room_id}")
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return {
        "roomid": room[0][0],
        "room_type": room[0][1],
        "floor": room[0][2],
        "view_type": room[0][3],
        "room_price": room[0][4]
    }

@router.put("/{room_id}", response_model=Room)
def update_room(room_id: int, room: RoomUpdate):
    db.update('Rooms', room.dict(), f"roomid = {room_id}")
    updated_room = db.read('Rooms', conditions=f"WHERE roomid = {room_id}")[0]
    return {
        "roomid": updated_room[0],
        "room_type": updated_room[1],
        "floor": updated_room[2],
        "view_type": updated_room[3],
        "room_price": updated_room[4]
    }

@router.delete("/{room_id}")
def delete_room(room_id: int):
    db.delete('Rooms', f"roomid = {room_id}")
    return {"message": "Room deleted successfully."}