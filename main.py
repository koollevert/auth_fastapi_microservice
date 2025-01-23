from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

@app.get("/api/auth-fastapi") 
async def test():
    return {"message": "Hello World"}