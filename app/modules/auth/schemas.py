from pydantic import BaseModel
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
    farm_id: Optional[str] = None
