from fastapi import FastAPI
from fastapi.routing import APIRouter
from routes.signup import router as signup_router

app = FastAPI()

router = APIRouter()

@router.get("/auth-fastapi/")
async def read_root():
    return {"message": "Hello World"}

app.include_router(router, prefix="/api")
app.include_router(signup_router, prefix="/api")