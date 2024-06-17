import mlflow

def loadmodel(run_id):
    return mlflow.pyfunc.load_model(f"runs:/{run_id}/model")