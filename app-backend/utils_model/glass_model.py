import mlflow
import numpy as np
from PIL import Image

mlflow.set_tracking_uri("http://localhost:5000")
logged_model = 'runs:/a11b9a456a2a42cf859eb143fa40eb2b/glassrunner'
loaded_model = mlflow.pyfunc.load_model(logged_model)

def predict(image: Image.Image):
    image = np.asarray(image.convert('RGB'))
    return loaded_model.predict(image)

