from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from pydantic import BaseModel
import io
from PIL import Image
from utils_model import paddleocr_model as paddle
from utils_model import glass_model as glass_model
import os
import base64

router = APIRouter()

@router.post("/predict", tags=["model"])
async def predict(file: UploadFile = File(...), model: str = Form('paddle')):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type.")
    try:
        image = Image.open(io.BytesIO(await file.read()))
        if model == 'paddle':
            prediction = paddle.predict(image)
        elif model == 'glass':
            prediction = glass_model.predict(image)
        
        image.save("./Project/images/img_1.jpg")        
        return {"prediction": prediction} 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during prediction: {e}")
