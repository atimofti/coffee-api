"""Models module."""
from sqlalchemy import Column, Integer, String, Float, TIMESTAMP
from db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True)
    password = Column(String, index=True)
    email = Column(String, unique=True, index=True)


class Machine(Base):
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    caffeine = Column(Float, index=True)


class Coffee_Records(Base):
    __tablename__ = "coffee"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(TIMESTAMP, index=True)
    user_id = Column(Integer, index=True)
    machine_id = Column(Integer, index=True)
