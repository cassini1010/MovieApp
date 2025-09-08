from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from app.database import get_db_session, authenticate
from typing import Annotated
from app.models import Token
from app.security import create_access_token
from datetime import timedelta
from app.config import settings

router = APIRouter(tags=["login"])


@router.post("/token")
async def login_access_token(
    session: Annotated[Session, Depends(get_db_session)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
                         ) -> Token:
    user = authenticate(
        session=session, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=create_access_token(
            user.username, expires_delta=access_token_expires
        )
    )