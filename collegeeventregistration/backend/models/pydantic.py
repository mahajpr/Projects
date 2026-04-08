from pydantic import BaseModel

class EventIn(BaseModel):
    title: str
    venue: str
    date: str
    time: str


class RegisterIn(BaseModel):
    name: str
    email: str
    phone: str
    gender: str
    year: str
    department: str
    college: str
    city: str
    event: str
    team_event: str
    team_name: str
    team_size: int
    teammates: str
    
class QRScanIn(BaseModel):
    qr_data: str

class LoginIn(BaseModel):
    email:str
    password:str