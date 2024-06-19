import mlflow
import numpy as np
from PIL import Image

mlflow.set_tracking_uri("http://localhost:5000")
logged_paddleocr = 'runs:/bdb2c42060fe431991b728dbebe71421/paddleocr'
loaded_paddleocr = mlflow.pyfunc.load_model(logged_paddleocr)

def predict(image: Image.Image):
    image = np.asarray(image.convert('RGB'))
    return loaded_paddleocr.predict(image)
