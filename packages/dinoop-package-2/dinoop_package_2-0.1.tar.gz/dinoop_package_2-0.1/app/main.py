from fastapi import FastAPI
from app.database import engine, Base
from app.routes import employee_routes

app = FastAPI(title="Employee Management API")

Base.metadata.create_all(bind=engine)

app.include_router(employee_routes.router)
