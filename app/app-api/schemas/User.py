from pydantic import BaseModel
from pydantic import EmailStr, Field
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Any, Dict, List


class User(BaseModel):
    id: int
    username: str
    email: EmailStr | None = Field(default=None)
    password: str

        
