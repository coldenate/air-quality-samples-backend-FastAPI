from fastapi import FastAPI
import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
from apps.db_save.models import EntryModel
from config.settings import settings
from fastapi.middleware.cors import CORSMiddleware

from apps.db_save.routers import (
    entry_router,
    response_router,
)  # pylint: disable=E0611, C0412

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000",
    "https://coldenate.github.io",
    "coldenate.github.io",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_db_client():
    """Connect to the database on startup""" ""
    app.mongodb_client = AsyncIOMotorClient(settings.DB_URL)  # type: ignore
    app.mongodb = app.mongodb_client[settings.DB_NAME]  # type: ignore


@app.on_event("shutdown")
async def shutdown_db_client():
    """Disconnect from the database on shutdown"""
    app.mongodb_client.close()  # type: ignore


app.include_router(entry_router, tags=["entry"], prefix="/entry")
# app.include_router(entry_router, tags=["entry"], prefix="/entries")
app.include_router(response_router, tags=["responses"], prefix="/responses")

cals = EntryModel()


# if __name__ == "__main__":
#     uvicorn.run(
#         "main:app",
#         host=settings.HOST,
#         reload=settings.DEBUG_MODE,
#         port=settings.PORT,  # type: ignore    )]
#     )
