from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, tools, history, profile
from app.config import settings
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="N Cloud Backend", version="1.0")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8080",
    "http://127.0.0.1:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(tools.router)
app.include_router(history.router)
app.include_router(profile.router)

@app.get("/")
def root():
    return {"status": "N Cloud backend running"}
