from fastapi import FastAPI, Depends
from fastapi.routing import APIRouter
from routes.signup import router as signup_router
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.getenv("MONGO_URL")
JWT_KEY = os.getenv("JWT_KEY")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "default_db")

client = AsyncIOMotorClient(MONGO_URL)
db = client[MONGO_DB_NAME]

def get_database():
    return db

async def lifespan(app: FastAPI):
    # Startup event
    try:
        await client.server_info()
        print("Connected to the MongoDB database!")
    except Exception as e:
        print(f"Failed to connect to the MongoDB database: {e}")
        raise e
    yield
    # Shutdown event
    
    client.close()
    print("Disconnected from the MongoDB database!")

app = FastAPI(lifespan=lifespan)

router = APIRouter()

@router.get("/auth-fastapi/")
async def read_root():
    return {"message": "Hello World"}

app.include_router(router, prefix="/api")
app.include_router(signup_router, prefix="/api")

# Start the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)