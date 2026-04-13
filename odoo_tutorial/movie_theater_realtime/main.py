"""
name: main.py
description: Main application entry point for the FastAPI movie theater server.
"""
from fastapi import FastAPI
import uvicorn
from routes.movie_theater import router as movie_router

app = FastAPI(
    title="Movie Theater Realtime API",
    description="API for managing movies and theater operations.",
    version="1.0.0"
)

# Register routes
app.include_router(movie_router)

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint verifying the server status.
    """
    return {"message": "Movie Theater Realtime API is online."}

def run():
    """
    Main function to start the uvicorn server.
    """
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    run()
