from typing import Optional
from pydantic import BaseModel, Field


class PasswordLoginRequest(BaseModel):
    email: str
    password: str
    long_lived: Optional[bool] = Field(alias="longLived", default=True)


class Jwt(BaseModel):
    access_token: str = Field(alias="accessToken")
    refresh_token: str = Field(alias="refreshToken")
    long_lived: bool = Field(alias="longLived")
    logout_url: Optional[str] = Field(alias="logoutUrl")
