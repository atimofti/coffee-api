"""Create, Read, Update and Delete module."""
from sqlalchemy import and_
from sqlalchemy.orm import Session
import models
import schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_login(db: Session, login: str):
    return db.query(models.User).filter(models.User.login == login).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_count_past24(db: Session, user_id: str, past24_time):
    return (
        db.query(models.Coffee_Records)
        .filter(
            and_(
                models.Coffee_Records.user_id == user_id,
                models.Coffee_Records.timestamp > past24_time,
            )
        )
        .count()
    )


def get_timestamp_list(db: Session, user_id: str, past24_time):
    return (
        db.query(models.Coffee_Records.timestamp)
        .filter(
            and_(
                models.Coffee_Records.user_id == user_id,
                models.Coffee_Records.timestamp > past24_time,
            )
        )
        .all()
    )


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(login=user.login, password=user.password, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


def create_machine(db: Session, machine: schemas.MachineCreate):
    print(machine)
    db_machine = models.Machine(name=machine.name, caffeine=machine.caffeine)
    db.add(db_machine)
    db.commit()
    db.refresh(db_machine)
    return db_machine


def log_coffee(db: Session, coffee: schemas.CoffeeBase):
    print(coffee)
    db_coffee = models.Coffee_Records(
        timestamp=coffee["timestamp"],
        user_id=coffee["user_id"],
        machine_id=coffee["machine_id"],
    )
    db.add(db_coffee)
    db.commit()
    db.refresh(db_coffee)
    return db_coffee
