from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from app.endpoints import admin, auth, employees, transactions
from .endpoints import customers, rooms, bookings, services

app = FastAPI()

async def add_no_cache_headers(request, call_next):
    response = await call_next(request)
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

origins = [
    "http://localhost:8000",  # Backend server
    "http://127.0.0.1:5500",  # Frontend server
    "http://localhost:3000",
    "http://localhost:8080", 
    "http://127.0.0.1:8080", # In case you're using something like React on default port
    # Add other origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
app.add_middleware(BaseHTTPMiddleware, dispatch=add_no_cache_headers)

# Include routers
app.include_router(customers.router, prefix="/customers", tags=["customers"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(rooms.router, prefix="/rooms", tags=["rooms"])
app.include_router(bookings.router, prefix="/bookings", tags=["bookings"])
app.include_router(services.router, prefix="/services", tags=["services"])
app.include_router(employees.router, prefix="/employees", tags=["employees"])
app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])

@app.get("/")
async def root():
    return {"message": "Hotel Management API is up and running!"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
