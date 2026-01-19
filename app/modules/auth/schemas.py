from pydantic import BaseModel 

class Login(BaseModel): 
    username: str
    password: str

class LoginRead(BaseModel):
    farmer_id: str 
    username: str

class Signup(BaseModel):
    username: str
    password: str
