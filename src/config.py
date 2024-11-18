import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATASET = os.getenv("DATASET")
    TARGET = os.getenv("TARGET")
    MODEL = os.getenv("MODEL")
    TRIALS = int(os.getenv("TRIALS", 10))
    DEPLOYMENT_TYPE = os.getenv("DEPLOYMENT_TYPE")
    INPUT_FOLDER = os.getenv("INPUT_FOLDER", "data/input/")
    OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER", "data/output/")
    PORT = int(os.getenv("PORT", 8000))
