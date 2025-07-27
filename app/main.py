from fastapi import FastAPI
from app.db.session import init_db
from app.api.routes import auth, project

app = FastAPI()

# Init DB when app loads
@app.on_event("startup")
async def on_startup():
    await init_db()

# Sample Route
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI RBAC"}

# Include Auth Routes
app.include_router(auth.router)

# Include Project Table Routes
app.include_router(project.router)
