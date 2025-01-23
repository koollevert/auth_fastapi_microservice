from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

router = APIRouter()

@router.get("/auth-fastapi/")
async def read_root():
    return {"message": "Hello World"}

app.include_router(router, prefix="/api")