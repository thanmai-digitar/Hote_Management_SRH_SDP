from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from .endpoints import customers, rooms, bookings, services

app = FastAPI()

origins = [
    "http://localhost:8000",  # Backend server
    "http://127.0.0.1:5500",  # Frontend server
    "http://localhost:3000",  # In case you're using something like React on default port
    # Add other origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(customers.router, prefix="/customers", tags=["customers"])
app.include_router(rooms.router, prefix="/rooms", tags=["rooms"])
app.include_router(bookings.router, prefix="/bookings", tags=["bookings"])
app.include_router(services.router, prefix="/services", tags=["services"])

@app.get("/")
async def root():
    return {"message": "Hotel Management API is up and running!"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
