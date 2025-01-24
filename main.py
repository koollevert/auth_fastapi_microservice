from fastapi import FastAPI
from fastapi.routing import APIRouter
from routes.signup import router as signup_router
from motor.motor_asyncio import AsyncIOMotorClient
import os


MONGO_URL = os.getenv("MONGO_URL")
JWT_KEY = os.getenv("JWT_KEY")

client = AsyncIOMotorClient(MONGO_URL)
db = client.get_default_database()

def get_database():
    return db

app = FastAPI()

router = APIRouter()
@app.on_event("startup")
async def startup_db_client():
    try:
        # Attempt to connect to the database
        await client.server_info()
        print("Connected to the MongoDB database!")
    except Exception as e:
        print(f"Failed to connect to the MongoDB database: {e}")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

@router.get("/auth-fastapi/")
async def read_root():
    return {"message": "Hello World"}

app.include_router(router, prefix="/api")
app.include_router(signup_router, prefix="/api")