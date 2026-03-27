from pydantic import BaseModel, Field
from typing import Optional

class Login(BaseModel): 
    username: str
    password: str

class LoginRead(BaseModel):
    farmer_id: str 
    username: str

class Signup(BaseModel):
    username: str
    password: str

class SignupFarmer(BaseModel):
    username: str
    password: str
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    farm_id: Optional[str] = None
