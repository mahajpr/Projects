from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.db import engine, Base
from routes.routes import router
from models import tables

app = FastAPI(title="Fake Review Detection explanation tool")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
app.include_router(router)
@app.get("/")
def home():
    return {"message": "Fake Review Detector API running"}
