from __future__ import annotations

from time import perf_counter
import os

from fastapi import Request, APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.app import app, user_handler
from src.utils import Token, TokenHandler

router = APIRouter(prefix="/v1", tags=["Users"])
JWT_SECRET = os.environ["JWT_SECRET"]

token_handler = TokenHandler(os.environ["JWT_SECRET"])
security = HTTPBearer()


def get_user_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return token_handler.decode_token(credentials.credentials)

@router.post("/follow/{user_id}")
async def follow_user(request: Request, user_id: str, token = Depends(get_user_token)):
    following_id = token.sub

    user_handler.follow(following_id=following_id, user_id=user_id)
    return True
