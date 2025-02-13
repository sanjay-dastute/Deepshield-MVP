from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .db.mongodb import connect_to_mongo, close_mongo_connection
from .api.endpoints import users, content, ai, notifications
from .services.api.instagram import router as instagram_router


app = FastAPI(title="DeepShield API")

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Mount static files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(content.router, prefix="/api/v1/content", tags=["content"])
app.include_router(ai.router, prefix="/api/v1/ai", tags=["ai"])
app.include_router(instagram_router, prefix="/api/v1/instagram", tags=["instagram"])
app.include_router(notifications.router, prefix="/api/v1/notifications", tags=["notifications"])

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
