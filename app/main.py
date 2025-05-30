from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.database import init_db
from contextlib import asynccontextmanager
from app.routes.users import router as users_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"errors": jsonable_encoder(exc.errors())},
    )

@app.get("/")
def read_root():
    return {"message": "Hello from Dockerized FastAPI"}

app.include_router(users_router)
