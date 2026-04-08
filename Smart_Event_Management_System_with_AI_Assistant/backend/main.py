from fastapi import FastAPI
from database.db import engine, Base, SessionLocal
from routes.routes import router
from services.rag import router as rag_router
from models.tables import User
from services.auth import hash_password
from dotenv import load_dotenv

load_dotenv()

Base.metadata.create_all(bind=engine)

api = FastAPI(title="College Event Registration System")

@api.on_event("startup")
def create_default_admin():
    db = SessionLocal()
    admin = db.query(User).filter(User.email == "admin1@gmail.com").first()

    if not admin:
        db.add(User(
            email="admin1@gmail.com",
            password=hash_password("admin123"),
            role="admin"
        ))
        db.commit()

    db.close()

api.include_router(router)
api.include_router(rag_router)