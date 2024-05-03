from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from auth.auth import create_access_token


auth_routes = APIRouter(prefix="/api/auth", tags=["auth"])


@auth_routes.post("/token")
async def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data.username)
    print(form_data.password)
    # validate credentials
    if form_data.username != 'die711':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    token = create_access_token({"username": form_data.username})
    print(token)
    return {
        "access_token": token
    }
