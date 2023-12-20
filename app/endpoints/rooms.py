from fastapi import APIRouter, HTTPException
from typing import List
from ..crud.crud import MySQLCRUD
from ..schemas.schemas import RoomCreate, RoomUpdate, Room

router = APIRouter()
db = MySQLCRUD('host', 'user', 'password', 'database')

@router.post("/", response_model=Room)
async def create_room(room: RoomCreate):
    room_id = db.create('Rooms', list(room.dict().keys()), list(room.dict().values()))
    created_room = db.read('Rooms', conditions=f"WHERE roomid = {room_id}")[0]
    return {
        "roomid": created_room[0],
        "room_type": created_room[1],
        "floor": created_room[2],
        "view_type": created_room[3],
        "room_price": created_room[4],
        "room_desc": created_room[5],
        "is_available": created_room[6] 
    }

@router.get("/", response_model=List[Room])
async def read_rooms():
    rooms_data = db.read('Rooms')
    return [{"roomid": room[0], "room_type": room[1], "floor": room[2], "view_type": room[3], "room_price": room[4],"room_desc":room[5]} for room in rooms_data]

@router.get("/{room_id}", response_model=Room)
async def read_room(room_id: int):
    room = db.read('Rooms', conditions=f"WHERE roomid = {room_id}")
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return {
        "roomid": room[0][0],
        "room_type": room[0][1],
        "floor": room[0][2],
        "view_type": room[0][3],
        "room_price": room[0][4],
        "room_desc": room[0][5],
        "is_available": room[0][6]
    }

@router.put("/{room_id}", response_model=Room)
async def update_room(room_id: int, room: RoomUpdate):
    db.update('Rooms', room.dict(), f"roomid = {room_id}")
    updated_room = db.read('Rooms', conditions=f"WHERE roomid = {room_id}")[0]
    return {
        "roomid": updated_room[0],
        "room_type": updated_room[1],
        "floor": updated_room[2],
        "view_type": updated_room[3],
        "room_price": updated_room[4],
        "room_desc": updated_room[5],
        "is_available": updated_room[6]
    }

@router.delete("/{room_id}")
async def delete_room(room_id: int):
    db.delete('Rooms', f"roomid = {room_id}")
    return {"message": "Room deleted successfully."}

@router.get("/available/", response_model=List[Room])
async def read_available_rooms():
    available_rooms_data = db.read('Rooms', conditions="WHERE is_available = TRUE")
    available_rooms = []
    for room_data in available_rooms_data:
        # Transform room_data into the structure expected by the Room model
        room = Room(
            roomid=room_data[0],
            room_type=room_data[1],
            floor=room_data[2],
            view_type=room_data[3],
            room_price=room_data[4],
            room_desc=room_data[5]
        )
        available_rooms.append(room)
    return available_rooms