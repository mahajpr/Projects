from database.deps import get_db
from models.pydantic import RegisterIn 
from models.tables import Registration , Event 
from sqlalchemy.orm import Session 
from sheets import save_to_sheet
from services.email_service import send_confirmation_email
from fastapi import Depends , HTTPException
from services.auth import get_current_user


def new_register(data, db):
    add_register = Registration(
        name=data.name,
        email=data.email,
        phone=data.phone,
        gender=data.gender,
        year=data.year,
        department=data.department,
        college=data.college,
        city=data.city,
        event=data.event,
        team_event=data.team_event,
        team_name=data.team_name,
        team_size=data.team_size,
        teammates=data.teammates
    )

    db.add(add_register)
    db.commit()

    save_to_sheet([data.name,data.email,data.event])

    send_confirmation_email(data.email,data.name,data.event)

    return {"message": "Registration successful"}


def events_get(db:Session):
    return db.query(Event).all()

def require_role(required_role: str):
    def checker(user=Depends(get_current_user)):
        if user["role"] != required_role:
            raise HTTPException(status_code=403,detail="Access denied")
        return user
    return checker