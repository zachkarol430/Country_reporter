from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from resources.countries_function import router as countries_router
from resources.capital_functions import router as capital_router
import os

app = FastAPI(
    title="Country Data API",
    description="API for accessing country data",
    version="1.0.0"
)

# Setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'Data')
FLAGS_DIR = os.path.join(DATA_DIR, 'flags')

# Mount flags directory
app.mount("/flags", StaticFiles(directory=FLAGS_DIR), name="flags")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://country-reporter-front-end.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(countries_router)
app.include_router(capital_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)