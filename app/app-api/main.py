from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import schemas.Predictor as Predictor
app = FastAPI()

app.include_router(Predictor.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}




