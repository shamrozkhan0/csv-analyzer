from fastapi.middleware.cors import CORSMiddleware
from database import insert_data_into_database
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from Cleaner import start
from pathlib import Path
import logging as log
import random
import os


log.basicConfig(level=log.INFO, format="%(asctime)s %(levelname)s %(message)s")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials= False,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

@app.get("/")
def show_home_page():
    return {"message": "Hello world"}


@app.post("/uploads")
async def uploads_files(file: UploadFile = File(...)):

    log.info("File upload request received")
    allowed_extension = [".csv"]
    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in allowed_extension:
        return {"message": "File is not valid"}

    id = int(random.random() * 10000000)
    filename = str(id) + '.csv' # Later this will changed to the following file extension
    file_path = f"{os.getenv('UPLOAD_PATH')}{filename}"

    with open(file_path, "wb") as file_writer:
        log.info(f"Saving to: {file_writer.name}")
        content = await file.read()
        file_writer.write(content)

    summary = start(filename)

    insert_data_into_database(summary, id)

    return {
        "status" : "success",
        "body": {
            "id": id,
            "content": summary
        }
    }


@app.get("/download/{filename}")
def download_file(filename: str):
    path = f"E:/CsvAnalyzer/cleaned/{filename}"
    return FileResponse(path, filename=filename)




