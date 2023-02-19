"""Schema modules."""
from datetime import datetime
from pydantic import BaseModel

## User schemas


class UserBase(BaseModel):
    email: str
    login: str
    password: str


class UserIdOut(BaseModel):
    id: str

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


## Coffee machine schemas


class MachineBase(BaseModel):
    name: str
    caffeine: float


class MachineCreate(MachineBase):
    pass


class Machine(MachineBase):
    id: int

    class Config:
        orm_mode = True


class MachineIdOut(BaseModel):
    id: str

    class Config:
        orm_mode = True


## Coffee schemas


class CoffeeBase(BaseModel):
    timestamp: datetime
    user_id: int
    machine_id: int

    class Config:
        orm_mode = True
