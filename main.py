from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException, Query, Body
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from db import SessionLocal, engine
import models
import schemas
import crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# API Request definitions


@app.get("/")
def main():
    return RedirectResponse(url="/docs/")


@app.put("/user/request", response_model=schemas.UserIdOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Add user to database while performing duplicate email and login validation."""
    db_user_email = crud.get_user_by_email(db, email=user.email)
    db_user_login = crud.get_user_by_login(db, login=user.login)
    if db_user_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    if db_user_login:
        raise HTTPException(status_code=401, detail="Login already registered")
    return crud.create_user(db=db, user=user)


@app.post("/machine", response_model=schemas.MachineIdOut)
def create_machine(machine: schemas.MachineCreate, db: Session = Depends(get_db)):
    """Register a coffee machine into the database. Returns the ID of the machine."""
    return crud.create_machine(db=db, machine=machine)


@app.put("/coffee/buy/{user_id}/{machine_id}")
async def log_coffee(
    user_id: int = Query(...),
    machine_id: int = Query(...),
    timestamp: datetime = Body(None, embed=True),
    db: Session = Depends(get_db),
):
    """Log coffee intake per user id and machine id given the timestamp as input.
    If not timestampt is provided, the current datetime is used."""
    result = {"user_id": user_id, "machine_id": machine_id, "timestamp": timestamp}
    if timestamp is None:
        result.update({"timestamp": datetime.now()})
    print(result)
    return crud.log_coffee(db=db, coffee=result)


@app.get("/stats/coffee")
def global_stats(db: Session = Depends(get_db)):
    """Return transaction history globally."""
    global_stats = db.query(models.Coffee_Records).all()
    global_stats_final = []
    for stat in global_stats:
        globalstatObject = {
            "machine": stat.machine_id,
            "user": stat.user_id,
            "timestamp": stat.timestamp,
        }
        global_stats_final.append(globalstatObject)
    return global_stats_final


@app.get("/stats/coffee/machine/{machine_id}")
def machine_stats(machine_id: int = Query(...), db: Session = Depends(get_db)):
    """Return transaction history globally per machine id provided."""
    machine_stats = (
        db.query(models.Coffee_Records).filter_by(machine_id=machine_id).all()
    )
    machine_stats_final = []
    for stat in machine_stats:
        machinestatObject = {
            "machine": stat.machine_id,
            "user": stat.user_id,
            "timestamp": stat.timestamp,
        }
        machine_stats_final.append(machinestatObject)
    return machine_stats_final


@app.get("/stats/coffee/user/{user_id}")
def user_stats(user_id: int = Query(...), db: Session = Depends(get_db)):
    """Return transaction history globally per user id provided."""
    user_stats = db.query(models.Coffee_Records).filter_by(user_id=user_id).all()
    user_stats_final = []
    for stat in user_stats:
        userstatObject = {
            "machine": stat.machine_id,
            "user": stat.user_id,
            "timestamp": stat.timestamp,
        }
        user_stats_final.append(userstatObject)
    return user_stats_final


@app.get("/stats/level/user/{user_id}")
def caf_level_stats(user_id: int = Query(...), db: Session = Depends(get_db)):
    """Return the history of user's caffeine level for the past 24hrs using a one hour resolution.
    Level goes from 0 to 100% after intake for the first hour then reduced by half every 5 hrs.
    """
    current_time = datetime.now()
    caffeine_stats_final = []
    past24_time = current_time - timedelta(hours=24)
    count_past24 = crud.get_count_past24(db, user_id=user_id, past24_time=past24_time)
    print(count_past24)
    if count_past24 == 0:
        for i in range(24):
            caffeinestatObject = {
                "time": current_time - timedelta(hours=i),
                "level": "0%",
            }
            caffeine_stats_final.append(caffeinestatObject)
        return caffeine_stats_final
    timestamps_list = crud.get_timestamp_list(db, user_id, past24_time=past24_time)
    print(timestamps_list)
    for i in range(24):
        caffeinestatObject = {
            "time": current_time - timedelta(hours=i),
            "level": "to be calculated..",
        }
        caffeine_stats_final.append(caffeinestatObject)
    return caffeine_stats_final
