from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import create_db_and_tables
from app.routers import transactions, forecasts


# ===========================================================================
# INITIALISING APP
# ===========================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="ForeCashier API", lifespan=lifespan)

# ===========================================================================
# ADDING MIDDLEWARE - to handle different origins
# ===========================================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],    # Vite server
    allow_methods=["*"],
    allow_headers=["*"]
)

# ===========================================================================
# ADDING ROUTERS
# ===========================================================================
app.include_router(transactions.router)
app.include_router(forecasts.router)


@app.get("/api/health", tags=["meta"])
def health():
    return {"status": "ok"}