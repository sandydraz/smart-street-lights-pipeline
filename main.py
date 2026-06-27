from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import lights , simulation
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Smart Street Lights API",
    description="API for Smart Street Lights Data Warehouse",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(lights.router, prefix="/api", tags=["Lights & Readings"])
app.include_router(simulation.router, prefix="/api", tags=["Simulation Control"])

app.mount("/dashboard", StaticFiles(directory="dashboard", html=True), name="dashboard")

@app.get("/")
def root():
    return {"message": "Smart Street Lights API is running 🟡"}