from fastapi import APIRouter , Depends , HTTPException 
from models.pydantic import RegisterIn  ,EventIn , QRScanIn , LoginIn
from models.tables import Event , Registration , User
from database.deps import get_db
from sqlalchemy.orm import Session
from typing import List
from services.data import new_register , events_get , require_role
from services.auth import create_access_token , verify_password
from services.email_service import send_confirmation_email
from sheets import save_to_sheet

router = APIRouter()

@router.post("/register")
def register (data:RegisterIn , db:Session = Depends(get_db)):
    reg =Registration(**data.dict())
    db.add(reg)
    db.commit()
    save_to_sheet([
        data.name,
        data.email,
        data.phone,
        data.college,
        data.event,
        data.team_name,
        data.team_size
    ])
    try:
        send_confirmation_email(data.email , data.name ,data.event)
    except Exception as e:
        print("Email failed:" , e)
    return {"msg":"Registration & email sent"}


@router.get("/events",response_model=List[EventIn])
def get_events(db:Session = Depends(get_db)):
    return db.query(Event).all()

@router.post("/login")
def login(data:LoginIn ,  db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password , user.password):
       raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({
        "email": user.email,
        "role": user.role
    })

    return {"access_token": token}

@router.post("/events")
def create_event(data: EventIn,db: Session = Depends(get_db),user=Depends(require_role("admin"))):

    existing = db.query(Event).filter(Event.title == data.title,Event.date == data.date).first()
    if existing:
        raise HTTPException(status_code=400, detail="Event already exists")
    event = Event(title=data.title,venue=data.venue,date=data.date,time=data.time)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

