from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.routes import job, candidate, auth

app = FastAPI()

# welcome api
@app.get("/")
def read_root():
    return {"message": "Welcome to the HR Process Optimization API"}


# CORS (Cross-Origin Resource Sharing) middleware to allow requests from any domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes from other files
app.include_router(auth.router)

if __name__ == "__main__":
    # Create database tables
    from app.database import Base, engine
    Base.metadata.create_all(bind=engine)

    # Run the application using Uvicorn server
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
