from dotenv import load_dotenv
import os

load_dotenv()
AUTH_HEADER = {"X-Api-Key": os.getenv("API_KEY")}
IMAGE_DOWNLOADER_WORKERS = 1

ACCEPTABLE_SUPERTYPES = [
    "pokemon",
    "trainer",
    "energy",
]

TRAINER_SUPERTYPES = ["trainer"]
