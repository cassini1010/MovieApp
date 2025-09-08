from app.routes import login, movies
from fastapi import FastAPI

app = FastAPI()
app.include_router(login.router)
app.include_router(movies.router)
