# from samba.dcerpc.dcerpc import payload
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from auth import utils as auth_utils
from core.models.db_helper import db_helper
from core.models.user_schemas import UserSchema
from core.models.crud import create_user, get_user_by_nickname
from pydantic import BaseModel


# http_bearer = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/login/",
)

class TokenInfo(BaseModel):
    access_token: str
    token_type: str

router = APIRouter()

john = UserSchema(
    nickname="johnathan",
    password=auth_utils.hash_password("secret"),
    email="johnathan@example.com",
)
sam = UserSchema(
    nickname="sam",
    password=auth_utils.hash_password("12345"),
    email="sam@example.com",
)

users_db: dict[str,UserSchema] = {
    john.nickname: john,
    sam.nickname: sam,
}


async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
    db: AsyncSession = Depends(db_helper.get_db)
):
    user = await get_user_by_nickname(db, username)

    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    if not user:
        raise unauthed_exc
    if not auth_utils.validate_password(
        password,
        user.password,
    ):
        raise unauthed_exc
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )

    return user


def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> UserSchema:
    # token = credentials.credentials
    try:
        payload = auth_utils.decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
        )
    return payload


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    db: AsyncSession = Depends(db_helper.get_db)
):
    nickname: str = payload.get("sub")
    user = await get_user_by_nickname(db, nickname)

    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid",
    )




def get_current_active_auth_user(
        user: UserSchema = Depends(get_current_auth_user),
):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="inactive user",
    )


@router.post("/login/", response_model=TokenInfo)
async def auth_user_issue_jwt(
        user: UserSchema = Depends(validate_auth_user),
):
   jwt_payload = {
       "sub": user.nickname,
       "nickname": user.nickname,
       "email": user.email,
   }
   token = auth_utils.encode_jwt(jwt_payload)
   return TokenInfo(
       access_token=token,
       token_type="Bearer"
   )

@router.get("/users/me/")
def auth_user_check_self_info(
        payload: dict = Depends(get_current_token_payload),
        user: UserSchema = Depends(get_current_active_auth_user),
):
    iat = payload.get("iat")
    return {
        "nickname": user.nickname,
        "email": user.email,
        "logged_in_at": iat,
    }